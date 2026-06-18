"""
返现路由
"""
from django.urls import path

from .views import CashbackAccountView, CashbackRecordListView

urlpatterns = [
    path('account/', CashbackAccountView.as_view(), name='cashback-account'),
    path('records/', CashbackRecordListView.as_view(), name='cashback-records'),
]
