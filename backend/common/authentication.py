"""
JWT 认证 + 微信登录认证逻辑
本期根据 API.md §2 暂不接入微信登录，采用可选鉴权 + X-Device-Id 匿名标识
"""
import logging
import hashlib
import secrets
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions

logger = logging.getLogger('apps.auth')
User = get_user_model()


class JWTAuthenticationFromHeader(JWTAuthentication):
    """
    可选 JWT 认证：
    - 有 Authorization 头且 token 有效 → 返回 (user, token)
    - 无 Authorization 头 → 返回 None（视为匿名用户，由 AnonymousDeviceMiddleware 处理）
    - token 无效/过期 → 抛出 AuthenticationFailed
    """
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # 匿名访问

        try:
            return super().authenticate(request)
        except Exception as e:
            # token 解析失败：不阻断，让请求以匿名方式继续
            logger.debug('JWT 解析失败，按匿名处理: %s', e)
            return None


def hash_device_id(device_id: str) -> str:
    """对设备 ID 做 SHA-256 哈希，避免明文存储"""
    if not device_id:
        return ''
    return hashlib.sha256(device_id.encode('utf-8')).hexdigest()


def get_or_create_anonymous_user(device_id: str) -> User:
    """
    根据 device_id 获取或创建匿名用户
    本期不接入微信登录，使用 device_id 作为唯一标识
    """
    if not device_id:
        return None

    device_hash = hash_device_id(device_id)
    # 用 device_hash 的一部分作为 openid（仅用于本期）
    fake_openid = f"dev_{device_hash[:32]}"

    user, created = User.objects.get_or_create(
        openid=fake_openid,
        defaults={
            'nickname': f'匿名用户{device_id[-4:]}',
            'avatar_url': '',
        }
    )
    if created:
        logger.info('新匿名用户创建: device_id=%s, user_id=%s', device_id[-4:], user.id)
        from apps.core.models import UserProfile
        UserProfile.objects.create(user=user)
    return user


# ⚠️ 本期不实现：微信登录相关函数
# def wechat_jscode2session(code: str) -> dict:
#     """暂不实现 - 等待 API.md 标记解除"""
#     pass

# def get_or_create_user_by_openid(openid: str, ...):
#     """暂不实现"""
#     pass

def generate_tokens_for_user(user):
    """为用户生成 JWT access + refresh token（保留以备 v2 启用）"""
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
