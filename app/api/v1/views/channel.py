from rest_framework import viewsets

from core.models import Channel
from core.serializers import ChannelSerializer


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()
