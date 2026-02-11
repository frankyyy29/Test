This folder is a placeholder for Alembic migrations. The project uses SQLModel metadata
for schema creation during startup (see `src/app/db.py`). To enable full migrations:

1. Configure `alembic.ini` connection string and `script_location`.
2. Use `alembic revision --autogenerate -m "init"` then `alembic upgrade head`.
