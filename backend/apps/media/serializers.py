"""
媒体文件序列化器
"""
from rest_framework import serializers

from .models import UploadedFile, Poster, FileScene, PosterType


class UploadedFileSerializer(serializers.ModelSerializer):
    """已上传文件序列化器"""
    class Meta:
        model = UploadedFile
        fields = [
            'id', 'object_key', 'cdn_url', 'scene', 'content_type',
            'size', 'uploader', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class FileUploadSerializer(serializers.Serializer):
    """文件上传序列化器"""
    scene = serializers.ChoiceField(choices=FileScene.choices)
    file = serializers.FileField(required=True)


class PosterSerializer(serializers.ModelSerializer):
    """海报序列化器"""
    class Meta:
        model = Poster
        fields = [
            'id', 'user', 'type', 'template', 'payload',
            'poster_url', 'qrcode_url', 'expires_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PosterCreateSerializer(serializers.Serializer):
    """海报创建序列化器"""
    type = serializers.ChoiceField(choices=PosterType.choices)
    template = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    payload = serializers.JSONField(required=True)
