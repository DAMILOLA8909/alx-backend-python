#!/usr/bin/python3
"""
Run multiple database queries concurrently using asyncio.gather
and the aiosqlite library.
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users from the database asynchronously."""
    db_name = "users.db"
    try:
        async with aiosqlite.connect(db_name) as db:
            async with db.execute("SELECT * FROM users") as cursor:
                results = await cursor.fetchall()
                print("\nAll users:")
                for row in results:
                    print(row)
                return results
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return []


async def async_fetch_older_users():
    """Fetch users older than 40 from the database asynchronously."""
    db_name = "users.db"
    try:
        async with aiosqlite.connect(db_name) as db:
            async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
                results = await cursor.fetchall()
                print("\nUsers older than 40:")
                for row in results:
                    print(row)
                return results
    except Exception as e:
        print(f"Error fetching older users: {e}")
        return []


async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather."""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
