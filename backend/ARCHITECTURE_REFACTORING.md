# 前后端分离架构改造方案

> 项目：宝妈英语早操小程序（mom-english-taro）  
> 时间：2026-06-18  
> 状态：已落地

---

## 一、改造背景

### 1.1 原架构

```
┌─────────────────────────────────┐
│   Taro 编译产物（dist/）           │
│   - 微信小程序原生运行              │
│   - 所有数据均为前端 mock           │
│   - 业务逻辑写在 common.js 中     │
│   - 数据持久化用 wx.setStorageSync │
└─────────────────────────────────┘
```

**问题**：
- 业务数据写死在前端代码中，无法统一管理
- localStorage 数据无法跨设备同步
- 无法做 A/B 测试、个性化推荐
- 运营无法独立更新课程、政策、徽章等内容
- 业务代码臃肿、修改成本高

### 1.2 新架构（已实施）

```
┌─────────────────────────────────┐
│  微信小程序（前端）                │
│  - Taro 3.6.40                   │
│  - api-utils/（统一 API 调用）    │
│  - X-Device-Id 匿名身份           │
│  - HTTPS + 域名白名单             │
└────────────────┬────────────────┘
                 │ HTTPS
                 ▼
┌─────────────────────────────────┐
│  Nginx（反向代理）                │
│  - HTTPS 终结                    │
│  - 跨域 / 限流 / 安全头            │
│  - 静态文件服务                   │
└────────────────┬────────────────┘
                 │ proxy_pass
                 ▼
┌─────────────────────────────────┐
│  Django + DRF（后端）            │
│  - 12 个 App / 13 个 Schema     │
│  - JWT + X-Device-Id 混合鉴权   │
│  - PostgreSQL 14 + Redis 7     │
│  - Gunicorn 3 workers           │
└────────────────┬────────────────┘
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
┌──────────────┐    ┌──────────────┐
│ PostgreSQL14 │    │   Redis 7    │
│ 13 schemas   │    │ Cache/Limit  │
└──────────────┘    └──────────────┘
```

---

## 二、本期 MVP 范围（依据 API.md）

### 2.1 本期实现的接口

✅ 用户模块
- `GET /v1/users/me` - 获取当前用户
- `PUT /v1/users/me` - 更新用户资料
- `GET /v1/users/me/stats` - 用户统计
- `POST /v1/users/me/push-tokens` - 注册推送

✅ 课程与打卡
- `GET /v1/lessons/today` - 今日课程
- `GET /v1/lessons/{day}` - 指定天课程
- `GET /v1/lessons/{day}/play-log` - 播放日志
- `POST /v1/checkins/` - 创建打卡
- `GET /v1/checkins/list/` - 打卡历史

✅ 计划与返现
- `GET /v1/plans/` - 计划列表
- `POST /v1/plans/trial21/activate/` - 激活 21 天（需邀请 3 人）
- `GET /v1/cashback/account/` - 返现账户
- `GET /v1/cashback/records/` - 返现流水

✅ 徽章与课程
- `GET /v1/badges/` `GET /v1/badges/me/` - 徽章
- `GET /v1/courses/` `GET /v1/courses/{id}/` - 课程
- `POST /v1/courses/{id}/inquiries/` - 课程咨询
- `POST /v1/courses/{id}/exchange/` - 课程兑换

✅ 社交
- `GET /v1/teams/` `POST /v1/teams/` `POST /v1/teams/join/` - 小队
- `GET /v1/square/posts/` `POST /v1/square/posts/` - 广场
- `GET /v1/love/profile/` `GET /v1/love/list/` - 交友

✅ 妈妈成长
- `GET /v1/milestones/` `GET /v1/milestones/me/` - 蜕变节点
- `GET /v1/milestones/activities/` - 同城活动

✅ 孩子评估
- `GET /v1/kid-assessment/templates/` - 测评模板
- `POST /v1/kid-assessment/submissions/` - 提交测评

✅ 政策、邀请、消息、文件、海报、后台
- 全部实现

### 2.2 本期不实现的接口（依据 API.md §0）

⛔ 微信登录 `POST /v1/auth/wechat-login`  
⛔ 微信支付 `POST /v1/payments/*`  
⛔ 提现 `POST /v1/account/cashback/withdraw`  
⛔ 付费开通 365 天 `POST /v1/plans/year365/activate`（仅运营后台手工开通）  
⛔ 退款相关接口  

---

## 三、前后端通信规范

### 3.1 协议与域名

- **必须 HTTPS**（生产环境）
- 基础路径：`https://api.yuanyuangao.com/v1`
- 开发环境：`http://localhost:8000/v1`

### 3.2 必带的请求头

| Header | 说明 | 必填 | 示例 |
|--------|------|------|------|
| `Content-Type` | 请求体类型 | 是 | `application/json` |
| `X-Device-Id` | 设备 UUID（匿名身份） | 是 | `xxxxxxxx-xxxx-4xxx-...` |
| `X-Platform` | 客户端平台 | 是 | `miniprogram` |
| `X-Client-Version` | 客户端版本 | 否 | `1.0.0` |
| `Authorization` | JWT Token（已登录时） | 否 | `Bearer eyJ0eXAi...` |

### 3.3 响应格式

成功：
```json
{ "code": 0, "message": "ok", "data": {...} }
```

错误：
```json
{ "code": 30001, "message": "今日已打卡", "data": null }
```

分页：
```json
{
  "code": 0,
  "data": {
    "list": [...],
    "pagination": { "page": 1, "page_size": 20, "total": 100, "total_pages": 5 }
  }
}
```

### 3.4 错误码体系

| 范围 | 模块 |
|------|------|
| 1xxxx | 通用（10001=参数错误、10002=未登录、10004=资源不存在、10007=服务器错误） |
| 2xxxx | 用户与认证 |
| 3xxxx | 打卡与课程（30001=已打卡） |
| 4xxxx | 计划（40004=邀请人数不足） |
| 5xxxx | 社交 / 课程（50002=小队已满、51004=操作过于频繁） |
| 6xxxx | 邀请 |
| 7xxxx | 政策 |
| 8xxxx | 评估 |

详见 [common/exceptions.py](file:///d:/Trae项目/YYG/backend/common/exceptions.py)

---

## 四、安全机制

### 4.1 传输层

- **HTTPS 强制**：生产环境必须使用 TLS 1.2+
- **证书管理**：Let's Encrypt 自动续期
- **HSTS**：强制 HTTPS 访问
- **CORS**：仅允许配置的来源（生产禁止 `*`）

### 4.2 鉴权

- **本期**：可选鉴权（未登录返回 200 + 空 data）
- **匿名身份**：X-Device-Id + SHA-256 哈希入库
- **未来**：JWT Token（access 7 天 / refresh 30 天）+ 微信登录

### 4.3 敏感数据加密

- **手机号**：AES-256-GCM 加密存储
- **身份证号**：AES-256-GCM 加密存储
- **展示时**：使用 `mask_*` 脱敏字段（如 `138****1234`）
- **统计去重**：SHA-256 哈希

详见 [common/crypto.py](file:///d:/Trae项目/YYG/backend/common/crypto.py)

### 4.4 限流

| 角色 | 限额 | 配置 |
|------|------|------|
| 匿名用户 | 100 次/分钟 | `AnonDeviceRateThrottle` |
| 登录用户 | 600 次/分钟 | `AuthedUserRateThrottle` |
| 写操作 | 30 次/分钟 | `WriteOperationThrottle` |

### 4.5 防护措施

- SQL 注入：Django ORM 参数化查询
- XSS：DRF 自动转义 JSON
- CSRF：API 项目无需（无 Cookie 会话）
- 安全响应头：X-Frame-Options / X-Content-Type-Options / HSTS
- 审计日志：所有管理操作记录 `admin_audit_log`

---

## 五、后端部署方案

### 5.1 推荐方案：Docker Compose

```bash
cd /opt/mom-english-backend
cp .env.example .env
# 编辑 .env
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

详见 [deploy/BACKEND_MIGRATION.md](file:///d:/Trae项目/YYG/backend/deploy/BACKEND_MIGRATION.md)

### 5.2 备选方案：传统部署

```bash
sudo bash deploy/deploy.sh api.yuanyuangao.com
```

### 5.3 关键文件

| 文件 | 用途 |
|------|------|
| [Dockerfile](file:///d:/Trae项目/YYG/backend/deploy/docker/Dockerfile) | Docker 镜像构建 |
| [docker-compose.yml](file:///d:/Trae项目/YYG/backend/deploy/docker/docker-compose.yml) | 容器编排 |
| [nginx.conf](file:///d:/Trae项目/YYG/backend/deploy/nginx/nginx.conf) | Nginx 主配置 |
| [api.conf](file:///d:/Trae项目/YYG/backend/deploy/nginx/conf.d/api.conf) | API 站点配置 |
| [deploy.sh](file:///d:/Trae项目/YYG/backend/deploy/deploy.sh) | 传统部署脚本 |
| [BACKEND_MIGRATION.md](file:///d:/Trae项目/YYG/backend/deploy/BACKEND_MIGRATION.md) | 完整迁移文档 |

---

## 六、前端集成步骤

### 6.1 在源码项目（推荐）

```bash
# 1. 将 api-utils 复制到源码项目
cp -r backend/api-utils frontend/src/utils/

# 2. 在页面中引用
# pages/daily/index.tsx
import api from '@/utils/api-utils';

useEffect(() => {
  api.lesson.getTodayLesson().then(lesson => setLesson(lesson));
}, []);
```

### 6.2 在现有 Taro 编译产物中

```bash
# 1. 将 api-utils 复制到 dist/
cp -r backend/api-utils dist/

# 2. 在 common.js 中引入
# 在 common.js 顶部
const api = require('./api-utils');

# 3. 替换页面中的 mock 数据为真实 API 调用
# 例如 pages/daily/index.js
const lesson = await api.lesson.getTodayLesson();
this.setData({ todayLesson: lesson });
```

### 6.3 切换环境

修改 `api-utils/config.js` 中的 `CURRENT_ENV`：

```js
const CURRENT_ENV = ENV.DEV;   // http://localhost:8000
const CURRENT_ENV = ENV.TEST;  // https://api-test.yuanyuangao.com
const CURRENT_ENV = ENV.PROD;  // https://api.yuanyuangao.com
```

### 6.4 微信小程序后台配置

发布前在微信公众平台「开发 - 开发管理 - 服务器域名」配置：
- request 合法域名：`api.yuanyuangao.com`
- uploadFile 合法域名：`api.yuanyuangao.com`

开发期可在微信开发者工具勾选「不校验合法域名」。

---

## 七、测试方案

### 7.1 后端单元测试

```bash
python manage.py test apps -v 2
```

### 7.2 集成测试

```bash
python scripts/test_api_integration.py
```

覆盖：
- CORS 跨域
- X-Device-Id 匿名访问
- 23+ 业务 API 联通
- 打卡写入
- 错误码统一
- 安全响应头
- 50 并发 × 5 轮性能压测

详见 [INTEGRATION_TEST.md](file:///d:/Trae项目/YYG/backend/INTEGRATION_TEST.md)

### 7.3 端到端测试

1. 在微信开发者工具中打开项目
2. 配置本地后端（修改 `api-utils/config.js` 为 `ENV.DEV`）
3. 启动后端：`python manage.py runserver`
4. 在小程序中点击每个页面，验证数据加载正常
5. 测试打卡、激活计划、留资等关键流程

---

## 八、迁移检查清单

### 8.1 数据迁移

- [ ] 旧系统的 localStorage 数据已上报
- [ ] 种子数据已通过 management command 导入
- [ ] 徽章、政策、计划等基础数据已就位

### 8.2 前端迁移

- [ ] api-utils 集成到源码项目
- [ ] 所有 mock 数据替换为 API 调用
- [ ] X-Device-Id 自动生成逻辑
- [ ] 错误提示与后端错误码统一
- [ ] 小程序后台域名白名单配置

### 8.3 后端部署

- [ ] PostgreSQL 13 个 schema 创建
- [ ] 12 个 app 的 migration 成功执行
- [ ] Nginx HTTPS 配置
- [ ] SSL 证书（Let's Encrypt）
- [ ] Supervisor / Docker 进程管理
- [ ] 日志目录创建并配置 logrotate
- [ ] 备份脚本配置
- [ ] 监控告警接入

### 8.4 联调验证

- [ ] CORS 测试通过
- [ ] 匿名访问测试通过
- [ ] 业务 API 全部 200
- [ ] 性能压测达标（p99 < 2s）
- [ ] 限流测试通过
- [ ] HTTPS 证书有效
- [ ] 跨域头正确

---

## 九、文件清单

### 9.1 后端新增文件

```
backend/
├── common/
│   ├── authentication.py        # ✅ 修改：可选 JWT + 设备 ID 匿名
│   ├── middleware.py            # ✅ 重写：日志 + 设备 ID 识别
│   ├── crypto.py                # ✅ 新增：敏感字段加密
│   ├── throttling.py            # ✅ 新增：限流配置
│   └── platform_check.py        # ✅ 新增：客户端能力探测
├── mom_english_backend/
│   └── settings.py              # ✅ 修改：CORS / 加密 / 中间件
├── api-utils/                   # ✅ 新增：前端 API 对接工具库
│   ├── index.js
│   ├── config.js
│   ├── request.js
│   ├── auth.js
│   ├── device.js
│   ├── README.md
│   └── api/  (15 个业务模块)
├── deploy/                      # ✅ 新增：部署方案
│   ├── docker/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── entrypoint.sh
│   ├── nginx/
│   │   ├── nginx.conf
│   │   ├── conf.d/api.conf
│   │   └── ssl/generate-ssl.sh
│   ├── supervisor/api.conf
│   ├── deploy.sh
│   └── BACKEND_MIGRATION.md
├── scripts/
│   └── test_api_integration.py  # ✅ 新增：集成测试
├── ARCHITECTURE_REFACTORING.md  # ✅ 新增：本文件
└── INTEGRATION_TEST.md          # ✅ 新增
```

### 9.2 前端待迁移

- [ ] `dist/api-utils/` 复制到前端项目
- [ ] `dist/common.js` 中替换 mock 为 API 调用
- [ ] 各页面的 `index.js` 中接入 API

---

## 十、风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| PostgreSQL 数据库迁移丢失 | 高 | 迁移前全量备份；先预发验证 |
| HTTPS 证书过期 | 中 | Let's Encrypt 自动续期（crontab） |
| API 性能不达标 | 中 | Redis 缓存、数据库索引、Nginx 限流 |
| 跨域被浏览器拦截 | 低 | 正确配置 CORS，OPTIONS 预检通过 |
| 敏感信息泄露 | 高 | AES-256-GCM 加密 + 脱敏展示 |
| 微信小程序域名白名单遗漏 | 中 | 上线前检查所有域名 |
| 旧 localStorage 数据 | 低 | 通过 `/users/me/migrate` 接口批量上报 |

---

## 十一、后续规划（v2）

1. **接入微信登录**：解除 API.md §0 中的微信登录禁制
2. **接入微信支付**：启用 `payment_order` / `payment_refund` 表
3. **用户提现**：启用 `withdraw_order` 表
4. **CDN 加速**：静态资源 + 文件上传接入 OSS/CDN
5. **异步任务**：Celery + Redis 处理推送通知、统计报表
6. **数据仓库**：Debezium → ClickHouse 同步
7. **多语言**：i18n 国际化
8. **A/B 测试**：按用户分桶测试不同功能

---

## 联系

- 文档：d:\Trae项目\YYG\backend\ARCHITECTURE_REFACTORING.md
- API 规范：d:\Trae项目\YYG\docs\API.md
- 数据库设计：d:\Trae项目\YYG\docs\DATABASE.md
- 微信开发规范：d:\Trae项目\YYG\docs\MINIPROGRAM_DEV.md
