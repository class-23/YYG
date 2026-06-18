from django.contrib import admin

from .models import User, UserProfile, UserAuth, PushToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'business_id', 'nickname', 'openid', 'phone_masked', 'role', 'is_disabled', 'created_at']
    list_filter = ['role', 'is_disabled', 'gender']
    search_fields = ['business_id', 'nickname', 'openid', 'phone_masked']
    readonly_fields = ['business_id', 'openid', 'created_at', 'updated_at']
    list_per_page = 20


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'baby_stage', 'plan_status', 'checked_days', 'consecutive_days', 'updated_at']
    list_filter = ['baby_stage', 'plan_status']
    search_fields = ['user__nickname', 'user__business_id']
    readonly_fields = ['updated_at']
    list_per_page = 20


@admin.register(UserAuth)
class UserAuthAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'last_login_ip', 'failed_login_count', 'locked_until', 'updated_at']
    search_fields = ['user__nickname', 'user__business_id']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20


@admin.register(PushToken)
class PushTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'provider', 'device_id', 'is_active', 'last_active_at', 'created_at']
    list_filter = ['provider', 'is_active']
    search_fields = ['user__nickname', 'user__business_id', 'device_id']
    readonly_fields = ['created_at']
    list_per_page = 20
