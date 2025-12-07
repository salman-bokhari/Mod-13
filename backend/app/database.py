from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB = f"sqlite:///{BASE_DIR / 'dev.db'}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()

def init_db():
    from backend.app.models.user import User
    Base.metadata.create_all(bind=engine)
