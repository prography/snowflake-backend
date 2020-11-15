from django.contrib import admin

from .models import Evaluation, Sutra, SutraComment


@admin.register(Sutra)
class SutraAdmin(admin.ModelAdmin):
    pass


@admin.register(SutraComment)
class SutraCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    pass
