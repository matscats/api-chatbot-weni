from rest_framework import viewsets

from core.serializers import AgentSerializer
from core.permissions import IsAgentSelf
from core.models import Agent


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAgentSelf]

    def get_permissions(self):
        if self.action == "create":
            return []

        return super().get_permissions()
