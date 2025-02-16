from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from core.models import Message
from core.serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Message.objects.select_related("contact", "user").all()
        contact_id = self.request.query_params.get("contact")
        user = self.request.user

        if contact_id:
            queryset = queryset.filter(contact_id=contact_id)

        if not user.is_anonymous:
            queryset = queryset.filter(user=user)

        return queryset
