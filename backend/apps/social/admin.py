"""social admin - 社交层管理"""
from django.contrib import admin

from .models import (
    SisterTeam, SisterTeamMember, SisterTeamActivity,
    SisterTeamInteraction, SisterTeamEncouragement, SisterTeamRemindLog,
    SquarePost, SquarePostImage, SquarePostLike, SquarePostComment,
    LoveProfile, LoveFollow,
)


@admin.register(SisterTeam)
class SisterTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'name', 'goal', 'invite_code', 'max_members', 'status', 'created_by', 'created_at')
    list_filter = ('goal', 'status')
    search_fields = ('business_id', 'name', 'invite_code')
    raw_id_fields = ('created_by',)


@admin.register(SisterTeamMember)
class SisterTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'user', 'role', 'is_active', 'joined_at', 'left_at')
    list_filter = ('role', 'is_active')
    search_fields = ('team__name', 'user__nickname')
    raw_id_fields = ('team', 'user')


@admin.register(SisterTeamActivity)
class SisterTeamActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'user', 'biz_date', 'type', 'hug_count', 'like_count', 'comment_count')
    list_filter = ('type',)
    date_hierarchy = 'biz_date'
    raw_id_fields = ('team', 'user')


@admin.register(SisterTeamInteraction)
class SisterTeamInteractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'activity', 'from_user', 'to_user', 'action', 'created_at')
    list_filter = ('action',)
    raw_id_fields = ('activity', 'from_user', 'to_user')


@admin.register(SisterTeamEncouragement)
class SisterTeamEncouragementAdmin(admin.ModelAdmin):
    list_display = ('id', 'activity', 'from_user', 'to_user', 'content', 'created_at')
    search_fields = ('content',)
    raw_id_fields = ('activity', 'from_user', 'to_user')


@admin.register(SisterTeamRemindLog)
class SisterTeamRemindLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'from_user', 'to_user', 'biz_date', 'channel', 'sent_at')
    list_filter = ('channel',)
    date_hierarchy = 'biz_date'
    raw_id_fields = ('team', 'from_user', 'to_user')


@admin.register(SquarePost)
class SquarePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'user', 'tag', 'audit_status', 'like_count', 'comment_count', 'is_anonymous', 'created_at')
    list_filter = ('audit_status', 'is_anonymous', 'tag')
    search_fields = ('business_id', 'text', 'user__nickname')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)


@admin.register(SquarePostImage)
class SquarePostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'url', 'sort')
    raw_id_fields = ('post',)


@admin.register(SquarePostLike)
class SquarePostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at')
    date_hierarchy = 'created_at'
    raw_id_fields = ('post', 'user')


@admin.register(SquarePostComment)
class SquarePostCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'parent', 'content', 'created_at')
    search_fields = ('content',)
    raw_id_fields = ('post', 'user', 'parent')


@admin.register(LoveProfile)
class LoveProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'baby_stage', 'is_unlocked', 'show_real_name', 'updated_at')
    list_filter = ('baby_stage', 'is_unlocked', 'show_real_name')
    search_fields = ('user__nickname', 'city', 'bio')
    raw_id_fields = ('user',)


@admin.register(LoveFollow)
class LoveFollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'created_at')
    date_hierarchy = 'created_at'
    raw_id_fields = ('from_user', 'to_user')
