# Odeta

A simple NoSQL-like interface for SQLite.

## Installation

```bash
pip install odeta
```

## Usages
### Importing the Library

```
from odeta import odeta
```

Initializing the Database

```
db = odeta("my_database.db")
users = db.table("users")
```

## Fetching Data
### Fetch all records from the table:

```
print(users.fetch())
```

### Fetch records that match a specific query:

```
print(users.fetch({"name": "Bob Johnson"}))
```

# Inserting Data
## Insert a new record into the table:
```
new_user_id = users.put({"name": "Alice Smith", "age": 30})
print(new_user_id)
```

## Updating Data

### Update an existing record in the table:
```
users.update({"name": "Alice Johnson", "age": 31}, new_user_id)
```

## Deleting Data
### Delete a record from the table:
```
users.delete(new_user_id)
```
