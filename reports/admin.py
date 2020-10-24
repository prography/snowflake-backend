from django.contrib import admin

from reports.models import Report


@admin.register(Report)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content_type", "object_id", "created_at")
