from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def fetch_users_task():
    logger.info("Executing fetch_users_task...")
    return "Users fetched successfully"
