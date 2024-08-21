from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker


# SQLAlchemy setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BACKEND_PATH = os.getenv("BACKEND_PATH", "")

DATABASE_URL = f"sqlite:///{os.path.join(BACKEND_PATH, 'test.db')}"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
