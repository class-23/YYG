"""
宝妈成长视图
里程碑 / 线下活动
"""
from django.db import IntegrityError
from django.db.models import F
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.response import success, created, fail, not_found
from .models import MilestoneDefinition, UserMilestone, OfflineActivity, OfflineActivitySignup
from .serializers import (
    MilestoneDefinitionSerializer, UserMilestoneSerializer,
    OfflineActivitySerializer,
)


class MilestoneListView(generics.ListAPIView):
    """里程碑列表"""
    serializer_class = MilestoneDefinitionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MilestoneDefinition.objects.filter(is_active=True)


class MyMilestoneListView(generics.ListAPIView):
    """我的已解锁里程碑"""
    serializer_class = UserMilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserMilestone.objects.filter(
            user=self.request.user,
        ).select_related('milestone').order_by('milestone__month')


class OfflineActivityListView(generics.ListAPIView):
    """线下活动列表"""
    serializer_class = OfflineActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = OfflineActivity.objects.filter(
            status=OfflineActivity.Status.OPEN,
        )

        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city=city)

        return queryset.order_by('start_at')


class OfflineActivitySignupView(generics.CreateAPIView):
    """线下活动报名"""
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        activity_id = self.kwargs['pk']
        try:
            activity = OfflineActivity.objects.get(id=activity_id)
        except OfflineActivity.DoesNotExist:
            return not_found(message='活动不存在')

        if activity.status != OfflineActivity.Status.OPEN:
            return fail(message='该活动不在报名状态')

        if activity.taken_seats >= activity.max_seats:
            return fail(message='名额已满')

        try:
            signup = OfflineActivitySignup.objects.create(
                activity=activity,
                user=request.user,
            )
        except IntegrityError:
            return fail(message='你已报名该活动')

        OfflineActivity.objects.filter(id=activity_id).update(
            taken_seats=F('taken_seats') + 1,
        )
        return created(data={'id': signup.id, 'status': signup.status}, message='报名成功')
