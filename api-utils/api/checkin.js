/**
 * 打卡相关 API
 */
const { get, post } = require('../request');

module.exports = {
  // 打卡列表
  list() {
    return get('/checkins/list');
  },
  // 今日打卡
  today() {
    return get('/checkins/');
  },
  // 按日期查
  byDate(bizDate) {
    return get('/checkins/' + bizDate);
  },
  // 提交打卡
  submit(payload) {
    return post('/checkins/', payload);
  },
};