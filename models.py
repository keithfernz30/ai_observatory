from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from database import Base
from datetime import datetime

class AILog(Base):
    __tablename__ = "ai_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    response_time = Column(Float, default=0.0)
    status = Column(String, default="success")