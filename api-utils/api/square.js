/**
 * 蜕变广场 API
 */
const { get, post } = require('../request');

module.exports = {
  posts() {
    return get('/square/posts');
  },
  create(payload) {
    return post('/square/posts/create', payload);
  },
  like(pk) {
    return post('/square/posts/' + pk + '/like');
  },
  comments(pk) {
    return get('/square/posts/' + pk + '/comments');
  },
};