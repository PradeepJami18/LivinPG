import sys
import os

# Add backend to path so 'app' is found
backend_path = os.path.join(os.getcwd(), 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

try:
    from app.database import Base
    # Import main to trigger router -> model imports
    from app.main import app
    
    print("Models imported via app.main.")
    
    for name, table in Base.metadata.tables.items():
        print(f"Table: {name}")
        for key in table.primary_key:
            print(f"  PK: {key.name}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
