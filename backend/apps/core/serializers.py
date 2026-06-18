"""
核心用户序列化器
"""
from rest_framework import serializers

from .models import User, UserProfile, PushToken


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""

    class Meta:
        model = UserProfile
        fields = [
            'id', 'baby_stage', 'region', 'city', 'bio', 'tags',
            'plan_status', 'plan_started_at', 'plan_expires_at',
            'trial21_unlocked', 'invite_progress',
            'checked_days', 'missed_days', 'consecutive_days', 'longest_streak',
            'course_unlocked', 'course_total',
        ]
        read_only_fields = [
            'id', 'plan_status', 'plan_started_at', 'plan_expires_at',
            'trial21_unlocked', 'invite_progress',
            'checked_days', 'missed_days', 'consecutive_days', 'longest_streak',
            'course_unlocked', 'course_total',
        ]


class UserSerializer(serializers.ModelSerializer):
    """用户基本信息序列化器（包含profile嵌套）"""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'business_id', 'openid', 'nickname', 'avatar_url',
            'phone_masked', 'gender', 'role', 'is_admin', 'is_disabled',
            'last_login_at', 'created_at', 'profile',
        ]
        read_only_fields = [
            'id', 'business_id', 'openid', 'role', 'is_admin', 'is_disabled',
            'last_login_at', 'created_at',
        ]


class WechatLoginSerializer(serializers.Serializer):
    """微信登录请求"""
    code = serializers.CharField(required=True, help_text='微信登录code')
    nickname = serializers.CharField(required=False, default='', help_text='用户昵称')
    avatar_url = serializers.CharField(required=False, default='', help_text='头像URL')

    def validate_code(self, value):
        if not value or len(value) < 10:
            raise serializers.ValidationError('无效的微信登录code')
        return value


class UpdateProfileSerializer(serializers.ModelSerializer):
    """更新用户资料"""
    nickname = serializers.CharField(
        source='user.nickname', required=False, max_length=64,
    )
    avatar_url = serializers.CharField(
        source='user.avatar_url', required=False, max_length=512,
    )
    gender = serializers.IntegerField(
        source='user.gender', required=False,
    )

    class Meta:
        model = UserProfile
        fields = [
            'nickname', 'avatar_url', 'gender',
            'baby_stage', 'region', 'city', 'bio', 'tags',
        ]

    def update(self, instance, validated_data):
        # 分离 user 和 profile 字段
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save(update_fields=list(user_data.keys()))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(update_fields=list(validated_data.keys()))
        return instance


class PushTokenSerializer(serializers.ModelSerializer):
    """注册推送Token"""

    class Meta:
        model = PushToken
        fields = ['provider', 'token', 'device_id']
