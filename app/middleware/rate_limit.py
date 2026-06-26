import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings
from app.services.caching import cache_service

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow swagger/redoc documentation routes to bypass rate limit
        path = request.url.path
        if path.startswith("/docs") or path.startswith("/redoc") or path.startswith("/openapi.json"):
            return await call_next(request)

        # Get client host/IP to identify rate limit buckets
        client_ip = request.client.host if request.client else "unknown"
        current_time = int(time.time())
        window_size = 60 # 1 minute window
        max_requests = settings.RATE_LIMIT_PER_MINUTE

        # Key representing this client inside the rate limit window
        key = f"ratelimit:{client_ip}:{current_time // window_size}"

        try:
            # We can retrieve current count from cache
            current_count = cache_service.get(key)
            if current_count is None:
                current_count = 0

            if current_count >= max_requests:
                logger.warning(f"Rate limit exceeded for client {client_ip}. Limit: {max_requests}/min")
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests. Please try again later."}
                )

            # Increment count
            cache_service.set(key, current_count + 1, expire_seconds=window_size)
        except Exception as e:
            # If caching service fails entirely, let request pass rather than crashing
            logger.error(f"Rate limiter error: {e}")

        response = await call_next(request)
        return response
