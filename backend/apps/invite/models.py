"""
邀请系统模型 - 邀请码、邀请记录
"""
import logging

from django.conf import settings
from django.db import models

from common.utils import generate_invite_code, now_cst

logger = logging.getLogger('apps.invite')


# ============================================================
# 枚举定义
# ============================================================

class InviteCodeType(models.TextChoices):
    """邀请码类型"""
    SISTER_TEAM = 'sister_team', '姐妹团'
    PLAN_TRIAL21 = 'plan_trial21', '21天试用'
    GENERAL = 'general', '通用'


class InviteStatus(models.TextChoices):
    """邀请状态"""
    PENDING = 'pending', '待注册'
    REGISTERED = 'registered', '已注册'
    FIRST_CHECKIN = 'first_checkin', '首次打卡'
    CONFIRMED = 'confirmed', '已确认'
    EXPIRED = 'expired', '已过期'


# ============================================================
# InviteCode 模型
# ============================================================

class InviteCode(models.Model):
    """邀请码"""
    id = models.BigAutoField(primary_key=True)
    code = models.CharField('邀请码', max_length=16, unique=True, db_index=True)
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='invite_codes', verbose_name='所属用户',
    )
    type = models.CharField(
        '邀请码类型', max_length=16, choices=InviteCodeType.choices, default=InviteCodeType.GENERAL,
    )
    ref_id = models.CharField('关联ID', max_length=32, null=True, blank=True)
    use_limit = models.IntegerField('使用次数限制', default=0, help_text='0=无限制')
    used_count = models.IntegerField('已使用次数', default=0)
    expires_at = models.DateTimeField('过期时间', null=True, blank=True)
    is_active = models.BooleanField('是否有效', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'invite_code'
        verbose_name = '邀请码'
        verbose_name_plural = '邀请码'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.code} ({self.get_type_display()})'

    @property
    def is_valid(self):
        """检查邀请码是否有效"""
        if not self.is_active:
            return False
        if self.expires_at and now_cst() > self.expires_at:
            return False
        if self.use_limit > 0 and self.used_count >= self.use_limit:
            return False
        return True


# ============================================================
# InviteRecord 模型
# ============================================================

class InviteRecord(models.Model):
    """邀请记录"""
    id = models.BigAutoField(primary_key=True)
    invite_code = models.ForeignKey(
        InviteCode, on_delete=models.CASCADE, related_name='records', verbose_name='邀请码',
    )
    inviter_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='invite_sent', verbose_name='邀请人',
    )
    invitee_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='invite_received', null=True, blank=True, verbose_name='被邀请人',
    )
    status = models.CharField(
        '邀请状态', max_length=16, choices=InviteStatus.choices, default=InviteStatus.PENDING,
    )
    first_checkin_at = models.DateTimeField('首次打卡时间', null=True, blank=True)
    confirmed_at = models.DateTimeField('确认时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'invite_record'
        verbose_name = '邀请记录'
        verbose_name_plural = '邀请记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.inviter_user} -> {self.invitee_user or "待注册"}'
