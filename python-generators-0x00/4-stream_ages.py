#!/usr/bin/python3
"""Compute average user age using a generator for memory efficiency."""

import mysql.connector


def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="damsony",
            database="alx_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data;")

        # Yield one age at a time instead of loading all rows
        for (age,) in cursor:
            yield age

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return


def compute_average_age():
    """Calculate and print the average age of users using a generator."""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found in database.")


if __name__ == "__main__":
    compute_average_age()
