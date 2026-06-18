"""
返现账户与计划（商业化层）模型
"""
import logging

from django.conf import settings
from django.db import models

from common.utils import generate_business_id

logger = logging.getLogger('apps.finance')


# ============================================================
# 枚举
# ============================================================

class UserPlanStatus(models.TextChoices):
    ACTIVE = 'active', '生效中'
    EXPIRED = 'expired', '已过期'
    CANCELLED = 'cancelled', '已取消'


class CashbackType(models.TextChoices):
    """本期只允许 earn / manual_adjust，withdraw / refund 暂不出现"""
    EARN = 'earn', '赚取'
    MANUAL_ADJUST = 'manual_adjust', '手工调整'


class CashbackSource(models.TextChoices):
    DAILY_CHECKIN = 'daily_checkin', '每日打卡'
    INVITE_REWARD = 'invite_reward', '邀请奖励'
    MANUAL = 'manual', '手工调整'


# ============================================================
# 计划 SKU
# ============================================================

class Plan(models.Model):
    """计划 SKU"""
    id = models.BigAutoField(primary_key=True)
    code = models.CharField('计划代码', max_length=32, unique=True, db_index=True)
    name = models.CharField('计划名称', max_length=64)
    price_cents = models.BigIntegerField('价格（分）')
    duration_days = models.IntegerField('时长（天）')
    cashback_per_day = models.IntegerField('每日返现（分）', default=0)
    course_reward_value_cents = models.BigIntegerField('满勤课程价值（分）', default=0)
    max_badges = models.IntegerField('最大勋章数', default=0)
    description = models.TextField('描述', null=True, blank=True)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'finance_plan'
        verbose_name = '计划SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} ({self.code})'


# ============================================================
# 用户计划
# ============================================================

class UserPlan(models.Model):
    """用户计划订阅"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_plans',
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField('状态', max_length=16, default=UserPlanStatus.ACTIVE, choices=UserPlanStatus.choices)
    started_at = models.DateTimeField('开始时间')
    expires_at = models.DateTimeField('到期时间')
    cancelled_at = models.DateTimeField('取消时间', null=True, blank=True)
    extra = models.JSONField('扩展字段', default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'finance_user_plan'
        verbose_name = '用户计划'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user', 'status'], name='idx_user_plan_user_status'),
            models.Index(fields=['expires_at'], name='idx_user_plan_expires_at',
                         condition=models.Q(status='active')),
        ]

    def __str__(self):
        return f'{self.user_id} - {self.plan.code} ({self.status})'


# ============================================================
# 返现账户
# ============================================================

class CashbackAccount(models.Model):
    """用户返现账户"""
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cashback_account',
    )
    balance_cents = models.BigIntegerField('当前余额（分）', default=0)
    frozen_cents = models.BigIntegerField('冻结金额（分）', default=0)  # 本期始终为 0
    total_earned_cents = models.BigIntegerField('累计赚取（分）', default=0)
    total_withdrawn_cents = models.BigIntegerField('累计提现（分）', default=0)  # 本期始终为 0
    expected_cashback_cents = models.BigIntegerField('应得返现（分）', default=0)
    version = models.IntegerField('乐观锁版本', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'finance_cashback_account'
        verbose_name = '返现账户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'用户{self.user_id}账户：余额 {self.balance_cents} 分'


# ============================================================
# 返现流水
# ============================================================

class CashbackRecord(models.Model):
    """返现流水"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cashback_records',
    )
    amount_cents = models.BigIntegerField('金额（分）', help_text='正为增加，负为扣减')
    type = models.CharField('类型', max_length=32, choices=CashbackType.choices)
    source = models.CharField('来源', max_length=32, choices=CashbackSource.choices)
    ref_id = models.CharField('关联业务ID', max_length=64, null=True, blank=True)
    biz_date = models.DateField('业务日期')
    description = models.CharField('描述', max_length=255, null=True, blank=True)
    operator_id = models.BigIntegerField('操作员ID', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finance_cashback_record'
        verbose_name = '返现流水'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user', '-biz_date'], name='idx_cashback_record_user_date'),
            models.Index(fields=['type', '-created_at'], name='idx_cashback_record_type'),
        ]

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('csh')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_id} {self.type} {self.amount_cents}分'
