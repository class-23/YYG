/**
 * 设备 ID 管理
 * 用于匿名用户标识
 */
const STORAGE_KEY = 'mom_english_device_id';

function generateUUID() {
  // 简单的 UUID v4 生成
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function getDeviceId() {
  try {
    let id = wx.getStorageSync(STORAGE_KEY);
    if (!id) {
      id = generateUUID();
      wx.setStorageSync(STORAGE_KEY, id);
    }
    return id;
  } catch (e) {
    return generateUUID();
  }
}

module.exports = {
  getDeviceId,
  generateUUID,
};