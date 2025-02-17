from .base import BaseWebhookView


class WhatsappWebhookView(BaseWebhookView):
    channel_type = "whatsapp"
