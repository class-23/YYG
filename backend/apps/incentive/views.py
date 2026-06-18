"""
激励系统视图
"""
import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView

from common.response import success, created, fail, not_found, bad_request
from common.utils import hash_phone, mask_phone

from .models import Badge, UserBadge, Course, CourseExchange, CourseInquiry
from .serializers import (
    BadgeSerializer, UserBadgeSerializer, CourseSerializer,
    CourseInquiryCreateSerializer, CourseInquirySerializer,
)

logger = logging.getLogger('apps.incentive')


class BadgeListView(APIView):
    """徽章列表"""

    def get(self, request):
        badges = Badge.objects.filter(is_active=True)
        return success(data=BadgeSerializer(badges, many=True, context={'request': request}).data)


class MyBadgeListView(APIView):
    """我的徽章列表"""

    def get(self, request):
        user_badges = UserBadge.objects.filter(user=request.user).select_related('badge')
        return success(data=UserBadgeSerializer(user_badges, many=True).data)


class CourseListView(APIView):
    """课程列表"""

    def get(self, request):
        courses = Course.objects.filter(is_active=True)
        return success(data=CourseSerializer(courses, many=True).data)


class CourseDetailView(APIView):
    """课程详情"""

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id, is_active=True)
        except Course.DoesNotExist:
            return not_found('课程不存在')
        return success(data=CourseSerializer(course).data)


class CourseInquiryCreateView(APIView):
    """课程咨询 - 留资"""
    RATE_LIMIT_PER_24H = 3  # 同一手机号24小时内最多3次

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id, is_active=True)
        except Course.DoesNotExist:
            return not_found('课程不存在')

        serializer = CourseInquiryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        phone = data.get('phone', '').strip()
        if not phone:
            return bad_request('请提供手机号')

        # 24小时内限频
        phone_h = hash_phone(phone)
        last_24h = timezone.now() - timedelta(hours=24)
        recent_count = CourseInquiry.objects.filter(
            phone_hash=phone_h, created_at__gte=last_24h,
        ).count()
        if recent_count >= self.RATE_LIMIT_PER_24H:
            return fail('咨询过于频繁，请稍后再试', code=51004, http_status=429)

        # 创建留资记录
        inquiry = CourseInquiry.objects.create(
            user=request.user if request.user.is_authenticated else None,
            course=course,
            phone=phone,  # TODO: 生产环境需 AES 加密
            phone_masked=mask_phone(phone),
            phone_hash=phone_h,
            wechat=data.get('wechat', ''),
            note=data.get('note', ''),
            client_meta={
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:512],
                'ip': request.META.get('REMOTE_ADDR'),
            },
        )
        return created(data=CourseInquirySerializer(inquiry).data, message='咨询已收到，客服将尽快与您联系')


class CourseExchangeView(APIView):
    """课程兑换（使用返现天数兑换）"""

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id, is_active=True)
        except Course.DoesNotExist:
            return not_found('课程不存在')

        # 检查是否已兑换
        if CourseExchange.objects.filter(
            user=request.user, course=course, status=CourseExchange.Status.SUCCESS,
        ).exists():
            return fail('您已兑换过该课程', code=51002)

        # 检查返现天数
        from apps.finance.models import CashbackAccount
        from apps.checkin.models import Checkin
        try:
            account = CashbackAccount.objects.get(user=request.user)
        except CashbackAccount.DoesNotExist:
            return fail('返现账户未开通', code=51003)

        # 用累计赚取 / 每日返现元算天数
        if account.total_earned_cents < course.required_cashback_days * 100:
            return fail('返现余额不足，无法兑换', code=51003)

        with transaction.atomic():
            exchange = CourseExchange.objects.create(
                user=request.user, course=course, status=CourseExchange.Status.SUCCESS,
            )
        return created(data={'exchange_id': exchange.id}, message='兑换成功')
