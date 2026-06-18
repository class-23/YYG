/**
 * API 工具统一入口
 * 在小程序入口（app.js）中引入一次：
 *   const api = require('./api-utils');
 *   api.init();
 * 之后页面可通过 getApp().globalData.api 访问。
 */
const api = require('./api');
const { config, ENV, CURRENT_ENV } = require('./config');
const { getDeviceId } = require('./device');
const auth = require('./auth');
const { request } = require('./request');

function init() {
  // 把 API 对象挂到小程序的 globalData 上
  if (typeof getApp === 'function') {
    const app = getApp();
    if (app && app.globalData) {
      app.globalData.api = api;
      app.globalData.auth = auth;
      app.globalData.config = config;
      app.globalData.deviceId = getDeviceId();
    }
  }
  if (config.enableLog) {
    console.log('[API] 已初始化', { env: CURRENT_ENV, baseURL: config.baseURL, deviceId: getDeviceId() });
  }
}

module.exports = {
  init,
  api,
  auth,
  config,
  ENV,
  CURRENT_ENV,
  request,
  getDeviceId,
};