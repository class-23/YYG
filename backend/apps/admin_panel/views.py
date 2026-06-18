"""
运营后台视图
"""
import hashlib
import logging

from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from common.response import success, created, fail, unauthorized, forbidden, not_found
from common.permissions import IsSuperAdmin, IsAdminUser
from common.authentication import generate_tokens_for_user

from .models import AdminUser, AdminRoleDefinition, AdminPermission, AdminAuditLog, DataDictionaryEntry
from .serializers import (
    AdminUserSerializer, AdminLoginSerializer, AdminRoleSerializer,
    AdminPermissionSerializer, AdminAuditLogSerializer, DataDictionaryEntrySerializer
)

logger = logging.getLogger('apps.admin_panel')


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def _make_admin_token(admin_user: AdminUser) -> dict:
    """为后台账号生成专用 JWT（user_id 字段复用）"""
    refresh = RefreshToken()
    refresh['user_id'] = admin_user.id
    refresh['username'] = admin_user.username
    refresh['role_code'] = admin_user.role_code
    refresh['is_admin'] = True
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'admin_user': AdminUserSerializer(admin_user).data,
    }


class AdminLoginView(APIView):
    """后台账号登录"""
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            admin_user = AdminUser.objects.get(username=username, is_active=True)
        except AdminUser.DoesNotExist:
            return fail('用户名或密码错误', code=10002, http_status=status.HTTP_401_UNAUTHORIZED)

        if admin_user.is_locked():
            return fail('账号已被锁定，请稍后重试', http_status=status.HTTP_403_FORBIDDEN)

        if admin_user.password_hash != _hash_password(password):
            admin_user.failed_login_count += 1
            if admin_user.failed_login_count >= 5:
                from datetime import timedelta
                admin_user.locked_until = timezone.now() + timedelta(minutes=15)
            admin_user.save(update_fields=['failed_login_count', 'locked_until'])
            return fail('用户名或密码错误', code=10002, http_status=status.HTTP_401_UNAUTHORIZED)

        # 登录成功
        ip = request.META.get('REMOTE_ADDR')
        admin_user.failed_login_count = 0
        admin_user.locked_until = None
        admin_user.last_login_at = timezone.now()
        admin_user.last_login_ip = ip
        admin_user.save(update_fields=['failed_login_count', 'locked_until', 'last_login_at', 'last_login_ip'])

        # 记录审计
        AdminAuditLog.objects.create(
            operator=admin_user, action='admin.login', target_type='admin_user',
            target_id=str(admin_user.id), ip=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:512],
            result='success',
        )

        return success(data=_make_admin_token(admin_user), message='登录成功')


class AdminDashboardView(APIView):
    """后台首页数据统计"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        # TODO: 实现统计逻辑
        from apps.core.models import User
        from apps.checkin.models import Checkin
        from django.db.models import Count
        from datetime import timedelta

        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        data = {
            'user_total': User.objects.filter(deleted_at__isnull=True).count(),
            'user_today_new': User.objects.filter(
                created_at__date=today, deleted_at__isnull=True
            ).count(),
            'checkin_today': Checkin.objects.filter(
                biz_date=today, main_checkin_completed=True
            ).count(),
            'checkin_yesterday': Checkin.objects.filter(
                biz_date=yesterday, main_checkin_completed=True
            ).count(),
        }
        return success(data=data)


class AdminUserListView(APIView):
    """后台用户列表（普通小程序用户）"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        from apps.core.models import User
        keyword = request.query_params.get('keyword', '').strip()
        page = int(request.query_params.get('page', 1))
        page_size = min(int(request.query_params.get('page_size', 20)), 100)
        offset = (page - 1) * page_size

        qs = User.objects.filter(deleted_at__isnull=True)
        if keyword:
            qs = qs.filter(nickname__icontains=keyword) | qs.filter(phone_masked__icontains=keyword)

        total = qs.count()
        items = qs.order_by('-created_at')[offset:offset + page_size]
        from apps.core.serializers import UserSerializer
        return success(data={
            'list': UserSerializer(items, many=True).data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': (total + page_size - 1) // page_size,
            }
        })


class AdminAdjustCashbackView(APIView):
    """手动调整返现余额（运营后台）"""
    permission_classes = [IsSuperAdmin]

    def post(self, request, user_id):
        from apps.core.models import User
        from apps.finance.models import CashbackAccount, CashbackRecord
        from django.db import transaction

        amount_cents = request.data.get('amount_cents')
        description = request.data.get('description', '')

        if amount_cents is None or not isinstance(amount_cents, int):
            return fail('amount_cents 必须是整数（分）', http_status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return not_found('用户不存在')

        with transaction.atomic():
            account, _ = CashbackAccount.objects.select_for_update().get_or_create(user=user)
            account.balance_cents += amount_cents
            if amount_cents > 0:
                account.total_earned_cents += amount_cents
            account.version += 1
            account.save()

            CashbackRecord.objects.create(
                user=user,
                amount_cents=amount_cents,
                type='manual_adjust',
                source='manual',
                biz_date=timezone.now().date(),
                description=description or '运营后台手工调整',
                operator_id=request.user.id if hasattr(request.user, 'id') else None,
            )

        # 审计日志
        AdminAuditLog.objects.create(
            operator_id=request.user.id if hasattr(request.user, 'id') else 0,
            action='user.adjust_cashback',
            target_type='user',
            target_id=str(user_id),
            payload_after={'amount_cents': amount_cents, 'description': description},
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:512],
            result='success',
        )

        return success(message='返现调整成功')


class AdminAuditLogListView(APIView):
    """审计日志列表"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = min(int(request.query_params.get('page_size', 20)), 100)
        offset = (page - 1) * page_size

        qs = AdminAuditLog.objects.all().order_by('-created_at')
        action = request.query_params.get('action')
        if action:
            qs = qs.filter(action=action)
        target_type = request.query_params.get('target_type')
        if target_type:
            qs = qs.filter(target_type=target_type)

        total = qs.count()
        items = qs[offset:offset + page_size]
        return success(data={
            'list': AdminAuditLogSerializer(items, many=True).data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': (total + page_size - 1) // page_size,
            }
        })


class DataDictionaryListView(APIView):
    """数据字典查询"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        dict_type = request.query_params.get('type')
        qs = DataDictionaryEntry.objects.filter(is_active=True)
        if dict_type:
            qs = qs.filter(type=dict_type)
        qs = qs.order_by('type', 'sort', 'id')
        return success(data=DataDictionaryEntrySerializer(qs, many=True).data)
