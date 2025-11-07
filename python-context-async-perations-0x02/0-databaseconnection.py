#!/usr/bin/python3
"""
A class-based context manager that handles opening and closing
a database connection automatically with error handling.
"""

import sqlite3


class DatabaseConnection:
    """Custom context manager for managing database connections."""

    def __init__(self, db_name):
        """Initialize with database name."""
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Open and return the database connection."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            return self.connection
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection upon exit."""
        if self.connection:
            self.connection.close()
        # Returning False ensures that exceptions are not suppressed
        return False


if __name__ == "__main__":
    db_name = "users.db"

    with DatabaseConnection(db_name) as conn:
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()

                if results:
                    print("Users table results:")
                    for row in results:
                        print(row)
                else:
                    print("No records found in the 'users' table.")

            except sqlite3.OperationalError as e:
                # This typically happens if the table does not exist
                print(f"Database operation failed: {e}")
            except Exception as e:
                # Catch any other unexpected errors
                print(f"An unexpected error occurred: {e}")
        else:
            print("Failed to connect to the database.")
