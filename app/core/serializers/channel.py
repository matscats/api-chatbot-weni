from core.models import Channel
from core.serializers import BaseModelSerializer


class ChannelSerializer(BaseModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"
