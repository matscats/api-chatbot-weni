from celery import shared_task

from django.utils import timezone

from datetime import timedelta

from core.models import Message

import logging

logger = logging.getLogger(__name__)


@shared_task(name="core.tasks.delete_old_messages")
def delete_old_messages():
    try:
        delete_date = timezone.now() - timedelta(days=30)

        deleted_count = Message.objects.filter(created_at__lt=delete_date).delete()[0]

        logger.info(f"{deleted_count} mensagens foram excluídas.")

    except Exception as e:
        logger.error(f"Erro ao limpar mensagens: {str(e)}")
