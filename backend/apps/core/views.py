"""
核心用户视图 - 用户资料、统计数据、推送Token

⚠️ 本期根据 API.md §2 暂不接入微信登录，仅保留 X-Device-Id 匿名访问
   WechatLoginView 暂时停用，相关函数保留以备 v2 启用
"""
import logging

from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

# 微信登录相关函数（本期停用）
# from common.authentication import (
#     wechat_jscode2session,
#     get_or_create_user_by_openid,
#     generate_tokens_for_user,
# )
from common.response import success, created, fail, unauthorized
from common.utils import now_cst

from .models import PushToken
from .serializers import (
    UserSerializer,
    UpdateProfileSerializer,
    PushTokenSerializer,
)

logger = logging.getLogger('apps.core')


# ============================================================
# WechatLoginView - 暂不启用（API.md §2 标记为本期不实现）
# ============================================================
# class WechatLoginView(APIView):
#     """微信小程序登录 - 暂不启用"""
#     permission_classes = [AllowAny]
#     authentication_classes = []
#
#     def post(self, request):
#         from .serializers import WechatLoginSerializer
#         serializer = WechatLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         code = serializer.validated_data['code']
#         nickname = serializer.validated_data.get('nickname', '')
#         avatar_url = serializer.validated_data.get('avatar_url', '')
#
#         wx_data = wechat_jscode2session(code)
#         openid = wx_data.get('openid')
#         unionid = wx_data.get('unionid')
#
#         if not openid:
#             return unauthorized('微信登录失败：未获取到openid')
#
#         user = get_or_create_user_by_openid(
#             openid=openid,
#             nickname=nickname,
#             avatar_url=avatar_url,
#             unionid=unionid,
#         )
#
#         if user.is_disabled:
#             return fail(message=user.disabled_reason or '账号已被禁用',
#                         code=20002, http_status=403)
#
#         user.last_login_at = now_cst()
#         user.save(update_fields=['last_login_at'])
#
#         tokens = generate_tokens_for_user(user)
#
#         return success(data={'user': UserSerializer(user).data, 'token': tokens},
#                        message='登录成功')


class UserProfileView(APIView):
    """当前用户资料"""
    permission_classes = [AllowAny]  # 本期允许匿名访问

    def get(self, request):
        if not request.user.is_authenticated:
            return success(data=None, message='未登录（匿名用户）')
        return success(data=UserSerializer(request.user).data)

    def put(self, request):
        if not request.user.is_authenticated:
            return unauthorized('请先登录')
        profile = request.user.profile
        serializer = UpdateProfileSerializer(
            profile, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success(data=UserSerializer(request.user).data, message='更新成功')


class UserStatsView(APIView):
    """用户统计数据"""
    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return success(data=None, message='未登录')
        return success(data={
            'user_id': request.user.id,
            'checked_days': getattr(request.user.profile, 'checked_days', 0),
            'consecutive_days': getattr(request.user.profile, 'consecutive_days', 0),
            'longest_streak': getattr(request.user.profile, 'longest_streak', 0),
        })


class RegisterPushTokenView(APIView):
    """注册推送 Token"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PushTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if not request.user.is_authenticated:
            return success(message='匿名用户，跳过推送注册')

        PushToken.objects.update_or_create(
            user=request.user,
            token=data['token'],
            provider=data.get('provider', 'wechat_mp'),
            defaults={
                'is_active': True,
                'last_active_at': timezone.now(),
                'device_id': data.get('device_id', ''),
            },
        )
        return success(message='推送 Token 注册成功')
