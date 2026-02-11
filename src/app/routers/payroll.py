from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..models import Employee, PayrollRun, Payslip
from ..payroll import compute_payslip_for_employee
from datetime import date
from fastapi.responses import FileResponse
from pathlib import Path
from ..utils.exporter import generate_payslip_pdf, generate_summary_excel

router = APIRouter(prefix="/payroll", tags=["payroll"])


@router.post("/run")
def run_payroll(start_date: str, end_date: str, session: Session = Depends(get_session)):
    try:
        s = date.fromisoformat(start_date)
        e = date.fromisoformat(end_date)
    except Exception:
        raise HTTPException(status_code=400, detail="start_date and end_date must be ISO dates YYYY-MM-DD")

    # Create payroll run record
    pr = PayrollRun(start_date=s, end_date=e, generated_at=date.today(), status="completed")
    session.add(pr)
    session.commit()
    session.refresh(pr)

    employees = session.exec(select(Employee)).all()
    result = []
    for emp in employees:
        slip = compute_payslip_for_employee(session, emp, s, e)
        ps = Payslip(payroll_run_id=pr.id, employee_id=emp.id, gross=slip["gross"], deductions=slip["deductions"], net_pay=slip["net"], details=slip["details"])
        session.add(ps)
        result.append({"employee_id": emp.id, "net": slip["net"]})

    session.commit()

    return {"payroll_run_id": pr.id, "summary": result}


@router.get("/runs/{run_id}/payslips")
def list_payslips(run_id: int, session: Session = Depends(get_session)):
    pr = session.get(PayrollRun, run_id)
    if not pr:
        raise HTTPException(status_code=404, detail="Payroll run not found")
    slips = session.exec(select(Payslip).where(Payslip.payroll_run_id == run_id)).all()
    return slips


@router.get("/runs/{run_id}/payslip/{employee_id}/pdf")
def get_payslip_pdf(run_id: int, employee_id: int, session: Session = Depends(get_session)):
    pr = session.get(PayrollRun, run_id)
    if not pr:
        raise HTTPException(status_code=404, detail="Payroll run not found")
    # ensure payslip exists
    ps = session.exec(select(Payslip).where(Payslip.payroll_run_id == run_id, Payslip.employee_id == employee_id)).one_or_none()
    if not ps:
        raise HTTPException(status_code=404, detail="Payslip not found for employee in this run")
    out_dir = Path("storage/payslips") / f"{pr.start_date.isoformat()}_{pr.end_date.isoformat()}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"payslip_{employee_id}.pdf"
    generate_payslip_pdf(session, run_id, employee_id, out_path)
    return FileResponse(str(out_path), media_type="application/pdf", filename=out_path.name)


@router.get("/runs/{run_id}/export/summary.xlsx")
def get_summary_excel(run_id: int, session: Session = Depends(get_session)):
    pr = session.get(PayrollRun, run_id)
    if not pr:
        raise HTTPException(status_code=404, detail="Payroll run not found")
    out_dir = Path("storage/exports") / f"{pr.start_date.isoformat()}_{pr.end_date.isoformat()}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "payroll_summary.xlsx"
    generate_summary_excel(session, run_id, out_path)
    return FileResponse(str(out_path), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=out_path.name)
