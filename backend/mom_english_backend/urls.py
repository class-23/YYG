"""
URL configuration for mom_english_backend project.
总路由配置 - 汇聚各应用子路由
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1 路由
    path('v1/', include([
        path('auth/', include('apps.core.urls_auth')),
        path('users/', include('apps.core.urls_user')),
        path('lessons/', include('apps.checkin.urls_lesson')),
        path('checkins/', include('apps.checkin.urls_checkin')),
        path('plans/', include('apps.finance.urls_plan')),
        path('cashback/', include('apps.finance.urls_cashback')),
        path('badges/', include('apps.incentive.urls_badge')),
        path('courses/', include('apps.incentive.urls_course')),
        path('teams/', include('apps.social.urls_team')),
        path('square/', include('apps.social.urls_square')),
        path('love/', include('apps.social.urls_love')),
        path('milestones/', include('apps.mom_growth.urls')),
        path('kid-assessment/', include('apps.kid_assessment.urls')),
        path('policies/', include('apps.policy_app.urls')),
        path('invite/', include('apps.invite.urls')),
        path('messages/', include('apps.message.urls')),
        path('files/', include('apps.media.urls')),
        path('posters/', include('apps.media.urls_poster')),
        path('admin-api/', include('apps.admin_panel.urls')),
    ])),
]
