from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.serializers import BaseSerializer


class CreateDestroyAPIView(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericAPIView
):
    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(user=self.request.user, video_id=self.kwargs.get("video_id"))

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
