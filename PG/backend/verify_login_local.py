from app.database import SessionLocal
from app.models import User
from app.auth import verify_password, hash_password

def verify_login_check():
    db = SessionLocal()
    email = "admin@example.com"
    password = "admin123"
    
    print(f"--- Verifying Login for {email} ---")
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print("❌ User not found in database!")
            return

        print(f"User found: ID={user.id}, Role={user.role}")
        print(f"Stored Hash: {user.password}")

        # Test verification
        is_valid = verify_password(password, user.password)
        
        if is_valid:
            print("✅ Password 'admin123' works correctly with the stored hash.")
        else:
            print("❌ Password verification FAILED.")
            print("Attempting to re-hash and update immediately...")
            
            new_hash = hash_password(password)
            user.password = new_hash
            db.commit()
            print("Updated password hash.")
            
            # Re-verify
            if verify_password(password, new_hash):
                 print("✅ Re-verification successful. Try logging in again.")
            else:
                 print("❌ CRITICAL: Even the new hash failed verification immediately.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_login_check()
