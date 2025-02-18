from typing import Protocol, Dict, Any

from core.models import Message

from uuid import UUID


class ReceiveMessageServiceInterface(Protocol):
    """
    Interface base para definir a estrutura do serviço de receber mensagens.
    """

    def receive_message(
        self, channel_type: str, payload: Dict[str, Any]
    ) -> Message: ...

    """
    Método para receber uma mensagem com base em um canal.
    """


class SendMessageServiceInterface(Protocol):
    """
    Interface base para definir a estrutura do serviço de enviar mensagens.
    """

    def send_message(
        self, contact_id: UUID, content: str, agent_id: UUID
    ) -> Message: ...

    """
    Método para enviar mensagem de um agente para um canal.
    """
