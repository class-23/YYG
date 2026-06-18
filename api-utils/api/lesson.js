/**
 * 课程相关 API
 */
const { get, post } = require('../request');

module.exports = {
  // 今日课程
  today() {
    return get('/lessons/today');
  },
  // 按 day 获取课程
  byDay(day) {
    return get('/lessons/' + day);
  },
  // 记录播放
  playLog(day, payload) {
    return post('/lessons/' + day + '/play-log', payload);
  },
  // 反思问题
  reflections() {
    return get('/lessons/reflections');
  },
  // 子任务
  subTasks() {
    return get('/lessons/sub-tasks');
  },
};