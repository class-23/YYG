"""
打卡与课程核心域模型
"""
import logging

from django.conf import settings
from django.db import models

from common.utils import generate_business_id, today_cst

logger = logging.getLogger('apps.checkin')


# ============================================================
# 枚举
# ============================================================

class SubTaskSource(models.TextChoices):
    DAILY = 'daily', '每日任务'
    POLICY_IMPACT = 'policy_impact', '政策影响'


class ReflectionCategory(models.TextChoices):
    DAILY = 'daily', '每日'
    WEEKLY = 'weekly', '每周'
    MILESTONE = 'milestone', '里程碑'


# ============================================================
# 每日课程
# ============================================================

class DailyLesson(models.Model):
    """每日英语早操课程（一年365天）"""
    id = models.BigAutoField(primary_key=True)
    day = models.IntegerField('第N天', unique=True, db_index=True, help_text='1-365')
    theme = models.CharField('主题', max_length=255)
    task = models.CharField('当日任务', max_length=500)
    cover_image = models.CharField('封面图', max_length=512, null=True, blank=True)
    audio_src = models.CharField('音频URL', max_length=512, null=True, blank=True)
    audio_title = models.CharField('音频标题', max_length=255, null=True, blank=True)
    audio_subtitle = models.CharField('音频副标题', max_length=255, null=True, blank=True)
    audio_duration = models.CharField('音频时长', max_length=16, null=True, blank=True)
    quote = models.CharField('金句', max_length=255)
    meaning = models.CharField('金句释义', max_length=500, null=True, blank=True)
    copy = models.TextField('当日文案')
    pronunciation = models.JSONField('发音拆解', default=list, blank=True)
    speaking_examples = models.JSONField('口语例句', default=list, blank=True)
    definition_notes = models.JSONField('表达理解', default=list, blank=True)
    takeaways = models.JSONField('短语提炼', default=list, blank=True)
    translation_practice = models.JSONField('翻译练习', default=list, blank=True)
    encouragement = models.CharField('鼓励语', max_length=500, null=True, blank=True)
    version = models.IntegerField('课程版本', default=1)
    is_published = models.BooleanField('已发布', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'checkin_daily_lesson'
        verbose_name = '每日课程'
        verbose_name_plural = verbose_name
        ordering = ['day']
        indexes = [
            models.Index(fields=['is_published'], name='idx_daily_lesson_published',
                         condition=models.Q(is_published=True)),
        ]

    def __str__(self):
        return f'Day {self.day}: {self.theme}'


# ============================================================
# 打卡主表
# ============================================================

class Checkin(models.Model):
    """打卡主表 - 一条记录 = 一个用户 + 一个自然日"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='checkins', verbose_name='用户',
    )
    lesson = models.ForeignKey(
        DailyLesson, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='checkins', verbose_name='关联课程',
    )
    biz_date = models.DateField('自然日', db_index=True)
    main_checkin_completed = models.BooleanField('主打卡完成', default=False)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    reflection = models.TextField('反思内容', null=True, blank=True)
    audio_played_seconds = models.IntegerField('音频播放秒数', default=0)
    cashback_earned = models.BigIntegerField('当日返现（分）', default=0)
    is_missed = models.BooleanField('是否漏打卡', default=False)
    client_meta = models.JSONField('客户端元信息', default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'checkin_checkin'
        verbose_name = '打卡记录'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'biz_date'),)
        indexes = [
            models.Index(fields=['user', '-completed_at'], name='idx_checkin_user_completed_at'),
            models.Index(fields=['-biz_date'], name='idx_checkin_biz_date'),
        ]

    def __str__(self):
        return f'{self.user_id} - {self.biz_date}'


# ============================================================
# 子任务
# ============================================================

class SubTask(models.Model):
    """子任务模板 - 每日扩展任务 + 政策影响任务"""
    id = models.BigAutoField(primary_key=True)
    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    source = models.CharField('来源', max_length=32, choices=SubTaskSource.choices, default=SubTaskSource.DAILY)
    source_policy_id = models.BigIntegerField('关联政策ID', null=True, blank=True)
    title = models.CharField('任务标题', max_length=255)
    category = models.CharField('分类', max_length=64, null=True, blank=True)
    description = models.TextField('任务描述', null=True, blank=True)
    frequency = models.CharField('频率', max_length=64, null=True, blank=True)
    estimated_time = models.CharField('预计耗时', max_length=32, null=True, blank=True)
    grade_range = models.JSONField('适用年级', default=list, blank=True)
    ability_tags = models.JSONField('能力标签', default=list, blank=True)
    is_template = models.BooleanField('是否模板', default=True)
    extra = models.JSONField('扩展字段', default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'checkin_sub_task'
        verbose_name = '子任务'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['source', 'source_policy_id'], name='idx_sub_task_source_policy'),
            models.Index(fields=['category'], name='idx_sub_task_category'),
        ]

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('stk')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CheckinSubTask(models.Model):
    """打卡-子任务关联"""
    id = models.BigAutoField(primary_key=True)
    checkin = models.ForeignKey(Checkin, on_delete=models.CASCADE, related_name='sub_tasks')
    sub_task = models.ForeignKey(SubTask, on_delete=models.CASCADE)
    completed = models.BooleanField('已完成', default=False)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    note = models.CharField('用户留言', max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'checkin_checkin_sub_task'
        verbose_name = '打卡子任务'
        verbose_name_plural = verbose_name
        unique_together = (('checkin', 'sub_task'),)

    def __str__(self):
        return f'{self.checkin_id} - {self.sub_task_id}'


# ============================================================
# 音频播放日志
# ============================================================

class AudioPlayLog(models.Model):
    """音频播放日志 - 风控与统计"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='audio_play_logs',
    )
    lesson = models.ForeignKey(DailyLesson, on_delete=models.CASCADE)
    biz_date = models.DateField('自然日')
    play_seconds = models.IntegerField('播放秒数')
    played_at = models.DateTimeField('播放时间', auto_now_add=True)
    client_meta = models.JSONField('客户端元信息', default=dict, blank=True)

    class Meta:
        db_table = 'checkin_audio_play_log'
        verbose_name = '音频播放日志'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user', 'biz_date'], name='idx_audio_play_user_date'),
        ]


# ============================================================
# 反思问题库
# ============================================================

class ReflectionQuestion(models.Model):
    """反思问题库"""
    id = models.BigAutoField(primary_key=True)
    category = models.CharField('分类', max_length=32, choices=ReflectionCategory.choices, default=ReflectionCategory.DAILY)
    question = models.CharField('问题', max_length=500)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'checkin_reflection_question'
        verbose_name = '反思问题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question
