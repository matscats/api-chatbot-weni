from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination

from core.models import Message
from core.serializers import MessageSerializer
from core.filters import MessageFilter

from django_filters import rest_framework as filters


class MessageViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MessageSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = Message.objects.all()
    filterset_class = MessageFilter
