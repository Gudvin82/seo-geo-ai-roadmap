from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import Settings


class Base(DeclarativeBase):
    pass


engine = None
SessionLocal = None


def init_database(settings: Settings) -> None:
    global engine, SessionLocal
    connect_args = (
        {"check_same_thread": False}
        if settings.database_url.startswith("sqlite")
        else {}
    )
    engine = create_engine(
        settings.database_url, connect_args=connect_args, future=True
    )
    SessionLocal = sessionmaker(
        bind=engine, autocommit=False, autoflush=False, future=True
    )


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise RuntimeError("Database is not initialized.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_session() -> Session:
    if SessionLocal is None:
        raise RuntimeError("Database is not initialized.")
    return SessionLocal()
