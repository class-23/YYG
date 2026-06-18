"""
广场路由
"""
from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.SquarePostListView.as_view(), name='square-post-list'),
    path('posts/create/', views.SquarePostCreateView.as_view(), name='square-post-create'),
    path('posts/<int:pk>/like/', views.SquarePostLikeView.as_view(), name='square-post-like'),
    path('posts/<int:pk>/comments/', views.SquarePostCommentView.as_view(), name='square-post-comment'),
]
