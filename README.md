# AI Observability (FastAPI + React Dashboard)

Monorepo with:
- Backend API: FastAPI + SQLAlchemy + SQLite
- Frontend Dashboard: React + Vite + Recharts

## Project Structure

- `main.py` FastAPI app and metrics endpoints
- `database.py` async SQLAlchemy engine/session config
- `models.py` DB models
- `requirements.txt` Python dependencies
- `ai-dashboard/` React dashboard app

## Local Run

### 1) Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2) Frontend

```bash
cd ai-dashboard
npm install
npm run dev
```

The dashboard calls backend metrics at `http://127.0.0.1:8000/metrics`.

## Push to GitHub

Run from repository root (`ai_observability`):

```bash
git init
git add .
git commit -m "Initial commit: FastAPI backend + React observability dashboard"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
git push -u origin main
```

If the remote already exists:

```bash
git remote set-url origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
git push -u origin main
```

## Recommended Next Improvements

- Move API base URL in frontend to environment variable.
- Add backend tests for `/metrics`, `/log`, `/ask`.
- Add CI for lint/build/test.
