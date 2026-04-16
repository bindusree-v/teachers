from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, dotenv_values
import os
from pathlib import Path

# Always load teachers/.env explicitly (works regardless of current terminal cwd)
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)
ENV_VALUES = dotenv_values(ENV_PATH)

# Database connection
DATABASE_URL = ENV_VALUES.get("DATABASE_URL") or os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = URL.create(
        "postgresql+psycopg2",
        username=ENV_VALUES.get("POSTGRES_USER") or os.getenv("POSTGRES_USER", "postgres"),
        password=ENV_VALUES.get("POSTGRES_PASSWORD") or os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=ENV_VALUES.get("POSTGRES_HOST") or os.getenv("POSTGRES_HOST", "localhost"),
        port=int(ENV_VALUES.get("POSTGRES_PORT") or os.getenv("POSTGRES_PORT", "5432")),
        database=ENV_VALUES.get("POSTGRES_DB") or os.getenv("POSTGRES_DB", "learnpath_db"),
    ).render_as_string(hide_password=False)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DATABASE_ECHO", "False").lower() == "true",
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()