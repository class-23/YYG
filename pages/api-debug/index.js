/**
 * API 调试页 - 端到端验证前后端连通
 * 入口：从首页（或任意页）navigateTo 到 /pages/api-debug/index
 * 测试接口：
 *   - GET /v1/users/me/         （匿名用户：code=0, data=null）
 *   - GET /v1/users/me/stats/   （未登录统计）
 */
Page({
  data: {
    baseURL: '',
    deviceId: '',
    log: [],
    responseText: '',
    loading: false,
  },

  onLoad() {
    const app = getApp();
    const api = app && app.globalData && app.globalData.api;
    this.setData({
      baseURL: (app && app.globalData && app.globalData.config && app.globalData.config.baseURL) || '未初始化',
      deviceId: (app && app.globalData && app.globalData.deviceId) || '未生成',
      apiReady: !!api,
    });
    this.appendLog('页面加载完成');
    if (!api) {
      this.appendLog('❌ API 未初始化！请检查 app.js 是否已注入 require("./api-utils").init()');
    } else {
      this.appendLog('✓ API 工具已就绪');
    }
  },

  async callMe() {
    const app = getApp();
    if (!app.globalData.api) { return; }
    this.setData({ loading: true });
    this.appendLog('→ GET /v1/users/me/');
    try {
      const res = await app.globalData.api.user.me();
      const text = JSON.stringify(res, null, 2);
      this.appendLog('✓ 200 响应：' + text);
      this.setData({ responseText: text });
    } catch (e) {
      const text = JSON.stringify(e, null, 2);
      this.appendLog('✗ 错误：' + text);
      this.setData({ responseText: text });
    } finally {
      this.setData({ loading: false });
    }
  },

  async callStats() {
    const app = getApp();
    if (!app.globalData.api) { return; }
    this.setData({ loading: true });
    this.appendLog('→ GET /v1/users/me/stats/');
    try {
      const res = await app.globalData.api.user.myStats();
      const text = JSON.stringify(res, null, 2);
      this.appendLog('✓ 200 响应：' + text);
      this.setData({ responseText: text });
    } catch (e) {
      const text = JSON.stringify(e, null, 2);
      this.appendLog('✗ 错误：' + text);
      this.setData({ responseText: text });
    } finally {
      this.setData({ loading: false });
    }
  },

  async testCORS() {
    const app = getApp();
    if (!app.globalData.api) { return; }
    this.setData({ loading: true });
    this.appendLog('→ OPTIONS 预检（验证 CORS）');
    try {
      const res = await new Promise((resolve, reject) => {
        wx.request({
          url: (app.globalData.config.baseURL) + '/users/me/',
          method: 'OPTIONS',
          header: {
            'X-Device-Id': app.globalData.deviceId,
            'Origin': 'https://servicewechat.com',
            'Access-Control-Request-Method': 'GET',
          },
          success: resolve,
          fail: reject,
        });
      });
      const text = 'HTTP ' + res.statusCode + '  header: ' + JSON.stringify(res.header, null, 2);
      this.appendLog('✓ ' + text);
      this.setData({ responseText: text });
    } catch (e) {
      this.appendLog('✗ 错误：' + JSON.stringify(e));
    } finally {
      this.setData({ loading: false });
    }
  },

  clearLog() {
    this.setData({ log: [], responseText: '' });
  },

  copyDeviceId() {
    wx.setClipboardData({ data: this.data.deviceId });
    wx.showToast({ title: '已复制', icon: 'success' });
  },

  appendLog(msg) {
    const ts = new Date().toLocaleTimeString();
    const log = this.data.log.concat(['[' + ts + '] ' + msg]);
    this.setData({ log: log.slice(-50) });
  },
});
