from core.serializers import BaseModelSerializer
from core.models import Agent

from rest_framework import serializers


class AgentSerializer(BaseModelSerializer):
    class Meta:
        model = Agent
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        agent = super().create(validated_data)

        if password:
            agent.set_password(password)
            agent.save()

        return agent


class CompactAgentSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
