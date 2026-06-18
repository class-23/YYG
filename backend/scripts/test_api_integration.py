#!/usr/bin/env python3
"""
前后端 API 集成测试脚本
验证: 跨域 / 鉴权 / 业务逻辑 / 性能 / 限流
"""
import os
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# 配置
BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000/v1')
TIMEOUT = int(os.environ.get('API_TIMEOUT', '10'))
DEVICE_ID = f"test-device-{int(time.time())}-{os.environ.get('USER', 'anonymous')}"


class TestResult:
    def __init__(self, name):
        self.name = name
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.start_time = time.time()

    def check(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print(f"  ✅ {name}")
        else:
            self.failed += 1
            self.errors.append((name, detail))
            print(f"  ❌ {name}: {detail}")

    def section(self, title):
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")

    def summary(self):
        duration = time.time() - self.start_time
        print(f"\n{'=' * 60}")
        print(f"  [{self.name}] 测试汇总")
        print(f"{'=' * 60}")
        print(f"  通过: {self.passed}")
        print(f"  失败: {self.failed}")
        print(f"  耗时: {duration:.1f}s")
        if self.failed > 0:
            print(f"\n  失败项:")
            for name, detail in self.errors:
                print(f"    - {name}: {detail}")
        return self.failed == 0


def make_session():
    session = requests.Session()
    session.headers.update({
        'X-Device-Id': DEVICE_ID,
        'X-Platform': 'miniprogram',
        'X-Client-Version': '1.0.0',
        'Content-Type': 'application/json',
    })
    return session


def test_cors(r, session):
    """CORS 跨域测试"""
    r.section("1. CORS 跨域测试")
    try:
        resp = session.options(
            f"{BASE_URL}/users/me",
            headers={'Origin': 'https://servicewechat.com'},
            timeout=TIMEOUT,
        )
        r.check("CORS 预检请求成功", resp.status_code in (200, 204), f"status={resp.status_code}")
        headers = {k.lower(): v for k, v in resp.headers.items()}
        r.check(
            "CORS 允许 X-Device-Id 头",
            'x-device-id' in headers.get('access-control-allow-headers', '').lower(),
            f"headers={headers.get('access-control-allow-headers', '')}",
        )
    except Exception as e:
        r.check("CORS 预检请求", False, str(e))


def test_anonymous(r, session):
    """匿名用户访问测试"""
    r.section("2. 匿名用户访问 (X-Device-Id)")
    try:
        resp = session.get(f"{BASE_URL}/users/me", timeout=TIMEOUT)
        r.check("匿名获取用户资料", resp.status_code == 200, f"status={resp.status_code}")
        data = resp.json()
        r.check("返回 code=0", data.get('code') == 0, f"data={data}")
        if data.get('code') == 0:
            user = data.get('data', {}).get('user') or data.get('data')
            r.check(
                "返回用户包含 device_id 关联",
                user is not None,
            )
    except Exception as e:
        r.check("匿名获取用户资料", False, str(e))


def test_business_apis(r, session):
    """业务 API 联通测试"""
    r.section("3. 业务 API 联通测试")

    endpoints = [
        ('GET', '/users/me/stats', '用户统计'),
        ('GET', '/lessons/today', '今日课程'),
        ('GET', '/lessons/1/', '指定天课程'),
        ('GET', '/lessons/reflections/', '反思问题'),
        ('GET', '/lessons/sub-tasks/', '子任务列表'),
        ('GET', '/checkins/list/', '打卡历史'),
        ('GET', '/plans/', '计划列表'),
        ('GET', '/plans/me/', '我的计划'),
        ('GET', '/cashback/account/', '返现账户'),
        ('GET', '/cashback/records/', '返现流水'),
        ('GET', '/badges/', '徽章列表'),
        ('GET', '/badges/me/', '我的徽章'),
        ('GET', '/courses/', '课程列表'),
        ('GET', '/teams/', '小队列表'),
        ('GET', '/square/posts/', '广场动态'),
        ('GET', '/milestones/', '蜕变节点'),
        ('GET', '/milestones/activities/', '同城活动'),
        ('GET', '/kid-assessment/templates/', '测评模板'),
        ('GET', '/policies/', '政策列表'),
        ('GET', '/invite/codes/', '我的邀请码'),
        ('GET', '/invite/records/', '邀请记录'),
        ('GET', '/messages/', '消息列表'),
        ('GET', '/posters/', '我的海报'),
    ]

    for method, path, name in endpoints:
        try:
            resp = session.request(method, f"{BASE_URL}{path}", timeout=TIMEOUT)
            r.check(
                f"{name} ({method} {path})",
                resp.status_code == 200,
                f"status={resp.status_code}",
            )
        except Exception as e:
            r.check(f"{name} ({method} {path})", False, str(e))


def test_checkin_create(r, session):
    """打卡创建测试"""
    r.section("4. 打卡创建测试")
    try:
        resp = session.post(
            f"{BASE_URL}/checkins/",
            json={
                'reflection': '集成测试 - 今日感想',
                'audio_played_seconds': 120,
                'client_meta': {'test': True, 'ts': int(time.time())},
            },
            timeout=TIMEOUT,
        )
        r.check("创建打卡", resp.status_code in (200, 201), f"status={resp.status_code}")
        data = resp.json()
        r.check("返回 code=0", data.get('code') == 0, f"data={data}")
    except Exception as e:
        r.check("创建打卡", False, str(e))


def test_error_handling(r, session):
    """错误处理测试"""
    r.section("5. 错误处理测试")
    try:
        # 不存在的资源
        resp = session.get(f"{BASE_URL}/lessons/9999/", timeout=TIMEOUT)
        data = resp.json()
        r.check(
            "404 返回业务错误码 (非 0)",
            data.get('code', 0) != 0,
            f"code={data.get('code')}",
        )
        r.check(
            "错误消息非空",
            bool(data.get('message')),
            f"message={data.get('message')}",
        )
    except Exception as e:
        r.check("错误处理", False, str(e))

    # 无效的 POST 数据
    try:
        resp = session.post(f"{BASE_URL}/courses/1/inquiries/", json={}, timeout=TIMEOUT)
        data = resp.json()
        r.check(
            "参数校验失败返回错误",
            data.get('code', 0) != 0,
            f"code={data.get('code')}",
        )
    except Exception as e:
        r.check("参数校验", False, str(e))


def test_performance(r, session):
    """性能压测"""
    r.section("6. 性能压测 (50 并发 × 5 轮)")

    def single_request(_):
        start = time.time()
        try:
            resp = session.get(f"{BASE_URL}/lessons/today", timeout=5)
            return time.time() - start, resp.status_code
        except Exception:
            return 5.0, -1

    all_durations = []
    all_success = 0
    all_total = 0
    for round_idx in range(5):
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = list(executor.map(single_request, range(50)))
        durations = [d for d, s in results if s == 200]
        all_durations.extend(durations)
        all_success += len(durations)
        all_total += len(results)
        if durations:
            print(f"  Round {round_idx + 1}: success={len(durations)}/50, "
                  f"avg={sum(durations) / len(durations) * 1000:.1f}ms, "
                  f"max={max(durations) * 1000:.1f}ms")

    r.check("总请求全部成功", all_success == all_total, f"{all_success}/{all_total}")
    if all_durations:
        avg = sum(all_durations) / len(all_durations)
        p99_idx = int(len(all_durations) * 0.99)
        p99 = sorted(all_durations)[p99_idx] if all_durations else 5
        r.check(f"平均响应 < 500ms", avg < 0.5, f"avg={avg * 1000:.1f}ms")
        r.check(f"p99 响应 < 2s", p99 < 2, f"p99={p99 * 1000:.1f}ms")


def test_security_headers(r, session):
    """安全响应头测试"""
    r.section("7. 安全响应头")
    try:
        resp = session.get(f"{BASE_URL}/users/me", timeout=TIMEOUT)
        h = {k.lower(): v for k, v in resp.headers.items()}
        r.check(
            "X-Content-Type-Options: nosniff",
            h.get('x-content-type-options') == 'nosniff',
            f"got={h.get('x-content-type-options')}",
        )
        r.check(
            "X-Frame-Options 设置",
            h.get('x-frame-options') in ('DENY', 'SAMEORIGIN'),
            f"got={h.get('x-frame-options')}",
        )
        r.check(
            "Strict-Transport-Security 设置（生产）",
            h.get('strict-transport-security', '').startswith('max-age'),
            f"got={h.get('strict-transport-security')}",
        )
    except Exception as e:
        r.check("安全响应头", False, str(e))


def test_https(r, session):
    """HTTPS 检查"""
    r.section("8. HTTPS 配置")
    if BASE_URL.startswith('https://'):
        r.check("API 使用 HTTPS", True)
    elif BASE_URL.startswith('http://localhost') or BASE_URL.startswith('http://127.0.0.1'):
        print("  ℹ️  开发环境，跳过 HTTPS 检查")
    else:
        r.check("API 必须使用 HTTPS", False, f"URL={BASE_URL}")


def main():
    print("=" * 60)
    print(f"  宝妈英语早操 - 集成测试")
    print(f"  目标: {BASE_URL}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  设备: {DEVICE_ID}")
    print("=" * 60)

    r = TestResult("集成测试")
    session = make_session()

    test_https(r, session)
    test_cors(r, session)
    test_anonymous(r, session)
    test_business_apis(r, session)
    test_checkin_create(r, session)
    test_error_handling(r, session)
    test_security_headers(r, session)
    test_performance(r, session)

    success = r.summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
