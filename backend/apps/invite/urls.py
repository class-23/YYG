"""
邀请系统路由配置
"""
from django.urls import path

from . import views

urlpatterns = [
    path('codes/', views.InviteCodeCreateView.as_view(), name='invite-code-create'),
    path('codes/list/', views.InviteCodeListView.as_view(), name='invite-code-list'),
    path('apply/', views.InviteApplyView.as_view(), name='invite-apply'),
    path('records/', views.InviteRecordListView.as_view(), name='invite-record-list'),
]
