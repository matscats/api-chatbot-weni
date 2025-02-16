from typing import Dict, Type
from core.interfaces.channel import ChannelInterface
from channels.telegram import TelegramChannel
from channels.mock import MockChannel


class ChannelFactory:
    _handlers: Dict[str, Type[ChannelInterface]] = {
        "telegram": TelegramChannel,
        "mock": MockChannel,
    }

    @classmethod
    def create_channel(cls, channel_type: str, config: dict) -> ChannelInterface:
        handler_class = cls._handlers.get(channel_type)

        if not handler_class:
            raise ValueError(f"Canal '{channel_type}' não é válido.")

        return handler_class(config)

    @classmethod
    def register_channel(cls, channel_type: str, handler_class: Type[ChannelInterface]):
        cls._handlers[channel_type] = handler_class
