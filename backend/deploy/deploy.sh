#!/bin/bash
# ============================================================
# 传统部署脚本（不使用 Docker）
# 适用于: 裸机部署、虚拟机部署、内网环境
# 组件: Python 3.11 + PostgreSQL 14 + Redis 7 + Nginx + Gunicorn + Supervisor
# ============================================================
set -e

APP_NAME="mom-english-backend"
APP_DIR="/opt/$APP_NAME"
APP_USER="momapp"
PYTHON_VERSION="3.11"
DOMAIN=${1:-api.yuanyuangao.com}

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()  { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查 root 权限
if [ "$EUID" -ne 0 ]; then
    err "请使用 root 权限运行: sudo bash $0"
    exit 1
fi

# ============================================================
# 1. 系统准备
# ============================================================
log "=== 1/8 系统依赖安装 ==="
apt-get update
apt-get install -y software-properties-common curl wget git vim \
    build-essential libpq-dev libssl-dev libffi-dev \
    postgresql postgresql-contrib \
    redis-server \
    nginx supervisor \
    certbot python3-certbot-nginx

# ============================================================
# 2. Python 3.11 安装
# ============================================================
log "=== 2/8 Python 3.11 安装 ==="
add-apt-repository -y ppa:deadsnakes/ppa 2>/dev/null || true
apt-get update
apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# ============================================================
# 3. 创建应用用户
# ============================================================
log "=== 3/8 创建应用用户 ==="
if ! id "$APP_USER" &>/dev/null; then
    useradd -m -s /bin/bash "$APP_USER"
fi

# ============================================================
# 4. 部署应用代码
# ============================================================
log "=== 4/8 部署应用代码 ==="
mkdir -p "$APP_DIR"
cp -r . "$APP_DIR/"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

# 创建 Python 虚拟环境
sudo -u "$APP_USER" python3.11 -m venv "$APP_DIR/venv"
sudo -u "$APP_USER" "$APP_DIR/venv/bin/pip" install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
sudo -u "$APP_USER" "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt" -i https://mirrors.aliyun.com/pypi/simple/
sudo -u "$APP_USER" "$APP_DIR/venv/bin/pip" install gunicorn==22.0.0 -i https://mirrors.aliyun.com/pypi/simple/

# ============================================================
# 5. PostgreSQL 配置
# ============================================================
log "=== 5/8 PostgreSQL 配置 ==="
systemctl enable postgresql
systemctl start postgresql

# 创建数据库和用户
sudo -u postgres psql <<EOF
CREATE DATABASE mom_english WITH ENCODING='UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8';
ALTER USER postgres PASSWORD '$(grep DB_PASSWORD /opt/$APP_NAME/.env 2>/dev/null | cut -d= -f2 || echo postgres)';
EOF

# 初始化 schema
sudo -u postgres psql -d mom_english -f "$APP_DIR/sql/init_schemas.sql"

# ============================================================
# 6. Redis 配置
# ============================================================
log "=== 6/8 Redis 配置 ==="
systemctl enable redis-server
systemctl start redis-server

# ============================================================
# 7. Supervisor 配置（Gunicorn 进程管理）
# ============================================================
log "=== 7/8 Supervisor 配置 ==="
cat > /etc/supervisor/conf.d/$APP_NAME.conf <<EOF
[program:$APP_NAME]
command=$APP_DIR/venv/bin/gunicorn mom_english_backend.wsgi:application --bind 127.0.0.1:8000 --workers 3 --worker-class sync --timeout 60 --access-logfile $APP_DIR/logs/access.log --error-logfile $APP_DIR/logs/error.log
directory=$APP_DIR
user=$APP_USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$APP_DIR/logs/supervisor.log
environment=
    PATH="$APP_DIR/venv/bin",
    DJANGO_SETTINGS_MODULE="mom_english_backend.settings",
    PYTHONUNBUFFERED="1"
EOF

supervisorctl reread
supervisorctl update
supervisorctl restart $APP_NAME

# 数据库迁移
sudo -u "$APP_USER" bash -c "cd $APP_DIR && venv/bin/python manage.py migrate --noinput"
sudo -u "$APP_USER" bash -c "cd $APP_DIR && venv/bin/python manage.py collectstatic --noinput"

# ============================================================
# 8. Nginx 配置
# ============================================================
log "=== 8/8 Nginx 配置 ==="
cp "$APP_DIR/deploy/nginx/nginx.conf" /etc/nginx/nginx.conf
cp "$APP_DIR/deploy/nginx/conf.d/api.conf" /etc/nginx/conf.d/

# 替换域名
sed -i "s/api.yuanyuangao.com/$DOMAIN/g" /etc/nginx/conf.d/api.conf

# 生成自签名证书（生产请用 Let's Encrypt 替换）
if [ ! -f "/etc/nginx/ssl/$DOMAIN.crt" ]; then
    mkdir -p /etc/nginx/ssl
    bash "$APP_DIR/deploy/nginx/ssl/generate-ssl.sh" "$DOMAIN"
fi

nginx -t
systemctl enable nginx
systemctl restart nginx

# ============================================================
# 完成
# ============================================================
log "================================================"
log "✅ 部署完成！"
log "================================================"
echo ""
echo "应用信息:"
echo "  域名: https://$DOMAIN"
echo "  应用目录: $APP_DIR"
echo "  进程管理: supervisorctl status $APP_NAME"
echo "  日志目录: $APP_DIR/logs/"
echo ""
echo "常用命令:"
echo "  查看状态: sudo supervisorctl status $APP_NAME"
echo "  重启应用: sudo supervisorctl restart $APP_NAME"
echo "  查看日志: sudo tail -f $APP_DIR/logs/error.log"
echo "  Django Admin: https://$DOMAIN/admin/"
echo ""
warn "下一步:"
echo "  1. 配置 /opt/$APP_NAME/.env 环境变量"
echo "  2. 创建超级管理员: cd $APP_DIR && sudo -u $APP_USER venv/bin/python manage.py createsuperuser"
echo "  3. 生产环境请使用 Let's Encrypt 替换自签名证书"
