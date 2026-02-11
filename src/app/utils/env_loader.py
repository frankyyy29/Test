import os
from pathlib import Path
from typing import Iterable


def load_dotenv(path: str | Path) -> None:
    """Load a simple .env file into environment variables.

    Format: lines with KEY=VALUE, ignores comments and blank lines.
    Existing environment variables are not overwritten.
    """
    p = Path(path)
    if not p.exists():
        return

    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and os.environ.get(key) is None:
                os.environ[key] = val


def load_from_files(paths: Iterable[str | Path]) -> None:
    for p in paths:
        load_dotenv(p)
