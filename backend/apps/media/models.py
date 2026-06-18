"""
媒体文件模型 - 上传文件、海报
"""
import logging

from django.conf import settings
from django.db import models

logger = logging.getLogger('apps.media')


# ============================================================
# 枚举定义
# ============================================================

class FileScene(models.TextChoices):
    """文件场景"""
    AVATAR = 'avatar', '头像'
    POST_IMAGE = 'post_image', '帖子图片'
    POSTER_IMAGE = 'poster_image', '海报图片'
    POLICY_IMAGE = 'policy_image', '政策图片'


class PosterType(models.TextChoices):
    """海报类型"""
    DAILY = 'daily', '每日海报'
    SISTER_INVITE = 'sister_invite', '姐妹邀请海报'


# ============================================================
# UploadedFile 模型
# ============================================================

class UploadedFile(models.Model):
    """已上传文件"""
    id = models.BigAutoField(primary_key=True)
    object_key = models.CharField('对象键', max_length=255, unique=True)
    cdn_url = models.CharField('CDN地址', max_length=512)
    scene = models.CharField('场景', max_length=32, choices=FileScene.choices)
    content_type = models.CharField('文件类型', max_length=64)
    size = models.BigIntegerField('文件大小(字节)')
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='uploaded_files', verbose_name='上传者',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'media_uploaded_file'
        verbose_name = '已上传文件'
        verbose_name_plural = '已上传文件'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.object_key} ({self.get_scene_display()})'


# ============================================================
# Poster 模型
# ============================================================

class Poster(models.Model):
    """海报"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='posters', verbose_name='用户',
    )
    type = models.CharField(
        '海报类型', max_length=32, choices=PosterType.choices,
    )
    template = models.CharField('模板标识', max_length=64, null=True, blank=True)
    payload = models.JSONField('生成参数')
    poster_url = models.CharField('海报图片URL', max_length=512, null=True, blank=True)
    qrcode_url = models.CharField('二维码URL', max_length=512, null=True, blank=True)
    expires_at = models.DateTimeField('过期时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'media_poster'
        verbose_name = '海报'
        verbose_name_plural = '海报'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.get_type_display()}'
