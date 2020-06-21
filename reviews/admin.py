from django.contrib import admin

from reviews.models import Review, ReviewCondom, ReviewGel
from products.models import Product


class ProductInline(admin.TabularInline):
    model = Product


class ReviewAdmin(admin.ModelAdmin):
    def manufacturer(self, obj):
        return '%s(%s)' % (obj.product.manufacturer_kor, obj.product.manufacturer_eng)

    list_display = ("product", "manufacturer", "user", "total")
    search_fields = (
        "product__name_kor", "product__name_eng", "product__manufacturer_kor", "product__manufacturer_eng",
        "user__email", "user__username")

    readonly_fields = ("created_at", "updated_at")


admin.site.register(ReviewCondom, ReviewAdmin)
admin.site.register(ReviewGel, ReviewAdmin)
