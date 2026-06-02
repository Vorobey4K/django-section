from django.urls import path, include
from rest_framework import routers
from .views import (
    VideoViewSet,
    VideoLikeView,
    VideoIdsView,
    VideoStatsGroupView,
    VideoStatsSubqueryView,
)

router = routers.SimpleRouter()
router.register("", VideoViewSet, basename="videos")

urlpatterns = [
    path("", include(router.urls)),
    path("ids/", VideoIdsView.as_view()),
    path("statistics-group-by/", VideoStatsGroupView.as_view()),
    path("statistics-subquery/", VideoStatsSubqueryView.as_view()),
    path("<int:video_id>/likes/", VideoLikeView.as_view()),
]
