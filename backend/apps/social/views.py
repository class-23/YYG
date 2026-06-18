"""
社交层视图
小队 / 广场 / 恋爱交友
"""
from django.db import IntegrityError
from django.db.models import F
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.response import success, created, fail, not_found, bad_request
from .models import (
    SisterTeam, SisterTeamMember, SisterTeamActivity,
    SisterTeamInteraction, SisterTeamEncouragement,
    SquarePost, SquarePostImage, SquarePostLike, SquarePostComment,
    LoveProfile, LoveFollow,
)
from .serializers import (
    SisterTeamSerializer, SisterTeamCreateSerializer, SisterTeamMemberSerializer,
    SisterTeamActivitySerializer, InteractionCreateSerializer, EncouragementCreateSerializer,
    SquarePostSerializer, SquarePostCreateSerializer, SquarePostCommentSerializer,
    LoveProfileSerializer, LoveProfileUpdateSerializer, LoveFollowSerializer,
)


# ============================================================
# 小队相关视图
# ============================================================

class TeamCreateView(generics.CreateAPIView):
    """创建小队"""
    serializer_class = SisterTeamCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        # 检查用户是否已有活跃小队
        if SisterTeamMember.objects.filter(user=request.user, is_active=True).exists():
            return fail(message='你已在小队中，请先退出当前小队')

        team = SisterTeam.objects.create(
            name=ser.validated_data['name'],
            goal=ser.validated_data['goal'],
            created_by=request.user,
        )
        # 创建者自动成为队长
        SisterTeamMember.objects.create(
            team=team, user=request.user,
            role=SisterTeamMember.Role.LEADER,
        )
        return created(data=SisterTeamSerializer(team).data)


class TeamListView(generics.ListAPIView):
    """小队列表"""
    serializer_class = SisterTeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SisterTeam.objects.filter(status=SisterTeam.Status.ACTIVE)


class TeamDetailView(generics.RetrieveAPIView):
    """小队详情"""
    serializer_class = SisterTeamSerializer
    permission_classes = [IsAuthenticated]
    queryset = SisterTeam.objects.filter(status=SisterTeam.Status.ACTIVE)


class TeamJoinView(generics.CreateAPIView):
    """通过邀请码加入小队"""
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        invite_code = request.data.get('invite_code', '')
        if not invite_code:
            return bad_request(message='请提供邀请码')

        try:
            team = SisterTeam.objects.get(invite_code=invite_code, status=SisterTeam.Status.ACTIVE)
        except SisterTeam.DoesNotExist:
            return not_found(message='邀请码无效或小队已解散')

        # 检查是否已在该小队
        if SisterTeamMember.objects.filter(team=team, user=request.user, is_active=True).exists():
            return fail(message='你已在该小队中')

        # 检查是否在其他小队
        if SisterTeamMember.objects.filter(user=request.user, is_active=True).exists():
            return fail(message='你已在其他小队中，请先退出')

        # 检查小队是否满员
        if team.members.filter(is_active=True).count() >= team.max_members:
            return fail(message='小队已满员')

        try:
            SisterTeamMember.objects.create(team=team, user=request.user)
        except IntegrityError:
            return fail(message='加入失败，请稍后重试')

        return created(data=SisterTeamSerializer(team).data, message='加入成功')


class TeamActivityListView(generics.ListAPIView):
    """小队动态列表"""
    serializer_class = SisterTeamActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        team_id = self.kwargs['pk']
        return SisterTeamActivity.objects.filter(
            team_id=team_id,
        ).select_related('user').order_by('-biz_date', '-created_at')


class TeamInteractionCreateView(generics.CreateAPIView):
    """小队互动（点赞/拥抱/提醒）"""
    serializer_class = InteractionCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        activity_id = self.kwargs['pk']
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        try:
            activity = SisterTeamActivity.objects.get(id=activity_id)
        except SisterTeamActivity.DoesNotExist:
            return not_found(message='动态不存在')

        action = ser.validated_data['action']
        if activity.user == request.user:
            return fail(message='不能给自己互动')

        try:
            interaction = SisterTeamInteraction.objects.create(
                activity=activity,
                from_user=request.user,
                to_user=activity.user,
                action=action,
            )
        except IntegrityError:
            return fail(message='你已执行过该互动')

        # 更新计数
        if action == SisterTeamInteraction.Action.HUG:
            SisterTeamActivity.objects.filter(id=activity_id).update(hug_count=F('hug_count') + 1)
        elif action == SisterTeamInteraction.Action.LIKE:
            SisterTeamActivity.objects.filter(id=activity_id).update(like_count=F('like_count') + 1)

        return created(data={'id': interaction.id, 'action': action})


class TeamEncouragementCreateView(generics.CreateAPIView):
    """发送鼓励留言"""
    serializer_class = EncouragementCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        activity_id = self.kwargs['pk']
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        try:
            activity = SisterTeamActivity.objects.get(id=activity_id)
        except SisterTeamActivity.DoesNotExist:
            return not_found(message='动态不存在')

        if activity.user == request.user:
            return fail(message='不能给自己留言')

        encouragement = SisterTeamEncouragement.objects.create(
            activity=activity,
            from_user=request.user,
            to_user=activity.user,
            content=ser.validated_data['content'],
        )
        SisterTeamActivity.objects.filter(id=activity_id).update(
            comment_count=F('comment_count') + 1,
        )
        return created(data={'id': encouragement.id, 'content': encouragement.content})


# ============================================================
# 广场相关视图
# ============================================================

class SquarePostListView(generics.ListAPIView):
    """广场帖子列表"""
    serializer_class = SquarePostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = SquarePost.objects.filter(
            audit_status=SquarePost.AuditStatus.APPROVED,
            deleted_at__isnull=True,
        ).select_related('user').prefetch_related('images')

        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tag=tag)

        return queryset.order_by('-created_at')


class SquarePostCreateView(generics.CreateAPIView):
    """发布广场帖子"""
    serializer_class = SquarePostCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        post = SquarePost.objects.create(
            user=request.user,
            text=ser.validated_data['text'],
            tag=ser.validated_data.get('tag', ''),
            is_anonymous=ser.validated_data.get('is_anonymous', False),
        )

        # 保存图片
        images = ser.validated_data.get('images', [])
        for idx, url in enumerate(images):
            SquarePostImage.objects.create(post=post, url=url, sort=idx)

        return created(data=SquarePostSerializer(post, context={'request': request}).data)


class SquarePostLikeView(generics.CreateAPIView):
    """帖子点赞"""
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        try:
            post = SquarePost.objects.get(id=post_id, deleted_at__isnull=True)
        except SquarePost.DoesNotExist:
            return not_found(message='帖子不存在')

        like, created_flag = SquarePostLike.objects.get_or_create(
            post=post, user=request.user,
        )
        if not created_flag:
            return fail(message='你已点赞过该帖子')

        SquarePost.objects.filter(id=post_id).update(like_count=F('like_count') + 1)
        return success(message='点赞成功')


class SquarePostCommentView(generics.CreateAPIView):
    """帖子评论"""
    serializer_class = SquarePostCommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        try:
            post = SquarePost.objects.get(id=post_id, deleted_at__isnull=True)
        except SquarePost.DoesNotExist:
            return not_found(message='帖子不存在')

        content = request.data.get('content', '')
        if not content:
            return bad_request(message='评论内容不能为空')

        parent_id = request.data.get('parent')
        parent = None
        if parent_id:
            try:
                parent = SquarePostComment.objects.get(id=parent_id, post=post, deleted_at__isnull=True)
            except SquarePostComment.DoesNotExist:
                return not_found(message='父评论不存在')

        comment = SquarePostComment.objects.create(
            post=post, user=request.user,
            content=content, parent=parent,
        )
        SquarePost.objects.filter(id=post_id).update(comment_count=F('comment_count') + 1)
        return created(data=SquarePostCommentSerializer(comment).data)


# ============================================================
# 恋爱交友视图
# ============================================================

class LoveProfileView(generics.RetrieveUpdateAPIView):
    """交友资料（获取/更新）"""
    serializer_class = LoveProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = LoveProfile.objects.get_or_create(user=self.request.user)
        return profile

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        ser = LoveProfileUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        for field, value in ser.validated_data.items():
            setattr(profile, field, value)
        profile.save()

        return success(data=LoveProfileSerializer(profile).data)


class LoveListView(generics.ListAPIView):
    """交友列表"""
    serializer_class = LoveProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LoveProfile.objects.exclude(user=self.request.user).select_related('user')


class LoveFollowView(generics.CreateAPIView):
    """关注用户"""
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        to_user_id = self.kwargs.get('user_id')
        if str(to_user_id) == str(request.user.id):
            return fail(message='不能关注自己')

        follow, created_flag = LoveFollow.objects.get_or_create(
            from_user=request.user,
            to_user_id=to_user_id,
        )
        if not created_flag:
            return fail(message='你已关注该用户')

        return success(message='关注成功')
