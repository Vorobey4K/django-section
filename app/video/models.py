from django.contrib.auth import get_user_model
from django.db import models

from .querysets import VideoQuerySet

User = get_user_model()


class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    is_published = models.BooleanField(default=False)
    name = models.CharField(max_length=90)
    total_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = VideoQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name

    def publish(self) -> None:
        self.is_published = True
        self.save(update_fields=["is_published"])

    def unpublish(self) -> None:
        self.is_published = False
        self.save(update_fields=["is_published"])


class VideoFile(models.Model):
    class Quality(models.TextChoices):
        HD = "HD", "720p"
        FULL_HD = "FHD", "1080p"
        ULTRA_HD = "UHD", "4K"

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="files")

    file = models.FileField(upload_to="videos/")

    quality = models.CharField(
        max_length=3, choices=Quality.choices, default=Quality.FULL_HD
    )

    def __str__(self) -> str:
        return f"{self.video.name} ({self.quality})"


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["video", "user"], name="unique_video_like")
        ]

    def __str__(self) -> str:
        return f"{self.user} -> {self.video}"
