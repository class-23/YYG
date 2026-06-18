"""
消息系统视图
"""
import logging

from rest_framework import generics, permissions
from rest_framework.views import APIView

from common.response import success, not_found
from common.utils import now_cst

from .models import Message, MessageReceipt
from .serializers import MessageSerializer

logger = logging.getLogger('apps.message')


class MessageListView(generics.ListAPIView):
    """GET /v1/messages/ - 消息列表"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageReadView(APIView):
    """POST /v1/messages/{id}/read/ - 标记消息已读"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            message = Message.objects.get(pk=pk, user=request.user)
        except Message.DoesNotExist:
            return not_found('消息不存在')

        receipt, created = MessageReceipt.objects.get_or_create(
            message=message, user=request.user,
            defaults={'is_read': True, 'read_at': now_cst()},
        )
        if not created and not receipt.is_read:
            receipt.is_read = True
            receipt.read_at = now_cst()
            receipt.save(update_fields=['is_read', 'read_at'])

        return success(message='消息已标记为已读')


class MessageUnreadCountView(APIView):
    """GET /v1/messages/unread-count/ - 未读消息数"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 获取用户的所有消息
        message_ids = Message.objects.filter(
            user=request.user,
        ).values_list('id', flat=True)

        # 统计未读数（没有回执或回执 is_read=False）
        read_ids = MessageReceipt.objects.filter(
            user=request.user, is_read=True,
        ).values_list('message_id', flat=True)

        unread_count = len(set(message_ids) - set(read_ids))

        return success(data={'unread_count': unread_count})
