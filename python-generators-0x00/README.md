# Python Generators – Task 0: Database Setup

### Objective
Create a generator that streams rows from an SQL database one by one.

This first task sets up a MySQL database and populates it with sample data.

### Files
- **seed.py** – Contains all database setup and seeding functions.
- **0-main.py** – Test script to verify functionality.
- **user_data.csv** – Sample user data.

### Functions Implemented
- `connect_db()` – Connects to the MySQL server.
- `create_database(connection)` – Creates `ALX_prodev` database if it doesn’t exist.
- `connect_to_prodev()` – Connects to the `ALX_prodev` database.
- `create_table(connection)` – Creates the `user_data` table.
- `insert_data(connection, data)` – Inserts data from `user_data.csv`.

### Expected Output

connection successful
Table user_data created successfully
Database ALX_prodev is present
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com
', 67), ...]


### Dependencies
- `mysql-connector-python`
- Python 3.8+

Install using:
```bash
pip install mysql-connector-python
```