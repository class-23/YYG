"""
API 限流配置
按用户身份（匿名/登录）+ 操作类型（读/写）进行差异化限流
"""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle


class AnonDeviceRateThrottle(AnonRateThrottle):
    """匿名用户限流（基于 X-Device-Id）"""
    scope = 'anon_device'

    def get_cache_key(self, request, view):
        device_id = getattr(request, 'device_id', '')
        if not device_id:
            # 无设备 ID 时降级到 IP
            return self.cache_format % {
                'scope': self.scope,
                'ident': self.get_ident(request),
            }
        return self.cache_format % {
            'scope': self.scope,
            'ident': device_id,
        }


class AuthedUserRateThrottle(UserRateThrottle):
    """登录用户限流"""
    scope = 'authed_user'


class WriteOperationThrottle(UserRateThrottle):
    """写操作限流（防刷）"""
    scope = 'write_op'


# 在 settings.py REST_FRAMEWORK 中配置:
# 'DEFAULT_THROTTLE_CLASSES': (
#     'common.throttling.AnonDeviceRateThrottle',
# ),
# 'DEFAULT_THROTTLE_RATES': {
#     'anon_device': '100/min',
#     'authed_user': '600/min',
#     'write_op': '30/min',
# }
