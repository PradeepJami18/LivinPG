import logging
import sys
import os

# 1. Silence SQLAlchemy logs BEFORE importing anything else
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.orm').setLevel(logging.ERROR)

from app.database import SessionLocal
from app.models import User
from app.auth import verify_password, hash_password

def verify_login_check():
    print("STARTING VERIFICATION...")
    db = SessionLocal()
    email = "admin@example.com"
    password = "admin123"
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ User {email} not found in database!")
            return

        print(f"User found: ID={user.id}")
        
        # Test verification
        try:
            is_valid = verify_password(password, user.password)
        except Exception as e:
            print(f"❌ verify_password logic crashed: {e}")
            is_valid = False

        if is_valid:
            print(f"✅ Success! Password '{password}' matches the stored hash.")
        else:
            print(f"❌ Password verification FAILED for '{password}'.")
            
            # Debugging: Try creating a new hash and seeing if THAT works
            print("Debug: Attempting to hash 'admin123' fresh...")
            new_hash = hash_password("admin123")
            print(f"Generated hash: {new_hash}")
            if verify_password("admin123", new_hash):
                print("Self-verification of new hash works. Updating DB...")
                user.password = new_hash
                db.commit()
                print("✅ Database updated with new working hash.")
            else:
                print("❌ Self-verification failed! Hashing library is broken.")

    except Exception as e:
        print(f"General Error: {e}")
    finally:
        db.close()
        print("VERIFICATION DONE.")

if __name__ == "__main__":
    verify_login_check()
