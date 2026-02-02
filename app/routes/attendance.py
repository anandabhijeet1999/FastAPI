from __future__ import annotations

from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, Query, status

from app.db import get_db
from app.errors import http_404, http_409
from app.models import AttendanceCreate, AttendanceOut, AttendanceStatus


router = APIRouter(prefix="/employees/{employee_id}/attendance", tags=["attendance"])


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def _ensure_employee_exists(db, employee_id: str):
    employees = db["employees"]
    exists = await employees.find_one({"employeeId": employee_id}, {"_id": 1})
    if not exists:
        http_404("Employee not found.")


@router.post("", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
async def mark_attendance(employee_id: str, payload: AttendanceCreate, db=Depends(get_db)):
    await _ensure_employee_exists(db, employee_id)

    attendance = db["attendance"]
    # one record per employee per date
    existing = await attendance.find_one(
        {"employeeId": employee_id, "date": payload.date.isoformat()}, {"_id": 1}
    )
    if existing:
        http_409("Attendance for this date already exists.")

    doc = {
        "employeeId": employee_id,
        "date": payload.date.isoformat(),
        "status": payload.status.value,
        "createdAt": _now_iso(),
    }
    await attendance.insert_one(doc)

    # adapt back to model field types
    return {
        "employeeId": doc["employeeId"],
        "date": payload.date,
        "status": payload.status,
        "createdAt": doc["createdAt"],
    }


@router.get("", response_model=list[AttendanceOut])
async def list_attendance(
    employee_id: str,
    db=Depends(get_db),
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
):
    await _ensure_employee_exists(db, employee_id)
    attendance = db["attendance"]

    query: dict = {"employeeId": employee_id}
    if from_date or to_date:
        date_filter: dict = {}
        if from_date:
            date_filter["$gte"] = from_date.isoformat()
        if to_date:
            date_filter["$lte"] = to_date.isoformat()
        query["date"] = date_filter

    cursor = attendance.find(query, {"_id": 0}).sort("date", -1)
    items = []
    async for doc in cursor:
        items.append(
            {
                "employeeId": doc["employeeId"],
                "date": date.fromisoformat(doc["date"]),
                "status": AttendanceStatus(doc["status"]),
                "createdAt": doc.get("createdAt"),
            }
        )
    return items


@router.get("/stats")
async def attendance_stats(employee_id: str, db=Depends(get_db)):
    await _ensure_employee_exists(db, employee_id)
    attendance = db["attendance"]
    total_present = await attendance.count_documents(
        {"employeeId": employee_id, "status": AttendanceStatus.PRESENT.value}
    )
    return {"employeeId": employee_id, "totalPresentDays": total_present}

