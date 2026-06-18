"""
返现与计划序列化器
"""
from rest_framework import serializers

from .models import Plan, UserPlan, CashbackAccount, CashbackRecord


class PlanSerializer(serializers.ModelSerializer):
    """计划 SKU 序列化器"""
    price_yuan = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = (
            'id', 'code', 'name', 'price_cents', 'price_yuan', 'duration_days',
            'cashback_per_day', 'course_reward_value_cents', 'max_badges',
            'description', 'is_active',
        )

    def get_price_yuan(self, obj):
        return f"{obj.price_cents / 100:.2f}"


class UserPlanSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = UserPlan
        fields = ('id', 'plan', 'status', 'started_at', 'expires_at', 'cancelled_at', 'created_at')


class CashbackAccountSerializer(serializers.ModelSerializer):
    """返现账户序列化器"""
    balance_yuan = serializers.SerializerMethodField()

    class Meta:
        model = CashbackAccount
        fields = (
            'id', 'balance_cents', 'balance_yuan', 'frozen_cents',
            'total_earned_cents', 'total_withdrawn_cents',
            'expected_cashback_cents', 'version', 'updated_at',
        )

    def get_balance_yuan(self, obj):
        return f"{obj.balance_cents / 100:.2f}"


class CashbackRecordSerializer(serializers.ModelSerializer):
    """返现流水序列化器"""
    amount_yuan = serializers.SerializerMethodField()

    class Meta:
        model = CashbackRecord
        fields = (
            'id', 'business_id', 'amount_cents', 'amount_yuan', 'type', 'source',
            'ref_id', 'biz_date', 'description', 'created_at',
        )

    def get_amount_yuan(self, obj):
        return f"{obj.amount_cents / 100:.2f}"
