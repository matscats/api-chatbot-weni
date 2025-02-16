from core.serializers import (
    BaseModelSerializer,
    CompactContactSerializer,
    CompactUserSerializer,
)
from core.models import Message
from core.services import SendMessageService

from rest_framework import serializers


class MessageSerializer(BaseModelSerializer):
    contact = CompactContactSerializer(read_only=True)
    user = CompactUserSerializer(read_only=True)
    contact_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["status", "direction"]

    def validate(self, attrs):
        direction = attrs.get("direction")
        user = attrs.get("user")

        if direction == "OUT" and user is None:
            raise serializers.ValidationError(
                "É necessário informar um usuário para mensagens de saída."
            )

        return attrs

    def create(self, validated_data):
        message_service = SendMessageService()
        message = message_service.send_message(
            contact_id=validated_data.get("contact_id"),
            content=validated_data.get("content"),
            user_id=self.context["request"].user.id,
        )
        return message
