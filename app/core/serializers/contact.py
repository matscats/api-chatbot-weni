from core.serializers import BaseModelSerializer
from core.models import Contact

from rest_framework import serializers


class ContactSerializer(BaseModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class CompactContactSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    external_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
