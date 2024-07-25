class RedisException(Exception):
    """Base exception for all Redis related errors."""
    pass


class KeyNotFoundException(RedisException):
    """Exception raised when a key is not found in Redis."""

    def __init__(self, key: str):
        self.key = key
        self.message = f"Key '{self.key}' not found in Redis."
        super().__init__(self.message)


class InvalidKeyException(RedisException):
    """Exception raised for invalid keys in Redis."""

    def __init__(self, key: str):
        self.key = key
        self.message = f"Key '{self.key}' is invalid."
        super().__init__(self.message)
