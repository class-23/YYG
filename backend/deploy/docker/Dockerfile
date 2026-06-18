FROM python:3.11-slim

# 防止 Python 写入 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# 设置工作目录
WORKDIR /app

# 系统依赖（PostgreSQL 客户端、编译工具）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip 并安装 Python 依赖
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt && \
    pip install -i https://mirrors.aliyun.com/pypi/simple/ gunicorn==22.0.0

# 复制项目代码
COPY . /app/

# 创建非 root 用户
RUN useradd -m -s /bin/bash momapp && \
    chown -R momapp:momapp /app && \
    mkdir -p /app/logs /app/media /app/staticfiles && \
    chown -R momapp:momapp /app/logs /app/media /app/staticfiles

USER momapp

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -fsS http://localhost:8000/v1/admin-api/dashboard/ -H "X-Device-Id: healthcheck" || exit 1

# 默认启动命令（可被 docker-compose 覆盖）
CMD ["gunicorn", "mom_english_backend.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--worker-class", "sync", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
