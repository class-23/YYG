"""
邀请系统序列化器
"""
from rest_framework import serializers

from .models import InviteCode, InviteRecord


class InviteCodeSerializer(serializers.ModelSerializer):
    """邀请码序列化器"""
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = InviteCode
        fields = [
            'id', 'code', 'owner_user', 'type', 'ref_id',
            'use_limit', 'used_count', 'expires_at', 'is_active',
            'is_valid', 'created_at',
        ]
        read_only_fields = ['id', 'code', 'used_count', 'created_at']


class InviteCodeCreateSerializer(serializers.Serializer):
    """邀请码创建序列化器"""
    type = serializers.ChoiceField(
        choices=InviteCode.type.field.choices,
        default='general',
    )
    ref_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    use_limit = serializers.IntegerField(required=False, default=0, min_value=0)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)


class InviteApplySerializer(serializers.Serializer):
    """使用邀请码序列化器"""
    code = serializers.CharField(required=True, max_length=16)


class InviteRecordSerializer(serializers.ModelSerializer):
    """邀请记录序列化器"""
    inviter_nickname = serializers.CharField(source='inviter_user.nickname', read_only=True)
    invitee_nickname = serializers.CharField(source='invitee_user.nickname', read_only=True, default=None)

    class Meta:
        model = InviteRecord
        fields = [
            'id', 'invite_code', 'inviter_user', 'inviter_nickname',
            'invitee_user', 'invitee_nickname', 'status',
            'first_checkin_at', 'confirmed_at', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
