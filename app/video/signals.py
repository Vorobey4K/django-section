from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Like, Video


def update_video_likes(video_id: int, delta: int) -> None:
    Video.objects.filter(pk=video_id).update(total_likes=F("total_likes") + delta)


@receiver(post_save, sender=Like)
def add_like(sender, instance, created, raw=False, **kwargs):
    if raw:
        return
    if created:
        update_video_likes(instance.video_id, 1)


@receiver(post_delete, sender=Like)
def remove_like(sender, instance, raw=False, **kwargs):
    if raw:
        return
    update_video_likes(instance.video_id, -1)
