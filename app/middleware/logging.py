import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.api.requests")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        # Process request
        response = await call_next(request)

        # Log request stats
        process_time_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"Client IP: {client_ip} | Method: {method} | Path: {path} | "
            f"Status: {response.status_code} | Process Time: {process_time_ms}ms"
        )
        return response
