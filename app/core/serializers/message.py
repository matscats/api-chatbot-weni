from core.serializers import (
    BaseModelSerializer,
    CompactContactSerializer,
    CompactUserSerializer,
)
from core.models import Message

from rest_framework import serializers


class MessageSerializer(BaseModelSerializer):
    contact = CompactContactSerializer(read_only=True)
    user = CompactUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"

    def validate(self, attrs):
        direction = attrs.get("direction")
        user = attrs.get("user")

        if direction == "OUT" and user is None:
            raise serializers.ValidationError(
                "É necessário informar um usuário para mensagens de saída."
            )

        return attrs
