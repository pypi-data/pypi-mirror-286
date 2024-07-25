# Redis Management

A utility package for managing Redis keys in Python. This package provides an easy-to-use interface for interacting with
Redis, including setting, getting, and managing expiration of keys.

## Features

- Manage public keys in Redis
- Set and get values (including JSON and boolean)
- Create and validate OTP codes
- Set and get expiration times for keys
- Check if a key exists and delete it

## Requirements

- Python 3.6+
- Redis server
- [redis](https://pypi.org/project/redis/)
- Optional: [python-decouple](https://pypi.org/project/python-decouple/) for configuration

## Installation

You can install this package directly from GitHub:

```bash
pip install git+https://github.com/AAbbasRR/redis-manager.git
```

Alternatively, clone the repository and install manually:

```bash
git clone https://github.com/AAbbasRR/redis-manager.git
cd my_redis_utils
pip install .
```

## Configuration

By default, the package uses `localhost` and the default Redis port (6379). You can configure the Redis connection
using `python-decouple` or by providing the parameters directly.

### Configuration Keys

- `REDIS_HOST`: The hostname or IP address of the Redis server. Default is `localhost`.
- `REDIS_PORT`: The port number on which the Redis server is listening. Default is `6379`.
- `REDIS_DB`: The Redis database number to use. Default is `0`.
- `FERNET_KEY`: Before using the application, it's essential to set up the `FERNET_KEY`. This key is used for encrypting
  and decrypting sensitive data.

### Example Configuration using `python-decouple`

1. Install `python-decouple`:
   ```bash
   pip install python-decouple
   ```

2. Create a `.env` file in your project root and add your Redis configuration:
   ```env
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   FERNET_KEY=YourGeneratedKeyHere
   ```

3. Use the configuration in your code:
   ```python 
   from redis_management.redis_manager import RedisManager
   redis_manager = RedisManager(identifier="user123", key="session_token")
   ```

### Generating the FERNET_KEY

To generate a `FERNET_KEY`, you can use the following command in your terminal:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Usage

### Example Code
```python
from redis_management.redis_manager import RedisManager
```

# Initialize RedisManager with identifier and key
```python
redis_manager = RedisManager(identifier="user123", key="session_token")
```

# Set a value
```python
redis_manager.set_value("some_value")
```

# Get a value
```python
value = redis_manager.get_value()
print(value)
```

# Set a JSON value
```python
redis_manager.set_json_value({"key": "value"})
```

# Get a JSON value
```python
json_value = redis_manager.get_json_value()
print(json_value)
```

# Create and set OTP key
```python
otp_code = redis_manager.create_and_set_otp_key()
print(otp_code)
```

# Validate OTP code
```python
is_valid = redis_manager.validate(otp_code)
print(is_valid)
```

# Check if key exists
```python
exists = redis_manager.exists()
print(exists)
```

# Delete the key
```python
redis_manager.delete()
```


## Exception Handling

The package provides custom exceptions for better error handling:

- `RedisException`: Base exception for Redis errors.
- `KeyNotFoundException`: Raised when a key is not found in Redis.
- `InvalidKeyException`: Raised when an invalid key is provided.

Example:

```python
from redis_management.redis_manager import RedisManager
from redis_management.exceptions import KeyNotFoundException

try:
    redis_manager = RedisManager(identifier="user123", key="non_existent_key")
    value = redis_manager.get_value()
except KeyNotFoundException:
    print("Key not found in Redis.")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Author

Abbas Rahimzadeh - [arahimzadeh79@gmail.com](mailto:arahimzadeh79@gmail.com)

## Acknowledgments

Special thanks to the open-source community for their valuable contributions and resources.
