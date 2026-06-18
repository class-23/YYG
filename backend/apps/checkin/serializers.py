"""
打卡与课程序列化器
"""
from rest_framework import serializers

from .models import DailyLesson, Checkin, SubTask, CheckinSubTask, AudioPlayLog, ReflectionQuestion


class DailyLessonSerializer(serializers.ModelSerializer):
    """每日课程序列化器"""

    class Meta:
        model = DailyLesson
        fields = (
            'id', 'day', 'theme', 'task', 'cover_image',
            'audio_src', 'audio_title', 'audio_subtitle', 'audio_duration',
            'quote', 'meaning', 'copy',
            'pronunciation', 'speaking_examples', 'definition_notes',
            'takeaways', 'translation_practice', 'encouragement',
            'version', 'is_published',
        )


class CheckinCreateSerializer(serializers.Serializer):
    """创建打卡请求"""
    lesson_id = serializers.IntegerField(required=False, allow_null=True)
    reflection = serializers.CharField(required=False, allow_blank=True, max_length=2000)
    audio_played_seconds = serializers.IntegerField(required=False, default=0, min_value=0)
    client_meta = serializers.JSONField(required=False, default=dict)
    sub_tasks = serializers.ListField(
        child=serializers.DictField(),
        required=False, default=list,
        help_text='[{sub_task_id, completed, note}]'
    )


class CheckinSubTaskSerializer(serializers.ModelSerializer):
    sub_task_title = serializers.CharField(source='sub_task.title', read_only=True)

    class Meta:
        model = CheckinSubTask
        fields = ('id', 'sub_task', 'sub_task_title', 'completed', 'completed_at', 'note')


class CheckinSerializer(serializers.ModelSerializer):
    """打卡记录序列化器"""
    sub_tasks = CheckinSubTaskSerializer(many=True, read_only=True)
    lesson_day = serializers.IntegerField(source='lesson.day', read_only=True, default=None)

    class Meta:
        model = Checkin
        fields = (
            'id', 'user', 'lesson', 'lesson_day', 'biz_date',
            'main_checkin_completed', 'completed_at', 'reflection',
            'audio_played_seconds', 'cashback_earned', 'is_missed',
            'client_meta', 'sub_tasks', 'created_at',
        )
        read_only_fields = fields


class AudioPlayLogCreateSerializer(serializers.Serializer):
    play_seconds = serializers.IntegerField(min_value=0, max_value=3600)
    client_meta = serializers.JSONField(required=False, default=dict)


class ReflectionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReflectionQuestion
        fields = ('id', 'category', 'question', 'is_active')


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            'id', 'business_id', 'source', 'source_policy_id', 'title', 'category',
            'description', 'frequency', 'estimated_time', 'grade_range',
            'ability_tags', 'is_template', 'extra',
        )
