"""checkin admin - 打卡与课程管理后台"""
from django.contrib import admin

from .models import DailyLesson, Checkin, SubTask, CheckinSubTask, AudioPlayLog, ReflectionQuestion


@admin.register(DailyLesson)
class DailyLessonAdmin(admin.ModelAdmin):
    list_display = ('day', 'theme', 'audio_title', 'version', 'is_published', 'updated_at')
    list_filter = ('is_published', 'version')
    search_fields = ('day', 'theme', 'task', 'quote')
    ordering = ('day',)
    list_per_page = 30


@admin.register(Checkin)
class CheckinAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'biz_date', 'main_checkin_completed', 'cashback_earned', 'is_missed', 'completed_at')
    list_filter = ('main_checkin_completed', 'is_missed', 'biz_date')
    search_fields = ('user__nickname', 'user__business_id')
    date_hierarchy = 'biz_date'
    list_per_page = 50
    raw_id_fields = ('user', 'lesson')


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'source', 'title', 'category', 'frequency', 'is_template')
    list_filter = ('source', 'is_template', 'category')
    search_fields = ('business_id', 'title', 'description')


@admin.register(CheckinSubTask)
class CheckinSubTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'checkin', 'sub_task', 'completed', 'completed_at')
    list_filter = ('completed',)
    raw_id_fields = ('checkin', 'sub_task')


@admin.register(AudioPlayLog)
class AudioPlayLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lesson', 'biz_date', 'play_seconds', 'played_at')
    list_filter = ('biz_date',)
    date_hierarchy = 'played_at'
    raw_id_fields = ('user', 'lesson')


@admin.register(ReflectionQuestion)
class ReflectionQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'question', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('question',)
