"""
小队路由
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeamCreateView.as_view(), name='team-create'),
    path('list/', views.TeamListView.as_view(), name='team-list'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('join/', views.TeamJoinView.as_view(), name='team-join'),
    path('<int:pk>/activities/', views.TeamActivityListView.as_view(), name='team-activities'),
    path('activities/<int:pk>/interact/', views.TeamInteractionCreateView.as_view(), name='team-interact'),
    path('activities/<int:pk>/encourage/', views.TeamEncouragementCreateView.as_view(), name='team-encourage'),
]
