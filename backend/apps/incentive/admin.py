"""incentive admin - 徽章/课程/兑换/咨询管理"""
from django.contrib import admin

from .models import Badge, UserBadge, Course, CourseExchange, CourseInquiry


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'name', 'level', 'required_days', 'is_active')
    list_filter = ('level', 'is_active')
    search_fields = ('business_id', 'name', 'description')
    ordering = ('level', 'required_days')


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'badge', 'unlocked_at')
    list_filter = ('badge',)
    search_fields = ('user__nickname', 'user__business_id', 'badge__name')
    date_hierarchy = 'unlocked_at'
    raw_id_fields = ('user', 'badge')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'title', 'value_cents', 'required_cashback_days', 'redeem_limit_per_user', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('business_id', 'title', 'description')
    filter_horizontal = ()
    readonly_fields = ('business_id',)


@admin.register(CourseExchange)
class CourseExchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'user', 'course', 'status', 'redeemed_at')
    list_filter = ('status',)
    search_fields = ('business_id', 'user__nickname', 'course__title')
    date_hierarchy = 'redeemed_at'
    raw_id_fields = ('user', 'course')


@admin.register(CourseInquiry)
class CourseInquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_id', 'user', 'course', 'phone_masked', 'status', 'operator_id', 'created_at')
    list_filter = ('status', 'follow_up_channel', 'from_page')
    search_fields = ('business_id', 'phone_masked', 'phone_hash', 'wechat', 'note', 'user__nickname')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'course')
    readonly_fields = ('phone_hash', 'business_id', 'created_at', 'updated_at')
