from typing import Protocol, Dict, Any

from core.models import Message

from uuid import UUID


class ReceiveMessageServiceInterface(Protocol):
    def receive_message(
        self, channel_type: str, payload: Dict[str, Any]
    ) -> Message: ...


class SendMessageServiceInterface(Protocol):
    def send_message(
        self, contact_id: UUID, content: str, agent_id: UUID
    ) -> Message: ...
