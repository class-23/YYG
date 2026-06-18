"""
政策CMS视图
"""
import logging

from rest_framework import generics, permissions
from rest_framework.views import APIView

from common.response import success, created, fail, not_found, bad_request
from common.permissions import IsPolicyEditor, IsPolicyReviewer
from common.utils import now_cst

from .models import (
    Policy, PolicyVersion, PolicyReview, PolicyTag,
    PolicyTagRelation, ContentStatus, ReviewAction,
)
from .serializers import (
    PolicyListSerializer, PolicyDetailSerializer,
    PolicyCreateUpdateSerializer, PolicyVersionSerializer,
    PolicyReviewSerializer, PolicyTagSerializer,
)

logger = logging.getLogger('apps.policy_app')


# ============================================================
# 公开接口（小程序端）
# ============================================================

class PolicyListView(generics.ListAPIView):
    """GET /v1/policies/ - 已发布政策列表（公开）"""
    serializer_class = PolicyListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Policy.objects.filter(content_status=ContentStatus.PUBLISHED)
        region = self.request.query_params.get('region')
        stage = self.request.query_params.get('stage')
        if region:
            queryset = queryset.filter(region=region)
        if stage:
            queryset = queryset.filter(stage=stage)
        return queryset


class PolicyDetailView(generics.RetrieveAPIView):
    """GET /v1/policies/{id}/ - 政策详情（公开）"""
    serializer_class = PolicyDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'business_id'

    def get_queryset(self):
        return Policy.objects.filter(content_status=ContentStatus.PUBLISHED)


# ============================================================
# 管理后台接口
# ============================================================

class PolicyAdminListView(generics.ListAPIView):
    """GET /v1/admin-api/policies/ - 管理后台政策列表"""
    serializer_class = PolicyListSerializer
    permission_classes = [permissions.IsAuthenticated, IsPolicyEditor]

    def get_queryset(self):
        queryset = Policy.objects.all()
        status_filter = self.request.query_params.get('status')
        region = self.request.query_params.get('region')
        keyword = self.request.query_params.get('keyword')
        if status_filter:
            queryset = queryset.filter(content_status=status_filter)
        if region:
            queryset = queryset.filter(region=region)
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        return queryset


class PolicyAdminCreateView(generics.CreateAPIView):
    """POST /v1/admin-api/policies/ - 创建政策"""
    serializer_class = PolicyCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsPolicyEditor]

    def perform_create(self, serializer):
        policy = serializer.save(created_by=str(self.request.user.id))
        # 创建版本快照
        PolicyVersion.objects.create(
            policy=policy,
            version=policy.version,
            snapshot=PolicyDetailSerializer(policy).data,
            change_summary='初始创建',
            editor=str(self.request.user.id),
        )
        return policy

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        policy = self.perform_create(serializer)
        return created(
            data=PolicyDetailSerializer(policy).data,
            message='政策创建成功',
        )


class PolicyAdminUpdateView(generics.UpdateAPIView):
    """PUT /v1/admin-api/policies/{id}/ - 更新政策"""
    serializer_class = PolicyCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsPolicyEditor]
    queryset = Policy.objects.all()

    def update(self, request, *args, **kwargs):
        policy = self.get_object()
        serializer = self.get_serializer(policy, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        policy = serializer.save()
        # 递增版本号并创建快照
        policy.version += 1
        policy.save(update_fields=['version', 'updated_at'])
        PolicyVersion.objects.create(
            policy=policy,
            version=policy.version,
            snapshot=PolicyDetailSerializer(policy).data,
            change_summary=request.data.get('change_summary', ''),
            editor=str(request.user.id),
        )
        return success(
            data=PolicyDetailSerializer(policy).data,
            message='政策更新成功',
        )


class PolicyReviewCreateView(APIView):
    """POST /v1/admin-api/policies/{id}/review/ - 提交/处理审核"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            policy = Policy.objects.get(pk=pk)
        except Policy.DoesNotExist:
            return not_found('政策不存在')

        action = request.data.get('action')
        comment = request.data.get('comment', '')
        reviewer = str(request.user.id)

        if action not in [c[0] for c in ReviewAction.choices]:
            return bad_request('无效的审核动作')

        # 创建审核记录
        review = PolicyReview.objects.create(
            policy=policy,
            version=policy.version,
            reviewer=reviewer,
            action=action,
            comment=comment,
        )

        # 根据审核动作更新政策状态
        if action == ReviewAction.SUBMIT:
            policy.content_status = ContentStatus.PENDING_REVIEW
        elif action == ReviewAction.APPROVE:
            policy.content_status = ContentStatus.PUBLISHED
            policy.reviewed_by = reviewer
            policy.review_comment = comment
        elif action == ReviewAction.REJECT:
            policy.content_status = ContentStatus.DRAFT
            policy.reviewed_by = reviewer
            policy.review_comment = comment
        elif action == ReviewAction.REQUEST_CHANGES:
            policy.content_status = ContentStatus.DRAFT
            policy.reviewed_by = reviewer
            policy.review_comment = comment

        policy.save()

        return created(
            data=PolicyReviewSerializer(review).data,
            message='审核操作成功',
        )


class PolicyPublishView(APIView):
    """POST /v1/admin-api/policies/{id}/publish/ - 发布政策"""
    permission_classes = [permissions.IsAuthenticated, IsPolicyEditor]

    def post(self, request, pk):
        try:
            policy = Policy.objects.get(pk=pk)
        except Policy.DoesNotExist:
            return not_found('政策不存在')

        if policy.content_status == ContentStatus.PUBLISHED:
            return fail('政策已发布，无需重复操作')

        policy.content_status = ContentStatus.PUBLISHED
        policy.published_at = now_cst().date()
        policy.published_at_system = now_cst()
        policy.save()

        # 更新版本快照发布时间
        PolicyVersion.objects.filter(
            policy=policy, version=policy.version,
        ).update(published_at=now_cst())

        return success(
            data=PolicyDetailSerializer(policy).data,
            message='政策发布成功',
        )


class PolicyTagListView(generics.ListAPIView):
    """GET /v1/admin-api/policy-tags/ - 政策标签列表"""
    serializer_class = PolicyTagSerializer
    permission_classes = [permissions.IsAuthenticated, IsPolicyEditor]
    queryset = PolicyTag.objects.filter(enabled=True)

    def get_queryset(self):
        queryset = PolicyTag.objects.filter(enabled=True)
        tag_type = self.request.query_params.get('type')
        if tag_type:
            queryset = queryset.filter(type=tag_type)
        return queryset
