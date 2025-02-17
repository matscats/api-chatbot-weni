from django.db import models

from core.models import BaseModel


class Channel(BaseModel):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, unique=True)
    config = models.JSONField()
