import pytest
from unittest.mock import MagicMock, patch
from .redis_manager import RedisManager
from cryptography.fernet import Fernet


@pytest.fixture
def mock_redis():
    with patch('redis_management.redis_management.redis_manager.redis.StrictRedis') as mock_redis_cls:
        mock_cache = MagicMock()
        mock_redis_cls.return_value = mock_cache
        yield mock_cache


@pytest.fixture
def redis_manager_instance(mock_redis):
    return RedisManager("test_identifier", "test_key")


def test_set_value(redis_manager_instance, mock_redis):
    assert redis_manager_instance.set_value("test_value")
    mock_redis.set.assert_called_once()


def test_set_json_value(redis_manager_instance, mock_redis):
    test_json = {"key": "value"}
    assert redis_manager_instance.set_json_value(test_json)
    mock_redis.set.assert_called_once()


def test_set_status_value(redis_manager_instance, mock_redis):
    assert redis_manager_instance.set_status_value(True)
    mock_redis.set.assert_called_once()


def test_create_and_set_otp_key(redis_manager_instance, mock_redis):
    otp_code = redis_manager_instance.create_and_set_otp_key()
    assert otp_code
    mock_redis.set.assert_called_once()


def test_get_value(redis_manager_instance, mock_redis):
    mock_redis.get.return_value = "test_value"
    assert redis_manager_instance.get_value() == "test_value"
    mock_redis.get.assert_called_once()


def test_get_json_value(redis_manager_instance, mock_redis):
    test_json = {"key": "value"}
    mock_redis.get.return_value = '{"key": "value"}'
    assert redis_manager_instance.get_json_value() == test_json
    mock_redis.get.assert_called_once()


def test_get_status_value(redis_manager_instance, mock_redis):
    mock_redis.get.return_value = "TRUE"
    assert redis_manager_instance.get_status_value() is True
    mock_redis.get.assert_called_once()


def test_set_expire(redis_manager_instance, mock_redis):
    assert redis_manager_instance.set_expire(300)
    mock_redis.expire.assert_called_once()


def test_get_expire(redis_manager_instance, mock_redis):
    mock_redis.ttl.return_value = 300
    assert redis_manager_instance.get_expire() == 300
    mock_redis.ttl.assert_called_once()


def test_exists(redis_manager_instance, mock_redis):
    mock_redis.exists.return_value = True
    assert redis_manager_instance.exists() is True
    mock_redis.exists.assert_called_once()


def test_delete(redis_manager_instance, mock_redis):
    mock_redis.delete.return_value = 1
    assert redis_manager_instance.delete() is True
    mock_redis.delete.assert_called_once()


@patch('redis_management.redis_management.redis_manager.RedisManager.decrypt_value')
def test_validate_successful(mock_decrypt_value, redis_manager_instance, mock_redis):
    mock_redis.get.return_value = "encrypted_value"
    mock_decrypt_value.return_value = "test_value"
    assert redis_manager_instance.validate("test_value")
    mock_redis.get.assert_called_once()
    mock_decrypt_value.assert_called_once_with("encrypted_value")


@patch('redis_management.redis_management.redis_manager.RedisManager.decrypt_value')
def test_validate_decryption_failure(mock_decrypt_value, redis_manager_instance, mock_redis):
    mock_redis.get.return_value = "encrypted_value"
    mock_decrypt_value.side_effect = ValueError("Failed to decrypt value")
    assert not redis_manager_instance.validate("test_value")
    mock_redis.get.assert_called_once()
    mock_decrypt_value.assert_called_once_with("encrypted_value")
