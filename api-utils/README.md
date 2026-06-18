# 前端 API 工具库

> 微信小程序调用 Django 后端 API 的统一封装

---

## 使用方式

### 1. 在 `app.js` 入口初始化（仅一次）

```js
const apiUtils = require('./api-utils');
apiUtils.init();
```

### 2. 在页面中调用

```js
const app = getApp();
Page({
  onLoad() {
    app.globalData.api.user.me()
      .then(res => {
        console.log('当前用户:', res.data);
        this.setData({ user: res.data });
      })
      .catch(err => {
        console.error('获取用户失败', err);
      });
  }
});
```

---

## 当前环境

| 环境 | baseURL |
|---|---|
| development（默认） | `http://localhost:8000/v1` |
| test | `https://api-test.yuanyuangao.com/v1` |
| production | `https://api.yuanyuangao.com/v1` |

修改 `config.js` 中的 `CURRENT_ENV` 切换环境。

---

## 微信开发者工具配置

本地调试（`http://localhost:8000`）必须在微信开发者工具中勾选：
**详情 → 本地设置 → 不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书**

否则会报 `url not in domain list` 错误。

---

## 真机预览配置

手机扫码预览时，手机无法访问电脑的 `localhost`，需要：

1. 后端绑定到 `0.0.0.0`：`python manage.py runserver 0.0.0.0:8000`
2. 电脑和手机在同一局域网
3. 修改 `config.js` 的 `baseURL` 为 `http://<电脑局域网IP>:8000/v1`
4. 如有防火墙，需放行 8000 端口

---

## API 模块

- `api.user`        — 用户（me、stats、pushTokens、wxLogin）
- `api.lesson`      — 课程（today、byDay、playLog）
- `api.checkin`     — 打卡（list、today、submit）
- `api.plan`        — 计划（me、activateTrial）
- `api.cashback`    — 返现（account、records）
- `api.badge`       — 徽章（list、my）
- `api.course`      — 课程兑换（list、detail、exchange）
- `api.team`        — 姐妹组队（list、join、activities）
- `api.square`      — 蜕变广场（posts、like、comments）
- `api.love`        — 爱人连接（profile、list、follow）
- `api.milestone`   — 妈妈成长（my、activities）
- `api.message`     — 消息中心（list、read、unreadCount）
- `api.policy`      — 政策（list、detail）
- `api.invite`      — 邀请（codes、apply、records）
- `api.file`        — 文件上传
- `api.poster`      — 海报（list）
- `api.kidAssessment`— 孩子评估（templates、submissions）