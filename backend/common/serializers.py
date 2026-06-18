"""
公共序列化器
"""
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

User = get_user_model()


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    """自定义 JWT token 获取序列化器"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 在 token 中添加自定义声明
        token['nickname'] = user.nickname
        token['role'] = user.role
        return token


class WechatLoginSerializer(serializers.Serializer):
    """微信登录序列化器"""
    code = serializers.CharField(required=True, help_text='微信登录 code')
    nickname = serializers.CharField(required=False, default='', help_text='用户昵称')
    avatar_url = serializers.CharField(required=False, default='', help_text='头像URL')

    def validate_code(self, value):
        if not value or len(value) < 10:
            raise serializers.ValidationError('无效的微信登录code')
        return value
