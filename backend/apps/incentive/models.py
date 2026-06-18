"""
激励系统模型 - 徽章、课程、兑换
"""
import logging

from django.conf import settings
from django.db import models

from common.utils import generate_business_id

logger = logging.getLogger('apps.incentive')


class CourseExchangeStatus(models.TextChoices):
    PENDING = 'pending', '待处理'
    SUCCESS = 'success', '兑换成功'
    FAILED = 'failed', '兑换失败'


class InquiryStatus(models.TextChoices):
    RECEIVED = 'received', '已收到'
    CONTACTED = 'contacted', '已联系'
    CONVERTED = 'converted', '已转化'
    CLOSED = 'closed', '已关闭'


# ============================================================
# 徽章
# ============================================================

class Badge(models.Model):
    """徽章定义"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    name = models.CharField('徽章名称', max_length=64)
    description = models.CharField('描述', max_length=255, null=True, blank=True)
    required_days = models.IntegerField('达成所需天数')
    level = models.IntegerField('等级（1初心/2坚持/3点亮/4节奏）', default=1)
    icon = models.CharField('图标URL', max_length=512, null=True, blank=True)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'incentive_badge'
        verbose_name = '徽章定义'
        verbose_name_plural = verbose_name
        ordering = ['level', 'required_days']

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('bdg')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} (Lv.{self.level})'


class UserBadge(models.Model):
    """用户徽章"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_badges',
    )
    badge = models.ForeignKey(Badge, on_delete=models.PROTECT)
    unlocked_at = models.DateTimeField('解锁时间', auto_now_add=True)
    context = models.JSONField('解锁上下文', default=dict, blank=True)

    class Meta:
        db_table = 'incentive_user_badge'
        verbose_name = '用户徽章'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'badge'),)

    def __str__(self):
        return f'{self.user_id} - {self.badge.name}'


# ============================================================
# 课程
# ============================================================

class Course(models.Model):
    """课程"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    title = models.CharField('课程标题', max_length=255)
    cover = models.CharField('封面图', max_length=512, null=True, blank=True)
    description = models.TextField('描述', null=True, blank=True)
    tags = models.JSONField('标签', default=list, blank=True)
    value_cents = models.BigIntegerField('价值（分）', default=0)
    required_cashback_days = models.IntegerField('兑换所需返现天数', default=0)
    redeem_limit_per_user = models.IntegerField('每人限兑', default=1)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'incentive_course'
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('crs')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseExchange(models.Model):
    """课程兑换记录"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_exchanges',
    )
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    status = models.CharField(
        '状态', max_length=16,
        default=CourseExchangeStatus.PENDING,
        choices=CourseExchangeStatus.choices,
    )
    redeemed_at = models.DateTimeField('兑换时间', auto_now_add=True)

    class Meta:
        db_table = 'incentive_course_exchange'
        verbose_name = '课程兑换'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'course'),)

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('exg')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_id} - {self.course.title} - {self.status}'


class CourseInquiry(models.Model):
    """课程咨询线索"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='course_inquiries',
    )
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    from_page = models.CharField('来源页面', max_length=128, default='pages/courses/index')
    phone = models.CharField('手机号（加密）', max_length=128, null=True, blank=True)
    phone_masked = models.CharField('手机号（脱敏）', max_length=20, null=True, blank=True)
    phone_hash = models.CharField('手机号SHA256', max_length=64, null=True, blank=True, db_index=True)
    wechat = models.CharField('微信号', max_length=128, null=True, blank=True)
    note = models.CharField('咨询意向', max_length=200, null=True, blank=True)
    status = models.CharField(
        '状态', max_length=16, default=InquiryStatus.RECEIVED, choices=InquiryStatus.choices,
    )
    follow_up_channel = models.CharField('触达渠道', max_length=32, default='wechat_enterprise')
    operator_id = models.BigIntegerField('跟进人ID', null=True, blank=True)
    contacted_at = models.DateTimeField('首次联系时间', null=True, blank=True)
    closed_at = models.DateTimeField('关闭时间', null=True, blank=True)
    client_meta = models.JSONField('客户端元信息', default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'incentive_course_inquiry'
        verbose_name = '课程咨询'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user', '-created_at'], name='idx_course_inquiry_user'),
            models.Index(fields=['course', '-created_at'], name='idx_course_inquiry_course'),
            models.Index(fields=['status', '-created_at'], name='idx_course_inquiry_status'),
        ]

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('inq')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.phone_masked or "匿名"} 咨询 {self.course.title}'
