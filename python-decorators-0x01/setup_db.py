import sqlite3

# Connect to (or create) users.db
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

# Insert some sample users
cursor.executemany('''
INSERT INTO users (name, email)
VALUES (?, ?)
''', [
    ('Alice Johnson', 'alice@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Charlie Brown', 'charlie@example.com')
])

conn.commit()
conn.close()

print("✅ users.db successfully created and populated!")
