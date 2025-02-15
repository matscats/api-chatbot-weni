from core.models import Channel
from core.serializers import BaseModelSerializer

from rest_framework import serializers


class ChannelSerializer(BaseModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"

    def validate_config(self, value):
        if "token" not in value:
            raise serializers.ValidationError(
                "Token não informado para criação de canal."
            )

        return value
