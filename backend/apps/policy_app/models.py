"""
政策CMS模型 - 政策内容管理、版本、审核、标签、任务
"""
import logging

from django.db import models

from common.utils import generate_business_id, now_cst

logger = logging.getLogger('apps.policy_app')


# ============================================================
# 枚举定义
# ============================================================

class ContentStatus(models.TextChoices):
    """政策内容状态"""
    DRAFT = 'draft', '草稿'
    PENDING_REVIEW = 'pending_review', '待审核'
    PUBLISHED = 'published', '已发布'
    OFFLINE = 'offline', '已下线'
    ARCHIVED = 'archived', '已归档'


class ReviewAction(models.TextChoices):
    """审核动作"""
    SUBMIT = 'submit', '提交审核'
    APPROVE = 'approve', '通过'
    REJECT = 'reject', '驳回'
    REQUEST_CHANGES = 'request_changes', '要求修改'


class TagType(models.TextChoices):
    """标签类型"""
    REGION = 'region', '地区'
    STAGE = 'stage', '阶段'
    GRADE = 'grade', '年级'
    DOMAIN = 'domain', '领域'
    ABILITY = 'ability', '能力'
    TASK = 'task', '任务'
    USER_PROFILE = 'user_profile', '用户画像'


# ============================================================
# Policy 模型
# ============================================================

class Policy(models.Model):
    """政策内容"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField(
        '业务主键', max_length=32, unique=True, db_index=True,
        default='',
    )
    title = models.CharField('标题', max_length=255)
    source_name = models.CharField('来源名称', max_length=128, null=True, blank=True)
    source_url = models.CharField('来源链接', max_length=512, null=True, blank=True)
    policy_summary = models.TextField('政策摘要', null=True, blank=True)
    effective_date = models.DateField('生效日期', null=True, blank=True)
    region = models.CharField('地区', max_length=64, null=True, blank=True)
    stage = models.CharField('阶段', max_length=64, null=True, blank=True)
    grade_range = models.JSONField('年级范围', default=list, blank=True)
    domains = models.JSONField('领域', default=list, blank=True)
    influence_abilities = models.JSONField('影响能力', default=list, blank=True)
    parent_action_suggestions = models.JSONField('家长行动建议', default=list, blank=True)

    # 前端展示字段
    front_display_title = models.CharField('前端展示标题', max_length=255, null=True, blank=True)
    front_display_summary = models.TextField('前端展示摘要', null=True, blank=True)
    impact_explanation = models.TextField('影响说明', null=True, blank=True)
    monthly_suggestions = models.JSONField('月度建议', default=list, blank=True)
    weekly_task_suggestions = models.JSONField('每周任务建议', default=list, blank=True)
    focus_directions = models.JSONField('重点方向', default=list, blank=True)
    child_impact_analysis = models.TextField('对孩子的影响分析', null=True, blank=True)

    # 状态与审核
    content_status = models.CharField(
        '内容状态', max_length=16, choices=ContentStatus.choices, default=ContentStatus.DRAFT,
    )
    version = models.IntegerField('版本号', default=1)
    created_by = models.CharField('编辑者标识', max_length=64)
    reviewed_by = models.CharField('审核者标识', max_length=64, null=True, blank=True)
    review_comment = models.TextField('审核意见', null=True, blank=True)
    published_at = models.DateField('发布日期', null=True, blank=True)
    published_at_system = models.DateTimeField('系统发布时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'policy_policy'
        verbose_name = '政策'
        verbose_name_plural = '政策'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.business_id})'

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('policy')
        super().save(*args, **kwargs)


# ============================================================
# PolicyVersion 模型
# ============================================================

class PolicyVersion(models.Model):
    """政策版本快照"""
    id = models.BigAutoField(primary_key=True)
    policy = models.ForeignKey(
        Policy, on_delete=models.CASCADE, related_name='versions', verbose_name='政策',
    )
    version = models.IntegerField('版本号')
    snapshot = models.JSONField('快照数据')
    change_summary = models.CharField('变更说明', max_length=500, null=True, blank=True)
    editor = models.CharField('编辑者', max_length=64)
    published_at = models.DateTimeField('发布时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'policy_version'
        verbose_name = '政策版本'
        verbose_name_plural = '政策版本'
        unique_together = ('policy', 'version')
        ordering = ['-version']

    def __str__(self):
        return f'{self.policy.title} v{self.version}'


# ============================================================
# PolicyReview 模型
# ============================================================

class PolicyReview(models.Model):
    """政策审核记录"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField(
        '业务主键', max_length=32, unique=True, db_index=True,
        default='',  # 由 save() 方法在保存前生成
    )
    policy = models.ForeignKey(
        Policy, on_delete=models.CASCADE, related_name='reviews', verbose_name='政策',
    )
    version = models.IntegerField('版本号')
    reviewer = models.CharField('审核者', max_length=64, null=True, blank=True)
    action = models.CharField('审核动作', max_length=16, choices=ReviewAction.choices)
    comment = models.TextField('审核意见')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'policy_review'
        verbose_name = '政策审核记录'
        verbose_name_plural = '政策审核记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.policy.title} - {self.get_action_display()}'


# ============================================================
# PolicyTag 模型
# ============================================================

class PolicyTag(models.Model):
    """政策标签"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField(
        '业务主键', max_length=64, unique=True, db_index=True,
    )
    type = models.CharField('标签类型', max_length=32, choices=TagType.choices)
    name = models.CharField('标签名称', max_length=64)
    value = models.CharField('标签值', max_length=255, null=True, blank=True)
    enabled = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'policy_tag'
        verbose_name = '政策标签'
        verbose_name_plural = '政策标签'
        ordering = ['type', 'name']

    def __str__(self):
        return f'[{self.get_type_display()}] {self.name}'


# ============================================================
# PolicyTagRelation 模型
# ============================================================

class PolicyTagRelation(models.Model):
    """政策-标签关联"""
    id = models.BigAutoField(primary_key=True)
    policy = models.ForeignKey(
        Policy, on_delete=models.CASCADE, related_name='tag_relations', verbose_name='政策',
    )
    tag = models.ForeignKey(
        PolicyTag, on_delete=models.CASCADE, related_name='policy_relations', verbose_name='标签',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'policy_tag_relation'
        verbose_name = '政策标签关联'
        verbose_name_plural = '政策标签关联'
        unique_together = ('policy', 'tag')

    def __str__(self):
        return f'{self.policy.title} - {self.tag.name}'


# ============================================================
# PolicyTask 模型
# ============================================================

class PolicyTask(models.Model):
    """政策关联任务"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField(
        '业务主键', max_length=32, unique=True, db_index=True,
        default='',  # 由 save() 方法在保存前生成
    )
    policy = models.ForeignKey(
        Policy, on_delete=models.CASCADE, related_name='tasks', verbose_name='政策',
    )
    title = models.CharField('任务标题', max_length=255)
    category = models.CharField('任务分类', max_length=64, null=True, blank=True)
    description = models.TextField('任务描述', null=True, blank=True)
    frequency = models.CharField('频率', max_length=64, null=True, blank=True)
    estimated_time = models.CharField('预计耗时', max_length=32, null=True, blank=True)
    grade_range = models.JSONField('适用年级', default=list, blank=True)
    ability_tags = models.JSONField('能力标签', default=list, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'policy_task'
        verbose_name = '政策任务'
        verbose_name_plural = '政策任务'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.title} ({self.business_id})'


# ============================================================
# PolicyWeeklyTask 模型
# ============================================================

class PolicyWeeklyTask(models.Model):
    """政策每周任务"""
    id = models.BigAutoField(primary_key=True)
    policy = models.ForeignKey(
        Policy, on_delete=models.CASCADE, related_name='weekly_tasks', verbose_name='政策',
    )
    title = models.CharField('任务标题', max_length=255)
    category = models.CharField('任务分类', max_length=64, null=True, blank=True)
    description = models.TextField('任务描述', null=True, blank=True)
    frequency = models.CharField('频率', max_length=64, null=True, blank=True)
    estimated_time = models.CharField('预计耗时', max_length=32, null=True, blank=True)
    grade_range = models.JSONField('适用年级', default=list, blank=True)
    ability_tags = models.JSONField('能力标签', default=list, blank=True)
    sort = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'policy_weekly_task'
        verbose_name = '政策每周任务'
        verbose_name_plural = '政策每周任务'
        ordering = ['sort', 'created_at']

    def __str__(self):
        return f'{self.policy.title} - {self.title}'


# ============================================================
# PolicyAiGenerationLog 模型
# ============================================================

class PolicyAiGenerationLog(models.Model):
    """AI生成日志"""
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField('用户ID', null=True, blank=True)
    source_text_hash = models.CharField('源文本哈希', max_length=64)
    source_text_length = models.IntegerField('源文本长度')
    preset_tags = models.JSONField('预设标签')
    output = models.JSONField('输出结果')
    tokens_input = models.IntegerField('输入Token数', null=True, blank=True)
    tokens_output = models.IntegerField('输出Token数', null=True, blank=True)
    latency_ms = models.IntegerField('耗时(毫秒)', null=True, blank=True)
    error = models.TextField('错误信息', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'policy_ai_generation_log'
        verbose_name = 'AI生成日志'
        verbose_name_plural = 'AI生成日志'
        ordering = ['-created_at']

    def __str__(self):
        return f'AI生成记录 #{self.id}'
