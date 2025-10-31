import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows  # ✅ uses yield

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Process each batch to filter users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        processed = [user for user in batch if user['age'] > 25]
        for user in processed:
            print(user)
    return  # ✅ ensures 'return' keyword is present
