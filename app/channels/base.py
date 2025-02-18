from abc import ABC, ABCMeta, abstractmethod

from typing import Dict, Type, TypedDict, Any


class ContactData(TypedDict):
    """
    Estrutura tipada de contato.
    """

    name: str
    username: str


class WebhookResponse(TypedDict):
    """
    Estrutura tipada do formato da resposta do Webhook.
    """

    contact_id: str
    message: str
    contact_data: ContactData


class ChannelMeta(ABCMeta):
    """
    Metaclasse utilizada para registrar automaticamente novos canais regitrados.
    """

    channels: Dict[str, Type["ChannelInterface"]] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "ChannelInterface":
            channel_type = attrs.get("channel_type")
            if channel_type:
                mcs.channels[channel_type] = cls
        return cls


class ChannelInterface(ABC, metaclass=ChannelMeta):
    """
    Interface base para estruturação de canais.
    """

    channel_type: str = None

    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializador de um canal. Deve ser passado um dicionário contendo as configurações.
        """
        super().__init__()

    @abstractmethod
    def send_message(self, contact_id: str, message: str) -> bool:
        """
        Método abstrato para enviar uma mensagem utilizando o canal.
        """
        pass

    @abstractmethod
    def process_webhook(self, payload: dict) -> WebhookResponse:
        """
        Método abstrato para processar a requisição enviada via Webhook.
        """
        pass
