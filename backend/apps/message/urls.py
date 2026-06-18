"""
消息系统路由配置
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.MessageListView.as_view(), name='message-list'),
    path('<int:pk>/read/', views.MessageReadView.as_view(), name='message-read'),
    path('unread-count/', views.MessageUnreadCountView.as_view(), name='message-unread-count'),
]
