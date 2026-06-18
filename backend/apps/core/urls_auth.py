"""
用户认证路由

⚠️ 本期根据 API.md §2 暂不接入微信登录，wechat-login 路由暂时禁用
   保留路由定义以便 v2 一键启用
"""
from django.urls import path

# from .views import WechatLoginView  # 本期不启用

urlpatterns = [
    # path('wechat-login/', WechatLoginView.as_view(), name='wechat-login'),
    # path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),  # v2 启用
    # path('logout/', LogoutView.as_view(), name='logout'),  # v2 启用
]
