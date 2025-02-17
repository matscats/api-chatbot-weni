import telegram
import asyncio

from channels.base import ChannelInterface, WebhookResponse

from typing import Dict, Any

from uuid import UUID


class TelegramChannel(ChannelInterface):
    channel_type = "telegram"

    def __init__(self, config: Dict[str, Any]):
        self.bot = telegram.Bot(token=config["token"])

    def send_message(self, contact_id: UUID, message: str) -> bool:
        try:
            asyncio.run(self.bot.send_message(chat_id=contact_id, text=message))
            return True
        except:
            return False

    def process_webhook(self, payload: Dict[str, Any]) -> WebhookResponse:
        try:
            message = payload.get("message", {})
            chat = message.get("chat", {})

            return {
                "contact_id": str(chat.get("id")),
                "message": message.get("text", ""),
                "contact_data": {
                    "name": chat.get("first_name", "")
                    + " "
                    + chat.get("last_name", ""),
                    "username": chat.get("username"),
                },
            }
        except:
            raise ValueError("Formato de Webhook inválido.")
