/**
 * 用户相关 API
 */
const { get } = require('../request');

module.exports = {
  // 获取当前用户信息（未登录返回 null）
  me() {
    return get('/users/me');
  },
  // 获取用户统计
  myStats() {
    return get('/users/me/stats');
  },
  // 我的推送 token
  pushTokens() {
    return get('/users/me/push-tokens');
  },
  // 微信登录：wx.login → /v1/auth/wx-login
  wxLogin(code, userInfo) {
    const { post } = require('../request');
    return post('/auth/wx-login', { code, userInfo });
  },
};