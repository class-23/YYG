"""
敏感字段加密工具
- 使用 AES-256-GCM 加密手机号、身份证等 PII 数据
- 数据库存储密文，展示时使用脱敏字段
- 加密格式: base64(nonce + ciphertext + tag)
"""
import base64
import os
import hashlib
import hmac
import secrets
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.conf import settings


def _get_key() -> bytes:
    """获取 32 字节的加密密钥"""
    key = settings.SENSITIVE_FIELDS_KEY
    if isinstance(key, str):
        key = key.encode('utf-8')
    if len(key) != 32:
        # 兜底：使用 SHA-256 派生
        return hashlib.sha256(key).digest()
    return key


def encrypt_sensitive(plaintext: str) -> str:
    """
    加密敏感数据（如手机号）
    返回: base64(nonce(12字节) + ciphertext + tag(16字节))
    """
    if not plaintext:
        return ''

    key = _get_key()
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    return base64.b64encode(nonce + ciphertext).decode('ascii')


def decrypt_sensitive(ciphertext_b64: str) -> str:
    """
    解密敏感数据
    """
    if not ciphertext_b64:
        return ''

    try:
        key = _get_key()
        aesgcm = AESGCM(key)
        raw = base64.b64decode(ciphertext_b64.encode('ascii'))
        nonce = raw[:12]
        ciphertext = raw[12:]
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')
    except Exception:
        return ''


def mask_phone(phone: str) -> str:
    """手机号脱敏: 138****1234"""
    if not phone or len(phone) < 7:
        return phone or ''
    return f"{phone[:3]}****{phone[-4:]}"


def mask_id_card(id_card: str) -> str:
    """身份证脱敏: 110101****1234"""
    if not id_card or len(id_card) < 8:
        return id_card or ''
    return f"{id_card[:6]}****{id_card[-4:]}"


def hash_phone_sha256(phone: str) -> str:
    """手机号 SHA-256 哈希（用于去重统计）"""
    if not phone:
        return ''
    return hashlib.sha256(phone.encode('utf-8')).hexdigest()


# ============================================================
# 请求签名（HMAC-SHA256）
# ============================================================

def sign_request(method: str, path: str, body: str, timestamp: str, nonce: str) -> str:
    """
    计算请求签名（用于敏感操作）
    签名串: METHOD\nPATH\nTIMESTAMP\nNONCE\nBODY
    """
    sign_str = f"{method.upper()}\n{path}\n{timestamp}\n{nonce}\n{body}"
    secret = settings.REQUEST_SIGN_KEY.encode('utf-8')
    return hmac.new(secret, sign_str.encode('utf-8'), hashlib.sha256).hexdigest()


def verify_request_signature(
    method: str, path: str, body: str,
    timestamp: str, nonce: str, signature: str,
    max_age_seconds: int = 300,
) -> bool:
    """
    验证请求签名
    - 时间戳需在 5 分钟内（防重放）
    - nonce 防重放（需服务端缓存）
    """
    import time
    try:
        ts = int(timestamp)
    except (TypeError, ValueError):
        return False

    if abs(int(time.time()) - ts) > max_age_seconds:
        return False

    expected = sign_request(method, path, body, timestamp, nonce)
    return hmac.compare_digest(expected, signature or '')


def generate_nonce(length: int = 16) -> str:
    """生成请求 nonce"""
    return secrets.token_hex(length)
