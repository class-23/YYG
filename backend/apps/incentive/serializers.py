"""
激励系统序列化器
"""
from rest_framework import serializers

from .models import Badge, UserBadge, Course, CourseExchange, CourseInquiry


class BadgeSerializer(serializers.ModelSerializer):
    unlocked = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = (
            'id', 'business_id', 'name', 'description', 'required_days',
            'level', 'icon', 'is_active', 'unlocked',
        )

    def get_unlocked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return UserBadge.objects.filter(user=request.user, badge=obj).exists()


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ('id', 'badge', 'unlocked_at', 'context')


class CourseSerializer(serializers.ModelSerializer):
    value_yuan = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id', 'business_id', 'title', 'cover', 'description', 'tags',
            'value_cents', 'value_yuan', 'required_cashback_days',
            'redeem_limit_per_user', 'is_active',
        )

    def get_value_yuan(self, obj):
        return f"{obj.value_cents / 100:.2f}"


class CourseInquiryCreateSerializer(serializers.Serializer):
    """课程咨询请求"""
    phone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    wechat = serializers.CharField(required=False, allow_blank=True, max_length=128)
    note = serializers.CharField(required=False, allow_blank=True, max_length=200)


class CourseInquirySerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseInquiry
        fields = (
            'id', 'business_id', 'user', 'course', 'course_title', 'from_page',
            'phone_masked', 'wechat', 'note', 'status', 'follow_up_channel',
            'contacted_at', 'closed_at', 'created_at',
        )
        read_only_fields = fields
