from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.html import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="100" height="100" />' % (obj.image.url))

    image_tag.short_description = "Image 미리보기"

    fieldsets = (
        (None, {"fields": ("email", "username", "password", "social")}),
        ("Profile", {"fields": ("birth_year", "image", "image_tag")}),
        ("Gender", {"fields": ("gender", "partner_gender")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    readonly_fields = ("image_tag",)
    list_display = ("email", "username", "social")
