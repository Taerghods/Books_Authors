# celery_app.py
from celery import Celery
from celery.schedules import crontab


app = Celery('tasks_manager',
             broker='redis://redis_db:6379/0',
             backend='redis://redis_db:6379/0'
)

app.conf.beat_schedule = {
    'refresh-materialized-view-every-5-minutes': {
        'task': 'app_book_author.tasks.refresh_search_view',
        'schedule': 300.0,
    },
}