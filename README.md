
# 🚀 AI Observatory Dashboard

A full-stack AI monitoring and observatory system built with **FastAPI + React**.

This project simulates and monitors AI model behavior, tracks performance metrics, logs requests, and visualizes analytics in a real-time dashboard.

---

## 📌 Project Overview

This system is designed to demonstrate how AI observatory platforms work.

It tracks:

- 📊 Total Requests
- ⏱ Average Response Time
- ⚡ Fastest & Slowest Requests
- ❌ Failure Rate
- 📈 Response Time Trends (Live Chart)

Even though a mock AI engine is used, the Observatory pipeline is real and production-style.

---

## 🏗 Architecture

```

User → FastAPI Backend → Mock AI Engine → SQLite DB → Metrics API → React Dashboard

````

---

## 🛠 Tech Stack

### Backend
- FastAPI (Async)
- SQLAlchemy (Async ORM)
- SQLite
- Middleware-based request logging

### Frontend
- React (Vite)
- Axios
- Recharts (for visualization)
- Responsive CSS Grid layout

---

## ✨ Features

### 🔹 Backend
- Async request handling
- Middleware auto-logging
- Response time tracking
- Failure simulation
- Metrics aggregation endpoint
- SQLite database logging

### 🔹 Frontend
- KPI dashboard
- Live auto-refresh (every 5 seconds)
- Response time trend chart
- Enterprise-style UI layout
- Responsive design

---

## 📊 API Endpoints

### `POST /ask`
Simulates an AI request and logs:
- user_input
- ai_response
- response_time
- status

### `GET /metrics`
Returns aggregated statistics:
```json
{
  "total_requests": 15,
  "average_response_time": 0.52,
  "fastest_request": 0.21,
  "slowest_request": 1.02,
  "failure_rate_percent": 6.6
}
````

---

## 🚀 Running Locally

### 1️⃣ Backend Setup

```bash
cd ai_Observatory
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### 2️⃣ Frontend Setup

```bash
cd ai-dashboard
npm install
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## 🗄 Database

SQLite database file:

```
ai_logs.db
```

To inspect:

* Use DB Browser for SQLite
* Or run:

```bash
sqlite3 ai_logs.db
SELECT * FROM ai_logs;
```

---

## 🎯 What This Project Demonstrates

* Observatory architecture design
* Async backend engineering
* Real-time metrics aggregation
* Full-stack API integration
* Data visualization
* Monitoring system design principles

---

## 👨‍💻 Author

Keith Fernandes

