import telegram

from core.interfaces import ChannelInterface

from typing import Dict, Any

from uuid import UUID


class TelegramChannel(ChannelInterface):
    def __init__(self, config: Dict[str, Any]):
        self.bot = telegram.Bot(token=config["token"])

    async def send_message(self, contact_id: UUID, message: str) -> bool:
        try:
            await self.bot.send_message(chat_id=contact_id, text=message)
            return True
        except:
            return False

    async def process_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            chat = payload.get("chat", {})
            message = payload.get("message", {})

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
        except Exception as e:
            raise ValueError("Formato de Webhook inválido.")
