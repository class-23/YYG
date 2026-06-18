"""
运营后台序列化器
"""
from rest_framework import serializers

from .models import AdminUser, AdminRoleDefinition, AdminPermission, AdminAuditLog, DataDictionaryEntry


class AdminUserSerializer(serializers.ModelSerializer):
    """后台账号序列化器"""

    class Meta:
        model = AdminUser
        fields = ('id', 'username', 'nickname', 'email', 'phone', 'role_code',
                  'is_active', 'last_login_at', 'created_at')
        read_only_fields = ('id', 'last_login_at', 'created_at')


class AdminLoginSerializer(serializers.Serializer):
    """后台登录"""
    username = serializers.CharField(required=True, max_length=64)
    password = serializers.CharField(required=True, max_length=128, write_only=True)


class AdminRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRoleDefinition
        fields = ('id', 'code', 'name', 'description', 'created_at')


class AdminPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPermission
        fields = ('id', 'code', 'name', 'module', 'created_at')


class AdminAuditLogSerializer(serializers.ModelSerializer):
    operator_username = serializers.CharField(source='operator.username', read_only=True)

    class Meta:
        model = AdminAuditLog
        fields = ('id', 'operator', 'operator_username', 'action', 'target_type', 'target_id',
                  'payload_before', 'payload_after', 'ip', 'user_agent', 'result',
                  'error_message', 'created_at')
        read_only_fields = fields


class DataDictionaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataDictionaryEntry
        fields = ('id', 'type', 'code', 'name', 'sort', 'extra', 'is_active',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
