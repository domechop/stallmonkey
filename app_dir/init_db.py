import sqlite3
import os

print("Starting database creation...")
db_path = os.path.join(os.path.dirname(__file__), "permits.db")
print(f"Creating database at: {db_path}")

try:
    connection = sqlite3.connect(db_path)
    print("Connected to database")

    # Create permits table
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
    print("Created table")

    # Add test data
    connection.execute(
        """
        INSERT INTO permits (name, lot, price, school)
        VALUES
            ('Test Owner', 'Lot A', 100.00, 'Test University'),
            ('Another Owner', 'Lot B', 150.00, 'Another University')
    """
    )
    print("Added test data")

    connection.commit()
    connection.close()
    print("Database initialized successfully!")
except Exception as e:
    print(f"Error: {e}")
