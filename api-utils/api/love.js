/**
 * 爱人连接 API
 */
const { get, post } = require('../request');

module.exports = {
  profile() {
    return get('/love/profile');
  },
  list() {
    return get('/love/list');
  },
  follow(userId) {
    return post('/love/follow/' + userId);
  },
};