from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from .models import Message as Model


class ModelAdmin(admin.ModelAdmin):
    fields = [
        "id",
        "command",
        "message",
        "created_at",
        "time",
        "timesince",
    ]
    list_display = [
        "id",
        "command",
        "message",
        "time",
        "timesince",
    ]
    list_filter = [
        "command",
    ]
    search_fields = [
        "command",
        "message",
    ]

    def time(self, obj):
        return datetime.fromtimestamp(obj.created_at)

    def timesince(self, obj):
        return timesince(datetime.fromtimestamp(obj.created_at)) + " ago"

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(Model, ModelAdmin)
