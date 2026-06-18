"""
恋爱交友路由
"""
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.LoveProfileView.as_view(), name='love-profile'),
    path('list/', views.LoveListView.as_view(), name='love-list'),
    path('follow/<int:user_id>/', views.LoveFollowView.as_view(), name='love-follow'),
]
