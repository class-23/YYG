# 前后端集成测试方案

> 验证前后端分离部署后的数据交互完整性、响应速度、系统稳定性

---

## 1. 测试环境

| 环境 | 后端 | 前端 | 数据库 |
|------|------|------|--------|
| 开发 | localhost:8000 | 微信开发者工具 | PostgreSQL 14 |
| 测试 | api-test.yuanyuangao.com | 体验版小程序 | PostgreSQL 14 |
| 预发 | pre-api.yuanyuangao.com | 体验版小程序 | PostgreSQL 14 |
| 生产 | api.yuanyuangao.com | 正式版小程序 | PostgreSQL 14 |

---

## 2. 测试工具

```bash
# 1. 后端单元测试
cd /opt/mom-english-backend
source venv/bin/activate
python manage.py test apps -v 2

# 2. API 集成测试
pip install pytest pytest-django locust

# 3. 前端 Mock 测试（在源码项目）
npm install --save-dev jest
```

---

## 3. 自动化测试脚本

### 3.1 完整 API 联通性测试

`scripts/test_api_integration.py`：

```python
"""
前后端 API 集成测试
验证：跨域 / 鉴权 / 业务逻辑 / 性能
"""
import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://api.yuanyuangao.com/v1"
DEVICE_ID = f"test-device-{int(time.time())}"

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def check(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print(f"✅ {name}")
        else:
            self.failed += 1
            self.errors.append((name, detail))
            print(f"❌ {name}: {detail}")

r = TestResult()
session = requests.Session()
session.headers.update({
    'X-Device-Id': DEVICE_ID,
    'X-Platform': 'miniprogram',
    'Content-Type': 'application/json',
})

# ============================================================
# 1. 跨域测试
# ============================================================
print("\n=== 1. CORS 跨域测试 ===")
try:
    resp = session.options(f"{BASE_URL}/users/me")
    r.check("CORS 预检请求", 
            resp.status_code in (200, 204),
            f"status={resp.status_code}")
    r.check("CORS 允许 X-Device-Id 头",
            'x-device-id' in resp.headers.get('Access-Control-Allow-Headers', '').lower(),
            f"headers={resp.headers.get('Access-Control-Allow-Headers', '')}")
except Exception as e:
    r.check("CORS 预检请求", False, str(e))

# ============================================================
# 2. 设备 ID 匿名访问
# ============================================================
print("\n=== 2. 设备 ID 匿名访问 ===")
try:
    resp = session.get(f"{BASE_URL}/users/me")
    r.check("匿名获取用户资料", resp.status_code == 200, f"status={resp.status_code}")
    data = resp.json()
    r.check("返回 code=0", data.get('code') == 0)
except Exception as e:
    r.check("匿名获取用户资料", False, str(e))

# ============================================================
# 3. 业务 API 联通
# ============================================================
print("\n=== 3. 业务 API 联通 ===")

# 3.1 今日课程
try:
    resp = session.get(f"{BASE_URL}/lessons/today")
    r.check("获取今日课程", resp.status_code == 200)
    data = resp.json()
    r.check("返回 code=0", data.get('code') == 0)
except Exception as e:
    r.check("获取今日课程", False, str(e))

# 3.2 课程列表
try:
    resp = session.get(f"{BASE_URL}/courses/")
    r.check("获取课程列表", resp.status_code == 200)
except Exception as e:
    r.check("获取课程列表", False, str(e))

# 3.3 徽章列表
try:
    resp = session.get(f"{BASE_URL}/badges/")
    r.check("获取徽章列表", resp.status_code == 200)
except Exception as e:
    r.check("获取徽章列表", False, str(e))

# 3.4 蜕变广场
try:
    resp = session.get(f"{BASE_URL}/square/posts/", params={"page": 1, "page_size": 10})
    r.check("获取广场动态", resp.status_code == 200)
    data = resp.json()
    r.check("返回 data.list", 'list' in (data.get('data') or {}))
except Exception as e:
    r.check("获取广场动态", False, str(e))

# 3.5 计划列表
try:
    resp = session.get(f"{BASE_URL}/plans/")
    r.check("获取计划列表", resp.status_code == 200)
except Exception as e:
    r.check("获取计划列表", False, str(e))

# 3.6 打卡
try:
    resp = session.post(f"{BASE_URL}/checkins/", json={
        "reflection": "集成测试",
        "audio_played_seconds": 100,
    })
    r.check("创建打卡", resp.status_code in (200, 201))
    data = resp.json()
    r.check("返回 code=0", data.get('code') == 0)
except Exception as e:
    r.check("创建打卡", False, str(e))

# 3.7 错误处理
try:
    resp = session.get(f"{BASE_URL}/lessons/9999/")  # 不存在的 day
    data = resp.json()
    r.check("404 返回业务错误码", data.get('code') not in (0, None))
except Exception as e:
    r.check("错误处理", False, str(e))

# ============================================================
# 4. 性能压测
# ============================================================
print("\n=== 4. 性能压测 ===")
def make_request(_):
    try:
        start = time.time()
        resp = session.get(f"{BASE_URL}/lessons/today", timeout=5)
        return time.time() - start, resp.status_code
    except Exception as e:
        return 5.0, -1

with ThreadPoolExecutor(max_workers=20) as executor:
    start = time.time()
    results = list(executor.map(make_request, range(100)))
    total = time.time() - start

durations = [d for d, s in results if s == 200]
r.check("100 并发请求成功",
        len(durations) == 100,
        f"成功 {len(durations)}/100")
r.check("平均响应 < 500ms",
        (sum(durations) / len(durations)) < 0.5 if durations else False,
        f"avg={sum(durations)/len(durations)*1000:.1f}ms" if durations else "no data")
r.check("p99 响应 < 2s",
        (sorted(durations)[int(len(durations)*0.99)] if durations else 5) < 2,
        f"p99={sorted(durations)[int(len(durations)*0.99)]*1000:.1f}ms" if durations else "no data")

# ============================================================
# 5. 限流测试
# ============================================================
print("\n=== 5. 限流测试 ===")
# 快速发起 200 个请求，预期部分被限流
limited_count = 0
for i in range(200):
    try:
        resp = session.get(f"{BASE_URL}/badges/", timeout=2)
        if resp.status_code == 429:
            limited_count += 1
    except:
        pass
r.check("限流生效", limited_count > 0, f"限流次数: {limited_count}/200")

# ============================================================
# 汇总
# ============================================================
print(f"\n========================================")
print(f"通过: {r.passed}  失败: {r.failed}")
print(f"========================================")
if r.failed > 0:
    print("\n失败项:")
    for name, detail in r.errors:
        print(f"  - {name}: {detail}")
    exit(1)
```

### 3.2 前端小程序端测试

在小程序源码项目中：

```js
// test/api.test.js
const api = require('../api-utils');

describe('API 集成测试', () => {
  test('获取今日课程', async () => {
    const lesson = await api.lesson.getTodayLesson();
    expect(lesson).toHaveProperty('theme');
  });

  test('匿名用户创建打卡', async () => {
    const result = await api.checkin.createCheckin({
      reflection: 'test',
      audio_played_seconds: 60,
    });
    expect(result).toHaveProperty('biz_date');
  });

  test('X-Device-Id 自动生成', () => {
    const deviceId = api.getDeviceId();
    expect(deviceId).toMatch(/^[0-9a-f-]{36}$/);
  });
});
```

---

## 4. 测试清单

### 4.1 部署前功能验证

- [ ] 后端 `python manage.py check` 通过
- [ ] 12 个 app 的 migration 成功生成
- [ ] 所有 API 路径返回 200
- [ ] HTTPS 证书有效（curl -vI https://api.xxx.com）
- [ ] CORS 跨域正常
- [ ] Nginx 配置语法正确（nginx -t）

### 4.2 联调测试

- [ ] 微信小程序能成功发起请求
- [ ] 设备 ID 自动生成并持久化
- [ ] 各页面数据正常加载
- [ ] 错误提示正常显示
- [ ] 性能达标（< 500ms）

### 4.3 安全测试

- [ ] SQL 注入防护（已通过 ORM 防护）
- [ ] XSS 防护（DRF 自动转义）
- [ ] CSRF 防护（API 项目无需）
- [ ] 限流生效
- [ ] 敏感字段已加密
- [ ] 错误日志不泄露敏感信息

### 4.4 性能测试

- [ ] 单接口响应 < 500ms
- [ ] 100 并发无错误
- [ ] 1000 QPS 稳定运行
- [ ] 数据库连接池正常

---

## 5. 监控指标

部署后建议监控以下指标：

| 指标 | 阈值 | 监控方式 |
|------|------|----------|
| API 响应时间 p99 | < 2s | Nginx access log / APM |
| 错误率 | < 0.5% | 应用日志 |
| 数据库连接数 | < 80% | `pg_stat_activity` |
| CPU 使用率 | < 70% | top / Prometheus |
| 内存使用率 | < 80% | free / Prometheus |
| 磁盘使用率 | < 85% | df |
| 日志大小 | < 10GB | logrotate |

---

## 6. 故障演练

### 6.1 数据库故障

```bash
# 模拟数据库挂掉
sudo systemctl stop postgresql

# 观察：
# - 应用日志应记录数据库连接错误
# - 错误率应上升但服务不挂
# - 恢复后自动重连

# 恢复
sudo systemctl start postgresql
```

### 6.2 Redis 故障

```bash
sudo systemctl stop redis-server
# 观察：限流是否降级为不限制
sudo systemctl start redis-server
```

### 6.3 磁盘满

```bash
# 触发条件：日志未清理
df -h
# 清理
find /opt/mom-english-backend/logs -name "*.log" -mtime +30 -delete
```

---

## 7. 测试报告模板

每次发版前填写：

```markdown
## v1.x.x 测试报告

**测试时间**：YYYY-MM-DD
**测试人**：[姓名]
**测试环境**：测试 / 预发 / 生产

### 功能测试
| API | 期望 | 实际 | 通过 |
|-----|------|------|------|
| /users/me | 200 | 200 | ✅ |
| /lessons/today | 200 | 200 | ✅ |
| /checkins/ | 201 | 201 | ✅ |
| ... | | | |

### 性能测试
| 指标 | 目标 | 实际 | 通过 |
|------|------|------|------|
| 响应时间 p99 | < 2s | 800ms | ✅ |
| 100 并发 | 无错 | 无错 | ✅ |
| 1000 QPS | 稳定 | 稳定 | ✅ |

### 安全测试
- [x] 跨域配置正确
- [x] HTTPS 有效
- [x] 限流生效
- [x] 敏感字段加密
- [x] SQL 注入防护

### 结论
✅ 通过 / ❌ 不通过
```

---

## 8. 持续集成建议

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - python manage.py test
    - python scripts/test_api_integration.py

build:
  stage: build
  script:
    - docker build -t mom-english-backend:$CI_COMMIT_SHA .
    - docker push registry.yuanyuangao.com/mom-english-backend:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - ssh deploy@server "cd /opt/mom-english-backend && docker-compose pull && docker-compose up -d"
  only:
    - main
```
