"""
统一响应格式工具函数
"""
from rest_framework.response import Response
from rest_framework import status


def success(data=None, message='ok', code=0, http_status=200):
    """成功响应"""
    return Response({
        'code': code,
        'message': message,
        'data': data,
    }, status=http_status)


def created(data=None, message='创建成功'):
    """201 响应"""
    return success(data=data, message=message, http_status=status.HTTP_201_CREATED)


def no_content():
    """204 响应"""
    return Response(status=status.HTTP_204_NO_CONTENT)


def fail(message='操作失败', code=1, http_status=400, errors=None):
    """失败响应"""
    resp = {
        'code': code,
        'message': message,
        'data': None,
    }
    if errors:
        resp['errors'] = errors
    return Response(resp, status=http_status)


def bad_request(message='请求参数错误', errors=None):
    """400 响应"""
    return fail(message=message, http_status=status.HTTP_400_BAD_REQUEST, errors=errors)


def unauthorized(message='未登录或认证已过期'):
    """401 响应"""
    return fail(message=message, code=10002, http_status=status.HTTP_401_UNAUTHORIZED)


def forbidden(message='权限不足'):
    """403 响应"""
    return fail(message=message, code=10003, http_status=status.HTTP_403_FORBIDDEN)


def not_found(message='请求的资源不存在'):
    """404 响应"""
    return fail(message=message, code=10004, http_status=status.HTTP_404_NOT_FOUND)


def server_error(message='服务器内部错误'):
    """500 响应"""
    return fail(message=message, code=10007, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
