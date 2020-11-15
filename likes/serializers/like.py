from rest_framework import serializers

from likes.models import Like
from products.serializers.condom import CondomListSerializer


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
