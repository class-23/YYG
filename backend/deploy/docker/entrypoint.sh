#!/bin/bash
# ============================================================
# 后端容器启动脚本
# ============================================================
set -e

echo "==================================="
echo "宝妈英语早操 - 后端服务启动"
echo "==================================="

# 等待数据库就绪
echo "[1/5] 等待 PostgreSQL 就绪..."
for i in {1..30}; do
    if python -c "
import psycopg2
import os
try:
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        port=int(os.environ.get('DB_PORT', 5432)),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        dbname=os.environ.get('DB_NAME', 'mom_english'),
    )
    conn.close()
    print('OK')
except Exception as e:
    print(f'FAIL: {e}')
    exit(1)
"; then
        echo "数据库已就绪"
        break
    fi
    echo "等待数据库 ($i/30)..."
    sleep 2
done

# 执行数据库迁移
echo "[2/5] 执行数据库迁移..."
python manage.py migrate --noinput

# 收集静态文件
echo "[3/5] 收集静态文件..."
python manage.py collectstatic --noinput || true

# 创建超级管理员（如果未存在）
echo "[4/5] 检查超级管理员..."
python manage.py shell -c "
from apps.core.models import User
if not User.objects.filter(is_admin=True).exists():
    print('提示: 暂未创建超级管理员')
    print('请运行: docker-compose exec web python manage.py createsuperuser')
" || true

# 启动服务
echo "[5/5] 启动 Gunicorn..."
exec gunicorn mom_english_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --worker-class sync \
    --timeout 60 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile -
