from app.database import engine, Base
from app import models # Ensure models are registered
import sys

def reset_db():
    print("Resetting MySQL Database...")
    try:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database successfully reset (New Schema Applied).")
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_db()
