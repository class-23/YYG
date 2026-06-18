"""
全局异常处理 - 统一错误响应格式
"""
import logging
import traceback
from rest_framework.views import exception_handler
from rest_framework import exceptions, status
from django.core.exceptions import PermissionDenied
from django.http import Http404

logger = logging.getLogger('apps')

# 错误码定义（与 API.md 对齐）
ERROR_CODES = {
    # 通用错误 1xxxx
    'invalid_request': 10001,
    'unauthorized': 10002,
    'forbidden': 10003,
    'not_found': 10004,
    'method_not_allowed': 10005,
    'throttled': 10006,
    'internal_error': 10007,
    'validation_error': 10008,

    # 用户相关 2xxxx
    'user_not_found': 20001,
    'user_disabled': 20002,
    'wechat_login_failed': 20003,
    'phone_bound': 20004,

    # 打卡相关 3xxxx
    'already_checkin': 30001,
    'checkin_not_found': 30002,
    'lesson_not_found': 30003,
    'plan_not_active': 30004,

    # 计划相关 4xxxx
    'plan_not_found': 40001,
    'plan_already_active': 40002,
    'plan_expired': 40003,
    'invite_count_not_enough': 40004,

    # 小队相关 5xxxx
    'team_not_found': 50001,
    'team_full': 50002,
    'already_in_team': 50003,
    'team_invite_expired': 50004,

    # 课程相关 51xxx
    'course_not_found': 51001,
    'course_already_redeemed': 51002,
    'insufficient_cashback': 51003,
    'inquiry_rate_limit': 51004,

    # 邀请相关 6xxxx
    'invite_code_invalid': 60001,
    'invite_code_used': 60002,
    'invite_self': 60003,

    # 政策相关 7xxxx
    'policy_not_found': 70001,
    'policy_already_published': 70002,
    'policy_review_required': 70003,

    # 评估相关 8xxxx
    'assessment_not_found': 80001,
    'child_profile_not_found': 80002,
}


def _build_error_response(code_key, detail, errors=None):
    """构建统一错误响应"""
    response_data = {
        'code': ERROR_CODES.get(code_key, 10007),
        'message': detail if isinstance(detail, str) else str(detail),
        'data': None,
    }
    if errors:
        response_data['errors'] = errors
    return response_data


def custom_exception_handler(exc, context):
    """DRF 全局异常处理器"""

    # 处理 Django 原生异常
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    # 调用 DRF 默认处理器
    response = exception_handler(exc, context)

    if response is not None:
        # 标准化错误格式
        if isinstance(exc, exceptions.ValidationError):
            code_key = 'validation_error'
            detail = '请求参数校验失败'
            errors = exc.detail if hasattr(exc, 'detail') else None
            response.data = _build_error_response(code_key, detail, errors)
        elif isinstance(exc, exceptions.AuthenticationFailed):
            code_key = 'unauthorized'
            detail = str(exc.detail) if hasattr(exc, 'detail') else '认证失败'
            response.data = _build_error_response(code_key, detail)
        elif isinstance(exc, exceptions.NotAuthenticated):
            code_key = 'unauthorized'
            response.data = _build_error_response(code_key, '未提供有效的认证凭证')
        elif isinstance(exc, exceptions.PermissionDenied):
            code_key = 'forbidden'
            detail = str(exc.detail) if hasattr(exc, 'detail') else '权限不足'
            response.data = _build_error_response(code_key, detail)
        elif isinstance(exc, exceptions.NotFound):
            code_key = 'not_found'
            detail = str(exc.detail) if hasattr(exc, 'detail') else '请求的资源不存在'
            response.data = _build_error_response(code_key, detail)
        elif isinstance(exc, exceptions.MethodNotAllowed):
            code_key = 'method_not_allowed'
            response.data = _build_error_response(code_key, '请求方法不允许')
        elif isinstance(exc, exceptions.Throttled):
            code_key = 'throttled'
            response.data = _build_error_response(code_key, '请求过于频繁，请稍后重试')
        else:
            code_key = 'internal_error'
            detail = str(exc.detail) if hasattr(exc, 'detail') else '服务器内部错误'
            response.data = _build_error_response(code_key, detail)
    else:
        # 未被 DRF 处理的异常 - 500
        logger.error('未处理的异常: %s\n%s', exc, traceback.format_exc())
        from rest_framework.response import Response
        response = Response(
            _build_error_response('internal_error', '服务器内部错误'),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
