from datetime import date
from typing import Dict
import json
from .models import Employee, AttendanceRecord
from sqlmodel import Session, select
from .tables import compute_sss_monthly, compute_philhealth_monthly, compute_pagibig_monthly, compute_annual_withholding


def _days_in_month(d: date) -> int:
    if d.month == 12:
        next_month = date(d.year + 1, 1, 1)
    else:
        next_month = date(d.year, d.month + 1, 1)
    return (next_month - date(d.year, d.month, 1)).days


def _hourly_rate_from_basic(basic_monthly: float) -> float:
    return basic_monthly / (22 * 8)


def compute_payslip_for_employee(session: Session, employee: Employee, start: date, end: date) -> Dict:
    # Gather attendance records in cutoff
    stmt = select(AttendanceRecord).where(
        AttendanceRecord.employee_id == employee.id,
        AttendanceRecord.date >= start,
        AttendanceRecord.date <= end,
    )
    records = session.exec(stmt).all()

    # Count paid days (present + leave)
    paid_days = sum(1 for r in records if r.status in ("present", "leave"))
    total_days = _days_in_month(start)

    cutoffs_per_year = 24  # semi-monthly

    if employee.employee_type == "non_attendance":
        gross = employee.rate_per_cutoff or 0.0
        hourly = _hourly_rate_from_basic(employee.basic_salary or 0.0)
        ot = 0.0
        lates = 0.0
    else:
        basic_monthly = employee.basic_salary or 0.0
        prorated = basic_monthly * (paid_days / total_days) if total_days > 0 else 0.0
        hourly = _hourly_rate_from_basic(basic_monthly)
        ot_minutes = sum(r.ot_minutes for r in records)
        ot = (ot_minutes / 60.0) * hourly * 1.25
        late_minutes = sum(r.late_minutes for r in records)
        lates = (late_minutes / 60.0) * hourly
        gross = prorated + ot

    # Convert cut-off gross to monthly equivalent (semi-monthly => *2)
    monthly_gross = gross * (cutoffs_per_year / 12)

    # statutory monthly contributions
    monthly_sss = compute_sss_monthly(monthly_gross)
    monthly_phil = compute_philhealth_monthly(monthly_gross)
    monthly_pagibig = compute_pagibig_monthly()

    # prorate back to cut-off
    sss_cutoff = round(monthly_sss / (cutoffs_per_year / 12), 2)
    phil_cutoff = round(monthly_phil / (cutoffs_per_year / 12), 2)
    pagibig_cutoff = round(monthly_pagibig / (cutoffs_per_year / 12), 2)

    # annualize taxable income for withholding calculation
    monthly_taxable = monthly_gross - (monthly_sss + monthly_phil + monthly_pagibig)
    annual_taxable = monthly_taxable * 12
    annual_withholding = compute_annual_withholding(annual_taxable)
    withholding_cutoff = round(annual_withholding / cutoffs_per_year, 2)

    total_deductions = sss_cutoff + phil_cutoff + pagibig_cutoff + lates + withholding_cutoff

    net = round(gross - total_deductions, 2)

    details = {
        "gross_components": {"basic_plus_proration": round(gross - ot, 2), "ot": round(ot, 2)},
        "deductions": {"sss": sss_cutoff, "philhealth": phil_cutoff, "pagibig": pagibig_cutoff, "lates": round(lates, 2), "tax": withholding_cutoff},
    }

    return {"gross": round(gross, 2), "deductions": round(total_deductions, 2), "net": net, "details": json.dumps(details)}
