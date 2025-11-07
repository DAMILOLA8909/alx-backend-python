#!/usr/bin/python3
"""
A reusable class-based context manager that manages both
database connection and query execution automatically.
"""

import sqlite3


class ExecuteQuery:
    """Custom context manager to handle database connection and query execution."""

    def __init__(self, db_name, query, params=None):
        """
        Initialize the context manager.
        Args:
            db_name (str): Name of the SQLite database file.
            query (str): SQL query to execute.
            params (tuple): Parameters for parameterized queries.
        """
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Establish a connection, execute the query, and return the results."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
            return self.results
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the connection is closed and handle exceptions if any."""
        if self.connection:
            self.connection.close()

        # Returning False allows exceptions to propagate if needed
        return False


if __name__ == "__main__":
    db_name = "users.db"
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(db_name, query, params) as results:
        if results is None:
            print("Query execution failed or returned no results.")
        elif len(results) == 0:
            print("No users found with age greater than 25.")
        else:
            print("Users older than 25:")
            for row in results:
                print(row)
