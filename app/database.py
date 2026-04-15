from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# PostgreSQL connection
DATABASE_URL= "postgresql://postgres:Bindu08@localhost:5433/ai_powered_adaptive_learning_system"
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql://postgres:Bindu08@localhost:5433/ai_powered_adaptive_learning_system"
# )

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DATABASE_ECHO", "False").lower() == "true"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()