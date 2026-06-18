"""
消息系统序列化器
"""
from rest_framework import serializers

from .models import Message, MessageReceipt


class MessageSerializer(serializers.ModelSerializer):
    """消息序列化器"""
    is_read = serializers.SerializerMethodField()
    read_at = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 'business_id', 'type', 'title', 'content',
            'link', 'extra', 'is_read', 'read_at', 'created_at',
        ]

    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user:
            receipt = MessageReceipt.objects.filter(
                message=obj, user=request.user,
            ).first()
            return receipt.is_read if receipt else False
        return False

    def get_read_at(self, obj):
        request = self.context.get('request')
        if request and request.user:
            receipt = MessageReceipt.objects.filter(
                message=obj, user=request.user,
            ).first()
            return receipt.read_at if receipt else None
        return None
