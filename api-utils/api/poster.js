/**
 * 海报 API
 */
const { get } = require('../request');

module.exports = {
  list() {
    return get('/posters/list');
  },
  detail(pk) {
    return get('/posters/' + pk);
  },
};