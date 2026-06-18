"""
宝宝测评路由
"""
from django.urls import path
from . import views

urlpatterns = [
    path('templates/', views.AssessmentTemplateView.as_view(), name='assessment-templates'),
    path('submissions/', views.AssessmentSubmissionCreateView.as_view(), name='assessment-submission-create'),
    path('submissions/list/', views.AssessmentSubmissionListView.as_view(), name='assessment-submission-list'),
    path('child-profile/', views.ChildProfileView.as_view(), name='child-profile'),
]
