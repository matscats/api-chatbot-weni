from django.core.cache import cache

from typing import Optional

from core.models import Message, Contact, Channel, User

from uuid import UUID

from channels import ChannelFactory
from core.interfaces.message_service import (
    SendMessageServiceInterface,
    ReceiveMessageServiceInterface,
)


class ReceiveMessageService(ReceiveMessageServiceInterface):
    def _get_active_channel(self, channel_type: str) -> Channel:
        return Channel.objects.get(type=channel_type, is_active=True)

    def _get_or_create_contact(
        self, external_id: str, channel: Channel, contact_data: dict
    ) -> Contact:
        contact, _ = Contact.objects.get_or_create(
            external_id=external_id,
            channel=channel,
            defaults={"name": contact_data.get("name", "Unknown")},
        )
        return contact

    def _get_available_user(self) -> Optional[User]:
        return User.objects.filter(is_available=True).order_by("last_activity").first()

    def _create_message(
        self, content: str, contact: Contact, user: Optional[User], direction: str
    ) -> Message:
        return Message.objects.create(
            content=content,
            contact=contact,
            user=user,
            direction=direction,
            status="RECEIVED",
        )

    def receive_message(self, channel_type: str, payload: dict) -> Message:
        try:
            channel = self._get_active_channel(channel_type)
            channel_handler = ChannelFactory.create_channel(
                channel.type, channel.config
            )

            processed_data = channel_handler.process_webhook(payload)

            contact = self._get_or_create_contact(
                external_id=processed_data["contact_id"],
                channel=channel,
                contact_data=processed_data.get("contact_data", {}),
            )

            user = self._get_available_user()

            return self._create_message(
                content=processed_data["message"],
                contact=contact,
                user=user,
                direction="IN",
            )

        except Exception as e:
            pass


class SendMessageService(SendMessageServiceInterface):
    def __init__(self):
        self.cache_ttl = 3600

    def _create_message(
        self, content: str, contact: Contact, user: User, direction: str
    ) -> Message:
        return Message.objects.create(
            content=content,
            contact=contact,
            user=user,
            direction=direction,
            status="PENDING",
        )

    def _update_frequent_messages_cache(self, content: str):
        cache_key = f"message_frequency_{content[:50]}"
        frequency = cache.get(cache_key, 0)
        cache.set(cache_key, frequency + 1, self.cache_ttl)

        if frequency > 10:
            cache.set(f"frequent_response_{content[:50]}", content, self.cache_ttl * 24)

    def send_message(self, contact_id: int, content: str, user_id: UUID) -> Message:
        try:
            contact = Contact.objects.get(id=contact_id)
            user = User.objects.get(id=user_id)

            cache_key = f"frequent_response_{content[:50]}"
            if cached_response := cache.get(cache_key):
                content = cached_response

            channel_handler = ChannelFactory.create_channel(
                contact.channel.type, contact.channel.config
            )

            message = self._create_message(
                content=content, contact=contact, user=user, direction="OUT"
            )

            success = channel_handler.send_message(contact.external_id, content)

            if not success:
                message.status = "FAILED"
                message.asave()

            return message

        except Exception as e:
            pass
