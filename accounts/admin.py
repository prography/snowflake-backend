from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.admin import ModelAdmin
from django.utils.html import mark_safe

from .models import User, Icon


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
        ("Icon", {"fields": ("icon", "color")})
    )

    readonly_fields = ("image_tag",)
    list_display = ("email", "username", "social")


@admin.register(Icon)
class IconAdmin(ModelAdmin):
    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="100" height="100" />' % (obj.image.url))

    image_tag.short_description = "Image 미리보기"
    readonly_fields = ("image_tag",)
    list_display = ("id", "name", "image", "created_at", "updated_at")
