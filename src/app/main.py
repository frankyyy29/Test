from fastapi import FastAPI
from .db import create_db_and_tables
from .routers import employees, attendance, payroll


app = FastAPI(title="Intersys I3 Payroll - MVP")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(payroll.router)


@app.get("/health")
def health():
    return {"status": "ok"}
