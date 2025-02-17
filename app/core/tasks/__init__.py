import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from .message import delete_old_messages

__all__ = ["delete_old_messages"]
