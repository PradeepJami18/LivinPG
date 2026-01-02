import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import urllib.parse

# Securely get credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "smart_pg")

if not DB_USER or not DB_PASSWORD:
    # Fallback for local development if desired, or raise error. 
    # For industry ready, we should probably warn or error.
    # For now, let's assume if missing, we use a placeholder or raise.
    # Let's keep it safe but strict.
    raise ValueError("Database credentials (DB_USER, DB_PASSWORD) must be set in .env")

# URL encode credentials to handle special characters like '@'
encoded_user = urllib.parse.quote_plus(DB_USER)
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

DATABASE_URL = f"mysql+pymysql://{encoded_user}:{encoded_password}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
