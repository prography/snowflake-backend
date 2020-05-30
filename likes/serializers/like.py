from rest_framework import serializers
from accounts.serializers import accounts
from likes.models import Like


# limit = models.Q(app_label='products', model='product') | \
#         models.Q(app_label='reviews', model='review')
# content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
# object_id = models.PositiveIntegerField()
# content_object = GenericForeignKey('content_type', 'object_id')
#
# user = models.ForeignKey(
#     User, verbose_name="작성자", on_delete=models.CASCADE, related_name="like"
# )
# created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")
# updated_at = models.DateTimeField(auto_now=True, verbose_name="업데이트 시간")

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            "id",
            "content_type",
            "object_id",
            "user",
            "created_at",
            "updated_at",
        ]
