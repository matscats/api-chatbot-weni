from .views import UserViewSet, MessageViewSet, ChannelViewSet, ContactViewSet

from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"channels", ChannelViewSet, basename="channel")
router.register(r"contacts", ContactViewSet, basename="contact")

urlpatterns = [
    path("", include(router.urls)),
]
