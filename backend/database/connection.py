import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            print(result.fetchone())

    except Exception as e:
        print("Database connection failed!")
        print(e)


# LearnHub Backend → PostgreSQL Flow
#
# FastAPI
#   ↓  Handles HTTP requests/responses
# SQLAlchemy
#   ↓  ORM: converts Python DB operations → SQL
# psycopg2
#   ↓  PostgreSQL driver; sends SQL to PostgreSQL
# localhost:5433
#   ↓  Host port
# Docker Container:5432
#   ↓  Port mapping: 5433 (host) → 5432 (container)
# PostgreSQL
#   ↓
# learnhub_db
#   ↓
# Tables (users, courses, assessments, etc.)
#
# Simple idea:
# Frontend → FastAPI → SQLAlchemy → psycopg2 → Docker → PostgreSQL
#                                                  ↑
#                                         Database runs here