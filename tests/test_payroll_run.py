import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from src.app.main import app


def test_payroll_run_creates_payslips():
    with TestClient(app) as client:
        # create employee
        emp_payload = {
            "employee_code": "E100",
            "full_name": "Ana Santos",
            "employee_type": "attendance",
            "position": "Engineer",
            "basic_salary": 30000.0,
            "bank_bpi_account": "9876543210"
        }
        r = client.post("/employees/", json=emp_payload)
        assert r.status_code == 200
        emp = r.json()

        # add one attendance record in cutoff
        attendance_payload = {
            "date": "2026-02-01",
            "time_in": "08:00",
            "time_out": "17:00",
            "break_minutes": 60,
            "ot_minutes": 0,
            "late_minutes": 0,
            "status": "present"
        }
        r2 = client.post(f"/attendance/{emp['id']}/records", json=attendance_payload)
        assert r2.status_code == 200

        # run payroll for cutoff
        r3 = client.post("/payroll/run?start_date=2026-02-01&end_date=2026-02-15")
        assert r3.status_code == 200
        data = r3.json()
        assert "payroll_run_id" in data
        assert any(item["employee_id"] == emp["id"] for item in data["summary"])
