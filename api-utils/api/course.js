/**
 * 课程兑换相关 API
 */
const { get, post } = require('../request');

module.exports = {
  list() {
    return get('/courses/');
  },
  detail(id) {
    return get('/courses/' + id);
  },
  inquiries(id) {
    return get('/courses/' + id + '/inquiries');
  },
  exchange(id, payload) {
    return post('/courses/' + id + '/exchange', payload);
  },
};