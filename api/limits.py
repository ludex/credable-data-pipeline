import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from redis import Redis

redis_url = os.getenv("RATE_LIMIT_REDIS_URL", "redis://localhost:6379/0")
limiter = Limiter(key_func=get_remote_address, storage_uri=redis_url)