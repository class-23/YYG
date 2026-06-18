"""
核心用户模型 - 用户、用户资料、认证信息、推送Token
"""
import logging

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from common.utils import generate_business_id

logger = logging.getLogger('apps.core')


# ============================================================
# 枚举定义
# ============================================================

class Gender(models.IntegerChoices):
    """性别"""
    UNKNOWN = 0, '未知'
    MALE = 1, '男'
    FEMALE = 2, '女'


class UserRole(models.TextChoices):
    """用户角色"""
    USER = 'user', '普通用户'
    ADMIN = 'admin', '管理员'
    EDITOR = 'editor', '编辑'
    REVIEWER = 'reviewer', '审核员'


class PlanStatus(models.TextChoices):
    """计划状态"""
    NONE = 'none', '未加入'
    TRIAL7 = 'trial7', '7天试用'
    TRIAL21 = 'trial21', '21天试用'
    PLAN_21D = '21d_plan', '21天计划'
    PLAN_100D = '100d_plan', '100天计划'
    YEAR_365 = 'year365', '365天年卡'


class BabyStage(models.TextChoices):
    """宝宝阶段"""
    KINDERGARTEN = 'kindergarten', '幼儿园'
    LOWER = 'lower', '小学低年级'
    UPPER = 'upper', '小学高年级'
    JUNIOR = 'junior', '初中'


class PushProvider(models.TextChoices):
    """推送渠道"""
    WECHAT_MP = 'wechat_mp', '微信小程序'
    WECHAT_SUBSCRIBE = 'wechat_subscribe', '微信订阅消息'


# ============================================================
# 自定义 UserManager
# ============================================================

class UserManager(BaseUserManager):
    """自定义用户管理器"""

    def create_user(self, openid, nickname='', password=None, **extra_fields):
        if not openid:
            raise ValueError('openid 不能为空')
        user = self.model(
            openid=openid,
            nickname=nickname or f'宝妈{openid[-6:]}',
            **extra_fields,
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, openid, nickname='管理员', password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('role', UserRole.ADMIN)
        return self.create_user(openid, nickname, password, **extra_fields)


# ============================================================
# User 模型
# ============================================================

class User(AbstractBaseUser):
    """自定义用户模型"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField(
        '业务主键', max_length=32, unique=True, db_index=True,
        default='',  # 由 save() 方法在保存前生成
    )
    openid = models.CharField('微信openid', max_length=64, unique=True, db_index=True)
    unionid = models.CharField('微信unionid', max_length=64, unique=True, null=True, blank=True)
    nickname = models.CharField('昵称', max_length=64, default='')
    avatar_url = models.CharField('头像URL', max_length=512, null=True, blank=True)
    phone = models.CharField('手机号(加密)', max_length=128, null=True, blank=True)
    phone_masked = models.CharField('手机号(脱敏)', max_length=20, null=True, blank=True)
    gender = models.SmallIntegerField(
        '性别', choices=Gender.choices, default=Gender.UNKNOWN,
    )
    role = models.CharField(
        '角色', max_length=32, choices=UserRole.choices, default=UserRole.USER,
    )
    is_admin = models.BooleanField('是否管理员', default=False)
    is_disabled = models.BooleanField('是否禁用', default=False)
    disabled_reason = models.CharField('禁用原因', max_length=256, null=True, blank=True)
    disabled_at = models.DateTimeField('禁用时间', null=True, blank=True)
    last_login_at = models.DateTimeField('最后登录时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    deleted_at = models.DateTimeField('删除时间', null=True, blank=True)

    # Django 认证相关
    is_active = True  # 始终为 True，用 is_disabled 控制禁用
    is_staff = False

    objects = UserManager()

    USERNAME_FIELD = 'openid'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        db_table = 'core_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.nickname} ({self.business_id})'

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('usr')
        super().save(*args, **kwargs)

    @property
    def is_deleted(self):
        return self.deleted_at is not None


# ============================================================
# UserProfile 模型
# ============================================================

class UserProfile(models.Model):
    """用户资料"""
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户',
    )
    baby_stage = models.CharField(
        '宝宝阶段', max_length=32, choices=BabyStage.choices, null=True, blank=True,
    )
    region = models.CharField('地区', max_length=64, null=True, blank=True)
    city = models.CharField('城市', max_length=64, null=True, blank=True)
    bio = models.CharField('个人简介', max_length=500, null=True, blank=True)
    tags = models.JSONField('标签', default=list, blank=True)
    plan_status = models.CharField(
        '计划状态', max_length=16, choices=PlanStatus.choices, default=PlanStatus.NONE,
    )
    plan_started_at = models.DateTimeField('计划开始时间', null=True, blank=True)
    plan_expires_at = models.DateTimeField('计划过期时间', null=True, blank=True)
    trial21_unlocked = models.BooleanField('是否解锁21天试用', default=False)
    invite_progress = models.IntegerField('邀请进度', default=0)
    checked_days = models.IntegerField('已打卡天数', default=0)
    missed_days = models.IntegerField('缺卡天数', default=0)
    consecutive_days = models.IntegerField('连续打卡天数', default=0)
    longest_streak = models.IntegerField('最长连续天数', default=0)
    course_unlocked = models.IntegerField('已解锁课程数', default=0)
    course_total = models.IntegerField('课程总数', default=0)
    extra = models.JSONField('扩展字段', default=dict, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'core_user_profile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f'{self.user.nickname} 的资料'


# ============================================================
# UserAuth 模型
# ============================================================

class UserAuth(models.Model):
    """用户认证信息"""
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='auth', verbose_name='用户',
    )
    password_hash = models.CharField('密码哈希', max_length=255, null=True, blank=True)
    refresh_token_hash = models.CharField('刷新Token哈希', max_length=255, null=True, blank=True)
    refresh_token_expires_at = models.DateTimeField('刷新Token过期时间', null=True, blank=True)
    last_login_ip = models.GenericIPAddressField('最后登录IP', null=True, blank=True)
    last_login_user_agent = models.CharField('最后登录UA', max_length=512, null=True, blank=True)
    failed_login_count = models.IntegerField('连续登录失败次数', default=0)
    locked_until = models.DateTimeField('锁定截止时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'core_user_auth'
        verbose_name = '用户认证'
        verbose_name_plural = '用户认证'

    def __str__(self):
        return f'{self.user.business_id} 的认证信息'


# ============================================================
# PushToken 模型
# ============================================================

class PushToken(models.Model):
    """推送Token"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='push_tokens', verbose_name='用户',
    )
    provider = models.CharField(
        '推送渠道', max_length=32, choices=PushProvider.choices,
    )
    token = models.CharField('Token', max_length=255)
    device_id = models.CharField('设备ID', max_length=128, null=True, blank=True)
    is_active = models.BooleanField('是否有效', default=True)
    last_active_at = models.DateTimeField('最后活跃时间')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'core_push_token'
        verbose_name = '推送Token'
        verbose_name_plural = '推送Token'
        indexes = [
            models.Index(fields=['user', 'provider'], name='idx_push_user_provider'),
        ]

    def __str__(self):
        return f'{self.user.business_id} - {self.provider}'
