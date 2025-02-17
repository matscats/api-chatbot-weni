from django.core.cache import cache
from django.shortcuts import get_object_or_404

from typing import Optional

from uuid import UUID

from channels import ChannelFactory

from core.models import Message, Contact, Channel, Agent
from core.interfaces.message_service import (
    SendMessageServiceInterface,
    ReceiveMessageServiceInterface,
)
from core import exceptions


class ReceiveMessageService(ReceiveMessageServiceInterface):
    def _get_available_agent(self) -> Optional[Agent]:
        return Agent.objects.filter(is_available=True).order_by("last_activity").first()

    def receive_message(self, channel_type: str, payload: dict) -> Message:
        try:
            channel = Channel.objects.get(type=channel_type)

            channel_handler = ChannelFactory.create_channel(
                channel.type, channel.config
            )

            processed_data = channel_handler.process_webhook(payload)

            contact, _ = Contact.objects.get_or_create(
                external_id=processed_data["contact_id"],
                channel=channel,
                name=processed_data.get("contact_data", {}).get("name", ""),
            )

            agent = self._get_available_agent()

            return Message.objects.create(
                content=processed_data["message"],
                contact=contact,
                agent=agent,
                direction="IN",
            )

        except Exception as e:
            raise exceptions.FailedToReceiveMessage(detail=str(e))


class SendMessageService(SendMessageServiceInterface):
    def __init__(self):
        self.cache_ttl = 3600

    def _update_frequent_messages_cache(self, content: str):
        cache_key = f"message_frequency_{content[:50]}"
        frequency = cache.get(cache_key, 0)
        cache.set(cache_key, frequency + 1, self.cache_ttl)

        if frequency > 10:
            cache.set(f"frequent_response_{content[:50]}", content, self.cache_ttl * 24)

    def send_message(self, contact_id: int, content: str, agent_id: UUID) -> Message:
        try:
            contact = get_object_or_404(Contact, id=contact_id)
            agent = get_object_or_404(Agent, id=agent_id)

            cache_key = f"frequent_response_{content[:50]}"
            if cached_response := cache.get(cache_key):
                content = cached_response

            channel_handler = ChannelFactory.create_channel(
                contact.channel.type, contact.channel.config
            )

            message = Message.objects.create(
                content=content,
                contact=contact,
                agent=agent,
                direction="OUT",
                status="PENDING",
            )

            success = channel_handler.send_message(contact.external_id, content)

            if not success:
                message.status = "FAILED"
                message.save()

            return message

        except Exception as e:
            raise exceptions.FailedToSendMessage(detail=str(e))
