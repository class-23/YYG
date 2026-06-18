from django.urls import path

from .views import UserProfileView, UserStatsView, RegisterPushTokenView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('me/stats/', UserStatsView.as_view(), name='user-stats'),
    path('me/push-tokens/', RegisterPushTokenView.as_view(), name='register-push-token'),
]
