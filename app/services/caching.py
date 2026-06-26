import json
import logging
from typing import Any, Optional
import redis
from app.core.config import settings

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis_client = None
        self._memory_cache = {} # Fallback in-memory dict

        try:
            # Parse Redis URL
            self.redis_client = redis.from_url(
                settings.REDIS_URL, 
                socket_connect_timeout=2, 
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Connected to Redis successfully for caching.")
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}. Caching will fallback to local in-memory store.")
            self.redis_client = None

    def get(self, key: str) -> Optional[Any]:
        if self.redis_client:
            try:
                val = self.redis_client.get(key)
                return json.loads(val) if val else None
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                return self._memory_cache.get(key)
        return self._memory_cache.get(key)

    def set(self, key: str, value: Any, expire_seconds: int = 3600) -> bool:
        if self.redis_client:
            try:
                serialized = json.dumps(value)
                return self.redis_client.set(key, serialized, ex=expire_seconds)
            except Exception as e:
                logger.error(f"Redis set error: {e}")
                self._memory_cache[key] = value
                return True
        self._memory_cache[key] = value
        # Implement a basic expiry simulation if desired (simplified)
        return True

    def delete(self, key: str) -> bool:
        if self.redis_client:
            try:
                return bool(self.redis_client.delete(key))
            except Exception as e:
                logger.error(f"Redis delete error: {e}")
                if key in self._memory_cache:
                    del self._memory_cache[key]
                return True
        if key in self._memory_cache:
            del self._memory_cache[key]
        return True

cache_service = CacheService()
