__all__ = [
    "Message",
]
import time
from django.conf import settings

from .models import Message

class MessageMixin:
    def message(self,message):
        command = type(self).__module__.split('.')[-1]
        Message(command=command,message=message,created_at=int(time.time())).save()
        if settings.DEBUG:
            print(message)
