from django.contrib import admin
from django.utils.html import mark_safe

from .models import WelcomeCard, DesignType


@admin.register(WelcomeCard)
class WelcomeCardAdmin(admin.ModelAdmin):
    # Image tag for admin page
    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.image.url))

    image_tag.short_description = "Image 미리보기"
    fields = ["title", "image", "image_tag"] + [
        field.name
        for field in WelcomeCard._meta.fields
        if field.name != "id" and field.name != "image" and field.name != "title"
    ]
    readonly_fields = ("image_tag", "created_at", "updated_at")
    # fields = [field.name for field in WelcomeCard._meta.fields if field.name != "id"]

    list_display = ("title", "status", 'category', 'col')


@admin.register(DesignType)
class DesignTypeAdmin(admin.ModelAdmin):
    pass