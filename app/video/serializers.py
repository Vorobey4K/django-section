from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Like, Video

User = get_user_model()


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    qualities = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = (
            "owner",
            "name",
            "total_likes",
            "created_at",
            "qualities",
        )

    def get_qualities(self, obj: Video) -> list[str]:
        return list(obj.files.values_list("quality", flat=True))


class VideoIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("id",)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("video", "user")
        read_only_fields = ("video", "user")


class UserStatsSerializer(serializers.ModelSerializer):
    likes_sum = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "likes_sum")
