"""
课程与反思问题路由
"""
from django.urls import path

from .views import (
    TodayLessonView, LessonDetailView, AudioPlayLogView,
    ReflectionQuestionListView, SubTaskListView,
)

urlpatterns = [
    path('today/', TodayLessonView.as_view(), name='lesson-today'),
    path('<int:day>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('<int:day>/play-log/', AudioPlayLogView.as_view(), name='lesson-play-log'),
    path('reflections/', ReflectionQuestionListView.as_view(), name='reflection-questions'),
    path('sub-tasks/', SubTaskListView.as_view(), name='sub-tasks'),
]
