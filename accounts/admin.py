from django.contrib import admin
from django.utils.html import mark_safe
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    # Image tag for admin page
    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.image.url))

    image_tag.short_description = 'Image'
    fields = ['image', 'image_tag'] + [field.name for field in User._meta.fields if
                                       field.name != "id" and field.name != 'image']
    readonly_fields = ('image_tag',)

# Register your models here.
