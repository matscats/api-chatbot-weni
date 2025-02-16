from django.urls import path

from .views import TelegramWebhookView

urlpatterns = [
    path(
        "telegram/<str:token>/", TelegramWebhookView.as_view(), name="telegram-webhook"
    ),
]
