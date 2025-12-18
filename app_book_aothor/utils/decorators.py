# app_book_author/utils/decorators.py
import logging
import functools
import json
import redis.asyncio as redis
from app_book_author import schemas
from fastapi.encoders import jsonable_encoder


logger = logging.getLogger("cache_errors")
redis_client = redis.from_url("redis://redis_db:6379", decode_responses=True)  # 👈 تغییر localhost به نام سرویس داکر

def cached_resilient(expire_seconds: int = 60):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            try:
                cached_value = await redis_client.get(cache_key)
                if cached_value:
                    return json.loads(cached_value)
            except Exception as e:
                logger.error(f"Redis is down! Falling back to DB: {e}")

            result = await func(*args, **kwargs)

            # تبدیل اشیاء SQLAlchemy به فرمت قابل سریال‌سازی (JSON Friendly)
            if result is not None:
                try:
                    serializable_result = jsonable_encoder(result)
                    # ذخیره داده تبدیل شده در ردیس
                    await redis_client.setex(cache_key, expire_seconds, json.dumps(serializable_result))

                except Exception as e:
                    logger.error(f"Failed to serialize or save to Redis: {e}")

            return result
        return wrapper
    return decorator