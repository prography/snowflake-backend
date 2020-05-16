from django.contrib import admin
from django.utils.html import mark_safe
from .models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "username", "password", "social")}),
        ("Gender", {"fields": ("gender", "partner_gender")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    list_display = ("email", "username", "social")
