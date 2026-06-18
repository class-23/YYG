"""
打卡路由
"""
from django.urls import path

from .views import CheckinCreateView, CheckinHistoryView, CheckinDetailView

urlpatterns = [
    path('', CheckinCreateView.as_view(), name='checkin-create'),
    path('list/', CheckinHistoryView.as_view(), name='checkin-list'),
    path('<str:biz_date>/', CheckinDetailView.as_view(), name='checkin-detail'),
]
