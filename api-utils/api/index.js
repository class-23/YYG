/**
 * 业务 API 聚合
 */
const user        = require('./user');
const lesson      = require('./lesson');
const checkin     = require('./checkin');
const plan        = require('./plan');
const cashback    = require('./cashback');
const badge       = require('./badge');
const course      = require('./course');
const team        = require('./team');
const square      = require('./square');
const love        = require('./love');
const milestone   = require('./milestone');
const message     = require('./message');
const policy      = require('./policy');
const invite      = require('./invite');
const file        = require('./file');
const poster      = require('./poster');
const kidAssessment = require('./kid-assessment');

module.exports = {
  user,
  lesson,
  checkin,
  plan,
  cashback,
  badge,
  course,
  team,
  square,
  love,
  milestone,
  message,
  policy,
  invite,
  file,
  poster,
  kidAssessment,
};