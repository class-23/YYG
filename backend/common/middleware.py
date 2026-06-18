"""
请求日志 + 匿名用户身份识别中间件
"""
import time
import logging
import hashlib

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('apps')


class RequestLoggingMiddleware:
    """记录每个 API 请求的耗时"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration_ms = (time.time() - start_time) * 1000

        user_id = None
        device_id = None
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_id = getattr(request.user, 'id', None)
        if hasattr(request, 'device_id'):
            device_id = request.device_id

        if request.path.startswith('/v1/'):
            logger.info(
                '%s %s %s user=%s device=%s %.1fms',
                request.method,
                request.path,
                response.status_code,
                user_id,
                (device_id or '-')[-4:] if device_id else '-',
                duration_ms,
            )
        return response


class AnonymousDeviceMiddleware:
    """
    设备 ID 识别中间件
    - 读取 X-Device-Id 请求头
    - 若用户未登录但提供了 device_id，关联到匿名用户
    - 在 request 上挂载 device_id 供视图使用
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.device_id = request.META.get('HTTP_X_DEVICE_ID', '').strip()

        # 匿名用户识别：未登录但提供了 device_id 时，自动关联
        if (
            hasattr(request, 'user')
            and not request.user.is_authenticated
            and request.device_id
            and request.path.startswith('/v1/')
        ):
            from common.authentication import get_or_create_anonymous_user
            user = get_or_create_anonymous_user(request.device_id)
            if user:
                request.user = user
                request._anonymous_device_auth = True

        return self.get_response(request)
