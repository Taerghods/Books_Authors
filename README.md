# Bookstore (fastAPI)

A scalable FastAPI service designed to handle high traffic (2M+ requests) using asynchronous patterns and intelligent caching.

## Key Features
- **Async Engine**: Powered by SQLAlchemy 2.0 & aiosqlite for non-blocking DB operations.
- **Resilient Caching**: Custom Python decorators for Redis integration with automatic fallback.
- **Observability**: Structured JSON logging and performance middleware.
- **Containerized**: Full Docker Compose setup (FastAPI, Redis, Dozzle).

## How to Run
```bash
docker-compose up --build
