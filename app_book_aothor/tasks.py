# app_book_author/tasks.py
from celery import shared_task
from sqlalchemy import text
from app_book_author.dbs import engine


@shared_task
def refresh_search_view():
    with engine.connect() as conn:
        # استفاده از CONCURRENTLY باعث می‌شود دیتابیس موقع آپدیت قفل نشود
        conn.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY author_book_counts;"))
        conn.commit()