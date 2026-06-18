/**
 * API 基础配置
 * 根据环境自动切换后端地址
 */

// ============================================================
// 环境配置
// ============================================================
const ENV = {
  DEV: 'development',
  TEST: 'test',
  PROD: 'production',
};

// 当前环境：开发期固定为 DEV（指向本机后端）
const CURRENT_ENV = ENV.DEV;

const ENV_CONFIG = {
  [ENV.DEV]: {
    // 本机后端（微信开发者工具中通过 localhost 访问）
    baseURL: 'http://localhost:8765/v1',
    enableLog: true,
    enableMock: true,
    timeout: 30000,
  },
  [ENV.TEST]: {
    // 测试环境：替换为你的测试服务器
    baseURL: 'https://api-test.yuanyuangao.com/v1',
    enableLog: true,
    enableMock: false,
    timeout: 20000,
  },
  [ENV.PROD]: {
    // 生产环境
    baseURL: 'https://api.yuanyuangao.com/v1',
    enableLog: false,
    enableMock: false,
    timeout: 15000,
  },
};

const config = ENV_CONFIG[CURRENT_ENV];

module.exports = {
  ENV,
  CURRENT_ENV,
  config,
};