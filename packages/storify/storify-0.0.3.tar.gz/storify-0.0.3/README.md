# Storify

Storify is a lightweight Python-based database system that utilizes msgpack for efficient data serialization. It provides a robust framework for data storage and retrieval, with an optional ORM model for interaction with data. Storify supports automatic backups and error handling, ensuring data integrity and reliability. Easily create, rename, and remove databases while benefiting from a logging mechanism that tracks all operations.

## Features

- Create and manage multiple msgpack-based databases with ease.
- Lightweight ORM-esque model for easy interaction with data.
- Automatic backups and data flushing to prevent data loss.
- Built-in error handling to manage database corruption and loading issues.
- Configurable save intervals for optimized performance.

## Installation

```bash
pip install storify
```

## Usage

Here's a simplified example of how to use the `storify` package:

```python
from storify import Storify

# Initialize Storify
storify = Storify(root="example_data")
db_name = "example_db"

# Check if the database exists
if storify.db_exists(db_name):
    print(f"Database '{db_name}' exists. It will be loaded.")

# Initialize a new database
 db = storify.get_db(name=db_name)

# Add some data to the database 
db["key1"] = "value1" 
db["key2"] = "value2"

# Get some data from the database
print(f"key1: {db['key1']}")
print(f"key2: {db['key2']}")

# Flush all databases (force save)
storify.flush()
```

For more complete examples, please check the `examples` folder.
