"""
邀请系统视图
"""
import logging

from rest_framework import generics, permissions
from rest_framework.views import APIView

from common.response import success, created, fail, bad_request
from common.utils import generate_invite_code, now_cst

from .models import InviteCode, InviteRecord, InviteStatus
from .serializers import (
    InviteCodeSerializer, InviteCodeCreateSerializer,
    InviteApplySerializer, InviteRecordSerializer,
)

logger = logging.getLogger('apps.invite')


class InviteCodeCreateView(APIView):
    """POST /v1/invite/codes/ - 生成邀请码"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = InviteCodeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        code = generate_invite_code()
        invite_code = InviteCode.objects.create(
            code=code,
            owner_user=request.user,
            type=data.get('type', 'general'),
            ref_id=data.get('ref_id'),
            use_limit=data.get('use_limit', 0),
            expires_at=data.get('expires_at'),
        )

        return created(
            data=InviteCodeSerializer(invite_code).data,
            message='邀请码创建成功',
        )


class InviteCodeListView(generics.ListAPIView):
    """GET /v1/invite/codes/ - 我的邀请码列表"""
    serializer_class = InviteCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InviteCode.objects.filter(owner_user=self.request.user)


class InviteApplyView(APIView):
    """POST /v1/invite/apply/ - 使用邀请码"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = InviteApplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        try:
            invite_code = InviteCode.objects.get(code=code)
        except InviteCode.DoesNotExist:
            return bad_request('邀请码不存在')

        if not invite_code.is_valid:
            return bad_request('邀请码已失效')

        # 检查是否是自己的邀请码
        if invite_code.owner_user and invite_code.owner_user.id == request.user.id:
            return bad_request('不能使用自己的邀请码')

        # 检查是否已经使用过该邀请码
        if InviteRecord.objects.filter(invite_code=invite_code, invitee_user=request.user).exists():
            return bad_request('您已使用过该邀请码')

        # 创建邀请记录
        record = InviteRecord.objects.create(
            invite_code=invite_code,
            inviter_user=invite_code.owner_user,
            invitee_user=request.user,
            status=InviteStatus.REGISTERED,
        )

        # 更新使用次数
        invite_code.used_count += 1
        invite_code.save(update_fields=['used_count'])

        logger.info(
            '邀请码使用: code=%s, inviter=%s, invitee=%s',
            code, invite_code.owner_user_id, request.user.id,
        )

        return created(
            data=InviteRecordSerializer(record).data,
            message='邀请码使用成功',
        )


class InviteRecordListView(generics.ListAPIView):
    """GET /v1/invite/records/ - 邀请记录列表"""
    serializer_class = InviteRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InviteRecord.objects.filter(inviter_user=self.request.user)
