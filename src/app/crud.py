from sqlmodel import Session, select
from .models import Employee, AttendanceRecord, Allowance
from datetime import date as _date


def create_employee(session: Session, employee: Employee) -> Employee:
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


def list_employees(session: Session) -> list[Employee]:
    return session.exec(select(Employee)).all()


def get_employee(session: Session, employee_id: int) -> Employee | None:
    return session.get(Employee, employee_id)


def create_attendance(session: Session, attendance: AttendanceRecord) -> AttendanceRecord:
    # coerce date strings to date objects for SQLite compatibility
    if isinstance(attendance.date, str):
        attendance.date = _date.fromisoformat(attendance.date)
    session.add(attendance)
    session.commit()
    session.refresh(attendance)
    return attendance


def list_attendance_for_employee(session: Session, employee_id: int):
    return session.exec(select(AttendanceRecord).where(AttendanceRecord.employee_id == employee_id)).all()
