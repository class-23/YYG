"""
宝宝测评视图
模板 / 提交 / 宝宝档案
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.response import success, created, fail, not_found
from .models import (
    KidAssessmentTemplate, KidAssessmentQuestion,
    KidAssessmentSubmission, KidAssessmentAnswer,
    KidAssessmentScoreItem, KidChildProfile,
)
from .serializers import (
    KidAssessmentTemplateSerializer,
    SubmissionCreateSerializer,
    KidAssessmentSubmissionSerializer,
    KidChildProfileSerializer,
)


class AssessmentTemplateView(generics.ListAPIView):
    """获取活跃的测评模板（含题目）"""
    serializer_class = KidAssessmentTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return KidAssessmentTemplate.objects.filter(
            is_active=True,
        ).prefetch_related('questions')


class AssessmentSubmissionCreateView(generics.CreateAPIView):
    """提交测评答案"""
    serializer_class = SubmissionCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        template_code = ser.validated_data['template_code']
        answers_data = ser.validated_data['answers']

        try:
            template = KidAssessmentTemplate.objects.get(
                code=template_code, is_active=True,
            )
        except KidAssessmentTemplate.DoesNotExist:
            return not_found(message='测评模板不存在')

        # 创建提交记录
        submission = KidAssessmentSubmission.objects.create(
            user=request.user,
            template=template,
        )

        # 保存答案
        for ans in answers_data:
            question_key = ans['question_key']
            try:
                question = KidAssessmentQuestion.objects.get(
                    template=template, key=question_key,
                )
            except KidAssessmentQuestion.DoesNotExist:
                continue

            KidAssessmentAnswer.objects.create(
                submission=submission,
                question=question,
                answer_text=ans.get('answer_text', ''),
                answer_options=ans.get('answer_options', []),
            )

        # 更新宝宝档案
        profile, _ = KidChildProfile.objects.get_or_create(user=request.user)
        profile.latest_submission = submission
        profile.has_done_assessment = True
        profile.answers_snapshot = {
            ans['question_key']: ans.get('answer_text') or ans.get('answer_options')
            for ans in answers_data
        }
        profile.save()

        return created(
            data=KidAssessmentSubmissionSerializer(submission).data,
            message='测评提交成功',
        )


class AssessmentSubmissionListView(generics.ListAPIView):
    """我的测评提交列表"""
    serializer_class = KidAssessmentSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return KidAssessmentSubmission.objects.filter(
            user=self.request.user,
        ).prefetch_related('score_items').order_by('-created_at')


class ChildProfileView(generics.RetrieveAPIView):
    """获取宝宝档案"""
    serializer_class = KidChildProfileSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            profile = KidChildProfile.objects.get(user=request.user)
        except KidChildProfile.DoesNotExist:
            return not_found(message='宝宝档案不存在')

        return success(data=KidChildProfileSerializer(profile).data)
