"""
媒体文件路由配置 - 海报
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PosterCreateView.as_view(), name='poster-create'),
    path('list/', views.PosterListView.as_view(), name='poster-list'),
]
