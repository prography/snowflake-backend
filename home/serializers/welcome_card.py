from home.models import WelcomeCard
from rest_framework import serializers


class WelcomeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomeCard
        fields = [
            "title",
            "description",
            "created_at",
            "updated_at",
            "button_src",
            "image",
            "row",
            "col",
            "status",
        ]
