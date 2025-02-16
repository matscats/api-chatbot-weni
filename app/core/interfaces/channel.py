from typing import Protocol, Dict, Any

from uuid import UUID


class ChannelInterface(Protocol):
    def send_message(self, contact_id: UUID, message: str) -> bool: ...
    def process_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]: ...
