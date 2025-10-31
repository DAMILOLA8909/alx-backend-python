#!/usr/bin/python3
"""
0-stream_users.py
A generator function that streams user data one row at a time from MySQL.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that streams rows one by one from user_data table.
    Yields each row as a dictionary.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",             # 👈 change to your MySQL username
            password="yourpassword", # 👈 change to your MySQL password
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            # Yield each row one by one
            for row in cursor:
                yield row

    except Error as e:
        print(f"Error while streaming users: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
