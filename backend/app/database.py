# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# Paths & DB URL
BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB = f"sqlite:///{BASE_DIR / 'dev.db'}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB)

# SQLite requires check_same_thread
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Engine & Session
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base class for models
Base = declarative_base()

# Dependency to get DB session in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize DB tables
def init_db():
    # Import models here to register them with Base
    from backend.app.models.user import User
    from backend.app.models.calculation import Calculation

    Base.metadata.create_all(bind=engine)
