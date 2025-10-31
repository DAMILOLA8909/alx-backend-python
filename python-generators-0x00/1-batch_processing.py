#!/usr/bin/python3
"""
1-batch_processing.py
Streams user data from the database in batches and processes them using generators.
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function to fetch rows in batches from user_data table.
    Yields one batch (a list of dicts) at a time.
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

            # Fetch rows in batches using fetchmany()
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch  # Yield one batch at a time

    except Error as e:
        print(f"Error while streaming in batches: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch: filters users over age 25 and yields them.
    Prints each filtered user (as required by the task).
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for user in batch:  # Loop 2
            if user["age"] > 25:
                print(user)  # Print each processed user
                yield user  # Optionally yield (for testing / reusability)
