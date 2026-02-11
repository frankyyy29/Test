import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from src.app.main import app


def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


def test_create_employee_and_attendance():
    emp_payload = {
        "employee_code": "E001",
        "full_name": "Juan Dela Cruz",
        "employee_type": "attendance",
        "position": "Staff",
        "basic_salary": 20000.0,
        "bank_bpi_account": "1234567890"
    }
    with TestClient(app) as client:
        r = client.post("/employees/", json=emp_payload)
        assert r.status_code == 200
        emp = r.json()
        assert emp["employee_code"] == "E001"

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
        rec = r2.json()
        assert rec["employee_id"] == emp["id"]
