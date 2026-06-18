# 宝妈英语早操小程序 · Django 后端

> 基于 Django 4.2 + DRF + PostgreSQL 14+ 的后端 API 服务  
> 完整对接 [API.md](../docs/API.md) 接口规范 和 [DATABASE.md](../docs/DATABASE.md) 数据库设计

---

## 目录结构

```
backend/
├── manage.py                       # Django 命令行入口
├── requirements.txt                # Python 依赖
├── .env.example                    # 环境变量模板
├── mom_english_backend/            # 项目配置
│   ├── settings.py                 # 全局配置
│   ├── urls.py                     # 根路由
│   └── wsgi.py
├── common/                         # 公共模块
│   ├── authentication.py           # JWT + 微信登录
│   ├── permissions.py              # 权限类
│   ├── exceptions.py               # 全局异常处理
│   ├── pagination.py               # 分页
│   ├── response.py                 # 统一响应
│   ├── middleware.py               # 请求日志中间件
│   ├── serializers.py              # 公共序列化器
│   └── utils.py                    # 工具函数
├── apps/                           # 业务应用(对应数据库 schema 划分)
│   ├── core/                       # 用户/认证/资料 (core schema)
│   ├── checkin/                    # 打卡/课程 (checkin schema)
│   ├── finance/                    # 计划/返现 (finance schema)
│   ├── incentive/                  # 徽章/课程 (incentive schema)
│   ├── social/                     # 社交(小队/广场/交友)
│   ├── mom_growth/                 # 妈妈成长计划
│   ├── kid_assessment/             # 孩子评估
│   ├── policy_app/                 # 政策 CMS
│   ├── invite/                     # 邀请
│   ├── message/                    # 消息
│   ├── media/                      # 文件/海报
│   └── admin_panel/                # 运营后台
├── sql/
│   └── init_schemas.sql            # PostgreSQL 初始化脚本
└── scripts/                        # 数据迁移与运维脚本
    └── migration/                  # 种子数据(参考 DATABASE.md 附录 D)
```

---

## 快速开始

### 1. 环境准备

- Python 3.10+
- PostgreSQL 14+
- (可选) Redis 6+

### 2. 安装依赖

```bash
cd backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 初始化数据库

```bash
# 创建数据库
psql -U postgres -c "CREATE DATABASE mom_english;"

# 创建 schema（13 个业务 schema）
psql -U postgres -d mom_english -f sql/init_schemas.sql
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入实际值
```

### 5. 生成数据库迁移并应用

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级管理员（后台登录用）

```bash
python manage.py createsuperuser
# 输入 openid（必填） / nickname / password
```

### 7. 启动开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

API 入口：`http://localhost:8000/v1/...`  
Django Admin：`http://localhost:8000/admin/`

---

## 关键技术决策

### 1. 12 个 Django App，对应 13 个 PostgreSQL Schema

| Django App | Schema | 主要功能 |
| --- | --- | --- |
| `core` | `core` | 用户/认证/资料/推送Token |
| `checkin` | `checkin` | 每日课程/打卡/子任务 |
| `finance` | `finance` | 计划/返现账户/流水 |
| `incentive` | `incentive` | 徽章/课程/兑换/咨询 |
| `social` | `social` | 姐妹小队/蜕变广场/同频交友 |
| `mom_growth` | `mom_growth` | 蜕变节点/同城活动 |
| `kid_assessment` | `kid_assessment` | 孩子阅读能力测评 |
| `policy_app` | `policy` | 政策内容 CMS |
| `invite` | `invite` | 邀请码/邀请记录 |
| `message` | `message` | 系统消息 |
| `media` | `media` | 文件上传/海报 |
| `admin_panel` | `admin` + `dict` | 后台账号/审计日志/字典 |

### 2. 统一响应格式

```json
{
  "code": 0,
  "message": "ok",
  "data": { ... }
}
```

错误码定义见 `common/exceptions.py` 的 `ERROR_CODES` 字典（与 API.md 对齐）。

### 3. JWT 认证

- 默认使用 `Authorization: Bearer <token>` 头
- Access token 有效期 7 天，Refresh token 30 天，自动轮换
- 自定义 token 中包含 `nickname`、`role` 字段

### 4. 微信登录流程

1. 客户端调用 `wx.login()` 获取 `code`
2. POST `/v1/auth/wechat-login` 提交 `code`
3. 后端调用微信 `jscode2session` 获取 `openid`
4. 自动注册/登录，返回 JWT

### 5. 本期不实现的模块

按 `DATABASE.md` §0 的指引，以下模块**本期不创建 migration**：

- `payment_order`（支付订单）
- `payment_refund`（退款）
- `withdraw_order`（提现订单）

返现可累计但**不可提现**；`cashback_record.type` 只允许 `earn` / `manual_adjust`。

### 6. 软删除

所有业务表保留 `deleted_at` 字段，由应用层处理（不物理删除）。

### 7. 金额单位

所有金额字段用 `BIGINT` 存储**分**（`price_cents` / `balance_cents`），绝不使用浮点数。  
前端展示时通过 `cents_to_yuan()` 转换为 `XX.XX` 字符串。

### 8. 业务主键

部分表使用 `business_id` 字段作为业务主键，格式为 `前缀_12位十六进制`（如 `usr_a1b2c3d4e5f6`）。  
通过 `common.utils.generate_business_id(prefix)` 生成。

---

## API 路由总览

| 路径 | 描述 |
| --- | --- |
| `POST /v1/auth/wechat-login` | 微信登录 |
| `GET /v1/users/me` | 当前用户资料 |
| `PUT /v1/users/me` | 更新用户资料 |
| `GET /v1/users/me/stats` | 用户统计 |
| `GET /v1/lessons/today` | 今日课程 |
| `GET /v1/lessons/{day}` | 指定天课程 |
| `POST /v1/checkins/` | 今日打卡 |
| `GET /v1/checkins/list` | 打卡历史 |
| `GET /v1/plans/` | 计划列表 |
| `POST /v1/plans/trial21/activate` | 激活21天体验 |
| `GET /v1/cashback/account` | 返现账户 |
| `GET /v1/cashback/records` | 返现流水 |
| `GET /v1/badges/` | 徽章列表 |
| `GET /v1/courses/` | 课程列表 |
| `POST /v1/courses/{id}/inquiries` | 课程咨询留资 |
| `POST /v1/courses/{id}/exchange` | 课程兑换 |
| `GET /v1/teams/` | 姐妹小队列表 |
| `POST /v1/teams/` | 创建小队 |
| `POST /v1/teams/join/` | 通过邀请码加入 |
| `GET /v1/square/posts/` | 蜕变广场动态 |
| `GET /v1/milestones/` | 蜕变节点定义 |
| `POST /v1/kid-assessment/submissions` | 提交孩子测评 |
| `GET /v1/policies/` | 政策列表 |
| `GET /v1/policies/{id}` | 政策详情 |
| `POST /v1/invite/codes/` | 生成邀请码 |
| `POST /v1/invite/apply/` | 使用邀请码 |
| `GET /v1/messages/` | 消息列表 |
| `POST /v1/files/upload` | 文件上传 |
| `POST /v1/posters/` | 生成海报 |
| `POST /v1/admin-api/login` | 后台登录 |
| `GET /v1/admin-api/dashboard` | 后台数据看板 |
| `POST /v1/admin-api/users/{id}/adjust-cashback` | 调整返现 |

---

## 日志

- 应用日志：`backend/logs/django.log`
- 错误日志：`backend/logs/error.log`
- 控制台输出（DEBUG 模式）

---

## 常见问题

### Q: 本地连接 PostgreSQL 失败
检查 `.env` 中 `DB_PASSWORD` 是否与本地 postgres 密码一致；  
如需重置：`psql -U postgres -c "ALTER USER postgres PASSWORD 'postgres';"`

### Q: 迁移时报 "Cannot serialize function: lambda"
确保所有 `default=lambda: ...` 改为 `default=''` 并在 `save()` 中生成业务ID。

### Q: 想重置整个数据库
```bash
psql -U postgres -c "DROP DATABASE mom_english;"
psql -U postgres -c "CREATE DATABASE mom_english;"
psql -U postgres -d mom_english -f sql/init_schemas.sql
python manage.py migrate
```

---

## 后续规划

1. 接入微信支付（启用 `payment_order` / `payment_refund` 表）
2. 用户提现功能（启用 `withdraw_order` 表）
3. Celery 异步任务（推送通知、统计报表）
4. OSS 文件存储对接
5. 数据仓库同步（Debezium → ClickHouse）

---

## License

Proprietary - 内部项目
