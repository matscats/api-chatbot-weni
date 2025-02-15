from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class User(BaseModel, AbstractUser):
    is_available = models.BooleanField(default=True)
