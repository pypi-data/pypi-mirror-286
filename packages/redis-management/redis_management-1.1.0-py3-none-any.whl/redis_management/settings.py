from decouple import config

# Get settings from Django settings, or use defaults
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)
REDIS_DB = config("REDIS_DB", default=0, cast=int)
# Fernet encryption key
# Use the key generated and stored in .env
FERNET_KEY = config('FERNET_KEY')
