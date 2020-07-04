from rest_framework import serializers
from accounts.serializers import accounts
from likes.models import Like
from products.models import Condom, Gel
from products.serializers.condom import CondomListSerializer


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


class LikeWithProductDetailSerializer(serializers.ModelSerializer):
    object_detail = serializers.SerializerMethodField()

    def get_object_detail(self, obj):
        related_obj = obj.content_object
        related_obj_name = related_obj.__class__.__name__.lower()
        if related_obj_name == 'product':
            serializer = CondomListSerializer(related_obj)
            return serializer.data
        return None

    class Meta:
        model = Like
        fields = [
            "id",
            "content_type",
            "object_id",
            "user",
            "created_at",
            "updated_at",
            "object_detail"
        ]
