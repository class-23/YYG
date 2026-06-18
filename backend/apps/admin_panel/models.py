"""
运营后台相关模型 - 管理员账号、角色权限、审计日志、数据字典
"""
import logging

from django.conf import settings
from django.db import models

logger = logging.getLogger('apps.admin_panel')


# ============================================================
# 角色与权限
# ============================================================

class AdminRole(models.TextChoices):
    SUPER_ADMIN = 'super_admin', '超级管理员'
    POLICY_EDITOR = 'policy_editor', '政策编辑'
    POLICY_REVIEWER = 'policy_reviewer', '政策审核'
    CS = 'cs', '客服'
    FINANCE = 'finance', '财务'


class AdminModule(models.TextChoices):
    POLICY = 'policy', '政策'
    USER = 'user', '用户'
    ORDER = 'order', '订单'


class AdminAuditResult(models.TextChoices):
    SUCCESS = 'success', '成功'
    FAILED = 'failed', '失败'


# ============================================================
# AdminUser 模型
# ============================================================

class AdminUser(models.Model):
    """后台管理员账号"""
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('用户名', max_length=64, unique=True, db_index=True)
    password_hash = models.CharField('密码哈希', max_length=255)
    nickname = models.CharField('昵称', max_length=64)
    email = models.CharField('邮箱', max_length=128, null=True, blank=True)
    phone = models.CharField('手机号', max_length=20, null=True, blank=True)
    role_code = models.CharField('角色', max_length=32, default=AdminRole.CS)
    is_active = models.BooleanField('是否激活', default=True)
    last_login_at = models.DateTimeField('最近登录时间', null=True, blank=True)
    last_login_ip = models.GenericIPAddressField('最近登录IP', null=True, blank=True)
    failed_login_count = models.IntegerField('失败登录次数', default=0)
    locked_until = models.DateTimeField('锁定截止时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'admin_panel_admin_user'
        verbose_name = '管理员账号'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.username} ({self.nickname})'

    def is_locked(self):
        from django.utils import timezone
        return self.locked_until and self.locked_until > timezone.now()


# ============================================================
# 角色与权限
# ============================================================

class AdminRoleDefinition(models.Model):
    """角色定义"""
    id = models.BigAutoField(primary_key=True)
    code = models.CharField('角色代码', max_length=32, unique=True, db_index=True)
    name = models.CharField('角色名称', max_length=64)
    description = models.CharField('描述', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_panel_role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} ({self.code})'


class AdminPermission(models.Model):
    """权限定义"""
    id = models.BigAutoField(primary_key=True)
    code = models.CharField('权限代码', max_length=64, unique=True, db_index=True)
    name = models.CharField('权限名称', max_length=64)
    module = models.CharField('所属模块', max_length=32, choices=AdminModule.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_panel_permission'
        verbose_name = '权限'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} ({self.code})'


class AdminRolePermission(models.Model):
    """角色-权限关联"""
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(AdminRoleDefinition, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(AdminPermission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'admin_panel_role_permission'
        verbose_name = '角色权限'
        verbose_name_plural = verbose_name
        unique_together = (('role', 'permission'),)


# ============================================================
# 审计日志
# ============================================================

class AdminAuditLog(models.Model):
    """操作审计日志"""
    id = models.BigAutoField(primary_key=True)
    operator = models.ForeignKey(AdminUser, on_delete=models.PROTECT, related_name='audit_logs')
    action = models.CharField('操作', max_length=64)
    target_type = models.CharField('目标类型', max_length=32)
    target_id = models.CharField('目标ID', max_length=64)
    payload_before = models.JSONField('变更前', null=True, blank=True)
    payload_after = models.JSONField('变更后', null=True, blank=True)
    ip = models.GenericIPAddressField('IP', null=True, blank=True)
    user_agent = models.CharField('UA', max_length=512, null=True, blank=True)
    result = models.CharField('结果', max_length=16, default=AdminAuditResult.SUCCESS, choices=AdminAuditResult.choices)
    error_message = models.TextField('错误信息', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'admin_panel_audit_log'
        verbose_name = '审计日志'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['operator', '-created_at'], name='idx_audit_operator_time'),
            models.Index(fields=['target_type', 'target_id', '-created_at'], name='idx_audit_target'),
        ]

    def __str__(self):
        return f'{self.operator.username} {self.action} {self.target_type}:{self.target_id}'


# ============================================================
# 数据字典
# ============================================================

class DataDictionaryEntry(models.Model):
    """通用数据字典"""
    id = models.BigAutoField(primary_key=True)
    type = models.CharField('字典类型', max_length=32, db_index=True)
    code = models.CharField('代码', max_length=64)
    name = models.CharField('名称', max_length=64)
    sort = models.IntegerField('排序', default=0)
    extra = models.JSONField('扩展字段', default=dict, blank=True)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_panel_data_dictionary'
        verbose_name = '数据字典'
        verbose_name_plural = verbose_name
        unique_together = (('type', 'code'),)

    def __str__(self):
        return f'[{self.type}] {self.name} ({self.code})'
