/**
 * 计划相关 API
 */
const { get, post } = require('../request');

module.exports = {
  list() {
    return get('/plans/');
  },
  me() {
    return get('/plans/me');
  },
  // 激活 21 天试用
  activateTrial(payload) {
    return post('/plans/trial21/activate', payload);
  },
};