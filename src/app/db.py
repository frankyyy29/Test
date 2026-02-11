from sqlmodel import create_engine, Session, SQLModel
from typing import Iterator
import os

DATABASE_URL = "sqlite:///./data/payroll.db"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    # Ensure data directory exists for SQLite file
    db_path = os.path.join(os.getcwd(), "data")
    os.makedirs(db_path, exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
