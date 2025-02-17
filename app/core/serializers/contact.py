from core.serializers import BaseModelSerializer
from core.models import Contact

from rest_framework import serializers


class ContactSerializer(BaseModelSerializer):
    channel_type = serializers.CharField(source="channel.type", read_only=True)

    class Meta:
        model = Contact
        fields = ["id", "external_id", "name", "channel_type"]


class CompactContactSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    external_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
