/**
 * 邀请相关 API
 */
const { get, post } = require('../request');

module.exports = {
  codes() {
    return get('/invite/codes');
  },
  codesList() {
    return get('/invite/codes/list');
  },
  apply(payload) {
    return post('/invite/apply', payload);
  },
  records() {
    return get('/invite/records');
  },
};