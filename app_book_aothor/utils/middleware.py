# app_book_author/utils/middleware.py
import time
import json
import logging
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("api_monitor")

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        log_data = {
            "method": request.method,
            "path": request.url.path,
            "duration": f"{duration:.4f}s",
            "status": response.status_code
        }
        logger.info(json.dumps(log_data))
        return response