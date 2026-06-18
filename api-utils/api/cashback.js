/**
 * 返现相关 API
 */
const { get, post } = require('../request');

module.exports = {
  account() {
    return get('/cashback/account');
  },
  records() {
    return get('/cashback/records');
  },
};