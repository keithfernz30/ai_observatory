
from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base, AsyncSessionLocal
from models import AILog
from sqlalchemy.future import select
from pydantic import BaseModel
from sqlalchemy import func
from starlette.middleware.base import BaseHTTPMiddleware
import time
import random
import asyncio

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Define Middleware FIRST
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            response = await call_next(request)
            status = "success"
        except Exception as e:
            status = "failure"
            raise e

        process_time = time.time() - start_time

        async with AsyncSessionLocal() as session:
            new_log = AILog(
                user_input=f"{request.method} {request.url.path}",
                ai_response="Auto logged",
                response_time=process_time,
                status=status
            )
            session.add(new_log)
            await session.commit()

        return response


# ✅ Add middleware AFTER class definition
app.add_middleware(LoggingMiddleware)


# ✅ Pydantic Model
class LogCreate(BaseModel):
    user_input: str
    ai_response: str


# ✅ Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Observability backend is running 🚀"}


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.post("/log")
async def create_log(log: LogCreate, db: AsyncSession = Depends(get_db)):
    start_time = time.time()

    ai_output = log.ai_response

    total_time = time.time() - start_time

    new_log = AILog(
        user_input=log.user_input,
        ai_response=ai_output,
        response_time=total_time,
        status="success"
    )

    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)

    return {
        "message": "Log saved",
        "response_time": total_time,
        "id": new_log.id
    }


@app.get("/logs")
async def get_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AILog))
    return result.scalars().all()


@app.get("/metrics")
async def get_metrics(db: AsyncSession = Depends(get_db)):
    total = (await db.execute(select(func.count(AILog.id)))).scalar()
    average = (await db.execute(select(func.avg(AILog.response_time)))).scalar()
    fastest = (await db.execute(select(func.min(AILog.response_time)))).scalar()
    slowest = (await db.execute(select(func.max(AILog.response_time)))).scalar()
    failed_count = (await db.execute(
        select(func.count(AILog.id)).where(AILog.status == "failure")
    )).scalar()

    failure_rate = (failed_count / total * 100) if total else 0

    return {
        "total_requests": total,
        "average_response_time": average,
        "fastest_request": fastest,
        "slowest_request": slowest,
        "failure_rate_percent": failure_rate
    }

@app.post("/ask")
async def ask_ai_mock(log: LogCreate, db: AsyncSession = Depends(get_db)):
    start_time = time.time()

    # Simulate processing delay (0.2 to 1.2 seconds)
    fake_delay = random.uniform(0.2, 1.2)
    await asyncio.sleep(fake_delay)

    # 10% chance to simulate failure
    simulate_failure = random.random() < 0.1

    total_time = time.time() - start_time

    if simulate_failure:
        status = "failure"
        ai_output = "Mock AI encountered an internal error."
    else:
        status = "success"
        ai_output = f"Mock AI Response to: '{log.user_input}'"

    new_log = AILog(
        user_input=log.user_input,
        ai_response=ai_output,
        response_time=total_time,
        status=status
    )

    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)

    return {
        "ai_response": ai_output,
        "response_time": total_time,
        "status": status
    }