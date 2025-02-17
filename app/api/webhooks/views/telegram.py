from .base import BaseWebhookView


class TelegramWebhookView(BaseWebhookView):
    channel_type = "telegram"

    def post(self, request, token):
        return super().post(request)
