"""
政策CMS路由配置
"""
from django.urls import path

from . import views

urlpatterns = [
    # 公开接口
    path('', views.PolicyListView.as_view(), name='policy-list'),
    path('<str:business_id>/', views.PolicyDetailView.as_view(), name='policy-detail'),
]
