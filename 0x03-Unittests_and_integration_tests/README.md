# Unit Testing and Integration Testing

This project focuses on implementing comprehensive unit tests and integration tests for Python applications. It demonstrates best practices for testing Python code using the `unittest` framework and the `parameterized` library.

## Project Structure

```pgsql
0x03-Unittests_and_integration_tests/
├── utils.py
├── test_utils.py
└── README.md
```


## Files Description

### `utils.py`
A utility module containing generic functions for working with nested data structures and HTTP requests. Key functions include:

- **`access_nested_map(nested_map, path)`**: Accesses values in nested dictionaries using a tuple path
- **`get_json(url)`**: Fetches JSON data from remote URLs
- **`memoize(fn)`**: Decorator for memoizing method results

### `test_utils.py`
Comprehensive unit tests for the `access_nested_map` function using the `unittest` framework with parameterized testing.

## Features

- **Parameterized Testing**: Uses `@parameterized.expand` to test multiple scenarios with minimal code duplication
- **Type Annotations**: All functions include proper type hints for better code clarity and IDE support
- **Pycodestyle Compliance**: Code follows Python style guidelines (PEP 8)
- **Comprehensive Documentation**: All modules, classes, and methods include detailed docstrings

## Testing Scenarios

The test suite covers the following scenarios for `access_nested_map`:

1. Accessing top-level keys in a flat dictionary
2. Accessing nested dictionaries
3. Accessing deeply nested values through multiple key paths

## Installation & Setup

1. **Clone the repository** (if applicable)
2. **Install dependencies**:
   ```bash
   pip install requests parameterized
   ```

3. **Make files executable**:
    ```bash
    chmod +x utils.py test_utils.py
    ```

### Running Tests

**Unit Tests**

```bash
    python -m unittest test_utils.py
```

**Code Style Check**

```bash
    pycodestyle utils.py test_utils.py
```

**Documentation Verification**

```bash
# Module documentation
python3 -c 'print(__import__("test_utils").__doc__)'

# Class documentation  
python3 -c 'print(__import__("test_utils").TestAccessNestedMap.__doc__)'

# Method documentation
python3 -c 'print(__import__("test_utils").TestAccessNestedMap.test_access_nested_map.__doc__)'
```

### Test Output

**Successful test execution displays**:
```bash
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

The three dots indicate all parameterized test cases passed.

---

### Requirements

- Python 3.7+

- Ubuntu 18.04 LTS (compatible)

- requests library

- parameterized library

- pycodestyle (version 2.5+)

---

### Code Quality Standards

- All files end with a newline

- Proper shebang line (#!/usr/bin/env python3)

- Executable file permissions

- Comprehensive documentation for all modules, classes, and functions

- Type annotations for all functions and coroutines

- Pycodestyle compliance

---

#### Author
ALX Backend Python Program

#### License
This project is part of the ALX Backend Python curriculum.