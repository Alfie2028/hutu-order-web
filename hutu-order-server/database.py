"""SQLAlchemy 引擎与会话"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI 依赖：每个请求一个独立会话，用完自动关闭"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
