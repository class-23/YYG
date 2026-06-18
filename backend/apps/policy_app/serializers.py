"""
政策CMS序列化器
"""
from rest_framework import serializers

from .models import (
    Policy, PolicyVersion, PolicyReview, PolicyTag,
    PolicyTagRelation, PolicyTask, PolicyWeeklyTask,
)


class PolicyTagSerializer(serializers.ModelSerializer):
    """政策标签序列化器"""
    class Meta:
        model = PolicyTag
        fields = [
            'id', 'business_id', 'type', 'name', 'value',
            'enabled', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'business_id', 'created_at', 'updated_at']


class PolicyTaskSerializer(serializers.ModelSerializer):
    """政策任务序列化器"""
    class Meta:
        model = PolicyTask
        fields = [
            'id', 'business_id', 'title', 'category', 'description',
            'frequency', 'estimated_time', 'grade_range', 'ability_tags',
            'created_at',
        ]
        read_only_fields = ['id', 'business_id', 'created_at']


class PolicyWeeklyTaskSerializer(serializers.ModelSerializer):
    """政策每周任务序列化器"""
    class Meta:
        model = PolicyWeeklyTask
        fields = [
            'id', 'title', 'category', 'description',
            'frequency', 'estimated_time', 'grade_range', 'ability_tags',
            'sort', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PolicyVersionSerializer(serializers.ModelSerializer):
    """政策版本序列化器"""
    class Meta:
        model = PolicyVersion
        fields = [
            'id', 'policy', 'version', 'snapshot', 'change_summary',
            'editor', 'published_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PolicyReviewSerializer(serializers.ModelSerializer):
    """政策审核记录序列化器"""
    class Meta:
        model = PolicyReview
        fields = [
            'id', 'business_id', 'policy', 'version', 'reviewer',
            'action', 'comment', 'created_at',
        ]
        read_only_fields = ['id', 'business_id', 'created_at']


class PolicyListSerializer(serializers.ModelSerializer):
    """政策列表序列化器（公开接口）"""
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Policy
        fields = [
            'id', 'business_id', 'title', 'source_name',
            'policy_summary', 'effective_date', 'region', 'stage',
            'grade_range', 'domains', 'front_display_title',
            'front_display_summary', 'content_status', 'version',
            'published_at', 'tags', 'created_at',
        ]

    def get_tags(self, obj):
        relations = PolicyTagRelation.objects.filter(policy=obj).select_related('tag')
        return PolicyTagSerializer([r.tag for r in relations], many=True).data


class PolicyDetailSerializer(serializers.ModelSerializer):
    """政策详情序列化器（含任务/每周任务/标签）"""
    tasks = PolicyTaskSerializer(many=True, read_only=True)
    weekly_tasks = PolicyWeeklyTaskSerializer(many=True, read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Policy
        fields = [
            'id', 'business_id', 'title', 'source_name', 'source_url',
            'policy_summary', 'effective_date', 'region', 'stage',
            'grade_range', 'domains', 'influence_abilities',
            'parent_action_suggestions', 'front_display_title',
            'front_display_summary', 'impact_explanation',
            'monthly_suggestions', 'weekly_task_suggestions',
            'focus_directions', 'child_impact_analysis',
            'content_status', 'version', 'created_by', 'reviewed_by',
            'review_comment', 'published_at', 'published_at_system',
            'tasks', 'weekly_tasks', 'tags', 'created_at', 'updated_at',
        ]

    def get_tags(self, obj):
        relations = PolicyTagRelation.objects.filter(policy=obj).select_related('tag')
        return PolicyTagSerializer([r.tag for r in relations], many=True).data


class PolicyCreateUpdateSerializer(serializers.ModelSerializer):
    """政策创建/更新序列化器"""
    tasks = PolicyTaskSerializer(many=True, required=False)
    weekly_tasks = PolicyWeeklyTaskSerializer(many=True, required=False)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True,
    )

    class Meta:
        model = Policy
        fields = [
            'title', 'source_name', 'source_url', 'policy_summary',
            'effective_date', 'region', 'stage', 'grade_range', 'domains',
            'influence_abilities', 'parent_action_suggestions',
            'front_display_title', 'front_display_summary',
            'impact_explanation', 'monthly_suggestions',
            'weekly_task_suggestions', 'focus_directions',
            'child_impact_analysis', 'content_status', 'created_by',
            'tasks', 'weekly_tasks', 'tag_ids',
        ]

    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks', [])
        weekly_tasks_data = validated_data.pop('weekly_tasks', [])
        tag_ids = validated_data.pop('tag_ids', [])

        policy = Policy.objects.create(**validated_data)

        for task_data in tasks_data:
            PolicyTask.objects.create(policy=policy, **task_data)

        for weekly_data in weekly_tasks_data:
            PolicyWeeklyTask.objects.create(policy=policy, **weekly_data)

        for tag_id in tag_ids:
            try:
                tag = PolicyTag.objects.get(id=tag_id)
                PolicyTagRelation.objects.create(policy=policy, tag=tag)
            except PolicyTag.DoesNotExist:
                pass

        return policy

    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('tasks', None)
        weekly_tasks_data = validated_data.pop('weekly_tasks', None)
        tag_ids = validated_data.pop('tag_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tasks_data is not None:
            instance.tasks.all().delete()
            for task_data in tasks_data:
                PolicyTask.objects.create(policy=instance, **task_data)

        if weekly_tasks_data is not None:
            instance.weekly_tasks.all().delete()
            for weekly_data in weekly_tasks_data:
                PolicyWeeklyTask.objects.create(policy=instance, **weekly_data)

        if tag_ids is not None:
            PolicyTagRelation.objects.filter(policy=instance).delete()
            for tag_id in tag_ids:
                try:
                    tag = PolicyTag.objects.get(id=tag_id)
                    PolicyTagRelation.objects.create(policy=instance, tag=tag)
                except PolicyTag.DoesNotExist:
                    pass

        return instance
