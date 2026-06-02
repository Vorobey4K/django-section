from django.db import models
from django.db.models import Q


class VideoQuerySet(models.QuerySet):
    def published_ids(self):
        return self.filter(is_published=True).values_list("id", flat=True)

    def visible_for(self, user=None):
        if not user or not user.is_authenticated:
            return self.filter(is_published=True)

        if user.is_staff:
            return self

        return self.filter(Q(is_published=True) | Q(owner=user))
