from rest_framework import serializers

from products.models import WelcomeCard


class WelcomeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomeCard
        fields = [
            "description",
            "tag_txt",
            "created_at",
            "updated_at",
            "button_src",
            "button_txt",
            "image",
            "design_type",
            "category",
            "col",
            "status",
        ]
