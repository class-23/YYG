/**
 * 徽章相关 API
 */
const { get } = require('../request');

module.exports = {
  list() {
    return get('/badges/');
  },
  my() {
    return get('/badges/me');
  },
};