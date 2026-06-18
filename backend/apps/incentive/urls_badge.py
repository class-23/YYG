"""
徽章路由
"""
from django.urls import path

from .views import BadgeListView, MyBadgeListView

urlpatterns = [
    path('', BadgeListView.as_view(), name='badge-list'),
    path('me/', MyBadgeListView.as_view(), name='badge-my'),
]
