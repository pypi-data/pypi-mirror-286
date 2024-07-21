__all__ = [
    "Message",
]

import sys
import time
from django.db import models

def get_timestamp():
    return int(time.time())

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    command = models.CharField(max_length=255)
    message = models.TextField(verbose_name="Message")
    created_at = models.IntegerField(default=get_timestamp)

    class Meta:
        db_table = "django_command_message"
        ordering = ("-created_at",'id')


    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = int(time.time())
        super().save(*args, **kwargs)
