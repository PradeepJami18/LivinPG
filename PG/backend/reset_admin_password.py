from app.database import SessionLocal
from app.models import User
from app.auth import hash_password

def reset_admin_password():
    db = SessionLocal()
    try:
        # 1. Try to find 'admin@example.com' first
        print("Searching for admin user...")
        admin = db.query(User).filter(User.email == "admin@example.com").first()

        # 2. If not found, look for ANY admin
        if not admin:
            print("Default admin 'admin@example.com' not found. Checking for any admin...")
            admin = db.query(User).filter(User.role == "admin").first()

        new_password = "admin123"
        hashed_pw = hash_password(new_password)

        if admin:
            # 3. Update existing admin
            print(f"Found admin account: {admin.email}")
            admin.password = hashed_pw
            db.commit()
            print(f"✅ Success! Password for '{admin.email}' has been reset to '{new_password}'")
        else:
            # 4. Create new admin if none exist
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
            print(f"✅ Success! Created new admin '{new_admin.email}' with password '{new_password}'")

    except Exception as e:
        print(f"❌ Error resetting password: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin_password()
