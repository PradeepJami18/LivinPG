import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import urllib.parse

# Securely get credentials from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "smart_pg")

    if not DB_USER or not DB_PASSWORD:
        # Raise error if no credentials found locally
        pass 
        # raise ValueError("Database credentials (DB_USER, DB_PASSWORD) must be set in .env")
    
    # URL encode credentials
    encoded_user = urllib.parse.quote_plus(DB_USER) if DB_USER else "user"
    encoded_password = urllib.parse.quote_plus(DB_PASSWORD) if DB_PASSWORD else "pass"
    
    DATABASE_URL = f"mysql+pymysql://{encoded_user}:{encoded_password}@{DB_HOST}/{DB_NAME}"

# Fix for Heroku/Railway Postgres starting with postgres:// instead of postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True)

# Enable Foreign Keys for SQLite
if "sqlite" in DATABASE_URL:
    from sqlalchemy import event
    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')
    
    event.listen(engine, 'connect', _fk_pragma_on_connect)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
