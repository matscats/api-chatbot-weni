from channels.base import ChannelInterface, WebhookResponse

from typing import Dict, Any

from uuid import UUID


class MockChannel(ChannelInterface):
    channel_type = "mock"

    def __init__(self, config: Dict[str, Any]):
        pass

    def send_message(self, contact_id: UUID, message: str) -> bool:
        return True

    def process_webhook(self, payload: Dict[str, Any]) -> WebhookResponse:
        return {
            "contact_id": payload.get("contact_id"),
            "message": payload.get("message"),
            "contact_data": {
                "name": payload.get("name"),
                "username": payload.get("username"),
            },
        }
