#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
宝妈英语早操后端 - 一键启动器
========================================
直接运行 `python main.py` 即可启动整个后端服务

功能:
  1. 加载 .env 环境变量(可选)
  2. 等待数据库就绪
  3. 自动执行数据库迁移
  4. 创建超级管理员(如果不存在)
  5. 收集静态文件
  6. 启动 Django 服务

使用方式:
  开发:    python main.py
  生产:    python main.py --prod --workers 3
  自定义:  python main.py --port 8080 --host 0.0.0.0
  SQLite:  DB_ENGINE_OVERRIDE=sqlite python main.py
"""
import os
import sys
import time
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mom_english_backend.settings')

# 提前解析 --sqlite 参数（在 django.setup 前生效）
if '--sqlite' in sys.argv:
    os.environ['DB_ENGINE_OVERRIDE'] = 'sqlite'


# 颜色输出
class C:
    G = '\033[92m'
    Y = '\033[93m'
    R = '\033[91m'
    B = '\033[94m'
    M = '\033[95m'
    W = '\033[0m'
    BOLD = '\033[1m'


def log(level, msg):
    color = {'info': C.B, 'ok': C.G, 'warn': C.Y, 'err': C.R, 'step': C.M}
    print(f"{color.get(level, C.W)}[{level.upper():>4}]{C.W} {msg}", flush=True)


def load_env():
    env_path = os.path.join(BASE_DIR, '.env')
    if not os.path.exists(env_path):
        log('warn', '.env 不存在,使用环境变量 / 参考 .env.example 模板创建')
        return
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        log('ok', '.env 已加载')
    except Exception as e:
        log('warn', f'.env 加载失败: {e}')


def wait_database(max_retries=30, interval=2):
    db_engine = os.environ.get('DB_ENGINE_OVERRIDE', '').lower()
    if db_engine == 'sqlite':
        log('ok', '使用 SQLite 数据库,跳过连接检查')
        return True

    log('step', '等待 PostgreSQL 数据库就绪...')
    try:
        import psycopg2
    except ImportError:
        log('err', 'psycopg2 未安装: pip install psycopg2-binary')
        return False

    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = int(os.environ.get('DB_PORT', '5432'))
    db_name = os.environ.get('DB_NAME', 'mom_english')
    db_user = os.environ.get('DB_USER', 'postgres')
    db_password = os.environ.get('DB_PASSWORD', 'postgres')

    for i in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(
                host=db_host, port=db_port,
                user=db_user, password=db_password,
                dbname=db_name, connect_timeout=3,
            )
            conn.close()
            log('ok', f'数据库连接成功 ({db_host}:{db_port}/{db_name})')
            return True
        except psycopg2.OperationalError as e:
            if i == max_retries:
                log('err', f'数据库连接失败,已重试 {max_retries} 次')
                log('err', f'  最后错误: {e}')
                log('warn', '提示: 可使用 SQLite 启动: DB_ENGINE_OVERRIDE=sqlite python main.py')
                return False
            print(f'  [{i}/{max_retries}] 数据库未就绪,{interval}s 后重试...', flush=True)
            time.sleep(interval)
    return False


def run_migrate():
    log('step', '执行数据库迁移...')
    from django.core.management import call_command
    try:
        call_command('makemigrations', interactive=False, verbosity=0)
        log('ok', 'migration 已生成')
        call_command('migrate', interactive=False, verbosity=1)
        log('ok', '迁移完成')
        return True
    except Exception as e:
        log('err', f'迁移失败: {e}')
        return False


def collect_static():
    log('step', '收集静态文件...')
    from django.core.management import call_command
    try:
        call_command('collectstatic', interactive=False, verbosity=0)
        log('ok', '静态文件已收集')
    except Exception as e:
        log('warn', f'静态文件收集失败(可忽略): {e}')


def create_superuser_interactive():
    from django.contrib.auth import get_user_model
    from apps.core.models import User
    User = get_user_model()

    if User.objects.filter(is_admin=True).exists():
        log('ok', '超级管理员已存在,跳过')
        return

    log('step', '未检测到超级管理员,初始化创建...')
    print(f'\n{C.BOLD}=== 创建超级管理员 ==={C.W}')
    username = 'admin'
    nickname = '超级管理员'
    password = 'admin123456'
    email = ""

    try:
        user = User.objects.create(
            username=username,
            nickname=nickname,
            email=email or f'{username}@admin.local',
            is_admin=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password(password)
        user.save()
        log('ok', f'管理员 {username} 创建成功(密码: {password})')
        log('warn', '生产环境请立即修改默认密码!')
    except Exception as e:
        log('err', f'创建失败: {e}')


def run_django_dev_server(host, port):
    log('step', f'开发模式启动 {host}:{port}')
    from django.core.management import call_command
    call_command('runserver', f'{host}:{port}', '--noreload')


def run_gunicorn_server(host, port, workers):
    log('step', f'生产模式启动 (workers={workers})')
    try:
        from gunicorn.app.wsgiapp import WSGIApplication
        sys.argv = [
            'gunicorn',
            'mom_english_backend.wsgi:application',
            '--bind', f'{host}:{port}',
            '--workers', str(workers),
            '--worker-class', 'sync',
            '--timeout', '60',
            '--access-logfile', '-',
            '--error-logfile', '-',
        ]
        WSGIApplication().run()
    except ImportError:
        log('err', 'gunicorn 未安装: pip install gunicorn')
        log('warn', '降级为 Django runserver')
        run_django_dev_server(host, port)


def run_server(host='0.0.0.0', port=8000, prod=False, workers=3):
    if prod:
        run_gunicorn_server(host, port, workers)
    else:
        run_django_dev_server(host, port)


def main():
    parser = argparse.ArgumentParser(
        description='宝妈英语早操后端 - 一键启动器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--host', default='0.0.0.0', help='监听地址 (默认 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='监听端口 (默认 8000)')
    parser.add_argument('--prod', action='store_true', help='生产模式 (gunicorn)')
    parser.add_argument('--workers', type=int, default=3, help='生产模式 worker 数')
    parser.add_argument('--no-migrate', action='store_true', help='跳过数据库迁移')
    parser.add_argument('--no-static', action='store_true', help='跳过静态文件收集')
    parser.add_argument('--no-superuser', action='store_true', help='跳过超级管理员创建')
    parser.add_argument('--sqlite', action='store_true', help='使用 SQLite 数据库（开发模式）')
    args = parser.parse_args()

    print(f"""
{C.BOLD}{C.G}================================================
  宝妈英语早操 - 后端服务启动器
================================================{C.W}
  模式:     {'生产' if args.prod else '开发'}
  监听:     {args.host}:{args.port}
  数据库:   {os.environ.get('DB_ENGINE_OVERRIDE', 'postgresql')}
  DEBUG:    {os.environ.get('DJANGO_DEBUG', 'True')}
  Workers:  {args.workers if args.prod else 1}
""")

    # 1. 加载 .env
    load_env()

    # 2. 启动 Django
    try:
        import django
        django.setup()

        # 强制应用 DB_ENGINE_OVERRIDE
        if os.environ.get('DB_ENGINE_OVERRIDE', '').lower() == 'sqlite':
            from django.conf import settings as dj_settings
            from pathlib import Path as _P
            db_path = _P(BASE_DIR) / 'db.sqlite3'
            dj_settings.DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': str(db_path),
                }
            }
            # 关闭可能存在的旧连接
            from django.db import connections
            for conn in connections.all():
                conn.close()
            log('info', f'已切换到 SQLite: {db_path}')

        log('ok', f'Django {django.get_version()} 已加载')
    except Exception as e:
        log('err', f'Django 启动失败: {e}')
        sys.exit(1)

    # 3. 等待数据库
    if not wait_database():
        sys.exit(1)

    # 4. 数据库迁移
    if not args.no_migrate:
        if not run_migrate():
            sys.exit(1)

    # 5. 静态文件
    if not args.no_static:
        collect_static()

    # 6. 创建超级管理员(仅开发模式)
    if not args.prod and not args.no_superuser:
        try:
            create_superuser_interactive()
        except Exception as e:
            log('warn', f'跳过超级管理员: {e}')

    # 7. 启动服务
    print(f'\n{C.BOLD}{C.G}================================================{C.W}')
    log('ok', f'服务已启动: http://{args.host}:{args.port}/')
    log('ok', f'API 入口:    http://{args.host}:{args.port}/v1/')
    log('ok', f'Django Admin: http://{args.host}:{args.port}/admin/')
    print(f'{C.BOLD}{C.G}================================================{C.W}\n')

    run_server(
        host=args.host,
        port=args.port,
        prod=args.prod,
        workers=args.workers,
    )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{C.Y}服务已停止{C.W}')
        sys.exit(0)
