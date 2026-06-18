/**
 * JWT Token 管理
 */
const TOKEN_KEY = 'mom_english_token';
const REFRESH_KEY = 'mom_english_refresh_token';

function setToken(token, refresh) {
  try {
    if (token) wx.setStorageSync(TOKEN_KEY, token);
    if (refresh) wx.setStorageSync(REFRESH_KEY, refresh);
  } catch (e) {
    console.error('setToken error', e);
  }
}

function getToken() {
  try {
    return wx.getStorageSync(TOKEN_KEY) || '';
  } catch (e) {
    return '';
  }
}

function getRefreshToken() {
  try {
    return wx.getStorageSync(REFRESH_KEY) || '';
  } catch (e) {
    return '';
  }
}

function clearToken() {
  try {
    wx.removeStorageSync(TOKEN_KEY);
    wx.removeStorageSync(REFRESH_KEY);
  } catch (e) {
    console.error('clearToken error', e);
  }
}

module.exports = {
  setToken,
  getToken,
  getRefreshToken,
  clearToken,
};