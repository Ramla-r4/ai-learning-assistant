import os
from app.db.base import Base, engine
from app.db import models

DB_FILE = "app.db"

# Delete old database file if it exists
if os.path.exists(DB_FILE):
    print("Deleting old database...")
    os.remove(DB_FILE)

# Recreate all tables
print("Creating new database and tables...")
Base.metadata.create_all(bind=engine)
print("Done! New database initialized.")
