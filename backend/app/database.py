from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

def get_db():
    """
    Dependency that provides a database session for the duration of a request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()