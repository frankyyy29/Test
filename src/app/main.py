from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from .db import create_db_and_tables
from .routers import employees, attendance, payroll
from .utils.env_loader import load_from_files


app = FastAPI(title="Intersys I3 Payroll - MVP")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Load environment files if present (project root `.env` and `.env.local`)
    load_from_files([Path.cwd() / ".env", Path.cwd() / ".env.local"])
    create_db_and_tables()


app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(payroll.router)


@app.get("/")
def root():
    return {
        "app": "Intersys I3 Payroll - MVP",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "health": "/health",
        "endpoints": {
            "employees": "POST /employees/, GET /employees/",
            "attendance": "POST /attendance/{employee_id}/records, GET /attendance/{employee_id}/records",
            "payroll": "POST /payroll/run, GET /payroll/runs/{run_id}/payslips, GET /payroll/runs/{run_id}/payslip/{employee_id}/pdf, GET /payroll/runs/{run_id}/export/summary.xlsx"
        }
    }


@app.get("/health")
def health():
    return {"status": "ok"}
