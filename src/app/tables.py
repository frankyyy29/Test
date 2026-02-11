import csv
import pkgutil
from pathlib import Path
from typing import List, Dict

BASE = Path(__file__).parent / "data"


def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def load_tax_brackets() -> List[Dict]:
    rows = _read_csv(BASE / "tax_brackets.csv")
    brackets = []
    for r in rows:
        brackets.append({
            "lower": float(r["lower"]),
            "upper": float(r["upper"]),
            "fixed": float(r.get("fixed", 0)),
            "pct": float(r.get("pct", 0)),
        })
    brackets.sort(key=lambda x: x["lower"])
    return brackets


def compute_annual_withholding(taxable_annual: float) -> float:
    brackets = load_tax_brackets()
    for b in brackets:
        if taxable_annual <= b["upper"]:
            over = max(0.0, taxable_annual - b["lower"])
            return round(b["fixed"] + b["pct"] * over, 2)
    return 0.0


def load_sss_table() -> List[Dict]:
    rows = _read_csv(BASE / "sss_table.csv")
    table = []
    for r in rows:
        table.append({
            "from": float(r["range_from"]),
            "to": float(r["range_to"]),
            "employee": float(r["employee_share"]),
        })
    table.sort(key=lambda x: x["from"])
    return table


def compute_sss_monthly(monthly_salary: float) -> float:
    table = load_sss_table()
    for row in table:
        if monthly_salary >= row["from"] and monthly_salary <= row["to"]:
            return row["employee"]
    return table[-1]["employee"] if table else 0.0


def load_philhealth_rate() -> float:
    rows = _read_csv(BASE / "philhealth.csv")
    if not rows:
        return 0.03
    return float(rows[0].get("rate", 0.03))


def compute_philhealth_monthly(monthly_salary: float) -> float:
    rate = load_philhealth_rate()
    # total rate applied to monthly salary, employee share is half
    total = monthly_salary * rate
    return round(total / 2.0, 2)


def compute_pagibig_monthly() -> float:
    # default fixed contribution per month (employee share)
    return 100.0
