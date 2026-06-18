"""
通用工具函数
"""
import uuid
import hashlib
import secrets
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))


def generate_business_id(prefix: str) -> str:
    """生成业务主键，形如: usr_xxxxxxxx"""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def generate_invite_code(length=8) -> str:
    """生成邀请码"""
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    return ''.join(secrets.choice(chars) for _ in range(length))


def now_cst() -> datetime:
    """获取当前东八区时间"""
    return datetime.now(CST)


def today_cst() -> datetime.date:
    """获取当前东八区日期"""
    return now_cst().date()


def mask_phone(phone: str) -> str:
    """手机号脱敏: 138****1234"""
    if not phone or len(phone) < 7:
        return phone
    return f"{phone[:3]}****{phone[-4:]}"


def hash_phone(phone: str) -> str:
    """手机号 SHA-256 哈希"""
    return hashlib.sha256(phone.encode('utf-8')).hexdigest()


def cents_to_yuan(cents: int) -> str:
    """分转元，保留两位小数"""
    return f"{cents / 100:.2f}"


def yuan_to_cents(yuan: float) -> int:
    """元转分"""
    return int(yuan * 100)
