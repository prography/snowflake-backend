from django.contrib import admin

from reviews.models import Review, ReviewCondom, ReviewGel


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "total")


# admin.site.register(Review)
admin.site.register(ReviewCondom, ReviewAdmin)
admin.site.register(ReviewGel, ReviewAdmin)
