from django.urls import path

from .views import TelegramWebhookView, WhatsappWebhookView

urlpatterns = [
    path(
        "telegram/<str:token>/",
        TelegramWebhookView.as_view(),
        name="telegram-webhook",
    ),
    path(
        "whatsapp/",
        WhatsappWebhookView.as_view(),
        name="whatsapp-webhook",
    ),
]
