/**
 * 孩子评估 API
 */
const { get, post } = require('../request');

module.exports = {
  templates() {
    return get('/kid-assessment/templates');
  },
  submissions() {
    return get('/kid-assessment/submissions');
  },
  submissionsList() {
    return get('/kid-assessment/submissions/list');
  },
  childProfile() {
    return get('/kid-assessment/child-profile');
  },
  submit(payload) {
    return post('/kid-assessment/submissions', payload);
  },
};