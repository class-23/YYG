"""
社交层序列化器
"""
from rest_framework import serializers

from .models import (
    SisterTeam, SisterTeamMember, SisterTeamActivity,
    SisterTeamInteraction, SisterTeamEncouragement,
    SquarePost, SquarePostImage, SquarePostLike, SquarePostComment,
    LoveProfile, LoveFollow,
)


# ============================================================
# 小队相关序列化器
# ============================================================

class SisterTeamSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = SisterTeam
        fields = [
            'id', 'business_id', 'name', 'goal', 'max_members',
            'invite_code', 'team_consecutive_days', 'growth_value',
            'created_by', 'status', 'disbanded_at',
            'created_at', 'updated_at', 'member_count',
        ]
        read_only_fields = [
            'id', 'business_id', 'invite_code', 'team_consecutive_days',
            'growth_value', 'created_by', 'status', 'disbanded_at',
            'created_at', 'updated_at',
        ]

    def get_member_count(self, obj):
        return obj.members.filter(is_active=True).count()


class SisterTeamCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    goal = serializers.ChoiceField(choices=SisterTeam.Goal.choices)


class SisterTeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SisterTeamMember
        fields = [
            'id', 'team', 'user', 'role', 'joined_at',
            'left_at', 'total_checkin_days', 'is_active',
        ]
        read_only_fields = ['id', 'joined_at', 'total_checkin_days']


class SisterTeamActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SisterTeamActivity
        fields = [
            'id', 'team', 'user', 'biz_date', 'type', 'content',
            'hug_count', 'like_count', 'comment_count', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'hug_count', 'like_count', 'comment_count']


class InteractionCreateSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=SisterTeamInteraction.Action.choices)


class EncouragementCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=50)


# ============================================================
# 广场相关序列化器
# ============================================================

class SquarePostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SquarePostImage
        fields = ['id', 'url', 'sort']


class SquarePostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SquarePostComment
        fields = ['id', 'post', 'user', 'content', 'parent', 'created_at']
        read_only_fields = ['id', 'post', 'user', 'created_at']


class SquarePostSerializer(serializers.ModelSerializer):
    images = SquarePostImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = SquarePost
        fields = [
            'id', 'business_id', 'user', 'text', 'tag',
            'like_count', 'comment_count', 'audit_status',
            'is_anonymous', 'created_at', 'images', 'is_liked',
        ]
        read_only_fields = [
            'id', 'business_id', 'user', 'like_count', 'comment_count',
            'audit_status', 'created_at',
        ]

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return SquarePostLike.objects.filter(post=obj, user=request.user).exists()
        return False


class SquarePostCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500)
    tag = serializers.CharField(max_length=32, required=False, allow_blank=True)
    is_anonymous = serializers.BooleanField(default=False)
    images = serializers.ListField(
        child=serializers.URLField(max_length=512),
        required=False, max_length=9,
    )


# ============================================================
# 恋爱交友序列化器
# ============================================================

class LoveProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoveProfile
        fields = [
            'id', 'user', 'city', 'baby_stage', 'tags', 'bio',
            'show_real_name', 'is_unlocked', 'unlocked_at',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'user', 'is_unlocked', 'unlocked_at',
            'created_at', 'updated_at',
        ]


class LoveProfileUpdateSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=64, required=False, allow_blank=True)
    baby_stage = serializers.CharField(max_length=32, required=False, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    show_real_name = serializers.BooleanField(required=False)


class LoveFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoveFollow
        fields = ['id', 'from_user', 'to_user', 'created_at']
        read_only_fields = ['id', 'from_user', 'created_at']
