/**
 * 政策内容 API
 */
const { get } = require('../request');

module.exports = {
  list() {
    return get('/policies/');
  },
  detail(businessId) {
    return get('/policies/' + businessId);
  },
};