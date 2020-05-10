from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Condom, Gel

product_admin_primary_fields = ['name', 'manufacturer', 'image', 'image_tag', 'thumbnail', 'thumbnail_tag']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    # Image tag for admin page
    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.image.url))

    image_tag.short_description = 'Image 미리보기'

    def thumbnail_tag(self, obj):
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.thumbnail.url))

    thumbnail_tag.short_description = 'Thumbnail 미리보기'

    fields = product_admin_primary_fields + [field.name for field in Product._meta.fields if
                                             field.name not in (['id'] + product_admin_primary_fields)]

    readonly_fields = ('image_tag', 'created_at', 'updated_at', 'thumbnail_tag')


admin.site.register(Condom)

admin.site.register(Gel)
