from celery import Celery
from celery.schedules import crontab
from core.config import get_settings


class CeleryManager:
    def __init__(self):
        self.settings = get_settings()
        self._app = self._create_app()
        self._configure_app()
        self._setup_schedule()

    def _create_app(self) -> Celery:
        return Celery(
            "worker",
            broker=self.settings.CELERY_BROKER_URL,
            backend="rpc://",
            include=['core.celery.tasks']
        )

    def _configure_app(self):
        self._app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
            broker_connection_retry_on_startup=True,
            beat_schedule_filename="/tmp/celerybeat-schedule"
        )

    def _setup_schedule(self):
        self._app.conf.beat_schedule = {
            "fetch-users": {
                "task": "core.celery.tasks.fetch_users_task",
                "schedule": crontab(minute=0, hour="*"),
            },
            "fetch-posts": {
                "task": "core.celery.tasks.fetch_posts_task",
                "schedule": crontab(minute=5, hour="*"),
            },
            "fetch-comments": {
                "task": "core.celery.tasks.fetch_comments_task",
                "schedule": crontab(minute=10, hour="*"),
            },
        }

    @property
    def app(self) -> Celery:
        return self._app


manager = CeleryManager()
celery_app = manager.app
