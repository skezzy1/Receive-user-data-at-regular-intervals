from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "worker", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)

celery_app.conf.update(
    timezone="UTC",
    task_serializer="json",
    accept_content=["json"],
)

celery_app.conf.beat_schedule = {
    "fetch-users-every-hour": {
        "task": "app.tasks.fetch_users_task",
        "schedule": crontab(minute=0, hour="*"),
    },
    "fetch-posts-every-30-mins": {
        "task": "app.tasks.fetch_posts_task",
        "schedule": crontab(minute="*/30"),
    },
}
