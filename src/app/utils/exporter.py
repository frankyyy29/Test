from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from pathlib import Path
from typing import Optional
from sqlmodel import Session, select
from ..models import Payslip, Employee
import json
from openpyxl import Workbook


def ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def generate_payslip_pdf(session: Session, payroll_run_id: int, employee_id: int, output_path: Path) -> Path:
    # load payslip and employee
    ps = session.exec(select(Payslip).where(Payslip.payroll_run_id == payroll_run_id, Payslip.employee_id == employee_id)).one()
    emp = session.get(Employee, employee_id)

    ensure_dir(output_path)
    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    styles = getSampleStyleSheet()
    flow = []

    flow.append(Paragraph(f"Payslip - {emp.full_name}", styles["Title"]))
    flow.append(Spacer(1, 12))

    details = json.loads(ps.details) if ps.details else {}

    rows = [
        ["Employee Code", emp.employee_code],
        ["Position", emp.position or ""],
        ["Gross", f"{ps.gross:.2f}"],
        ["Deductions", f"{ps.deductions:.2f}"],
        ["Net Pay", f"{ps.net_pay:.2f}"],
    ]

    t = Table(rows, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 12))

    # add breakdown if available
    if details:
        flow.append(Paragraph("Breakdown", styles["Heading2"]))
        for k, v in details.get("gross_components", {}).items():
            flow.append(Paragraph(f"{k}: {v}", styles["Normal"]))
        flow.append(Spacer(1, 6))
        for k, v in details.get("deductions", {}).items():
            flow.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    doc.build(flow)
    return output_path


def generate_summary_excel(session: Session, payroll_run_id: int, output_path: Path) -> Path:
    ensure_dir(output_path)
    wb = Workbook()
    ws = wb.active
    ws.title = "Payroll Summary"
    headers = ["employee_id", "employee_code", "full_name", "gross", "deductions", "net_pay"]
    ws.append(headers)

    slips = session.exec(select(Payslip).where(Payslip.payroll_run_id == payroll_run_id)).all()
    for s in slips:
        emp = session.get(Employee, s.employee_id)
        ws.append([s.employee_id, emp.employee_code, emp.full_name, float(s.gross or 0), float(s.deductions or 0), float(s.net_pay or 0)])

    wb.save(str(output_path))
    return output_path
