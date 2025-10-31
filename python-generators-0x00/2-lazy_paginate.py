#!/usr/bin/python3
"""Implements lazy pagination using a generator."""

import mysql.connector


def paginate_users(page_size, offset):
    """Fetch a page of users from the database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="damsony",
            database="alx_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset};"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []


def lazy_pagination(page_size):
    """Generator that yields users in pages, fetching lazily."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
