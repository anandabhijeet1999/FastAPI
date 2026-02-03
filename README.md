# HRMS Lite (Full-Stack)

Lightweight HRMS for a single admin to:
- Manage employees (add/list/delete)
- Track daily attendance (present/absent)

## Tech stack
- **Frontend**: React (Vite) + Tailwind CSS
- **Backend**: FastAPI (Python) + Pydantic validation
- **Database (NoSQL)**: MongoDB

## Monorepo structure
- `backend/` – FastAPI API server
- `frontend/` – React web app

## Features
### Employee Management
- Add employee: **employeeId (unique)**, **fullName**, **email**, **department**
- List employees
- Delete employee (also deletes their attendance records)

### Attendance Management
- Mark attendance for employee: **date**, **status (PRESENT/ABSENT)**
- View attendance records per employee
- Optional filters: `from` / `to` date range
- Employee stats: total present days

## Local setup
### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker (for MongoDB)

### 1) Start MongoDB
From repo root:

```bash
docker compose up -d
```

### 2) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend runs at `http://localhost:8080`.
Swagger docs: `http://localhost:8080/docs`

### 3) Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Environment variables
### Backend (`backend/.env`)
Copy from example:

```bash
cp backend/.env.example backend/.env
```

- `MONGODB_URI`: Mongo connection string (default points to docker compose)
- `DB_NAME`: Database name
- `CORS_ORIGINS`: Comma-separated list of allowed origins (e.g. `http://localhost:5173`)

### Frontend (`frontend/.env`)
Copy from example:

```bash
cp frontend/.env.example frontend/.env
```

- `VITE_API_BASE_URL`: Backend base URL (e.g. `http://localhost:8080`)

## Assumptions / limitations
- Single admin user; **no authentication**
- Employee deletion also removes their attendance records (to avoid orphan records)

## Deployment (suggested)
- **Backend**: Render (Docker or Python)
- **Frontend**: Netlify / Vercel
- Configure `VITE_API_BASE_URL` to point to deployed backend.

