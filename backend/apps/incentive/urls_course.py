"""
课程路由
"""
from django.urls import path

from .views import (
    CourseListView, CourseDetailView,
    CourseInquiryCreateView, CourseExchangeView,
)

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('<int:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:course_id>/inquiries/', CourseInquiryCreateView.as_view(), name='course-inquiry'),
    path('<int:course_id>/exchange/', CourseExchangeView.as_view(), name='course-exchange'),
]
