import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE videos ADD COLUMN IF NOT EXISTS topic VARCHAR(50)"))
        conn.execute(text("UPDATE videos SET topic = 'lm' WHERE topic IS NULL"))
    print("OK: videos.topic column ensured")


if __name__ == "__main__":
    main()
