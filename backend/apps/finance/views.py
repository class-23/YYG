"""
返现与计划视图
"""
import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView

from common.response import success, created, fail, not_found, bad_request
from common.utils import today_cst

from .models import Plan, UserPlan, CashbackAccount, CashbackRecord
from .serializers import (
    PlanSerializer, UserPlanSerializer,
    CashbackAccountSerializer, CashbackRecordSerializer,
)

logger = logging.getLogger('apps.finance')


class PlanListView(APIView):
    """获取计划列表"""

    def get(self, request):
        plans = Plan.objects.filter(is_active=True).order_by('price_cents')
        return success(data=PlanSerializer(plans, many=True).data)


class MyPlanView(APIView):
    """我的当前计划"""

    def get(self, request):
        user_plan = UserPlan.objects.filter(
            user=request.user, status=UserPlan.UserPlanStatus.ACTIVE,
        ).order_by('-started_at').first()
        if not user_plan:
            return success(data=None, message='当前没有生效中的计划')
        return success(data=UserPlanSerializer(user_plan).data)


class ActivateTrial21View(APIView):
    """激活 21 天体验计划（邀请 3 人达成）"""
    INVITE_REQUIRED = 3  # 需要邀请 3 个有效用户

    def post(self, request):
        user = request.user
        from apps.core.models import UserProfile

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return not_found('用户资料不存在')

        # 检查是否已经激活过
        if profile.trial21_unlocked:
            return fail('21天体验已激活，请勿重复', code=40002)

        # 检查是否已有生效中的 21 天计划
        existing = UserPlan.objects.filter(
            user=user, plan__code='trial21', status=UserPlan.UserPlanStatus.ACTIVE,
        ).exists()
        if existing:
            return fail('您已开通 21 天计划', code=40002)

        # 检查邀请人数
        from apps.invite.models import InviteRecord
        confirmed_invites = InviteRecord.objects.filter(
            inviter_user=user, status=InviteRecord.InviteStatus.CONFIRMED,
        ).count()
        if confirmed_invites < self.INVITE_REQUIRED:
            return fail(
                f'还需邀请 {self.INVITE_REQUIRED - confirmed_invites} 位好友完成首次打卡',
                code=40004,
            )

        # 激活
        try:
            plan = Plan.objects.get(code='trial21', is_active=True)
        except Plan.DoesNotExist:
            return not_found('21天体验计划未配置')

        with transaction.atomic():
            now = timezone.now()
            UserPlan.objects.create(
                user=user, plan=plan, status=UserPlan.UserPlanStatus.ACTIVE,
                started_at=now, expires_at=now + timedelta(days=plan.duration_days),
            )
            profile.trial21_unlocked = True
            profile.plan_status = 'trial21'
            profile.plan_started_at = now
            profile.plan_expires_at = now + timedelta(days=plan.duration_days)
            profile.save()

        return success(message='21天体验已激活')


class CashbackAccountView(APIView):
    """获取返现账户信息"""

    def get(self, request):
        account, _ = CashbackAccount.objects.get_or_create(user=request.user)
        return success(data=CashbackAccountSerializer(account).data)


class CashbackRecordListView(APIView):
    """返现流水列表"""

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = min(int(request.query_params.get('page_size', 20)), 100)
        offset = (page - 1) * page_size

        qs = CashbackRecord.objects.filter(user=request.user).order_by('-created_at')
        record_type = request.query_params.get('type')
        if record_type:
            qs = qs.filter(type=record_type)

        total = qs.count()
        items = qs[offset:offset + page_size]
        return success(data={
            'list': CashbackRecordSerializer(items, many=True).data,
            'pagination': {
                'page': page, 'page_size': page_size, 'total': total,
                'total_pages': (total + page_size - 1) // page_size,
            }
        })
