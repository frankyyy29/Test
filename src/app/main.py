from fastapi import FastAPI
from pathlib import Path
from .db import create_db_and_tables
from .routers import employees, attendance, payroll
from .utils.env_loader import load_from_files


app = FastAPI(title="Intersys I3 Payroll - MVP")


@app.on_event("startup")
def on_startup():
    # Load environment files if present (project root `.env` and `.env.local`)
    load_from_files([Path.cwd() / ".env", Path.cwd() / ".env.local"])
    create_db_and_tables()


app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(payroll.router)


@app.get("/health")
def health():
    return {"status": "ok"}
