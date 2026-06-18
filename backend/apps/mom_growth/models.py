"""
宝妈成长数据模型
里程碑 / 线下活动
"""
from django.conf import settings
from django.db import models

from common.utils import now_cst


class MilestoneDefinition(models.Model):
    """里程碑定义"""

    month = models.IntegerField('月份', unique=True)
    badge_level = models.IntegerField('徽章等级')
    label = models.CharField('标签', max_length=64)
    copy = models.TextField('文案')
    required_days = models.IntegerField('所需天数')
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = 'mom_growth_milestone_definition'
        verbose_name = '里程碑定义'
        verbose_name_plural = verbose_name
        ordering = ['month']

    def __str__(self):
        return f'{self.label} (第{self.month}月)'


class UserMilestone(models.Model):
    """用户已解锁的里程碑"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='milestones', verbose_name='用户',
    )
    milestone = models.ForeignKey(
        MilestoneDefinition, on_delete=models.CASCADE,
        related_name='unlock_records', verbose_name='里程碑',
    )
    unlocked_at = models.DateTimeField('解锁时间', default=now_cst)

    class Meta:
        db_table = 'mom_growth_user_milestone'
        verbose_name = '用户里程碑'
        verbose_name_plural = verbose_name
        unique_together = [('user', 'milestone')]

    def __str__(self):
        return f'{self.user} - {self.milestone}'


class OfflineActivity(models.Model):
    """线下活动"""

    class Status(models.TextChoices):
        OPEN = 'open', '报名中'
        CLOSED = 'closed', '已截止'
        CANCELLED = 'cancelled', '已取消'

    title = models.CharField('活动标题', max_length=255)
    description = models.TextField('活动描述', blank=True, null=True)
    city = models.CharField('城市', max_length=64)
    location = models.CharField('地点', max_length=255, blank=True, null=True)
    start_at = models.DateTimeField('开始时间')
    end_at = models.DateTimeField('结束时间')
    max_seats = models.IntegerField('最大名额')
    taken_seats = models.IntegerField('已占名额', default=0)
    cover = models.CharField('封面图', max_length=512, blank=True, null=True)
    status = models.CharField(
        '状态', max_length=16,
        choices=Status.choices, default=Status.OPEN,
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'mom_growth_offline_activity'
        verbose_name = '线下活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class OfflineActivitySignup(models.Model):
    """线下活动报名"""

    class Status(models.TextChoices):
        SIGNED = 'signed', '已报名'
        CANCELLED = 'cancelled', '已取消'
        ATTENDED = 'attended', '已参加'

    activity = models.ForeignKey(
        OfflineActivity, on_delete=models.CASCADE,
        related_name='signups', verbose_name='活动',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='activity_signups', verbose_name='用户',
    )
    status = models.CharField(
        '状态', max_length=16,
        choices=Status.choices, default=Status.SIGNED,
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'mom_growth_offline_activity_signup'
        verbose_name = '活动报名'
        verbose_name_plural = verbose_name
        unique_together = [('activity', 'user')]

    def __str__(self):
        return f'{self.user} - {self.activity}'
