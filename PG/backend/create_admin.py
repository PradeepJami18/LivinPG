from app.database import SessionLocal
from app.models import User
from app.auth import hash_password

def create_admin():
    db = SessionLocal()
    
    print("--- Create Admin User ---")
    email = input("Enter Admin Email: ")
    password = input("Enter Admin Password: ")
    full_name = input("Enter Admin Name: ")
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        print(f"Error: User with email {email} already exists.")
        db.close()
        return

    admin_user = User(
        full_name=full_name,
        email=email,
        password=hash_password(password),
        phone="0000000000",
        role="admin"
    )

    try:
        db.add(admin_user)
        db.commit()
        print(f"✅ Admin user '{email}' created successfully!")
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
