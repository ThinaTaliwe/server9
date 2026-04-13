"""Database engine and session configuration.

This module creates a SQLAlchemy engine and a session factory.  Use
``get_session`` as a dependency in your FastAPI endpoints to obtain a database session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings


# Create the SQLAlchemy engine.  The pool_pre_ping option checks the connection
# before each checkout to avoid stale connections.  echo can be enabled for
# debugging SQL statements.
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Session factory.  expire_on_commit=False allows objects to retain their state
# after session.commit().
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Yield a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()