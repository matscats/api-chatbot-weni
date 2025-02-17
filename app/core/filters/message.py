from django_filters import rest_framework as filters

from core.models import Message


class MessageFilter(filters.FilterSet):
    contact_id = filters.UUIDFilter(field_name="contact__id")
    agent_id = filters.UUIDFilter(field_name="agent__id")

    class Meta:
        model = Message
        fields = "__all__"
