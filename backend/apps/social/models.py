"""
社交层数据模型
小队 / 广场 / 恋爱交友
"""
from django.conf import settings
from django.db import models

from common.utils import generate_business_id, generate_invite_code, now_cst


# ============================================================
# 小队相关模型
# ============================================================

class SisterTeam(models.Model):
    """姐妹小队"""

    class Goal(models.TextChoices):
        EMOTION = 'emotion', '情绪管理'
        PARENT_CHILD_ENGLISH = 'parent_child_english', '亲自英语'
        SELF_GROWTH = 'self_growth', '自我成长'
        PERSISTENCE = 'persistence', '坚持打卡'

    class Status(models.TextChoices):
        ACTIVE = 'active', '活跃'
        DISBANDED = 'disbanded', '已解散'

    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    name = models.CharField('小队名称', max_length=64)
    goal = models.CharField('目标', max_length=32, choices=Goal.choices)
    max_members = models.IntegerField('最大成员数', default=5)
    invite_code = models.CharField('邀请码', max_length=16, unique=True)
    team_consecutive_days = models.IntegerField('小队连续打卡天数', default=0)
    growth_value = models.IntegerField('成长值', default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='created_teams', verbose_name='创建者',
    )
    status = models.CharField('状态', max_length=16, choices=Status.choices, default=Status.ACTIVE)
    disbanded_at = models.DateTimeField('解散时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'social_sister_team'
        verbose_name = '姐妹小队'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('team')
        if not self.invite_code:
            self.invite_code = generate_invite_code(16)
        super().save(*args, **kwargs)


class SisterTeamMember(models.Model):
    """小队成员"""

    class Role(models.TextChoices):
        LEADER = 'leader', '队长'
        MEMBER = 'member', '队员'

    team = models.ForeignKey(
        SisterTeam, on_delete=models.CASCADE,
        related_name='members', verbose_name='小队',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='team_memberships', verbose_name='用户',
    )
    role = models.CharField('角色', max_length=16, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField('加入时间', default=now_cst)
    left_at = models.DateTimeField('离开时间', null=True, blank=True)
    total_checkin_days = models.IntegerField('累计打卡天数', default=0)
    is_active = models.BooleanField('是否活跃', default=True)

    class Meta:
        db_table = 'social_sister_team_member'
        verbose_name = '小队成员'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_active=True),
                name='unique_active_team_per_user',
            ),
        ]

    def __str__(self):
        return f'{self.user} - {self.team}'


class SisterTeamActivity(models.Model):
    """小队动态（打卡记录）"""

    class Type(models.TextChoices):
        CHECKIN = 'checkin', '已打卡'
        PENDING = 'pending', '待打卡'

    team = models.ForeignKey(
        SisterTeam, on_delete=models.CASCADE,
        related_name='activities', verbose_name='小队',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='team_activities', verbose_name='用户',
    )
    biz_date = models.DateField('业务日期')
    type = models.CharField('类型', max_length=16, choices=Type.choices)
    content = models.CharField('内容', max_length=500, blank=True, null=True)
    hug_count = models.IntegerField('拥抱数', default=0)
    like_count = models.IntegerField('点赞数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'social_sister_team_activity'
        verbose_name = '小队动态'
        verbose_name_plural = verbose_name
        unique_together = [('team', 'user', 'biz_date')]

    def __str__(self):
        return f'{self.team} - {self.user} - {self.biz_date}'


class SisterTeamInteraction(models.Model):
    """小队互动（点赞/拥抱/提醒）"""

    class Action(models.TextChoices):
        HUG = 'hug', '拥抱'
        LIKE = 'like', '点赞'
        REMIND = 'remind', '提醒'

    activity = models.ForeignKey(
        SisterTeamActivity, on_delete=models.CASCADE,
        related_name='interactions', verbose_name='动态',
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sent_interactions', verbose_name='发起者',
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='received_interactions', verbose_name='接收者',
    )
    action = models.CharField('动作', max_length=16, choices=Action.choices)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'social_sister_team_interaction'
        verbose_name = '小队互动'
        verbose_name_plural = verbose_name
        unique_together = [('activity', 'from_user', 'action')]

    def __str__(self):
        return f'{self.from_user} -> {self.to_user} ({self.action})'


class SisterTeamEncouragement(models.Model):
    """小队鼓励留言"""

    activity = models.ForeignKey(
        SisterTeamActivity, on_delete=models.CASCADE,
        related_name='encouragements', verbose_name='动态',
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sent_encouragements', verbose_name='发送者',
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='received_encouragements', verbose_name='接收者',
    )
    content = models.CharField('内容', max_length=50)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'social_sister_team_encouragement'
        verbose_name = '小队鼓励'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}: {self.content}'


class SisterTeamRemindLog(models.Model):
    """小队提醒日志"""

    team = models.ForeignKey(
        SisterTeam, on_delete=models.CASCADE,
        related_name='remind_logs', verbose_name='小队',
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sent_reminds', verbose_name='发送者',
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='received_reminds', verbose_name='接收者',
    )
    biz_date = models.DateField('业务日期')
    channel = models.CharField('渠道', max_length=16, choices=[
        ('system_msg', '系统消息'),
        ('push', '推送'),
    ])
    sent_at = models.DateTimeField('发送时间', default=now_cst)

    class Meta:
        db_table = 'social_sister_team_remind_log'
        verbose_name = '提醒日志'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['team', 'from_user', 'to_user', 'biz_date'],
                name='unique_remind_per_day',
            ),
        ]

    def __str__(self):
        return f'{self.from_user} -> {self.to_user} ({self.biz_date})'


# ============================================================
# 广场相关模型
# ============================================================

class SquarePost(models.Model):
    """广场帖子"""

    class AuditStatus(models.TextChoices):
        PENDING = 'pending', '待审核'
        APPROVED = 'approved', '已通过'
        REJECTED = 'rejected', '已拒绝'

    business_id = models.CharField('业务ID', max_length=32, unique=True, default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='square_posts', verbose_name='用户',
    )
    text = models.CharField('内容', max_length=500)
    tag = models.CharField('标签', max_length=32, blank=True, null=True)
    like_count = models.IntegerField('点赞数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    audit_status = models.CharField(
        '审核状态', max_length=16,
        choices=AuditStatus.choices, default=AuditStatus.APPROVED,
    )
    is_anonymous = models.BooleanField('是否匿名', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    deleted_at = models.DateTimeField('删除时间', null=True, blank=True)

    class Meta:
        db_table = 'social_square_post'
        verbose_name = '广场帖子'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Post({self.business_id})'

    def save(self, *args, **kwargs):
        if not self.business_id:
            self.business_id = generate_business_id('sq')
        super().save(*args, **kwargs)


class SquarePostImage(models.Model):
    """帖子图片"""

    post = models.ForeignKey(
        SquarePost, on_delete=models.CASCADE,
        related_name='images', verbose_name='帖子',
    )
    url = models.CharField('图片URL', max_length=512)
    sort = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'social_square_post_image'
        verbose_name = '帖子图片'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return f'Image({self.post_id})'


class SquarePostLike(models.Model):
    """帖子点赞"""

    post = models.ForeignKey(
        SquarePost, on_delete=models.CASCADE,
        related_name='likes', verbose_name='帖子',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='square_likes', verbose_name='用户',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'social_square_post_like'
        verbose_name = '帖子点赞'
        verbose_name_plural = verbose_name
        unique_together = [('post', 'user')]

    def __str__(self):
        return f'Like({self.post_id}, {self.user_id})'


class SquarePostComment(models.Model):
    """帖子评论"""

    post = models.ForeignKey(
        SquarePost, on_delete=models.CASCADE,
        related_name='comments', verbose_name='帖子',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='square_comments', verbose_name='用户',
    )
    content = models.CharField('评论内容', max_length=500)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='replies', verbose_name='父评论',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    deleted_at = models.DateTimeField('删除时间', null=True, blank=True)

    class Meta:
        db_table = 'social_square_post_comment'
        verbose_name = '帖子评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Comment({self.post_id}, {self.user_id})'


# ============================================================
# 恋爱交友相关模型
# ============================================================

class LoveProfile(models.Model):
    """交友资料"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='love_profile', verbose_name='用户',
    )
    city = models.CharField('城市', max_length=64, blank=True, null=True)
    baby_stage = models.CharField('宝宝阶段', max_length=32, blank=True, null=True)
    tags = models.JSONField('标签', default=list)
    bio = models.CharField('个人简介', max_length=500, blank=True, null=True)
    show_real_name = models.BooleanField('是否显示真名', default=False)
    is_unlocked = models.BooleanField('是否已解锁', default=False)
    unlocked_at = models.DateTimeField('解锁时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'social_love_profile'
        verbose_name = '交友资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'LoveProfile({self.user_id})'


class LoveFollow(models.Model):
    """交友关注"""

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='love_following', verbose_name='关注者',
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='love_followers', verbose_name='被关注者',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'social_love_follow'
        verbose_name = '交友关注'
        verbose_name_plural = verbose_name
        unique_together = [('from_user', 'to_user')]

    def __str__(self):
        return f'Follow({self.from_user_id} -> {self.to_user_id})'
