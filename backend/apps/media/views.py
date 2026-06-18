"""
媒体文件视图
"""
import logging
import uuid

from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.views import APIView

from common.response import success, created, fail, bad_request

from .models import UploadedFile, FileScene, Poster
from .serializers import (
    UploadedFileSerializer, FileUploadSerializer,
    PosterSerializer, PosterCreateSerializer,
)

logger = logging.getLogger('apps.media')


class FileUploadView(APIView):
    """POST /v1/files/upload/ - 文件上传"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        scene = serializer.validated_data['scene']
        file_obj = serializer.validated_data['file']

        # 生成对象键
        ext = file_obj.name.rsplit('.', 1)[-1] if '.' in file_obj.name else 'bin'
        object_key = f'{scene}/{uuid.uuid4().hex[:16]}.{ext}'

        # 构建CDN地址（实际项目中应对接对象存储服务）
        cdn_url = f'{settings.MEDIA_URL}{object_key}'

        # 保存文件记录
        uploaded_file = UploadedFile.objects.create(
            object_key=object_key,
            cdn_url=cdn_url,
            scene=scene,
            content_type=file_obj.content_type or 'application/octet-stream',
            size=file_obj.size,
            uploader=request.user,
        )

        logger.info(
            '文件上传: user=%s, scene=%s, size=%s, key=%s',
            request.user.id, scene, file_obj.size, object_key,
        )

        return created(
            data=UploadedFileSerializer(uploaded_file).data,
            message='文件上传成功',
        )


class PosterCreateView(APIView):
    """POST /v1/posters/ - 创建海报"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PosterCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        poster = Poster.objects.create(
            user=request.user,
            type=data['type'],
            template=data.get('template'),
            payload=data['payload'],
        )

        return created(
            data=PosterSerializer(poster).data,
            message='海报创建成功',
        )


class PosterListView(generics.ListAPIView):
    """GET /v1/posters/ - 我的海报列表"""
    serializer_class = PosterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Poster.objects.filter(user=self.request.user)
