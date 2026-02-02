from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"


class EmployeeCreate(BaseModel):
    employeeId: str = Field(..., min_length=1, max_length=64)
    fullName: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=80)


class EmployeeOut(BaseModel):
    employeeId: str
    fullName: str
    email: EmailStr
    department: str
    createdAt: str | None = None


class AttendanceCreate(BaseModel):
    date: date
    status: AttendanceStatus


class AttendanceOut(BaseModel):
    employeeId: str
    date: date
    status: AttendanceStatus
    createdAt: str | None = None


class EmployeeWithStats(EmployeeOut):
    totalPresentDays: int = 0

