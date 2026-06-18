/**
 * 姐妹组队相关 API
 */
const { get, post } = require('../request');

module.exports = {
  list() {
    return get('/teams/list');
  },
  detail(pk) {
    return get('/teams/' + pk);
  },
  join(payload) {
    return post('/teams/join', payload);
  },
  activities(pk) {
    return get('/teams/' + pk + '/activities');
  },
  interact(pk, payload) {
    return post('/teams/activities/' + pk + '/interact', payload);
  },
  encourage(pk, payload) {
    return post('/teams/activities/' + pk + '/encourage', payload);
  },
};