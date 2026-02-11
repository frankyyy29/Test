from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import get_session
from ..models import AttendanceRecord, Employee
from ..crud import create_attendance, get_employee, list_attendance_for_employee

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/{employee_id}/records", response_model=AttendanceRecord)
def create_attendance_record(employee_id: int, payload: AttendanceRecord, session: Session = Depends(get_session)):
    emp = get_employee(session, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    payload.employee_id = employee_id
    return create_attendance(session, payload)


@router.get("/{employee_id}/records", response_model=list[AttendanceRecord])
def list_attendance(employee_id: int, session: Session = Depends(get_session)):
    emp = get_employee(session, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return list_attendance_for_employee(session, employee_id)
