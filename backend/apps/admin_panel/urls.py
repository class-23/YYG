"""
运营后台路由
"""
from django.urls import path

from .views import (
    AdminLoginView, AdminDashboardView, AdminUserListView,
    AdminAdjustCashbackView, AdminAuditLogListView, DataDictionaryListView,
)

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('users/', AdminUserListView.as_view(), name='admin-users'),
    path('users/<int:user_id>/adjust-cashback/', AdminAdjustCashbackView.as_view(), name='admin-adjust-cashback'),
    path('audit-logs/', AdminAuditLogListView.as_view(), name='admin-audit-logs'),
    path('dictionaries/', DataDictionaryListView.as_view(), name='admin-dictionaries'),
]
