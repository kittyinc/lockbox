from common.constants import (
    UPLOAD_STATUS_TYPES,
)
from common.utils import get_config
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from user.models import LockboxUser

from storage.models import File, FileChunk
from storage.serializers import FileChunkSerializer, FileSerializer


class FileModelViewSet(ModelViewSet):
    model = File
    queryset = File.objects.all()
    serializer_class = FileSerializer

    @action(detail=True, methods=["post"])
    def finalize(self, *args, **kwargs):  #noqa: ARG002
        file = self.get_object()
        file.status = UPLOAD_STATUS_TYPES.PROCESSING
        file.save()
        return Response(status=status.HTTP_200_OK)

class FileChunkViewSet(ModelViewSet):
    model = FileChunk
    queryset = FileChunk.objects.all()
    serializer_class = FileChunkSerializer


