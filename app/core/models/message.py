from django.db import models

from core.models import BaseModel


class Message(BaseModel):
    DIRECTION_CHOICES = (
        ("IN", "IN"),
        ("OUT", "OUT"),
    )

    content = models.TextField()
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)
    user = models.ForeignKey("User", null=True, on_delete=models.SET_NULL)
    direction = models.CharField(choices=DIRECTION_CHOICES)
