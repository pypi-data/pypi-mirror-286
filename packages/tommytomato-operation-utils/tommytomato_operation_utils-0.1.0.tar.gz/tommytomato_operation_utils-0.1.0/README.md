# tommytomato_operation_utils

Utility package for hash generation, database operations, and logging.

## Installation

```sh
pip install tommytomato_operation_utils
```
## Modules
### Hashing Client
The Hashing Client is used to generate hashes from lists of strings or specific columns of a DataFrame.

Usage:

```python
from tommytomato_utils.hashing_client.hashing_client import HashingClient
import pandas as pd

# Example usage with a list of strings
values = ["value1", "value2", "value3"]
hash_value = HashingClient.generate_hash(values)
print(f"Hash value: {hash_value}")

# Example usage with a DataFrame
data = {
    'col1': ['value1', 'value2'],
    'col2': ['value3', 'value4']
}
df = pd.DataFrame(data)
hash_columns = ['col1', 'col2']
hashed_df = HashingClient.generate_hash(df, hash_columns=hash_columns)
print(hashed_df)
```
#### Methods:

- `generate_hash(input_data: Union[List[str], DataFrame], hash_columns: List[str] = None, column_name: str = 'hash') -> Union[str, DataFrame]`: Generates a hash based on a list of string values or specific columns of a DataFrame.

### Database Client
The Database Client provides a set of methods for interacting with a PostgreSQL database, including creating tables, inserting data, and querying data.

Usage:

```python
from tommytomato_utils.database_client.database_client import DatabaseClient, DatabaseClientConfig
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Configuration for the database client
config = DatabaseClientConfig(
    host='localhost',
    port=5432,
    user='user',
    password='password',
    database='test_db'
)

# Creating the DatabaseClient instance
db_client = DatabaseClient(config)

# Test connection
db_client.test_connection()

# Create tables
db_client.create_tables(Base)

# Insert data
data = [
    {'column1': 'value1', 'column2': 'value2'},
    {'column1': 'value3', 'column2': 'value4'}
]
db_client.insert_data('table_name', data)

# Query data
query = "SELECT * FROM table_name"
df = db_client.query_data(query)
print(df)
```
#### Classes and Methods:

- `DatabaseClientConfig`: Configuration dataclass for the DatabaseClient.
- `DatabaseClient`: Main class for interacting with the database.
  - `test_connection()`: Test the database connection.
  - `reflect_schema()`: Reflect the database schema.
  - `refresh_schema()`: Refresh the database schema.
  - `session_scope()`: Context manager for database sessions.
  - `create_tables(base=Base)`: Create tables based on a provided base class.
  - `insert_data(table_name: str, data: List[Dict[str, Any]])`: Insert data into a specified table.
  - `query_data(query)`: Execute a query and return the results as a DataFrame.
  - `execute_sql(sql, params=None)`: Execute a raw SQL statement.

### Logger
The Logger provides logging capabilities to both STDOUT and optionally to a database. It uses a custom logging handler to log messages to a database table if desired.
Usage:

```python
import logging

from tommytomato_utils.database_client.database_client import DatabaseClient, DatabaseClientConfig
from tommytomato_utils.logger.configure_logging import configure_logging
from tommytomato_utils.logger.log_status import LogStatus

# Initialize the DatabaseClient
db_client = DatabaseClient(config=DatabaseClientConfig(
  host='localhost',
  port=5432,
  user='user',
  password='password',
  database='database'
))

# Example 1: Logger without database logging
logger1 = configure_logging(log_level=logging.INFO)
logger1.log(LogStatus.STARTED, "Task has started without DB logging.")
logger1.log(LogStatus.COMPLETED, "Task has completed without DB logging.")

# Example 2: Logger with database logging
logger2 = configure_logging(
  db_client=db_client,
  hub_id="hub123",
  run_id="run456",
  user_id="user789",
  tool_name="my_tool",
  log_to_db=True,
  log_level=logging.INFO
)
logger2.log(LogStatus.STARTED, "Task has started with DB logging.")
logger2.log(LogStatus.COMPLETED, "Task has completed with DB logging.")
logger2.log(LogStatus.FAILED, "Task has failed with DB logging.")
logger2.log(LogStatus.IN_PROGRESS, "Task is in progress with DB logging.")


```
#### Classes and Methods:

- `Logger`: Main class for logging messages.
  - `__init__(name: str = "tommytomato_operation_utils", level: int = logging.INFO)`: Initialize the Logger.
  - `get_logger()`: Returns the logger instance.
  - `log(status: LogStatus, message: str)`: Logs a message with the given status.
- `DatabaseLoggingHandler`: Custom logging handler for logging messages to a database.
  - `__init__(db_client: DatabaseClient, hub_id: str, run_id: str, user_id: str, tool_name: str)`: Initialize the DatabaseLoggingHandler.
  - `emit(record: logging.LogRecord)`: Emit a log record to the database.
- `configure_logging`: Function to configure logging based on user preferences.
  - `configure_logging(db_client: DatabaseClient = None, hub_id: str = None, run_id: str = None, user_id: str = None, tool_name: str = None, log_to_db: bool = False, log_level: int = logging.INFO)`: Configures the logging setup.
- `LogStatus`: Enum for logging statuses.
  - `LogStatus.STARTED`: Status for started tasks.
  - `LogStatus.COMPLETED`: Status for completed tasks.
  - `LogStatus.FAILED`: Status for failed tasks.
  - `LogStatus.IN_PROGRESS`: Status for tasks in progress.

### Secrets Manager
The Secrets Manager provides functionality to load secrets from environment variables and AWS Secrets Manager.

Usage:

```python
from tommytomato_utils.load_secrets.environment import Environment
from tommytomato_utils.load_secrets.secrets_loader import SecretsLoader

# Determine the environment
env_str = 'TESTING'
current_env = Environment.from_str(env_str)

# List of required secrets
required_secrets = [
    'GDRIVE_CLIENT_SECRET',
    'TOMMY_ADMIN_DJANGO_DB_USER',
    'TOMMY_ADMIN_DJANGO_DB_PASSWORD',
    'OPERATION_DB_USER',
    'OPERATION_DB_PASSWORD'
]

# Load the secrets based on the environment
secrets_loader = SecretsLoader(current_env)
secrets = secrets_loader.load_secrets(required_secrets)

# Use the loaded secrets in your application
GDRIVE_CLIENT_SECRET = secrets.get('GDRIVE_CLIENT_SECRET')
TOMMY_ADMIN_DJANGO_DB_USER = secrets.get('TOMMY_ADMIN_DJANGO_DB_USER')
TOMMY_ADMIN_DJANGO_DB_PASSWORD = secrets.get('TOMMY_ADMIN_DJANGO_DB_PASSWORD')
OPERATION_DB_USER = secrets.get('OPERATION_DB_USER')
OPERATION_DB_PASSWORD = secrets.get('OPERATION_DB_PASSWORD')
```

#### Classes and Methods:

- `Environment`: Enum class for defining valid environments.
  - `possible_environment_values()`: Returns a list of possible environment values.
  - `from_str(env_str: str)`: Converts a string to an Environment enum.
  - `ErrorWhenReadingInSecretsFromAWSSecretsManagerError`: Custom exception for AWS Secrets Manager errors.
- `SecretsLoader`: Class for loading secrets from environment variables and AWS Secrets Manager.
  - `__init__(environment: Environment)`: Initialize the SecretsLoader.
  - `load_env_files()`: Load the base .env file.
  - `validate_secrets(secrets: Dict[str, str], required_secrets: List[str])`: Validate that all required secrets are present.
  - `load_from_env(required_secrets: List[str])`: Load secrets from environment variables.
  - `load_from_aws(required_secrets: List[str])`: Load secrets from AWS Secrets Manager.
  - `load_secrets(required_secrets: List[str])`: Load secrets from environment variables and AWS Secrets Manager, validating that all required secrets are present.