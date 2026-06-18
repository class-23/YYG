"""finance admin - 计划与返现管理后台"""
from django.contrib import admin

from .models import Plan, UserPlan, CashbackAccount, CashbackRecord


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'price_cents', 'duration_days', 'cashback_per_day', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'name', 'description')


@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan', 'status', 'started_at', 'expires_at', 'cancelled_at')
    list_filter = ('status', 'plan')
    search_fields = ('user__nickname', 'user__business_id')
    date_hierarchy = 'started_at'
    raw_id_fields = ('user',)


@admin.register(CashbackAccount)
class CashbackAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance_cents', 'total_earned_cents', 'expected_cashback_cents', 'version', 'updated_at')
    search_fields = ('user__nickname', 'user__business_id')
    raw_id_fields = ('user',)
    readonly_fields = ('version', 'created_at', 'updated_at')


@admin.register(CashbackRecord)
class CashbackRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'user', 'amount_cents', 'type', 'source', 'biz_date', 'created_at')
    list_filter = ('type', 'source', 'biz_date')
    search_fields = ('business_id', 'user__nickname', 'ref_id', 'description')
    date_hierarchy = 'biz_date'
    raw_id_fields = ('user',)
