"""
宝宝测评序列化器
"""
from rest_framework import serializers

from .models import (
    KidAssessmentTemplate, KidAssessmentQuestion,
    KidAssessmentSubmission, KidAssessmentAnswer,
    KidAssessmentScoreItem, KidChildProfile,
)


class KidAssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KidAssessmentQuestion
        fields = [
            'id', 'key', 'type', 'title', 'options',
            'step', 'sort', 'score_rules',
        ]


class KidAssessmentTemplateSerializer(serializers.ModelSerializer):
    questions = KidAssessmentQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = KidAssessmentTemplate
        fields = ['id', 'code', 'name', 'version', 'is_active', 'created_at', 'questions']


class AnswerItemSerializer(serializers.Serializer):
    question_key = serializers.CharField(max_length=64)
    answer_text = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    answer_options = serializers.ListField(
        child=serializers.CharField(), required=False,
    )


class SubmissionCreateSerializer(serializers.Serializer):
    template_code = serializers.CharField(max_length=32)
    answers = AnswerItemSerializer(many=True)


class KidAssessmentScoreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = KidAssessmentScoreItem
        fields = ['id', 'key', 'name', 'score']


class KidAssessmentSubmissionSerializer(serializers.ModelSerializer):
    score_items = KidAssessmentScoreItemSerializer(many=True, read_only=True)

    class Meta:
        model = KidAssessmentSubmission
        fields = [
            'id', 'business_id', 'user', 'template',
            'score_total', 'result_title', 'result_copy',
            'action_list', 'matched_policy_ids', 'created_at',
            'score_items',
        ]
        read_only_fields = ['id', 'business_id', 'user', 'created_at']


class KidChildProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = KidChildProfile
        fields = [
            'id', 'business_id', 'user', 'latest_submission',
            'has_done_assessment', 'grade_group', 'grade_option',
            'english_level', 'core_insight', 'recommended_plan',
            'answers_snapshot', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'business_id', 'user', 'latest_submission',
            'has_done_assessment', 'created_at', 'updated_at',
        ]
