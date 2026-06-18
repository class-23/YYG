/**
 * 统一请求封装
 * - 自动注入 X-Device-Id 和 Authorization
 * - 统一错误处理（code != 0 视为业务错误）
 * - 401 自动跳转登录（小程序暂用 wx.showModal 提示）
 */
const { config } = require('./config');
const { getDeviceId } = require('./device');
const auth = require('./auth');

function buildHeaders(extra) {
  const headers = {
    'Content-Type': 'application/json',
    'X-Device-Id': getDeviceId(),
  };
  const token = auth.getToken();
  if (token) {
    headers['Authorization'] = 'Bearer ' + token;
  }
  if (extra) Object.assign(headers, extra);
  return headers;
}

function request(options) {
  const { url, method = 'GET', data, header, hideLoading = false } = options;
  const fullURL = (url.startsWith('http') ? url : config.baseURL + url);

  if (config.enableLog) {
    console.log(`[API] ${method} ${fullURL}`, data || '');
  }

  return new Promise((resolve, reject) => {
    wx.request({
      url: fullURL,
      method,
      data,
      header: buildHeaders(header),
      timeout: config.timeout,
      success: (res) => {
        if (config.enableLog) {
          console.log(`[API RES] ${method} ${fullURL}`, res.statusCode, res.data);
        }
        // HTTP 错误
        if (res.statusCode < 200 || res.statusCode >= 300) {
          wx.showToast({ title: '网络错误 ' + res.statusCode, icon: 'none' });
          reject(res);
          return;
        }
        // 业务错误统一格式：{ code, message, data }
        const body = res.data || {};
        if (body.code !== undefined && body.code !== 0) {
          // 401 未登录
          if (body.code === 10002) {
            auth.clearToken();
          }
          // 业务错误不弹 toast，由调用方决定
          reject(body);
          return;
        }
        resolve(body);
      },
      fail: (err) => {
        console.error(`[API FAIL] ${method} ${fullURL}`, err);
        wx.showToast({ title: '网络请求失败', icon: 'none' });
        reject(err);
      },
    });
  });
}

module.exports = {
  request,
  get:  (url, data, opt = {}) => request({ url, method: 'GET',  data, ...opt }),
  post: (url, data, opt = {}) => request({ url, method: 'POST', data, ...opt }),
  put:  (url, data, opt = {}) => request({ url, method: 'PUT',  data, ...opt }),
  del:  (url, data, opt = {}) => request({ url, method: 'DELETE', data, ...opt }),
};