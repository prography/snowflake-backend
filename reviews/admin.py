from django.contrib import admin

from reviews.models import Review, ReviewCondom, ReviewGel


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "total")
    readonly_fields = ("created_at", "updated_at")


# admin.site.register(Review)
admin.site.register(ReviewCondom, ReviewAdmin)
admin.site.register(ReviewGel, ReviewAdmin)
