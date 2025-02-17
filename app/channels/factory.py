from channels.base import ChannelMeta, ChannelInterface


class ChannelFactory:
    @staticmethod
    def create_channel(channel_type: str, config: dict) -> ChannelInterface:
        channel_class = ChannelMeta.channels.get(channel_type)
        if not channel_class:
            raise ValueError(f"Canal '{channel_type}' não suportado.")
        return channel_class(config)
