"""
宝宝测评数据模型
测评模板 / 题目 / 提交 / 宝宝档案
"""
from django.conf import settings
from django.db import models

from common.utils import generate_business_id, now_cst


class KidAssessmentTemplate(models.Model):
    """测评模板"""

    code = models.CharField('模板编码', max_length=32, unique=True)
    name = models.CharField('模板名称', max_length=64)
    version = models.IntegerField('版本号', default=1)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'kid_assessment_template'
        verbose_name = '测评模板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} v{self.version}'


class KidAssessmentQuestion(models.Model):
    """测评题目"""

    class QuestionType(models.TextChoices):
        SINGLE = 'single', '单选'
        MULTI = 'multi', '多选'
        TEXT = 'text', '文本'
        NUMBER = 'number', '数字'

    template = models.ForeignKey(
        KidAssessmentTemplate, on_delete=models.CASCADE,
        related_name='questions', verbose_name='模板',
    )
    key = models.CharField('题目标识', max_length=64)
    type = models.CharField('题目类型', max_length=16, choices=QuestionType.choices)
    title = models.CharField('题目标题', max_length=255)
    options = models.JSONField('选项', default=list)
    step = models.IntegerField('步骤')
    sort = models.IntegerField('排序', default=0)
    score_rules = models.JSONField('评分规则', default=dict)

    class Meta:
        db_table = 'kid_assessment_question'
        verbose_name = '测评题目'
        verbose_name_plural = verbose_name
        unique_together = [('template', 'key')]

    def __str__(self):
        return f'{self.title} ({self.key})'


class KidAssessmentSubmission(models.Model):
    """测评提交"""

    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='assessment_submissions', verbose_name='用户',
    )
    template = models.ForeignKey(
        KidAssessmentTemplate, on_delete=models.CASCADE,
        related_name='submissions', verbose_name='模板',
    )
    score_total = models.IntegerField('总分', null=True, blank=True)
    result_title = models.CharField('结果标题', max_length=255, blank=True, null=True)
    result_copy = models.TextField('结果文案', blank=True, null=True)
    action_list = models.JSONField('行动建议', default=list)
    matched_policy_ids = models.JSONField('匹配政策ID列表', default=list)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'kid_assessment_submission'
        verbose_name = '测评提交'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Submission({self.business_id})'

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('asm')
        super().save(*args, **kwargs)


class KidAssessmentAnswer(models.Model):
    """测评答案"""

    submission = models.ForeignKey(
        KidAssessmentSubmission, on_delete=models.CASCADE,
        related_name='answers', verbose_name='提交记录',
    )
    question = models.ForeignKey(
        KidAssessmentQuestion, on_delete=models.CASCADE,
        related_name='answers', verbose_name='题目',
    )
    answer_text = models.TextField('文本答案', blank=True, null=True)
    answer_options = models.JSONField('选项答案', default=list)

    class Meta:
        db_table = 'kid_assessment_answer'
        verbose_name = '测评答案'
        verbose_name_plural = verbose_name
        unique_together = [('submission', 'question')]

    def __str__(self):
        return f'Answer({self.submission_id}, {self.question_id})'


class KidAssessmentScoreItem(models.Model):
    """测评得分项"""

    submission = models.ForeignKey(
        KidAssessmentSubmission, on_delete=models.CASCADE,
        related_name='score_items', verbose_name='提交记录',
    )
    key = models.CharField('得分项标识', max_length=64)
    name = models.CharField('得分项名称', max_length=64)
    score = models.IntegerField('得分')

    class Meta:
        db_table = 'kid_assessment_score_item'
        verbose_name = '测评得分项'
        verbose_name_plural = verbose_name
        unique_together = [('submission', 'key')]

    def __str__(self):
        return f'{self.name}: {self.score}'


class KidChildProfile(models.Model):
    """宝宝档案"""

    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='child_profile', verbose_name='用户',
    )
    latest_submission = models.ForeignKey(
        KidAssessmentSubmission, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='child_profiles', verbose_name='最新测评',
    )
    has_done_assessment = models.BooleanField('是否已完成测评', default=False)
    grade_group = models.CharField('年级组', max_length=16, blank=True, null=True)
    grade_option = models.CharField('年级选项', max_length=16, blank=True, null=True)
    english_level = models.CharField('英语水平', max_length=4, blank=True, null=True)
    core_insight = models.JSONField('核心洞察', default=list)
    recommended_plan = models.CharField('推荐方案', max_length=16, blank=True, null=True)
    answers_snapshot = models.JSONField('答案快照', default=dict)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'kid_child_profile'
        verbose_name = '宝宝档案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'ChildProfile({self.business_id})'

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('cp')
        super().save(*args, **kwargs)
