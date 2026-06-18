"""
宝妈成长路由
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MilestoneListView.as_view(), name='milestone-list'),
    path('me/', views.MyMilestoneListView.as_view(), name='my-milestone-list'),
    path('activities/', views.OfflineActivityListView.as_view(), name='offline-activity-list'),
    path('activities/<int:pk>/signup/', views.OfflineActivitySignupView.as_view(), name='offline-activity-signup'),
]
