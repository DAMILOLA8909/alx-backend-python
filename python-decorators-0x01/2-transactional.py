#!/usr/bin/python3
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


def transactional(func):
    """Decorator to manage database transactions"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()      # ✅ Commit if successful
        except Exception as e:
            conn.rollback()    # ❌ Rollback if an error occurs
            raise e            # Re-raise the error for visibility
        return result
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Update user's email with automatic transaction handling
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("✅ Email updated successfully!")
