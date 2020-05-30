from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Condom, Gel

product_admin_primary_fields = [
    "name_kor",
    "manufacturer_kor",
    "image",
    "image_tag",
    "thumbnail",
    "thumbnail_tag",
]


class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        # print(self, obj)
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.image.url))

    image_tag.short_description = "Image 미리보기"

    def thumbnail_tag(self, obj):
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.thumbnail.url))

    thumbnail_tag.short_description = "Thumbnail 미리보기"

    # read-only 필드 설정
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = (
            "image_tag",
            "thumbnail_tag",
            "num_of_reviews",
            "num_of_views",
            "score",
        )

        if self.model == Condom:
            self.readonly_fields += ("avg_oily", "avg_thickness", "avg_durability")

        elif self.model == Gel:
            self.readonly_fields += ("avg_viscosity",)

        return self.readonly_fields + ("created_at", "updated_at")

    # admin 페이지에 보여주는 필드 설정
    def get_fields(self, request, obj=None):
        form = self._get_form_for_get_fields(request, obj)
        form_base = [*form.base_fields] + [*self.get_readonly_fields(request, obj)]

        fields = [field for field in form_base if field not in product_admin_primary_fields]

        return product_admin_primary_fields + fields

    list_display = ("name_kor", "manufacturer_kor", "score", "num_of_reviews")


# admin.site.register(Product, ProductAdmin)
admin.site.register(Condom, ProductAdmin)
admin.site.register(Gel, ProductAdmin)
