/**
 * 文件上传 API
 */
const { config } = require('../config');
const { getDeviceId } = require('../device');
const auth = require('../auth');

function uploadFile(filePath, formData) {
  const token = auth.getToken();
  const header = { 'X-Device-Id': getDeviceId() };
  if (token) header['Authorization'] = 'Bearer ' + token;

  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: config.baseURL + '/files/upload',
      filePath,
      name: 'file',
      formData: formData || {},
      header,
      success: (res) => {
        try {
          const body = JSON.parse(res.data);
          if (body.code === 0) resolve(body);
          else reject(body);
        } catch (e) {
          reject(res);
        }
      },
      fail: (err) => {
        console.error('[API UPLOAD FAIL]', err);
        reject(err);
      },
    });
  });
}

module.exports = { uploadFile };