from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Response, status

from app.db import get_db
from app.errors import http_404, http_409
from app.models import EmployeeCreate, EmployeeOut


router = APIRouter(prefix="/employees", tags=["employees"])


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.post("", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
async def create_employee(payload: EmployeeCreate, db=Depends(get_db)):
    employees = db["employees"]
    existing = await employees.find_one({"employeeId": payload.employeeId})
    if existing:
        http_409("Employee ID already exists.")

    existing_email = await employees.find_one({"email": payload.email})
    if existing_email:
        http_409("Email already exists.")

    doc = payload.model_dump()
    doc["createdAt"] = _now_iso()
    await employees.insert_one(doc)
    return doc


@router.get("", response_model=list[EmployeeOut])
async def list_employees(db=Depends(get_db)):
    employees = db["employees"]
    cursor = employees.find({}, {"_id": 0}).sort("createdAt", -1)
    return [doc async for doc in cursor]


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: str, db=Depends(get_db)):
    employees = db["employees"]
    attendance = db["attendance"]

    result = await employees.delete_one({"employeeId": employee_id})
    if result.deleted_count == 0:
        http_404("Employee not found.")

    # avoid orphan attendance
    await attendance.delete_many({"employeeId": employee_id})
    return Response(status_code=status.HTTP_204_NO_CONTENT)

