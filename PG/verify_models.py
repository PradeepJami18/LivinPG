import sys
import os

# Ensure backend acts as root
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from backend.app.database import Base
    from backend.app import models
    print("Models imported successfully.")
    
    for name, table in Base.metadata.tables.items():
        print(f"Table: {name}, Primary Keys: {[key.name for key in table.primary_key]}")

except Exception as e:
    print(f"Error: {e}")
