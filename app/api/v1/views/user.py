from rest_framework import viewsets, permissions

from django.contrib.auth import get_user_model

from core.serializers import UserSerializer
from core.permissions import IsUserSelf

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserSelf]

    def get_permissions(self):
        if self.action == "create":
            return []

        return super().get_permissions()
