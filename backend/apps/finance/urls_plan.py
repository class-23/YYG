"""
计划路由
"""
from django.urls import path

from .views import PlanListView, MyPlanView, ActivateTrial21View

urlpatterns = [
    path('', PlanListView.as_view(), name='plan-list'),
    path('me/', MyPlanView.as_view(), name='plan-me'),
    path('trial21/activate/', ActivateTrial21View.as_view(), name='plan-trial21-activate'),
]
