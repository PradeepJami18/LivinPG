import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv

from app.models import User
from app.auth import hash_password

def reset_admin_password_v2():
    load_dotenv(find_dotenv())
    
    # Re-construct DATABASE_URL as in app/database.py to avoid using the global engine with echo=True
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_NAME = os.getenv("DB_NAME", "smart_pg")
        
        encoded_user = urllib.parse.quote_plus(DB_USER) if DB_USER else "user"
        encoded_password = urllib.parse.quote_plus(DB_PASSWORD) if DB_PASSWORD else "pass"
        DATABASE_URL = f"mysql+pymysql://{encoded_user}:{encoded_password}@{DB_HOST}/{DB_NAME}"

    # Create engine with echo=False to silence logs
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    
    db = SessionLocal()
    try:
        print("Searching for admin user...")
        # 1. Search for 'admin@example.com'
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        
        # 2. Search for any admin
        if not admin:
            print("Specific admin 'admin@example.com' not found. Searching for any admin role...")
            admin = db.query(User).filter(User.role == "admin").first()

        new_password = "admin123"
        hashed_pw = hash_password(new_password)

        if admin:
            print(f"Found admin account: {admin.email}")
            admin.password = hashed_pw
            db.commit()
            print("--------------------------------------------------")
            print(f"PASSWORD RESET SUCCESSFUL")
            print(f"Email:    {admin.email}")
            print(f"Password: {new_password}")
            print("--------------------------------------------------")
        else:
            print("No admin account found. Creating a new one...")
            new_admin = User(
                full_name="System Admin",
                email="admin@example.com",
                password=hashed_pw,
                phone="0000000000",
                role="admin"
            )
            db.add(new_admin)
            db.commit()
            print("--------------------------------------------------")
            print(f"ADMIN CREATED SUCCESSFUL")
            print(f"Email:    {new_admin.email}")
            print(f"Password: {new_password}")
            print("--------------------------------------------------")

    except Exception as e:
        print(f"❌ Error resetting password: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin_password_v2()
