from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).parent
SQLALCHEMY_DB_URL = f"sqlite:///{BASE_DIR / 'app.db'}"

engine = create_engine(
    SQLALCHEMY_DB_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    with SessionLocal() as db:
        yield db
