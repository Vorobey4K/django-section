from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Subquery, Sum

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db.models import QuerySet


from .custom_generics import CreateDestroyAPIView
from .models import Like, Video
from .paganation import SmallPagePagination
from .serializers import (
    LikeSerializer,
    UserStatsSerializer,
    VideoIdSerializer,
    VideoSerializer,
)

User = get_user_model()


class VideoViewSet(ModelViewSet):
    serializer_class = VideoSerializer
    pagination_class = SmallPagePagination

    def get_queryset(self) -> QuerySet[Video]:
        return (
            Video.objects.select_related("owner")
            .prefetch_related("files")
            .visible_for(self.request.user)
        )


class VideoLikeView(CreateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class VideoIdsView(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = VideoIdSerializer

    def get(self, request) -> Response:
        return Response(list(Video.objects.published_ids()))


class VideoStatsGroupView(ListAPIView):
    serializer_class = UserStatsSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self) -> QuerySet:
        return User.objects.annotate(likes_sum=Sum("videos__total_likes")).order_by(
            "-likes_sum"
        )


class VideoStatsSubqueryView(ListAPIView):
    serializer_class = UserStatsSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self) -> QuerySet:
        likes_sum_subquery = (
            Video.objects.filter(owner=OuterRef("pk"))
            .values("owner")
            .annotate(total=Sum("total_likes"))
            .values("total")[:1]
        )

        return User.objects.annotate(likes_sum=Subquery(likes_sum_subquery)).order_by(
            "-likes_sum"
        )
