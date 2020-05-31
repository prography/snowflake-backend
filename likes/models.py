from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import User


class Like(models.Model):
    # Content type
    limit = models.Q(app_label='products', model='product') | \
            models.Q(app_label='reviews', model='review')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(
        User, verbose_name="작성자", on_delete=models.CASCADE, related_name="like"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="업데이트 시간")

    def __str__(self):
        return "{}-{}-{}".format(self.user, self.content_type.app_label, self.object_id)
