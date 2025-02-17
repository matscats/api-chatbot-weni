from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Channel


class Command(BaseCommand):
    help = "Popula o banco de dados com canais padrões"

    def handle(self, *args, **options):
        # Canal do Telegram
        try:
            channel, created = Channel.objects.get_or_create(
                name="Telegram Bot",
                type="telegram",
                defaults={
                    "config": {"token": settings.TELEGRAM_BOT_TOKEN},
                    "is_active": True,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS("Canal Telegram criado com sucesso")
                )
            else:
                self.stdout.write(self.style.WARNING("Canal Telegram já existe"))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Erro ao criar canal Telegram: {str(e)}")
            )

        # Canal do WhatsApp
        try:
            channel, created = Channel.objects.get_or_create(
                name="WhatsApp Bot",
                type="whatsapp",
                defaults={
                    "config": {
                        "account_sid": settings.WHATSAPP_ACCOUNT_SID,
                        "auth_token": settings.WHATSAPP_AUTH_TOKEN,
                        "from_number": settings.WHATSAPP_FROM_NUMBER,
                    },
                    "is_active": True,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS("Canal WhatsApp criado com sucesso")
                )
            else:
                self.stdout.write(self.style.WARNING("Canal WhatsApp já existe"))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Erro ao criar canal WhatsApp: {str(e)}")
            )
