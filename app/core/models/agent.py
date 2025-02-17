from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class Agent(BaseModel, AbstractUser):
    is_available = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)
