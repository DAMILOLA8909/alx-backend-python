#!/usr/bin/python3
import time
import sqlite3
import functools


def with_db_connection(func):
    """Decorator to automatically open and close a database connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Decorator factory to retry a function if it fails due to transient errors"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    attempts += 1
                    print(f"⚠️ Attempt {attempts} failed: {e}")
                    if attempts < retries:
                        print(f"⏳ Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("❌ All retry attempts failed.")
                        raise e
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
