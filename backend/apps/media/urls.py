"""
媒体文件路由配置 - 文件上传
"""
from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
]
