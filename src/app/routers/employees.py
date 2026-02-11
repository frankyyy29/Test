from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import get_session
from ..models import Employee
from ..crud import create_employee, list_employees

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=Employee)
def create_employee_endpoint(payload: Employee, session: Session = Depends(get_session)):
    # Basic validation
    if not payload.employee_code or not payload.full_name:
        raise HTTPException(status_code=400, detail="employee_code and full_name are required")
    return create_employee(session, payload)


@router.get("/", response_model=list[Employee])
def list_employees_endpoint(session: Session = Depends(get_session)):
    return list_employees(session)
