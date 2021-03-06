from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Condom, Gel, WelcomeCard

product_admin_primary_fields = [
    "name_kor",
    "name_eng",
    "manufacturer_kor",
    "manufacturer_eng",
    "category",
    "image",
    "image_tag",
    "thumbnail",
    "thumbnail_tag",
    "search_field"
]


class ProductDetailAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
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

    # # admin 페이지에 보여주는 필드 설정
    # def get_fields(self, request, obj=None):
    #     form = self._get_form_for_get_fields(request, obj)
    #     form_base = [*form.base_fields] + [*self.get_readonly_fields(request, obj)]
    #
    #     fields = [field for field in form_base if field not in product_admin_primary_fields]
    #
    #     return product_admin_primary_fields + fields

    list_display = ("id", "name_kor", "manufacturer_kor", "score", "num_of_reviews")


admin.site.register(Condom, ProductDetailAdmin)
admin.site.register(Gel, ProductDetailAdmin)


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
