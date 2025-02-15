from typing import Protocol, Dict, Any

from uuid import UUID


class ChannelInterface(Protocol):
    async def send_message(self, contact_id: UUID, message: str) -> bool: ...
    async def process_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]: ...
