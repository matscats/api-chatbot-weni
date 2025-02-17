from django.core.management.base import BaseCommand
from django.conf import settings

import requests


class Command(BaseCommand):
    help = "Configura o webhook do Telegram"

    def handle(self, *args, **options):
        token = settings.TELEGRAM_BOT_TOKEN
        webhook_url = f"{settings.BASE_URL}/webhooks/telegram/{token}/"

        api_url = f"https://api.telegram.org/bot{token}/setWebhook"
        data = {"url": webhook_url, "allowed_updates": ["message"]}

        try:
            response = requests.post(api_url, json=data)
            self.stdout.write(self.style.SUCCESS(f"Webhook configurado"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao configurar webhook: {e}"))
