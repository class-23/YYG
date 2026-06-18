"""
消息系统模型 - 消息、消息回执
"""
import logging

from django.conf import settings
from django.db import models

from common.utils import generate_business_id, now_cst

logger = logging.getLogger('apps.message')


# ============================================================
# 枚举定义
# ============================================================

class MessageType(models.TextChoices):
    """消息类型"""
    SYSTEM = 'system', '系统消息'
    CHECKIN_REMIND = 'checkin_remind', '打卡提醒'
    TEAM = 'team', '小队消息'
    POLICY = 'policy', '政策消息'


# ============================================================
# Message 模型
# ============================================================

class Message(models.Model):
    """消息"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField(
        '业务主键', max_length=32, unique=True, db_index=True,
        default='',  # 由 save() 方法在保存前生成
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='messages', verbose_name='用户',
    )
    type = models.CharField(
        '消息类型', max_length=32, choices=MessageType.choices, default=MessageType.SYSTEM,
    )
    title = models.CharField('标题', max_length=255)
    content = models.TextField('内容', null=True, blank=True)
    link = models.CharField('链接', max_length=512, null=True, blank=True)
    extra = models.JSONField('扩展数据', default=dict, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'message_message'
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.business_id})'

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('msg')
        super().save(*args, **kwargs)


# ============================================================
# MessageReceipt 模型
# ============================================================

class MessageReceipt(models.Model):
    """消息回执"""
    id = models.BigAutoField(primary_key=True)
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='receipts', verbose_name='消息',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='message_receipts', verbose_name='用户',
    )
    is_read = models.BooleanField('是否已读', default=False)
    read_at = models.DateTimeField('阅读时间', null=True, blank=True)
    is_pushed = models.BooleanField('是否已推送', default=False)
    pushed_at = models.DateTimeField('推送时间', null=True, blank=True)

    class Meta:
        db_table = 'message_receipt'
        verbose_name = '消息回执'
        verbose_name_plural = '消息回执'
        unique_together = ('message', 'user')

    def __str__(self):
        return f'{self.message.title} -> {self.user}'
