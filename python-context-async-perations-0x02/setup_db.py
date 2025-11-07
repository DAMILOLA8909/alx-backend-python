import sqlite3

def setup_database():
    # Connect to (or create) the database file
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    # Clear old data (optional, ensures clean setup)
    cursor.execute("DELETE FROM users")

    # Insert sample users
    users_data = [
        ("Alice Johnson", "alice@example.com"),
        ("Bob Smith", "bob@example.com"),
        ("Charlie Brown", "charlie@example.com")
    ]
    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users_data)

    # Save and close connection
    conn.commit()
    conn.close()
    print("✅ Database setup complete! users.db is ready.")

if __name__ == "__main__":
    setup_database()
