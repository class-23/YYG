/**
 * 妈妈成长里程碑 API
 */
const { get, post } = require('../request');

module.exports = {
  list() {
    return get('/milestones/');
  },
  my() {
    return get('/milestones/me');
  },
  activities() {
    return get('/milestones/activities');
  },
  signup(pk, payload) {
    return post('/milestones/activities/' + pk + '/signup', payload);
  },
};