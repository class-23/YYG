"""media admin - 文件/海报管理"""
from django.contrib import admin

from .models import UploadedFile, Poster


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_key', 'scene', 'content_type', 'size', 'uploader', 'created_at')
    list_filter = ('scene', 'content_type')
    search_fields = ('object_key', 'cdn_url', 'uploader__nickname')
    date_hierarchy = 'created_at'
    raw_id_fields = ('uploader',)


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'template', 'poster_url', 'qrcode_url', 'expires_at', 'created_at')
    list_filter = ('type', 'template')
    search_fields = ('user__nickname', 'poster_url', 'qrcode_url')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)
