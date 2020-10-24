from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import User


class Report(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(
        User, verbose_name="신고자", on_delete=models.CASCADE, related_name="report"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")

    class Meta:
        unique_together = (('content_type', 'object_id', 'user'),)

    def __str__(self):
        return f'{self.user}-{self.content_type.app_label}-{self.object_id}'
