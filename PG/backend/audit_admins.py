from app.database import SessionLocal
from app.models import User

def list_admins():
    db = SessionLocal()
    try:
        admins = db.query(User).filter(User.role == "admin").all()
        if not admins:
            print("No admin users found.")
        else:
            print("Found admin users:")
            for admin in admins:
                print(f" - ID: {admin.id}, Email: {admin.email}, Name: {admin.full_name}")
    except Exception as e:
        print(f"Error checking admins: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_admins()
