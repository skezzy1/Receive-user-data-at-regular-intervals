from celery import shared_task
from db.session_postgresql import get_postgresql_db_contextmanager
from core.importer.client import UserImporter, PostImporter, CommentImporter


@shared_task
def fetch_users_task():
    with get_postgresql_db_contextmanager() as session:
        importer = UserImporter(session)
        importer.run()


@shared_task
def fetch_posts_task():
    with get_postgresql_db_contextmanager() as session:
        importer = PostImporter(session)
        importer.run()


@shared_task
def fetch_comments_task():
    with get_postgresql_db_contextmanager() as session:
        importer = CommentImporter(session)
        importer.run()
