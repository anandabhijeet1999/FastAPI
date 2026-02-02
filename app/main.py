from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import close_mongo_connection, connect_to_mongo, get_db
from app.routes.attendance import router as attendance_router
from app.routes.employees import router as employees_router


def _parse_cors(origins_raw: str) -> list[str]:
    return [o.strip() for o in origins_raw.split(",") if o.strip()]


app = FastAPI(title="HRMS Lite API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def _startup():
    await connect_to_mongo()
    db = get_db()
    # Indexes for uniqueness + fast lookups
    await db["employees"].create_index("employeeId", unique=True)
    await db["employees"].create_index("email", unique=True)
    await db["attendance"].create_index([("employeeId", 1), ("date", 1)], unique=True)
    await db["attendance"].create_index("employeeId")


@app.on_event("shutdown")
async def _shutdown():
    await close_mongo_connection()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(employees_router)
app.include_router(attendance_router)

