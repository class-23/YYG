"""kid_assessment admin - 孩子成长评估"""
from django.contrib import admin

from .models import (
    KidAssessmentTemplate, KidAssessmentQuestion, KidAssessmentSubmission,
    KidAssessmentAnswer, KidAssessmentScoreItem, KidChildProfile,
)


@admin.register(KidAssessmentTemplate)
class KidAssessmentTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'version', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('code', 'name')


@admin.register(KidAssessmentQuestion)
class KidAssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'key', 'type', 'title', 'step', 'sort')
    list_filter = ('template', 'type', 'step')
    search_fields = ('key', 'title')


@admin.register(KidAssessmentSubmission)
class KidAssessmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'user', 'template', 'score_total', 'result_title', 'created_at')
    list_filter = ('template',)
    search_fields = ('business_id', 'user__nickname', 'result_title')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'template')


@admin.register(KidAssessmentAnswer)
class KidAssessmentAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'question')
    raw_id_fields = ('submission', 'question')


@admin.register(KidAssessmentScoreItem)
class KidAssessmentScoreItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'key', 'name', 'score')
    list_filter = ('key',)
    search_fields = ('name', 'key')
    raw_id_fields = ('submission',)


@admin.register(KidChildProfile)
class KidChildProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'user', 'grade_group', 'grade_option', 'english_level',
                    'recommended_plan', 'has_done_assessment', 'updated_at')
    list_filter = ('grade_group', 'grade_option', 'english_level', 'recommended_plan', 'has_done_assessment')
    search_fields = ('business_id', 'user__nickname')
    raw_id_fields = ('user', 'latest_submission')
