import sqlite3
from flask import current_app


def get_db_connection() -> sqlite3.Connection:
    print(f"Connecting to database at: {current_app.config['DATABASE']}")  # Debug print
    conn = sqlite3.connect(current_app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with schema and test data"""
    print(f"Initializing database at: {current_app.config['DATABASE']}")  # Debug print
    connection = sqlite3.connect(current_app.config["DATABASE"])

    # Drop existing table if it exists
    connection.execute("DROP TABLE IF EXISTS permits")

    # Create permits table with updated schema
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS permits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lot TEXT NOT NULL,
            price REAL NOT NULL,
            school TEXT NOT NULL
        )
    """
    )

    # Add some test data with school field
    connection.execute(
        """
        INSERT INTO permits (name, lot, price, school)
        VALUES 
            ('Test Owner', 'Lot A', 100.00, 'Test University'),
            ('Another Owner', 'Lot B', 150.00, 'Another University')
    """
    )

    connection.commit()
    connection.close()
    print("Database initialized successfully!")  # Debug print
