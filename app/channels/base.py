from abc import ABC, ABCMeta, abstractmethod

from typing import Dict, Type, TypedDict, Any


class ContactData(TypedDict):
    name: str
    username: str


class WebhookResponse(TypedDict):
    contact_id: str
    message: str
    contact_data: ContactData


class ChannelMeta(ABCMeta):
    channels: Dict[str, Type["ChannelInterface"]] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "ChannelInterface":
            channel_type = attrs.get("channel_type")
            if channel_type:
                mcs.channels[channel_type] = cls
        return cls


class ChannelInterface(ABC, metaclass=ChannelMeta):
    channel_type: str = None

    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        super().__init__()

    @abstractmethod
    def send_message(self, contact_id: str, message: str) -> bool:
        pass

    @abstractmethod
    def process_webhook(self, payload: dict) -> WebhookResponse:
        pass
