#!/usr/bin/python3
import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}


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


def cache_query(func):
    """Decorator to cache query results to avoid redundant DB calls"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        if query in query_cache:
            print("⚡ Using cached result for query:", query)
            return query_cache[query]

        print("🆕 Executing and caching result for query:", query)
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print("\nFirst call result:", users)
print("Second call result (from cache):", users_again)
