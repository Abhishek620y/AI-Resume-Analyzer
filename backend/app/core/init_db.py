"""
Run this once (or on app startup in dev) to create all tables from the
SQLAlchemy models. For production, this would be replaced by Alembic
migrations — kept simple here since we're on SQLite for now.

Usage:
    python -m app.core.init_db
"""
from app.core.database import Base, engine
from app import models  # noqa: F401 — ensures all models are registered on Base


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


if __name__ == "__main__":
    init_db()
