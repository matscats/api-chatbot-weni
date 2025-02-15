from django.db import models

from core.models import BaseModel


class Contact(BaseModel):
    external_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    channel = models.ForeignKey(
        "Channel", on_delete=models.CASCADE, related_name="contacts"
    )

    def __str__(self):
        return f"{self.external_id} - {self.name}"

    class Meta:
        unique_together = ("external_id", "channel")
