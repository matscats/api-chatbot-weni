from core.serializers import BaseModelSerializer

from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CompactUserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
