import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from src.app.main import app


def test_payslip_pdf_and_excel_export():
    with TestClient(app) as client:
        # create employee
        emp_payload = {
            "employee_code": "E200",
            "full_name": "Marco Polo",
            "employee_type": "attendance",
            "position": "Analyst",
            "basic_salary": 25000.0,
            "bank_bpi_account": "555666777"
        }
        r = client.post("/employees/", json=emp_payload)
        assert r.status_code == 200
        emp = r.json()

        attendance_payload = {
            "date": "2026-02-02",
            "time_in": "08:00",
            "time_out": "17:00",
            "break_minutes": 60,
            "ot_minutes": 0,
            "late_minutes": 0,
            "status": "present"
        }
        r2 = client.post(f"/attendance/{emp['id']}/records", json=attendance_payload)
        assert r2.status_code == 200

        # run payroll
        r3 = client.post("/payroll/run?start_date=2026-02-01&end_date=2026-02-15")
        assert r3.status_code == 200
        run_id = r3.json()["payroll_run_id"]

        # request pdf
        rpdf = client.get(f"/payroll/runs/{run_id}/payslip/{emp['id']}/pdf")
        assert rpdf.status_code == 200
        assert rpdf.headers.get("content-type") == "application/pdf"

        # request excel
        rex = client.get(f"/payroll/runs/{run_id}/export/summary.xlsx")
        assert rex.status_code == 200
        assert "openxmlformats-officedocument.spreadsheetml.sheet" in rex.headers.get("content-type")
