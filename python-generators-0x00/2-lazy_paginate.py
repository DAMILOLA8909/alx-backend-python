import mysql.connector

def lazy_pagination(batch_size):
    """Generator that yields pages of users lazily from the database"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",  # change if needed
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM user_data;")
    total_records = cursor.fetchone()['total']

    offset = 0
    while offset < total_records:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s;", (batch_size, offset))
        users = cursor.fetchall()
        if not users:
            break
        yield users  # ✅ yield each page lazily
        offset += batch_size

    cursor.close()
    connection.close()
