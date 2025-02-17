from channels.base import ChannelInterface, WebhookResponse

from typing import Dict, Any

from uuid import UUID


class MockChannel(ChannelInterface):
    def send_message(self, contact_id: UUID, message: str) -> bool:
        return True

    def process_webhook(self, payload: Dict[str, Any]) -> WebhookResponse:
        return {
            "contact_id": 1,
            "message": "Mensagem Mock",
            "contact_data": {
                "name": "Mock da Silva",
                "username": "mockado",
            },
        }
