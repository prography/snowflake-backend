from django.contrib import admin

from reviews.models import Review, ReviewCondom


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "total")


# admin.site.register(Review)
admin.site.register(ReviewCondom, ReviewAdmin)
