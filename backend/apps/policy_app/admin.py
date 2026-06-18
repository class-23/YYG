"""policy_app admin - 政策 CMS 管理"""
from django.contrib import admin

from .models import (
    Policy, PolicyVersion, PolicyReview, PolicyTag, PolicyTagRelation,
    PolicyTask, PolicyWeeklyTask, PolicyAiGenerationLog,
)


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'title', 'region', 'stage', 'content_status', 'version', 'published_at')
    list_filter = ('content_status', 'region', 'stage')
    search_fields = ('business_id', 'title', 'policy_summary', 'source_name')
    date_hierarchy = 'effective_date'
    raw_id_fields = ()


@admin.register(PolicyVersion)
class PolicyVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'policy', 'version', 'editor', 'published_at', 'created_at')
    list_filter = ('editor',)
    search_fields = ('policy__title', 'change_summary', 'editor')
    date_hierarchy = 'created_at'
    raw_id_fields = ('policy',)


@admin.register(PolicyReview)
class PolicyReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'policy', 'version', 'action', 'reviewer', 'created_at')
    list_filter = ('action',)
    search_fields = ('business_id', 'comment', 'reviewer')
    date_hierarchy = 'created_at'
    raw_id_fields = ('policy',)


@admin.register(PolicyTag)
class PolicyTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'type', 'name', 'value', 'enabled')
    list_filter = ('type', 'enabled')
    search_fields = ('business_id', 'name', 'value')


@admin.register(PolicyTagRelation)
class PolicyTagRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'policy', 'tag', 'created_at')
    list_filter = ('tag__type',)
    raw_id_fields = ('policy', 'tag')


@admin.register(PolicyTask)
class PolicyTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'policy', 'title', 'category', 'frequency', 'estimated_time')
    list_filter = ('category',)
    search_fields = ('business_id', 'title', 'description')
    raw_id_fields = ('policy',)


@admin.register(PolicyWeeklyTask)
class PolicyWeeklyTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'policy', 'title', 'category', 'frequency', 'sort')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    raw_id_fields = ('policy',)


@admin.register(PolicyAiGenerationLog)
class PolicyAiGenerationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'source_text_length', 'tokens_input', 'tokens_output', 'latency_ms', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
