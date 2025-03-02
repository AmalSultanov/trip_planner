from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from config import sql_database_uri

load_dotenv()

SQL_DATABASE_URI = sql_database_uri

engine = create_engine(
    SQL_DATABASE_URI,
    pool_size=10,
    max_overflow=20,
    pool_timeout=60
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
