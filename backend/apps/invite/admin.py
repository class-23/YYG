"""invite admin - 邀请管理"""
from django.contrib import admin

from .models import InviteCode, InviteRecord


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'type', 'owner_user', 'use_limit', 'used_count', 'is_active', 'expires_at', 'created_at')
    list_filter = ('type', 'is_active')
    search_fields = ('code', 'owner_user__nickname', 'ref_id')
    raw_id_fields = ('owner_user',)


@admin.register(InviteRecord)
class InviteRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'invite_code', 'inviter_user', 'invitee_user', 'status',
                    'first_checkin_at', 'confirmed_at', 'created_at')
    list_filter = ('status',)
    search_fields = ('invite_code__code', 'inviter_user__nickname', 'invitee_user__nickname')
    date_hierarchy = 'created_at'
    raw_id_fields = ('invite_code', 'inviter_user', 'invitee_user')
