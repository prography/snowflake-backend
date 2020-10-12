from django.contrib import admin
from .models import Sutra, SutraComment, Evaluation


@admin.register(Sutra)
class SutraAdmin(admin.ModelAdmin):
    pass


@admin.register(SutraComment)
class SutraCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    pass
