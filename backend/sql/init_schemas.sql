-- ============================================================
-- 宝妈英语早操小程序 - PostgreSQL 数据库初始化脚本
-- ============================================================
-- 本脚本在第一次部署时执行一次,创建所有 schema 和扩展
-- 后续的表结构由 Django migration 管理
-- ============================================================

-- 启用必要的扩展
CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- 加密函数(手机号加密)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  -- UUID 生成
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- 模糊搜索

-- ============================================================
-- Schema 划分(按业务域)
-- ============================================================
CREATE SCHEMA IF NOT EXISTS core;             -- 用户/认证/资料
CREATE SCHEMA IF NOT EXISTS checkin;          -- 打卡/课程
CREATE SCHEMA IF NOT EXISTS finance;          -- 商业化(账户/支付/返现)
CREATE SCHEMA IF NOT EXISTS social;           -- 社交(小队/广场/交友)
CREATE SCHEMA IF NOT EXISTS mom_growth;       -- 妈妈成长
CREATE SCHEMA IF NOT EXISTS kid_assessment;   -- 孩子评估
CREATE SCHEMA IF NOT EXISTS policy;           -- 政策 CMS
CREATE SCHEMA IF NOT EXISTS incentive;        -- 激励(徽章/课程)
CREATE SCHEMA IF NOT EXISTS invite;           -- 邀请
CREATE SCHEMA IF NOT EXISTS message;          -- 消息
CREATE SCHEMA IF NOT EXISTS media;            -- 文件/海报
CREATE SCHEMA IF NOT EXISTS admin;            -- 后台账号/审计
CREATE SCHEMA IF NOT EXISTS dict;             -- 通用字典

-- 设置默认 search_path(供 Django 使用)
ALTER DATABASE mom_english SET search_path TO core,checkin,finance,social,mom_growth,kid_assessment,policy,incentive,invite,message,media,admin,dict,public;

-- ============================================================
-- 授权
-- ============================================================
-- 假设应用连接用户为 mom_app
GRANT ALL ON SCHEMA core TO PUBLIC;
GRANT ALL ON SCHEMA checkin TO PUBLIC;
GRANT ALL ON SCHEMA finance TO PUBLIC;
GRANT ALL ON SCHEMA social TO PUBLIC;
GRANT ALL ON SCHEMA mom_growth TO PUBLIC;
GRANT ALL ON SCHEMA kid_assessment TO PUBLIC;
GRANT ALL ON SCHEMA policy TO PUBLIC;
GRANT ALL ON SCHEMA incentive TO PUBLIC;
GRANT ALL ON SCHEMA invite TO PUBLIC;
GRANT ALL ON SCHEMA message TO PUBLIC;
GRANT ALL ON SCHEMA media TO PUBLIC;
GRANT ALL ON SCHEMA admin TO PUBLIC;
GRANT ALL ON SCHEMA dict TO PUBLIC;

-- 输出成功信息
DO $$
BEGIN
    RAISE NOTICE '✅ 所有 schema 创建完成';
    RAISE NOTICE '下一步: 配置 .env 环境变量, 然后运行: python manage.py migrate';
END $$;
