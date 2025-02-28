from app import app
from database import init_db
import os

print("Starting database initialization...")
print(f"Current working directory: {os.getcwd()}")
print(f"Database path: {app.config['DATABASE']}")

try:
    with app.app_context():
        init_db()
        print("Database initialized successfully!")
except Exception as e:
    print(f"Error initializing database: {e}")
