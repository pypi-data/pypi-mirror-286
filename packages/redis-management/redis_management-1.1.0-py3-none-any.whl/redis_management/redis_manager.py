from .exceptions import RedisException, KeyNotFoundException, InvalidKeyException
from .settings import *

from typing import Optional, Any, Dict
from cryptography.fernet import Fernet

import redis
import json
import binascii


class RedisManager:
    """
    Manage public keys on Redis.
    """

    def __init__(self, identifier: str, key: str):
        """
        Initialize RedisManager with identifier and key.
        The key is generated using identifier and key for uniqueness.

        :param identifier: The unique identifier (e.g., mobile number, email).
        :param key: The specific key string.
        """
        self.cache = redis.StrictRedis(
            decode_responses=True,
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
        )
        self.key = f"{identifier}:{key}"
        self.cipher_suite = Fernet(FERNET_KEY)

    def set_value(self, value: str) -> bool:
        """
        Set a value in Redis for the key.

        :param value: The value to set.
        :return: True if successful, raises RedisException otherwise.
        """
        try:
            self.cache.set(self.key, value)
            return True
        except redis.RedisError as e:
            raise RedisException(f"Failed to set value: {e}")

    def set_json_value(self, value: Dict[str, Any]) -> bool:
        """
        Set a JSON value in Redis for the key.

        :param value: The JSON value (as dict) to set.
        :return: True if successful, raises RedisException otherwise.
        """
        try:
            return self.set_value(json.dumps(value))
        except (TypeError, json.JSONDecodeError) as e:
            raise RedisException(f"Invalid JSON value: {e}")

    def set_status_value(self, value: bool) -> bool:
        """
        Set a boolean value in Redis for the key.

        :param value: The boolean value to set.
        :return: True if successful.
        """
        return self.set_value(str(value).upper())

    def create_and_set_otp_key(self, length: int = 5, otp_code: Optional[str] = None, expire_time: int = 300) -> str:
        """
        Create and set a one-time password (OTP) key.

        :param length: The length of the OTP code (default is 5).
        :param otp_code: The OTP code to set (optional).
        :param expire_time: The time for expire key (default is 300 = 5min).
        :return: The OTP code that was set.
        """
        if otp_code is None:
            otp_code = self.create_otp_code(length)
        encrypted_otp = self.encrypt_value(otp_code)
        self.set_value(encrypted_otp)
        self.set_expire(expire_time)
        return otp_code

    def get_value(self) -> Optional[str]:
        """
        Get the value of the key from Redis.

        :return: The value of the key, or None if the key does not exist.
        """
        if self.cache.exists(self.key):
            return self.cache.get(self.key)
        return None

    def get_json_value(self) -> Optional[Dict[str, Any]]:
        """
        Get the JSON value of the key from Redis.

        :return: The JSON value (as dict), or None if the key does not exist or value is not valid JSON.
        """
        try:
            value = self.get_value()
            if value:
                return json.loads(value)
            return None
        except (TypeError, json.JSONDecodeError) as e:
            raise RedisException(f"Failed to decode JSON: {e}")

    def get_status_value(self) -> Optional[bool]:
        """
        Get the boolean status value of the key from Redis.

        :return: True if the value is 'TRUE', False if 'FALSE', None if the key does not exist.
        """
        value = self.get_value()
        if value is not None:
            return value.upper() == "TRUE"
        return None

    def set_expire(self, time: int = 300) -> bool:
        """
        Set the expiration time for the key in Redis.

        :param time: The expiration time in seconds (default is 300).
        :return: True if successful, raises RedisException otherwise.
        """
        try:
            self.cache.expire(self.key, time)
            return True
        except redis.RedisError as e:
            raise RedisException(f"Failed to set expiration: {e}")

    def get_expire(self) -> Optional[int]:
        """
        Get the expiration time of the key from Redis.

        :return: The number of seconds until the key expires, or None if the key does not exist.
        """
        try:
            return self.cache.ttl(self.key)
        except redis.RedisError as e:
            raise RedisException(f"Failed to get expiration: {e}")

    def validate(self, user_value: str) -> bool:
        """
        Validate the user-provided value against the value stored in Redis.

        :param user_value: The value provided by the user.
        :return: True if the user value matches the stored value, False otherwise.
        """
        if self.cache.exists(self.key):
            redis_value = self.cache.get(self.key)
            try:
                decrypted_redis_value = self.decrypt_value(redis_value)
                return str(decrypted_redis_value) == str(user_value)
            except Exception as e:
                return False
        return False

    def exists(self) -> bool:
        """
        Check if the key exists in Redis.

        :return: True if the key exists, False otherwise.
        """
        return self.cache.exists(self.key) == 1

    def delete(self) -> bool:
        """
        Delete the key from Redis.

        :return: True if the key was deleted, raises RedisException otherwise.
        """
        try:
            return self.cache.delete(self.key) == 1
        except redis.RedisError as e:
            raise RedisException(f"Failed to delete key: {e}")

    @staticmethod
    def create_otp_code(length: int) -> str:
        """
        Generate a random OTP code of specified length.

        :param length: The length of the OTP code.
        :return: The generated OTP code.
        """
        import random
        import string
        return ''.join(random.choices(string.digits, k=length))

    def encrypt_value(self, value: str) -> str:
        """
        Encrypt a value using Fernet symmetric encryption.

        :param value: The value to encrypt.
        :return: The encrypted value as a string.
        """
        return self.cipher_suite.encrypt(value.encode()).decode()

    def decrypt_value(self, encrypted_value: str) -> str:
        """
        Decrypt the encrypted value using Fernet.

        :param encrypted_value: The encrypted value to decrypt.
        :return: The decrypted value.
        """
        try:
            return self.cipher_suite.decrypt(encrypted_value.encode()).decode()
        except (TypeError, binascii.Error, ValueError) as e:
            raise ValueError("Failed to decrypt value") from e

