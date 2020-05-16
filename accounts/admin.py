# from django.contrib import admin
# from django.utils.html import mark_safe
# from .models import User


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):

#     # Image tag for admin page
#     def image_tag(self, obj):
#         return mark_safe('<img src="%s" width="150" height="150" />' % (obj.image.url))

#     image_tag.short_description = "Image 미리보기"
#     fields = ["image", "image_tag"] + [
#         field.name for field in User._meta.fields if field.name != "id" and field.name != "image"
#     ]
#     readonly_fields = ("image_tag", "date_joined", "password")
#     list_display = ("email", "nickname", "social")

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# from account.models import MyUser
# @admin.register(MyUser)
# class MyUserAdmin(AuthUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'login_method', 'password', 'avatar', 'social_avatar', 'nickname', 'subscribe', 'is_active')}),
#     )

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
