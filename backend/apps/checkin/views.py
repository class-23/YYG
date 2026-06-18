"""
打卡与课程视图
"""
import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView

from common.response import success, created, fail, not_found, bad_request
from common.utils import today_cst

from .models import DailyLesson, Checkin, SubTask, CheckinSubTask, AudioPlayLog, ReflectionQuestion
from .serializers import (
    DailyLessonSerializer, CheckinCreateSerializer, CheckinSerializer,
    AudioPlayLogCreateSerializer, ReflectionQuestionSerializer, SubTaskSerializer,
)

logger = logging.getLogger('apps.checkin')


def _compute_day_index() -> int:
    """根据开服日期计算今天是第几天（1-365）"""
    from datetime import date
    # MVP 简化：开服日为 2026-01-01
    START_DATE = date(2026, 1, 1)
    today = today_cst()
    delta = (today - START_DATE).days
    day = (delta % 365) + 1
    return day


class TodayLessonView(APIView):
    """获取今日课程"""

    def get(self, request):
        day = _compute_day_index()
        try:
            lesson = DailyLesson.objects.get(day=day, is_published=True)
        except DailyLesson.DoesNotExist:
            return not_found('今日课程未配置')
        return success(data=DailyLessonSerializer(lesson).data)


class LessonDetailView(APIView):
    """获取指定天的课程"""

    def get(self, request, day):
        try:
            day = int(day)
            lesson = DailyLesson.objects.get(day=day, is_published=True)
        except (ValueError, DailyLesson.DoesNotExist):
            return not_found('课程不存在')
        return success(data=DailyLessonSerializer(lesson).data)


class CheckinCreateView(APIView):
    """创建今日打卡"""

    def post(self, request):
        serializer = CheckinCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        today = today_cst()

        # 幂等检查：当日是否已打卡
        existing = Checkin.objects.filter(user=user, biz_date=today).first()
        if existing and existing.main_checkin_completed:
            return fail('今日已打卡，无需重复', code=30001)

        with transaction.atomic():
            checkin, _ = Checkin.objects.select_for_update().get_or_create(
                user=user, biz_date=today,
                defaults={'client_meta': data.get('client_meta', {})},
            )
            checkin.lesson_id = data.get('lesson_id') or checkin.lesson_id
            checkin.reflection = data.get('reflection', checkin.reflection)
            checkin.audio_played_seconds = data.get('audio_played_seconds', checkin.audio_played_seconds)
            checkin.main_checkin_completed = True
            checkin.completed_at = timezone.now()
            checkin.save()

            # 处理子任务
            for st in data.get('sub_tasks', []):
                sub_task_id = st.get('sub_task_id')
                if not sub_task_id:
                    continue
                CheckinSubTask.objects.update_or_create(
                    checkin=checkin, sub_task_id=sub_task_id,
                    defaults={
                        'completed': st.get('completed', True),
                        'completed_at': timezone.now() if st.get('completed') else None,
                        'note': st.get('note', ''),
                    }
                )

            # 更新用户资料统计
            self._update_user_stats(user, checkin)

        return created(data=CheckinSerializer(checkin).data, message='打卡成功')

    @staticmethod
    def _update_user_stats(user, checkin: Checkin):
        """更新用户资料的打卡统计"""
        from apps.core.models import UserProfile
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)

        if checkin.main_checkin_completed:
            profile.checked_days = (profile.checked_days or 0) + 1
            # 连续打卡：检查上一次打卡是否在前一天
            yesterday = checkin.biz_date - timedelta(days=1)
            prev = Checkin.objects.filter(
                user=user,
                biz_date=yesterday,
                main_checkin_completed=True,
            ).first()
            if prev:
                profile.consecutive_days = (profile.consecutive_days or 0) + 1
            else:
                profile.consecutive_days = 1
            if profile.consecutive_days > (profile.longest_streak or 0):
                profile.longest_streak = profile.consecutive_days
            profile.save(update_fields=['checked_days', 'consecutive_days', 'longest_streak', 'updated_at'])


class CheckinHistoryView(APIView):
    """打卡历史列表"""

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = min(int(request.query_params.get('page_size', 20)), 100)
        offset = (page - 1) * page_size

        qs = Checkin.objects.filter(user=request.user).order_by('-biz_date')
        total = qs.count()
        items = qs[offset:offset + page_size]
        return success(data={
            'list': CheckinSerializer(items, many=True).data,
            'pagination': {
                'page': page, 'page_size': page_size, 'total': total,
                'total_pages': (total + page_size - 1) // page_size,
            }
        })


class CheckinDetailView(APIView):
    """指定日期打卡详情"""

    def get(self, request, biz_date):
        try:
            checkin = Checkin.objects.get(user=request.user, biz_date=biz_date)
        except Checkin.DoesNotExist:
            return not_found('该日期没有打卡记录')
        return success(data=CheckinSerializer(checkin).data)


class AudioPlayLogView(APIView):
    """记录音频播放日志"""

    def post(self, request, day):
        serializer = AudioPlayLogCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            lesson = DailyLesson.objects.get(day=int(day))
        except (ValueError, DailyLesson.DoesNotExist):
            return not_found('课程不存在')

        AudioPlayLog.objects.create(
            user=request.user,
            lesson=lesson,
            biz_date=today_cst(),
            play_seconds=serializer.validated_data['play_seconds'],
            client_meta=serializer.validated_data.get('client_meta', {}),
        )
        return success(message='记录成功')


class ReflectionQuestionListView(APIView):
    """获取反思问题列表"""

    def get(self, request):
        category = request.query_params.get('category', 'daily')
        qs = ReflectionQuestion.objects.filter(is_active=True, category=category)
        return success(data=ReflectionQuestionSerializer(qs, many=True).data)


class SubTaskListView(APIView):
    """获取今日子任务模板列表"""

    def get(self, request):
        source = request.query_params.get('source', 'daily')
        qs = SubTask.objects.filter(is_template=True, source=source)
        return success(data=SubTaskSerializer(qs, many=True).data)
