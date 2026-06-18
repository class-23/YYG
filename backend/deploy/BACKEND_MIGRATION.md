# 宝妈英语早操小程序 · 后端迁移方案

> 完整的从开发环境到生产环境的迁移指南  
> 涵盖 Docker 部署、传统部署、数据库迁移、监控备份

---

## 目录

1. [架构总览](#1-架构总览)
2. [生产环境要求](#2-生产环境要求)
3. [Docker 部署（推荐）](#3-docker-部署推荐)
4. [传统部署](#4-传统部署)
5. [数据库迁移](#5-数据库迁移)
6. [HTTPS 证书配置](#6-https-证书配置)
7. [环境变量配置](#7-环境变量配置)
8. [监控与日志](#8-监控与日志)
9. [备份与恢复](#9-备份与恢复)
10. [前后端联调测试](#10-前后端联调测试)
11. [常见问题](#11-常见问题)

---

## 1. 架构总览

```
┌─────────────────────────────────────────────────┐
│                  微信小程序客户端                  │
│  (Taro 3.6.40 + api-utils)                       │
└────────────────────┬────────────────────────────┘
                     │ HTTPS (TLS 1.2+)
                     │ X-Device-Id / X-Platform
                     ▼
┌─────────────────────────────────────────────────┐
│         Nginx (反向代理 + HTTPS 终结)             │
│         - 静态文件服务                            │
│         - 限流 / 安全头                           │
└────────────────────┬────────────────────────────┘
                     │ proxy_pass
                     ▼
┌─────────────────────────────────────────────────┐
│         Gunicorn (WSGI) - 3 workers              │
│         Django 4.2 + DRF                         │
│         (mom-english-backend)                    │
└────────┬───────────────────┬────────────────────┘
         │                   │
         ▼                   ▼
┌──────────────┐    ┌──────────────────┐
│ PostgreSQL14 │    │   Redis 7        │
│ (13 schema)  │    │   (缓存/限流)     │
└──────────────┘    └──────────────────┘
```

### 1.1 端口规划

| 服务 | 端口 | 仅本地 | 用途 |
|------|------|--------|------|
| Nginx | 80 / 443 | 公开 | HTTPS 入口 |
| Gunicorn | 8000 | 127.0.0.1 | WSGI |
| PostgreSQL | 5432 | 127.0.0.1 | 数据库 |
| Redis | 6379 | 127.0.0.1 | 缓存 |

---

## 2. 生产环境要求

### 2.1 硬件（推荐）

| 角色 | CPU | 内存 | 磁盘 | 数量 |
|------|-----|------|------|------|
| Web 应用 | 2 核 | 4GB | 20GB SSD | 2 台（负载均衡） |
| 数据库 | 4 核 | 8GB | 100GB SSD | 1 主 1 备 |
| 缓存 | 2 核 | 4GB | 20GB SSD | 1 台 |

### 2.2 软件

| 软件 | 版本 | 用途 |
|------|------|------|
| Ubuntu Server | 22.04 LTS | 操作系统 |
| Python | 3.11+ | 运行时 |
| PostgreSQL | 14+ | 主数据库 |
| Redis | 7+ | 缓存 |
| Nginx | 1.18+ | 反向代理 |
| Gunicorn | 22.0+ | WSGI 服务器 |
| Supervisor | 4.2+ | 进程管理 |
| Let's Encrypt | - | SSL 证书 |

---

## 3. Docker 部署（推荐）

### 3.1 准备服务器

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo apt install -y docker-compose
```

### 3.2 上传代码

```bash
# 方式1: git clone
git clone https://git.yuanyuangao.com/mom-english-backend.git /opt/mom-english-backend

# 方式2: scp 上传
scp -r ./backend user@server:/opt/mom-english-backend
```

### 3.3 配置环境变量

```bash
cd /opt/mom-english-backend
cp .env.example .env
nano .env
```

### 3.4 启动服务

```bash
# 构建镜像并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f web

# 执行数据库迁移
docker-compose exec web python manage.py migrate

# 创建超级管理员
docker-compose exec web python manage.py createsuperuser
```

### 3.5 配置 SSL 证书

```bash
# 使用 certbot 自动申请 Let's Encrypt
docker-compose run --rm certbot certonly --webroot \
    --webroot-path /var/www/certbot \
    -d api.yuanyuangao.com

# 重启 nginx
docker-compose restart nginx
```

---

## 4. 传统部署

```bash
# 1. 上传代码
scp -r ./backend user@server:/tmp/

# 2. 执行部署脚本
ssh user@server
sudo mv /tmp/backend /opt/mom-english-backend
cd /opt/mom-english-backend
chmod +x deploy/deploy.sh
sudo bash deploy/deploy.sh api.yuanyuangao.com
```

部署脚本会自动完成：
- 系统依赖安装
- Python 虚拟环境
- PostgreSQL / Redis 配置
- Supervisor 进程管理
- Nginx 反向代理
- SSL 自签名证书（生产请用 Let's Encrypt 替换）

---

## 5. 数据库迁移

### 5.1 首次部署

```bash
# 1. 创建数据库
sudo -u postgres createdb mom_english -E UTF8

# 2. 创建 schema
sudo -u postgres psql -d mom_english -f sql/init_schemas.sql

# 3. Django 迁移
python manage.py migrate
```

### 5.2 数据导入（从开发环境导出）

```bash
# 导出开发库
pg_dump -h dev-host -U postgres -d mom_english -Fc -f backup.dump

# 导入生产库
pg_restore -h prod-host -U postgres -d mom_english --clean --if-exists backup.dump
```

### 5.3 Schema 迁移（无停机）

```bash
# 数据库迁移（自动检测差异）
python manage.py makemigrations
python manage.py migrate

# 大表加索引（不影响服务）
psql -d mom_english -c "CREATE INDEX CONCURRENTLY ..."
```

---

## 6. HTTPS 证书配置

### 6.1 Let's Encrypt（推荐）

```bash
# 安装 certbot
sudo apt install -y certbot python3-certbot-nginx

# 申请证书
sudo certbot --nginx -d api.yuanyuangao.com

# 自动续期（crontab）
echo "0 3 * * * certbot renew --quiet" | sudo crontab -
```

### 6.2 自签名证书（仅开发）

```bash
bash deploy/nginx/ssl/generate-ssl.sh api.yuanyuangao.com
```

---

## 7. 环境变量配置

参考 `.env.example`：

```bash
# Django
DJANGO_SECRET_KEY=使用 openssl rand -hex 32 生成
DJANGO_DEBUG=False  # 生产必须 False
DJANGO_ALLOWED_HOSTS=api.yuanyuangao.com

# 数据库
DB_NAME=mom_english
DB_USER=postgres
DB_PASSWORD=强密码
DB_HOST=127.0.0.1
DB_PORT=5432

# Redis
REDIS_URL=redis://:password@127.0.0.1:6379/0

# 微信小程序（本期可不填）
WECHAT_APPID=wx...
WECHAT_SECRET=...

# 跨域
CORS_ALLOWED_ORIGINS=https://servicewechat.com

# 加密密钥
SENSITIVE_FIELDS_KEY=32字节随机字符串
PHONE_ENCRYPT_KEY=32字节随机字符串
REQUEST_SIGN_KEY=32字节随机字符串

# 日志
LOG_LEVEL=INFO
```

---

## 8. 监控与日志

### 8.1 应用日志

```bash
# 实时查看
tail -f /opt/mom-english-backend/logs/error.log

# Nginx 访问日志
tail -f /var/log/nginx/api.yuanyuangao.com.access.log
```

### 8.2 进程监控

```bash
# Gunicorn 状态
supervisorctl status mom-english-backend

# 系统资源
top
free -h
df -h
```

### 8.3 数据库监控

```bash
# 连接数
psql -c "SELECT count(*) FROM pg_stat_activity;"

# 慢查询
psql -c "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"

# 表大小
psql -c "SELECT schemaname,tablename,pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema') ORDER BY pg_total_relation_size DESC LIMIT 20;"
```

### 8.4 推荐接入

- **Prometheus + Grafana**：指标可视化
- **Sentry**：应用异常监控
- **阿里云日志服务 / ELK**：集中日志

---

## 9. 备份与恢复

### 9.1 自动备份脚本

```bash
# /opt/scripts/backup.sh
#!/bin/bash
BACKUP_DIR="/var/backups/mom-english"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
pg_dump -U postgres -Fc mom_english > $BACKUP_DIR/db_$DATE.dump

# 保留最近 7 天
find $BACKUP_DIR -name "db_*.dump" -mtime +7 -delete
```

```bash
# crontab -e
0 2 * * * /opt/scripts/backup.sh
```

### 9.2 恢复

```bash
# 停服
supervisorctl stop mom-english-backend

# 恢复数据库
pg_restore -U postgres -d mom_english --clean --if-exists /var/backups/mom-english/db_20260618.dump

# 启动
supervisorctl start mom-english-backend
```

---

## 10. 前后端联调测试

详见 [INTEGRATION_TEST.md](file:///d:/Trae项目/YYG/backend/INTEGRATION_TEST.md)

测试要点：
- [x] 微信小程序域名白名单已配置
- [x] HTTPS 证书有效
- [x] 跨域请求正常
- [x] X-Device-Id 自动生成并传递
- [x] 各业务 API 联通
- [x] 错误码统一
- [x] 性能压测达标

---

## 11. 常见问题

### Q1: 502 Bad Gateway
Nginx 找不到 Gunicorn 进程。检查：
```bash
supervisorctl status mom-english-backend
curl http://127.0.0.1:8000/v1/users/me
```

### Q2: 数据库连接失败
```bash
# 检查 PostgreSQL 状态
systemctl status postgresql

# 检查 .env 中 DB_PASSWORD 是否正确
cat /opt/mom-english-backend/.env | grep DB_

# 测试连接
psql -U postgres -d mom_english
```

### Q3: CORS 跨域错误
生产环境必须配置具体域名，不能用 `*`：
```python
CORS_ALLOWED_ORIGINS = ['https://api.yuanyuangao.com', 'https://servicewechat.com']
```

### Q4: 微信小程序请求失败
1. 检查是否使用 HTTPS
2. 检查公众平台是否配置 request 合法域名
3. 开发期勾选"不校验合法域名"

### Q5: 性能优化建议
- 启用 Redis 缓存（`CACHES` 配置）
- 添加数据库索引（见 DATABASE.md §18）
- 启用 Gzip 压缩（Nginx 已配置）
- CDN 加速静态资源
- 读写分离（数据库主从）

---

## 附录：版本升级流程

1. 备份数据库
2. 拉取新代码
3. 更新依赖 `pip install -r requirements.txt`
4. 执行迁移 `python manage.py migrate`
5. 重启服务 `supervisorctl restart mom-english-backend`
6. 验证接口正常

---

## 联系

- 技术负责人：[姓名]
- 运维：[姓名]
- 紧急联系：[电话/微信]
