"""
宝妈成长序列化器
"""
from rest_framework import serializers

from .models import MilestoneDefinition, UserMilestone, OfflineActivity, OfflineActivitySignup


class MilestoneDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilestoneDefinition
        fields = [
            'id', 'month', 'badge_level', 'label',
            'copy', 'required_days', 'is_active',
        ]


class UserMilestoneSerializer(serializers.ModelSerializer):
    milestone = MilestoneDefinitionSerializer(read_only=True)

    class Meta:
        model = UserMilestone
        fields = ['id', 'milestone', 'unlocked_at']


class OfflineActivitySerializer(serializers.ModelSerializer):
    remaining_seats = serializers.SerializerMethodField()

    class Meta:
        model = OfflineActivity
        fields = [
            'id', 'title', 'description', 'city', 'location',
            'start_at', 'end_at', 'max_seats', 'taken_seats',
            'cover', 'status', 'created_at', 'remaining_seats',
        ]

    def get_remaining_seats(self, obj):
        return max(obj.max_seats - obj.taken_seats, 0)
