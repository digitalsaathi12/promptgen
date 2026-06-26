import re
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

# Basic patterns representing XSS and SQL injection attempts
XSS_PATTERN = re.compile(r"<script.*?>|javascript:|onload|onerror", re.IGNORECASE)
SQL_INJECTION_PATTERN = re.compile(r"UNION\s+SELECT|UNION\s+ALL\s+SELECT|OR\s+\d+=\d+", re.IGNORECASE)

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Sanitize query parameters and paths for common XSS/SQL Injection patterns
        query_string = request.url.query
        path = request.url.path

        if XSS_PATTERN.search(query_string) or XSS_PATTERN.search(path):
            logger.warning(f"Potential XSS attack detected from client {request.client.host if request.client else 'unknown'}")
            return JSONResponse(status_code=400, content={"detail": "Bad Request. Suspicious activity detected."})

        if SQL_INJECTION_PATTERN.search(query_string) or SQL_INJECTION_PATTERN.search(path):
            logger.warning(f"Potential SQL Injection attack detected from client {request.client.host if request.client else 'unknown'}")
            return JSONResponse(status_code=400, content={"detail": "Bad Request. Suspicious activity detected."})

        # Process the request
        response = await call_next(request)

        # 2. Inject Security Headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response
