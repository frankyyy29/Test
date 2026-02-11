# Intersys I3 Payroll (MVP FastAPI scaffold)

This repository contains a minimal FastAPI scaffold for a payroll application (attendance and non-attendance employees).

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

2. Run the app locally:

```bash
uvicorn src.app.main:app --reload
```

Run with Docker:

```bash
docker build -t intersys-payroll:latest .
docker run -p 10000:10000 -e PORT=10000 --name payroll intersys-payroll:latest
# then visit http://localhost:10000/health
```

3. Run tests:

```bash
pytest -q
```

Data files (SQLite) will be created under `data/payroll.db`. Put that `data/` folder inside a Google Drive-synced directory if you want it backed up.
