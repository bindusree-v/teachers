#!/usr/bin/env python3
"""
PostgreSQL Database Setup Script
Creates user and database for the adaptive learning system
"""

import psycopg2
from psycopg2 import sql
import sys

# Default PostgreSQL connection (using default postgres user, typically no password on Windows local install)
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = ""  # Empty on local Windows installations

# Database credentials to create
DB_USER = "learnpath_user"
DB_PASSWORD = "LearnPath@2024"
DB_NAME = "learnpath_db"

def setup_database():
    """Create database and user"""
    try:
        # Connect to PostgreSQL as superuser
        print(f"[*] Connecting to PostgreSQL as {POSTGRES_USER}...")
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if user already exists
        print(f"[*] Checking if user '{DB_USER}' exists...")
        cursor.execute(f"SELECT 1 FROM pg_user WHERE usename = '{DB_USER}'")
        if not cursor.fetchone():
            print(f"[+] Creating user '{DB_USER}'...")
            cursor.execute(
                sql.SQL("CREATE USER {} WITH PASSWORD %s CREATEDB")
                .format(sql.Identifier(DB_USER)),
                [DB_PASSWORD]
            )
            print(f"[✓] User '{DB_USER}' created successfully")
        else:
            print(f"[!] User '{DB_USER}' already exists")

        # Check if database already exists
        print(f"[*] Checking if database '{DB_NAME}' exists...")
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        if not cursor.fetchone():
            print(f"[+] Creating database '{DB_NAME}'...")
            cursor.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}")
                .format(sql.Identifier(DB_NAME), sql.Identifier(DB_USER))
            )
            print(f"[✓] Database '{DB_NAME}' created successfully")
        else:
            print(f"[!] Database '{DB_NAME}' already exists")

        cursor.close()
        conn.close()

        # Connect to new database and grant privileges
        print(f"[*] Connecting to database '{DB_NAME}' to set permissions...")
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=DB_NAME
        )
        conn.autocommit = True
        cursor = conn.cursor()

        print(f"[+] Granting schema privileges to '{DB_USER}'...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON SCHEMA public TO {DB_USER}")
        cursor.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {DB_USER}")
        cursor.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO {DB_USER}")

        cursor.close()
        conn.close()

        print(f"\n✅ PostgreSQL setup completed successfully!")
        print(f"   Database: {DB_NAME}")
        print(f"   User: {DB_USER}")
        print(f"   Host: {POSTGRES_HOST}:{POSTGRES_PORT}")
        return True

    except psycopg2.Error as e:
        print(f"\n❌ PostgreSQL Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
