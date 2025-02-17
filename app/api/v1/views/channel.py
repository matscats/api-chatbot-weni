from rest_framework import viewsets, mixins

from core.models import Channel
from core.serializers import ChannelSerializer


class ChannelViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()
