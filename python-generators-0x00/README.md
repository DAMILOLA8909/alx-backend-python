# 🐍 Python Generators — 0x00 Project
📘 Project Overview

This project demonstrates the use of Python generators to efficiently fetch, process, and stream data from a MySQL database.
Generators allow data to be loaded lazily — one item or batch at a time — improving memory efficiency and performance.

---

🎯 Learning Objectives

By completing this project, you will learn how to:

- Connect to and interact with a MySQL database using Python.

- Use **generators** (yield) to stream data lazily.

- Create **batch processors** for handling large datasets efficiently.

- Implement **lazy pagination** for large SQL tables.

---

## 📂 Project Structure

```bash
python-generators-0x00/
│
├── seed.py                # Sets up database and seeds user data
├── 0-main.py              # Tests seed.py setup
├── 0-stream_users.py      # Streams rows one by one using yield
├── 1-batch_processing.py  # Fetches and processes rows in batches
├── 2-lazy_paginate.py     # Implements lazy pagination generator
├── 3-main.py              # Tests the lazy pagination function
├── user_data.csv          # Sample user dataset
└── README.md              # Project documentation
```
---

## ⚙️ Setup Instructions
 1. Install Dependencies

Make sure you have Python and MySQL installed.
Then install the required Python library:
```bash
pip install mysql-connector-python
```

2. Database Setup

Run seed.py to create the database and populate it with sample data:

```bash
python3 0-main.py
```
You should see:

```pgsql
connection successful
Table user_data created successfully
Database ALX_prodev is present
```



---

## Task 0: Database Setup

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
---

## Task 1: Stream Users with Generators

### Objective
Create a Python generator that streams rows from the SQL database `user_data` table one by one.

### File
- **0-stream_users.py**

### Function
```python
def stream_users():
    """Streams rows one by one from user_data table."""
```

#### Usage
```bash
$ ./1-main.py
```

#### Example Output
```bash
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
...
```
### Notes

- Uses a Python generator (yield) for memory-efficient data streaming.

- Contains only one loop.

---

## Task 2: Batch Streaming and Processing

### Objective
Create a generator to fetch and process data in batches from the `user_data` table.

### Files
- **1-batch_processing.py**
- **2-main.py**

### Functions
```python
def stream_users_in_batches(batch_size):
    """Fetches users from database in batches and yields each batch."""

def batch_processing(batch_size):
    """Processes each batch, filtering users older than 25."""
```

#### Key Notes

- Uses Python’s yield for efficient streaming.

- Fetches limited records at a time (fetchmany()).

- No more than 3 loops are used.

- Filters and prints users where age > 25.

#### Example Usage
```bash
$ ./2-main.py | head -n 5
```

---
## Task 3: Lazy Pagination — 2-lazy_paginate.py

Implements a lazy pagination system that yields one page (batch) at a time.

Prototype:
```python
def lazy_pagination(batch_size)
```

### 🧪 Example Output

Running:
```bash
python3 3-main.py | head -n 7
```

Produces:
```bash
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...
```
---

🧠 Key Concepts

- Generator functions: Functions that yield data instead of returning it.

- Lazy evaluation: Only compute or fetch data when it’s needed.

- Batch processing: Divide large datasets into smaller, manageable chunks.

- Pagination: Retrieve and display data in fixed-size “pages” for scalability.

---

## 👩🏽‍💻 Author

**Damilola Ojo**
ALX Backend Python Project – python-generators-0x00
GitHub: https://github.com/DAMILOLA8909