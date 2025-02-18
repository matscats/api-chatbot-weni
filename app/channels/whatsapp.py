from channels.base import ChannelInterface, WebhookResponse
from twilio.rest import Client
from typing import Dict, Any


class WhatsAppChannel(ChannelInterface):
    """
    Canal para receber e enviar mensagens via Telegram.
    """

    channel_type = "whatsapp"

    def __init__(self, config: Dict[str, Any]):
        self.client = Client(config["account_sid"], config["auth_token"])
        self.from_number = config["from_number"]

    def send_message(self, contact_id: str, message: str) -> bool:
        """
        Envia uma mensagem a partir do número do Whatsapp configurado.
        """
        try:
            self.client.messages.create(
                body=message,
                from_=f"whatsapp:{self.from_number}",
                to=f"whatsapp:{contact_id}",
            )
            return True
        except Exception as e:
            print(str(e))
            return False

    def process_webhook(self, payload: Dict[str, Any]) -> WebhookResponse:
        """
        Recebe uma mensagem do Whatsapp por meio de webhook.
        """
        try:
            return {
                "contact_id": payload.get("From").split(":")[1],
                "message": payload.get("Body", ""),
                "contact_data": {
                    "name": payload.get("ProfileName"),
                    "username": payload.get("From", ""),
                },
            }
        except Exception:
            raise ValueError("Formato de Webhook inválido.")
