"""
Django settings for mom_english_backend project.
宝妈英语早操小程序后端配置
"""
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# 安全配置 - 生产环境应使用环境变量
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-change-me-in-production-env-key-2026'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

# ============================================================
# 安全配置（生产环境强制 HTTPS）
# ============================================================
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1', 'yes')
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False').lower() in ('true', '1', 'yes')
SECURE_HSTS_PRELOAD = os.environ.get('DJANGO_SECURE_HSTS_PRELOAD', 'False').lower() in ('true', '1', 'yes')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie 安全
SESSION_COOKIE_SECURE = os.environ.get('DJANGO_SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes')
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = os.environ.get('DJANGO_CSRF_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes')
CSRF_COOKIE_HTTPONLY = True

# ============================================================
# 应用注册
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 第三方
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',

    # 业务应用
    'apps.core',
    'apps.checkin',
    'apps.finance',
    'apps.social',
    'apps.mom_growth',
    'apps.kid_assessment',
    'apps.policy_app',
    'apps.incentive',
    'apps.invite',
    'apps.message',
    'apps.media',
    'apps.admin_panel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # API 项目通常禁用 CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'mom_english_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mom_english_backend.wsgi.application'

# ============================================================
# 数据库配置
# ============================================================
# 开发环境可设置 DB_ENGINE_OVERRIDE=sqlite 使用本地 SQLite
# 生产环境必须使用 PostgreSQL，并配合 init_schemas.sql 创建 schema
if os.environ.get('DB_ENGINE_OVERRIDE', '').lower() == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'mom_english'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
            'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'OPTIONS': {
                'options': '-c search_path=core,checkin,finance,social,mom_growth,kid_assessment,policy,incentive,invite,message,media,admin,dict,public',
            },
        }
    }
# 自定义用户模型
# ============================================================
AUTH_USER_MODEL = 'core.User'

# ============================================================
# 密码验证
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# ============================================================
# 国际化与时区
# ============================================================
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# ============================================================
# 静态文件
# ============================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# 默认主键类型
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# Django REST Framework 配置
# ============================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'common.authentication.JWTAuthenticationFromHeader',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # 本期可选鉴权：未登录返回 200 + 空 data
    ),
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.StandardPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
    'EXCEPTION_HANDLER': 'common.exceptions.custom_exception_handler',
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S+08:00',
    'DATE_FORMAT': '%Y-%m-%d',
    'NON_FIELD_ERRORS_KEY': 'message',
}

# ============================================================
# JWT 配置
# ============================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_OBTAIN_SERIALIZER': 'common.serializers.CustomTokenObtainSerializer',
}

# ============================================================
# 微信小程序配置
# ============================================================
# ⚠️ 本期不接入微信登录，保留配置供 v2 启用
WECHAT_APPID = os.environ.get('WECHAT_APPID', '')
WECHAT_SECRET = os.environ.get('WECHAT_SECRET', '')
WECHAT_LOGIN_URL = 'https://api.weixin.qq.com/sns/jscode2session'

# 微信小程序 AppID 列表（用于服务端校验）
WECHAT_MINIPROGRAM_APPIDS = [a.strip() for a in os.environ.get('WECHAT_APPIDS', '').split(',') if a.strip()]

# API 基础配置
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://api.yuanyuangao.com')
API_VERSION = 'v1'

# ============================================================
# CORS 跨域配置
# ============================================================
# 生产环境必须配置具体的允许来源，禁止使用通配符
CORS_ALLOW_ALL_ORIGINS = True

_cors_origins_raw = os.environ.get('CORS_ALLOWED_ORIGINS', '')
_cors_origins_list = [o.strip() for o in _cors_origins_raw.split(',') if o.strip()]
CORS_ALLOWED_ORIGINS = _cors_origins_list

# 允许携带凭证（Cookie / Authorization）
CORS_ALLOW_CREDENTIALS = True

# 允许的请求头
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-device-id',          # 设备 ID（匿名用户标识）
    'x-client-version',     # 客户端版本
    'x-platform',           # 平台：miniprogram / h5
]

# 允许的 HTTP 方法
CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]

# 预检请求缓存时间
CORS_PREFLIGHT_MAX_AGE = 86400

# 暴露给前端的响应头
CORS_EXPOSE_HEADERS = [
    'X-Request-ID',
    'X-Response-Time',
]

# ============================================================
# 日志配置
# ============================================================
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'apps': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ============================================================
# Redis 缓存（可选）
# ============================================================
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'

# ============================================================
# 文件上传配置
# ============================================================
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# ============================================================
# 加密配置
# ============================================================
PHONE_ENCRYPT_KEY = os.environ.get('PHONE_ENCRYPT_KEY', 'default-key-change-in-production-32b!')

# 敏感字段加密（使用 AES-256-GCM）
# 用于加密手机号、身份证等敏感 PII 数据
SENSITIVE_FIELDS_KEY = os.environ.get('SENSITIVE_FIELDS_KEY', 'change-me-to-32-byte-aes-key-here12345')
if len(SENSITIVE_FIELDS_KEY) != 32:
    # 自动截断或补齐到 32 字节
    SENSITIVE_FIELDS_KEY = (SENSITIVE_FIELDS_KEY + '0' * 32)[:32]

# 签名密钥（用于敏感操作的请求签名校验）
REQUEST_SIGN_KEY = os.environ.get('REQUEST_SIGN_KEY', 'change-me-in-production-sign-key')

# API 限流配置
API_RATE_LIMIT_ANONYMOUS = os.environ.get('API_RATE_LIMIT_ANONYMOUS', '100/min')   # 匿名用户
API_RATE_LIMIT_AUTHED = os.environ.get('API_RATE_LIMIT_AUTHED', '600/min')       # 登录用户
API_RATE_LIMIT_WRITE = os.environ.get('API_RATE_LIMIT_WRITE', '30/min')          # 写操作

# ============================================================
# 日志目录创建
# ============================================================
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
