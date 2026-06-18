"""mom_growth admin - 妈妈成长管理"""
from django.contrib import admin

from .models import MilestoneDefinition, UserMilestone, OfflineActivity, OfflineActivitySignup


@admin.register(MilestoneDefinition)
class MilestoneDefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'month', 'label', 'badge_level', 'required_days', 'is_active')
    list_filter = ('is_active', 'badge_level')
    search_fields = ('label', 'copy')
    ordering = ('month',)


@admin.register(UserMilestone)
class UserMilestoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'milestone', 'unlocked_at')
    date_hierarchy = 'unlocked_at'
    raw_id_fields = ('user', 'milestone')


@admin.register(OfflineActivity)
class OfflineActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'city', 'start_at', 'end_at', 'max_seats', 'taken_seats', 'status')
    list_filter = ('status', 'city')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_at'


@admin.register(OfflineActivitySignup)
class OfflineActivitySignupAdmin(admin.ModelAdmin):
    list_display = ('id', 'activity', 'user', 'status', 'created_at')
    list_filter = ('status',)
    date_hierarchy = 'created_at'
    raw_id_fields = ('activity', 'user')
