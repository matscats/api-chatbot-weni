from core.interfaces import ChannelInterface

from typing import Dict, Any

from uuid import UUID


class MockChannel(ChannelInterface):
    def send_message(self, contact_id: UUID, message: str) -> bool:
        return True

    def process_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass
