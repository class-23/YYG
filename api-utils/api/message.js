/**
 * 消息中心 API
 */
const { get, post } = require('../request');

module.exports = {
  list() {
    return get('/messages/');
  },
  read(pk) {
    return post('/messages/' + pk + '/read');
  },
  unreadCount() {
    return get('/messages/unread-count');
  },
};