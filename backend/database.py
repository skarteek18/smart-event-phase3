
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Database URL from environment variables

DATABASE_URL = os.getenv(
"DATABASE_URL",
"sqlite:///./smartevent.db",
)

SQLite requires this option for FastAPI's request handling

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
connect_args["check_same_thread"] = False

Create SQLAlchemy engine

engine = create_engine(
DATABASE_URL,
connect_args=connect_args,
pool_pre_ping=True,
)

Create database session factory

SessionLocal = sessionmaker(
autocommit=False,
autoflush=False,
bind=engine,
)

Base class for SQLAlchemy models

Base = declarative_base()

Dependency for database sessions

def get_db():
db = SessionLocal()

try:
    yield db
finally:
    db.close()

Initialize database tables

def init_db():
# Import models so SQLAlchemy registers every table
import models  # noqa: F401

Base.metadata.create_all(bind=engine)
