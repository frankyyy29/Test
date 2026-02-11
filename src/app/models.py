from __future__ import annotations
from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field


class Allowance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")
    name: str
    amount: float
    taxable: bool = True


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_code: str = Field(index=True)
    full_name: str
    employee_type: str = Field(default="attendance")  # 'attendance' | 'non_attendance'
    position: Optional[str] = None
    date_joined: Optional[date] = None
    basic_salary: Optional[float] = 0.0
    rate_per_cutoff: Optional[float] = 0.0
    bank_bpi_account: Optional[str] = None

    # allowances relationship intentionally omitted for a simpler MVP


class AttendanceRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    date: date
    time_in: Optional[str] = None
    time_out: Optional[str] = None
    break_minutes: int = 0
    ot_minutes: int = 0
    late_minutes: int = 0
    status: str = Field(default="present")  # present|absent|leave


class PayrollRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    generated_at: Optional[date] = None
    status: str = Field(default="completed")


class Payslip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    payroll_run_id: Optional[int] = Field(default=None, foreign_key="payrollrun.id")
    employee_id: int = Field(foreign_key="employee.id")
    gross: Optional[float] = 0.0
    deductions: Optional[float] = 0.0
    net_pay: Optional[float] = 0.0
    details: Optional[str] = None  # JSON string with breakdown
