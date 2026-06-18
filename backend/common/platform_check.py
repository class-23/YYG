"""
微信小程序客户端能力探测
- 验证请求来源（AppID 校验）
- 检测最低基础库版本
- 平台差异处理
"""
import logging
from django.conf import settings
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger('apps.platform')


def verify_miniprogram_request(request) -> bool:
    """
    校验请求是否来自合法的微信小程序
    生产环境应从 wx.login() 回调中获取 session_key 并验证
    本期仅做宽松校验（开发期）
    """
    if settings.DEBUG:
        return True

    # 平台标识
    platform = request.META.get('HTTP_X_PLATFORM', '')
    if platform and platform != 'miniprogram':
        return False

    # 客户端版本检查
    client_version = request.META.get('HTTP_X_CLIENT_VERSION', '')
    if not client_version:
        logger.warning('请求缺少 X-Client-Version 头: %s', request.path)

    return True


def get_miniprogram_lib_version(request) -> str:
    """获取客户端基础库版本（从 User-Agent 中提取）"""
    ua = request.META.get('HTTP_USER_AGENT', '')
    # 格式: MicroMessenger/7.0.5 nettype/WIFI language/zh_CN miniprogramversion/3.0.0
    if 'miniprogramversion/' in ua:
        try:
            return ua.split('miniprogramversion/')[1].split(' ')[0]
        except (IndexError, ValueError):
            pass
    return '0.0.0'


def check_lib_version_compat(request, required_version: str = '2.0.0') -> bool:
    """
    检查客户端基础库版本是否满足最低要求
    API.md §15.3 规定的最低基础库版本
    """
    current = get_miniprogram_lib_version(request)
    return _version_gte(current, required_version)


def _version_gte(v1: str, v2: str) -> bool:
    """比较版本号 v1 >= v2"""
    try:
        parts1 = [int(x) for x in v1.split('.')]
        parts2 = [int(x) for x in v2.split('.')]
        # 补齐到相同长度
        while len(parts1) < len(parts2):
            parts1.append(0)
        while len(parts2) < len(parts1):
            parts2.append(0)
        return parts1 >= parts2
    except (ValueError, AttributeError):
        return False
