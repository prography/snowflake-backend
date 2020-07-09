from django.contrib import admin

from likes.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content_type", "object_id", "created_at", "updated_at")
