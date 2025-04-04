from rest_framework import viewsets

from core.serializers import ContactSerializer
from core.models import Contact


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
