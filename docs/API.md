# 宝妈英语早操小程序 · 后端 API 接口文档

> **项目代号**：mom-english-taro
> **前端**：Taro 3 / 微信小程序
> **后端**：Django + Django REST Framework（待开发）
> **数据库**：PostgreSQL 14+
> **基础路径**：`https://api.yuanyuangao.com/v1`
> **认证方式**：JWT（`Authorization: Bearer <token>`）
> **版本**：v1.3
> **最后更新**：2026-06-17

***

## ⚠️ 本期暂不实现的模块（重要）

> 为聚焦 MVP 核心功能，**以下功能本期不开发、不交付、不写后端代码**。文档保留仅为后续版本做规划，前端切流时请直接忽略。

| 模块            | 涉及接口                                                                                                           | 暂不实现原因      |
| ------------- | -------------------------------------------------------------------------------------------------------------- | ----------- |
| **微信登录**      | `POST /v1/auth/wechat-login`、`POST /v1/auth/refresh`、`POST /v1/auth/logout`                                  | 暂不接入微信登录与 JWT 颁发 |
| **微信支付**      | `POST /v1/payments/orders`、`POST /v1/payments/wechat/callback`                                                 | 暂不接入微信支付商户号 |
| **付费开启计划**    | `POST /v1/plans/year365/activate`（依赖 `payment_order_id`）、`POST /v1/plans/trial21/activate` 的 `paid_99` trigger | 暂不开放付费入口    |
| **提现**        | `POST /v1/account/cashback/withdraw`、`GET /v1/account/cashback/records`                                        | 暂不开放用户提现    |
| **退款**        | `POST /v1/payments/wechat/refund`（隐含）                                                                          | 同微信支付       |
| **后台订单/退款**   | `/admin/orders/*`、`/admin/orders/{id}/refund`                                                                  | 无订单则无需      |
| **支付流水/提现流水** | 涉及 `cashback_record` 的 `withdraw` 类型、`payment_order`、`payment_refund`、`withdraw_order`                         | 同上          |

### 本期 MVP 替代方案

| 功能      | 本期做法                                                  | 暂不实现后用户感知           |
| ------- | ----------------------------------------------------- | ------------------- |
| 微信登录    | **不接入 jscode2session**，所有接口采用**可选鉴权**（未登录返回 200 + 空 data），客户端用 `X-Device-Id` 作为匿名标识 | 用户无感（前端不调用 wx.login），所有只读接口正常返回，写接口用设备 ID 兜底 |
| 21 天体验  | **仅支持** **`invite_3`** **邀请 3 人免费解锁**，关闭 `paid_99` 入口 | 用户看到 21 天按钮可点但走邀请逻辑 |
| 365 天计划 | **不开放入口**，仅在运营后台手工开通                                  | 暂时隐藏该入口             |
| 返现余额    | **可累计、不可提现**（账户金额仅展示）                                 | 用户可看到数字但无法提现        |
| 现金支付    | **无**                                                 | 用户购买计划只能走线下/免费邀请    |

> **相关接口在文档中以** ⛔ **图标标注**，请勿在 v1 阶段实现或联调。

***

## 目录

- [1. 通用约定](#1-通用约定)
  - [1.1 请求规范](#11-请求规范)
  - [1.2 响应结构](#12-响应结构)
  - [1.3 通用错误码](#13-通用错误码)
  - [1.4 鉴权与签名](#14-鉴权与签名)
  - [1.5 分页规范](#15-分页规范)
  - [1.6 时间与时区](#16-时间与时区)
  - [1.7 幂等性](#17-幂等性)
- [2. 用户与认证模块](#2-用户与认证模块)
  - [2.1 微信登录](#21-微信登录)
  - [2.2 刷新 Token](#22-刷新-token)
  - [2.3 退出登录](#23-退出登录)
  - [2.4 获取当前用户信息](#24-获取当前用户信息)
  - [2.5 更新用户资料](#25-更新用户资料)
  - [2.6 绑定手机号](#26-绑定手机号)
  - [2.7 用户数据迁移（localStorage 上报）](#27-用户数据迁移localstorage-上报)
- [3. 打卡与每日课程模块](#3-打卡与每日课程模块)
- [4. 返现账户与计划模块](#4-返现账户与计划模块)
- [5. 姐妹同行成长模块](#5-姐妹同行成长模块)
- [6. 蜕变广场与社交模块](#6-蜕变广场与社交模块)
- [7. 妈妈成长计划模块](#7-妈妈成长计划模块)
- [8. 孩子成长评估模块](#8-孩子成长评估模块)
- [9. 课程与权益模块](#9-课程与权益模块)
- [10. 政策内容 CMS 模块](#10-政策内容-cms-模块)
- [11. 海报与分享模块](#11-海报与分享模块)
- [12. 文件上传模块](#12-文件上传模块)
- [13. 通知与消息模块](#13-通知与消息模块)
- [14. 后台管理模块（运营端）](#14-后台管理模块运营端)
- [15. 小程序平台兼容性规范（依据 [MINIPROGRAM_DEV.md](file:///d:/Trae项目/YYG/docs/MINIPROGRAM_DEV.md) 第 6 章）](#15-小程序平台兼容性规范依据-miniprogram_devmd-第-6-章)
  - [15.1 客户端能力探测（请求头 / 探测接口）](#151-客户端能力探测请求头--探测接口)
  - [15.2 平台能力差异表（与本项目相关）](#152-平台能力差异表与本项目相关)
  - [15.3 最低基础库版本策略](#153-最低基础库版本策略)
  - [15.4 鸿蒙 OS 专项适配](#154-鸿蒙-os-专项适配)
  - [15.5 `wx.canIUse` 兼容性速查](#155-wxcaniuse-兼容性速查)
- [16. 前端对接规范（依据 [MINIPROGRAM_DEV.md](file:///d:/Trae项目/YYG/docs/MINIPROGRAM_DEV.md) 第 7 章）](#16-前端对接规范依据-miniprogram_devmd-第-7-章)
  - [16.1 性能优化](#161-性能优化)
  - [16.2 网络请求最佳实践](#162-网络请求最佳实践)
  - [16.3 隐私合规](#163-隐私合规)
  - [16.4 调试与日志](#164-调试与日志)
  - [16.5 安全建议](#165-安全建议)
  - [16.6 性能与体验](#166-性能与体验)
- [附录 A：完整数据字典（前端 → 后端 字段映射）](#附录-a完整数据字典前端--后端-字段映射)
- [附录 B：接口变更日志](#附录-b接口变更日志)

***

## 1. 通用约定

### 1.1 请求规范

| 项            | 说明                                          |
| ------------ | ------------------------------------------- |
| 协议           | **必须 HTTPS**（HTTP/1.1，仅开发期可走内网 HTTP）。前端 `wx.request` 仅支持 HTTPS，需在微信公众平台「开发-开发管理-服务器域名」中配置 `request 合法域名`。开发期可在开发者工具勾选「不校验合法域名」 |
| 字符集          | UTF-8                                       |
| Content-Type | `application/json; charset=utf-8`（除文件上传外）   |
| 请求方法         | `GET` / `POST` / `PUT` / `PATCH` / `DELETE` |
| 时间格式         | ISO 8601：`2026-06-17T10:00:00+08:00`        |
| 数值类型         | 金额单位「分」（避免浮点误差，仅在响应最外层可选转为元）                |
| URL 风格       | 资源名词复数：`/api/v1/checkins`                   |
| 命名风格         | 请求/响应字段统一 `snake_case`                      |
| 并发限制         | 小程序 `wx.request` 默认 **10 个并发上限**；后端需对 429 进行友好提示 |
| 频率限制         | 详见微信官方 [接口调用频率规范](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/api-frequency.html)，单 IP `wx.request` 10s 内最多 100 次 |

**通用请求头**：

```http
POST /v1/checkins HTTP/1.1
Host: api.yuanyuangao.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
X-Request-Id: 6c84fb90-12c4-11ee-be56-0242ac120002
X-Client: miniprogram/1.0.0
X-Platform: wechat
```

| Header            | 必填      | 说明                                     |
| ----------------- | ------- | -------------------------------------- |
| `Authorization`   | 是（除登录外） | JWT 凭证，格式 `Bearer <token>`             |
| `X-Request-Id`    | 否（强烈建议） | 客户端生成的 UUID，便于全链路追踪                     |
| `X-Client`        | 是       | 客户端版本 `miniprogram/<semver>`           |
| `X-Platform`      | 是       | 平台：`wechat` / `h5` / `ios` / `android` |
| `X-Platform-OS`   | 否       | 客户端 OS（`ios` / `android` / `ohos` / `ohos_pc` / `windows` / `mac` / `devtools`），来源 `wx.getDeviceInfo().platform` |
| `X-SDK-Version`   | 否       | 微信基础库版本，来源 `wx.getAppBaseInfo().SDKVersion` |
| `X-Device-Model`  | 否       | 设备型号（用于风控），来源 `wx.getDeviceInfo().model` |
| `Idempotency-Key` | 否（金额/状态变更必填） | 幂等键（POST/PUT 涉及金额、状态变更时必填）             |

> 📌 **后端开发要求**：
> 1. 接口域名统一收敛到 `api.yuanyuangao.com`，**必须** HTTPS（TLS 1.2+）。
> 2. 微信公众平台需分别配置 `request 合法域名`、`uploadFile 合法域名`、`downloadFile 合法域名`（不能复用）。
> 3. 任何文件下载链接（`https://cdn.../*.mp3`、图片等）**必须** 使用 HTTPS，否则 `wx.downloadFile` / `image src` 会失败。
> 4. 后端需把 `X-Request-Id` 透传到日志链路，与响应 `trace_id` 一致，便于全链路追踪。

### 1.2 响应结构

**成功响应**（HTTP 2xx）：

```json
{
  "code": 0,
  "message": "ok",
  "data": { /* 业务负载 */ },
  "trace_id": "6c84fb90-12c4-11ee-be56-0242ac120002"
}
```

**失败响应**（HTTP 4xx / 5xx，仍为 200 由网关层透传时除外）：

```json
{
  "code": 10001,
  "message": "用户未登录",
  "data": null,
  "errors": [
    { "field": "phone", "message": "手机号格式不正确" }
  ],
  "trace_id": "6c84fb90-12c4-11ee-be56-0242ac120002"
}
```

| 字段         | 类型                    | 说明                            |
| ---------- | --------------------- | ----------------------------- |
| `code`     | int                   | 业务码，`0` 表示成功；非 0 参见错误码表       |
| `message`  | string                | 人类可读的提示文案（中文）                 |
| `data`     | object / array / null | 业务负载                          |
| `errors`   | array<object>         | 字段级错误（表单/参数校验场景）              |
| `trace_id` | string                | 与请求头 `X-Request-Id` 一致，便于日志检索 |

### 1.3 通用错误码

| code  | HTTP | 含义                 | 处理建议          |
| ----- | ---- | ------------------ | ------------- |
| 0     | 200  | 成功                 | -             |
| 10001 | 401  | 未登录或登录已过期          | 跳转登录          |
| 10002 | 401  | Token 无效           | 跳转登录          |
| 10003 | 403  | 无权限访问              | 提示权限不足        |
| 10004 | 403  | 角色不匹配（如非管理员访问 CMS） | 隐藏入口          |
| 10101 | 400  | 参数校验失败             | 展示 `errors[]` |
| 10102 | 400  | 必填参数缺失             | 提示补全          |
| 10103 | 404  | 资源不存在              | 提示并返回         |
| 10104 | 409  | 资源冲突（如重复打卡）        | 友好提示          |
| 10105 | 429  | 请求过于频繁             | 触发限流提示        |
| 10201 | 500  | 服务器内部错误            | 通用兜底页         |
| 10202 | 502  | 上游依赖（支付/AI/短信）异常   | 稍后重试          |
| 10203 | 503  | 服务维护中              | 引导去首页         |
| 20001 | 422  | 业务前置条件不满足          | 引导完成前置任务      |

> 业务码按模块扩展，规则：`模块号(2 位) * 1000 + 序号`。
> 例如：打卡模块 `2xxxx`，姐妹模块 `3xxxx`，政策模块 `6xxxx`，见各模块内说明。
> ⛔ **错误码** **`21xxx`（账户/计划）中除** **`21001-21004`** **之外的支付/提现相关错误码本期不出现**；错误码 `21xxx` 本期仅保留账户余额展示相关。

### 1.4 鉴权与签名

> ⛔ **本期（v1）暂不实现微信登录**。本期接口采用**可选鉴权**策略：未携带 `Authorization` 头时按"匿名用户"处理（部分业务接口返回空数据 / 不创建用户级记录），携带 `Authorization` 头时按"已登录用户"处理（v2 启用 §2.1 后生效）。
> 详细说明见 [§2.1](#21-微信登录) 顶部说明与本节"本期鉴权模式"。

#### 1.4.1 本期鉴权模式（v1）

| 请求头 | 本期处理 | v2 启用 §2.1 后 |
| --- | --- | --- |
| `Authorization: Bearer <jwt>` | **本期忽略**（不校验） | 必填，校验通过后才执行业务 |
| 无 `Authorization` | 当作"匿名用户"处理 | 返回 401，强制登录 |
| `X-Device-Id` | **强烈建议** 必填（用于匿名用户标识） | 用于多端数据合并 |
| `X-Request-Id` | 必填（已存在约定） | 同 |

> 📌 **本期匿名用户行为**：
> - **只读接口**（GET）：正常返回数据，不区分登录态。
> - **写接口**（POST/PUT/DELETE）：本期**不强制登录**，但建议客户端在 `X-User-Id` 头中传入一个**设备级临时 ID**（如 `wx.getStorageSync('device_id')`），后端用其作为 `user_id` 兜底，等 v2 §2.1 微信登录启用后批量合并到正式 `usr_xxx` ID。
> - **个人数据接口**（如 `/v1/users/me`、`/v1/checkins`）：未登录时返回**空数据 + `200`**（不是 401），前端根据 `data == null` 显示"请登录"占位 UI。

#### 1.4.2 v2 启用后的 JWT 设计（保留供后续实现）

- 微信小程序登录：通过 `wx.login` 拿到 `code` → 后端调用微信 `jscode2session` → 颁发 JWT。
- JWT payload：

```json
{
  "sub": "usr_2c0a1f6b8a",
  "openid": "oUpF8uMuAJ...",
  "unionid": "onNkwz5...",
  "role": "user",
  "is_admin": false,
  "iat": 1718600000,
  "exp": 1719204800
}
```

- access token 有效期 7 天，refresh token 30 天，refresh 接口换取新 token。
- 涉及支付、提现等敏感操作需二次签名（HMAC-SHA256，时间戳 ± 5 分钟有效）。

#### 1.4.3 错误码本期调整

| code | HTTP | 含义 | 本期处理 |
| --- | --- | --- | --- |
| 10001 | 401 | 未登录或登录已过期 | ⛔ **本期不返回该错误**（未登录返回 200 + 空 data） |
| 10002 | 401 | Token 无效 | ⛔ **本期不返回**（Authorization 被忽略） |
| 10003 | 403 | 无权限访问 | ✅ 仍可返回（如非管理员访问 CMS） |
| 10004 | 403 | 角色不匹配 | ✅ 仍可返回 |

> 📌 **错误码 10001-10002 本期保留代码值但 v1 阶段不返回**，等 v2 §2.1 启用时再正式生效。

### 1.5 分页规范

请求参数：

| 参数          | 类型     | 默认 | 说明              |
| ----------- | ------ | -- | --------------- |
| `page`      | int    | 1  | 页码，从 1 开始       |
| `page_size` | int    | 20 | 每页条数，范围 `1-100` |
| `cursor`    | string | -  | 游标分页（用于时间线/动态流） |

响应包装（`data` 字段为列表时）：

```json
{
  "code": 0,
  "data": {
    "items": [],
    "total": 128,
    "page": 1,
    "page_size": 20,
    "has_next": true
  }
}
```

### 1.6 时间与时区

- 数据库统一存 UTC 时间戳。
- API 响应统一使用 ISO 8601 + `+08:00`。
- 业务侧以「自然日」为分界（凌晨 00:00 重置打卡日历），时区为东八区。

### 1.7 幂等性

POST 涉及金额、状态变更时必须携带 `Idempotency-Key: <uuid>`，后端在 24 小时内对相同 key 返回首次结果。

### 1.8 小程序客户端约束（依据 [MINIPROGRAM_DEV.md](file:///d:/Trae项目/YYG/docs/MINIPROGRAM_DEV.md)）

> 本节约束**后端在设计时必须考虑**，前端在调用 API 时也需满足。

#### 1.8.1 客户端平台枚举（`X-Platform-OS` 合法值）

来源 `wx.getDeviceInfo().platform`：

| 取值 | 含义 |
| --- | --- |
| `ios` | iOS 微信（iPhone / iPad） |
| `android` | Android 微信 |
| `ohos` | HarmonyOS 手机端微信 |
| `ohos_pc` | HarmonyOS PC 微信 |
| `windows` | Windows 微信 |
| `mac` | macOS 微信 |
| `devtools` | 微信开发者工具 |

后端建议：

- `ohos` / `ohos_pc`：**音频/视频** 部分场景有兼容问题（InnerAudioContext 播放网络音频可能闪退），后端可在响应头返回 `X-Client-Compat-Audio: fallback-http` 让前端降级到 HLS 流。
- `ios` + SDK 26.2+：InnerAudioContext 播放 mp3 有异常，后端需提供 m4a/aac 替代源。
- `devtools`：忽略 trace_id，便于开发调试不污染生产日志。

#### 1.8.2 localStorage / Storage 限制

`wx.setStorageSync` / `wx.setStorage` 受以下硬性约束（前后端迁移脚本也必须遵守）：

| 项 | 限制 |
| --- | --- |
| 单 key 最大数据 | **1 MB** |
| 全部 key 总大小 | **10 MB** |
| 写入类型 | 仅支持原生类型、`Date`、`JSON.stringify` 可序列化的对象 |
| 异步 vs 同步 | **异步优先**；启动时**严禁** 大量同步读取，影响启动耗时 |
| 同步 API 平台异常 | iOS 部分版本 `setStorageSync` 本地数据库有损坏问题；纯血鸿蒙有异常 |

迁移接口（见 [D.5](file:///d:/Trae项目/YYG/docs/DATABASE.md)）需在用户登录后立即上报，并在云端写入成功后**清除本地 5 个 key**。

#### 1.8.3 后端需对前端做兼容性兜底的场景

| 场景 | 兼容性 | 后端建议 |
| --- | --- | --- |
| `wx.requestPayment` | 需 `wx.canIUse('requestPayment')` | 后端响应订单接口始终返回 `wechat_pay_params`，前端做 `if (wx.canIUse('requestPayment'))` 兜底 |
| `button open-type="getPhoneNumber"` | 自基础库 2.21.2 安全升级，需后端换号 | `bindgetphonenumber` 返回 `code`（不再返回 `encryptedData`），**后端必须实现 `/v1/users/me/phone` 接口换号** |
| `wx.requestSubscribeMessage` | 每次触发需用户确认 | 后端响应推送 token，前端按用户选择提交 |
| `wx.getLocation` | 基础库 2.17.0 起调用频率限制；iOS 14+ 需精确授权 | 城市定位功能做"上次缓存优先 + 失败降级" |
| `wx.scanCode` | 用户拒绝摄像头权限时需降级 | 提供"手动输入邀请码"兜底方案 |
| `wx.createInnerAudioContext` | iOS 26.2 / 鸿蒙有兼容问题 | 后端必须同时提供 mp3 + m4a/aac 多源，前端按平台选择 |

#### 1.8.4 最低基础库版本与 SDK 标识

- 本期最低基础库版本：**2.30.0+**（覆盖 `wx.canIUse` 完整能力 + 自定义组件新特性）
- 前端在 `app.json` 显式设置：

```json
{
  "lazyCodeLoading": "requiredComponents",
  "requiredPrivateInfos": ["chooseImage", "getLocation"]
}
```

- 后端按 `X-SDK-Version` 区分能力：

| 基础库 | 后端可选兼容方案 |
| --- | --- |
| `≥ 3.0.0` | 默认方案 |
| `2.30.0 - 2.99.99` | 关闭 Skyline 相关接口、关闭自定义 tabBar |
| `< 2.30.0` | 不支持，前端提示升级微信 |

---

## 2. 用户与认证模块

> 业务码前缀 `10xxx`

### 2.1 微信登录

- **POST** `/v1/auth/wechat-login`
- 描述：微信小程序 code 换 JWT
- **前端调用规范**（依据 [MINIPROGRAM_DEV.md §5.8.1](file:///d:/Trae项目/YYG/docs/MINIPROGRAM_DEV.md)）：

```javascript
// 1. 调用 wx.login 获取临时凭证（code 5 分钟内有效）
wx.login({
  success: (res) => {
    if (res.code) {
      // 2. 用 code 换 JWT，**严禁** 在前端处理 session_key
      wx.request({
        url: 'https://api.yuanyuangao.com/v1/auth/wechat-login',
        method: 'POST',
        data: {
          code: res.code,
          nickname: '...',     // 可选
          avatar_url: '...',   // 可选
          invite_code: '...'    // 可选
        },
        header: {
          'X-Request-Id': generateUUID(),
          'X-Client': 'miniprogram/1.0.0',
          'X-Platform': 'wechat',
          'X-Platform-OS': wx.getDeviceInfo().platform,
          'X-SDK-Version': wx.getAppBaseInfo().SDKVersion
        },
        success: (loginRes) => {
          const { access_token, refresh_token, user } = loginRes.data.data
          // 3. token 仅存本地，**严禁** 在 storage 中明文长期存放（参见 §1.8.2）
          wx.setStorageSync('access_token', access_token)
          wx.setStorageSync('refresh_token', refresh_token)
        }
      })
    }
  }
})
```

> ⚠️ **wx.login 调用频率限制**：每个小程序每天调用次数有限，应在前端做"token 未过期不重登录"的判断，配合 `wx.checkSession()`。

- **请求参数**

| 名称            | 位置   | 类型     | 必填 | 描述                  |
| ------------- | ---- | ------ | -- | ------------------- |
| `code`        | body | string | 是  | `wx.login` 返回的临时凭证（5 分钟内有效，**严禁** 二次使用）  |
| `nickname`    | body | string | 否  | 微信昵称（首次登录回填）         |
| `avatar_url`  | body | string | 否  | 微信头像               |
| `invite_code` | body | string | 否  | 邀请码（21 天体验或姐妹组队时带入） |

- **响应** `data`：

```json
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "rt_8f2c...",
  "token_type": "Bearer",
  "expires_in": 604800,
  "user": {
    "id": "usr_2c0a1f6b8a",
    "nickname": "小雅妈妈",
    "avatar_url": "https://cdn.../avatar.jpg",
    "phone": null,
    "role": "user",
    "is_admin": false,
    "plan_status": "trial21",
    "team_id": "team_8e2c",
    "created_at": "2026-05-01T09:00:00+08:00"
  }
}
```

- **错误码**：`10001` 未授权、`10102` code 无效、`10202` 微信接口异常

### 2.2 刷新 Token

> ⛔ **本期（v1）暂不实现**。本章保留供 v2 启用时直接参考。

- **POST** `/v1/auth/refresh`
- 请求：`{ "refresh_token": "rt_..." }`
- 响应：同 2.1 的 `access_token` + `expires_in`

### 2.3 退出登录

> ⛔ **本期（v1）暂不实现**。本章保留供 v2 启用时直接参考。

- **POST** `/v1/auth/logout`
- 请求：无（JWT 在 Header）
- 响应：`{ "code": 0 }`
- 副作用：服务端将 refresh token 标记为失效

### 2.4 获取当前用户信息

- **GET** `/v1/users/me`
- 响应 `data`：

```json
{
  "id": "usr_2c0a1f6b8a",
  "nickname": "小雅妈妈",
  "avatar_url": "https://cdn...",
  "phone": "138****1234",
  "baby_stage": "kindergarten",
  "region": "上海",
  "bio": "想和姐妹们一起坚持英语早操",
  "plan_status": "year365",
  "plan_started_at": "2026-01-15T00:00:00+08:00",
  "team_id": "team_8e2c",
  "trial21_unlocked": false,
  "invite_progress": 2,
  "is_admin": false,
  "created_at": "2026-05-01T09:00:00+08:00"
}
```

### 2.5 更新用户资料

- **PATCH** `/v1/users/me`
- 请求：

```json
{
  "nickname": "小雅妈妈",
  "avatar_url": "https://cdn...",
  "baby_stage": "kindergarten",
  "region": "上海",
  "bio": "想和姐妹们一起坚持英语早操"
}
```

| 字段           | 类型     | 必填 | 描述                                            |
| ------------ | ------ | -- | --------------------------------------------- |
| `nickname`   | string | 否  | 2-20 字符                                       |
| `avatar_url` | string | 否  | 头像 URL                                        |
| `baby_stage` | enum   | 否  | `kindergarten` / `lower` / `upper` / `junior` |
| `region`     | string | 否  | 地区标签（北京/上海/广东/全国通用…）                          |
| `bio`        | string | 否  | 个人简介，≤ 200 字符                                 |

### 2.6 绑定手机号

- **POST** `/v1/users/me/phone`
- 描述：通过 `button open-type="getPhoneNumber"` 获取的加密数据，**自基础库 2.21.2 起安全升级，`bindgetphonenumber` 回调仅返回 `code`，需后端调用 `phonenumber.getPhoneNumber` 接口换号**。
- 请求：

```json
{
  "code": "82c2c8001bfc5d8a3f8c2c8e9b1f0c8e"
}
```

| 字段 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| `code` | string | 是 | `bindgetphonenumber` 回调返回的临时凭证（**不是** `encryptedData`） |

- 后端流程：

```
1. 接收前端传来的 `code`
2. 调用微信开放接口 https://api.weixin.qq.com/wxa/business/getuserphonenumber
   请求头携带 access_token（从服务端拿，不传前端）
3. 拿到手机号明文后 AES 加密入库（参见 DATABASE.md §4.1 user.phone）
4. 返回脱敏展示字段
```

- 响应：

```json
{
  "phone": "138****1234",
  "phone_raw_hash": "a1b2c3d4..." 
}
```

- 错误码：
  - `10204` `code` 无效或已过期（5 分钟内有效）
  - `10205` 微信接口换号失败
  - `10206` 该微信号已绑定其他用户

- **前端兼容**：在低版本基础库下，`bindgetphonenumber` 仍返回 `encryptedData` + `iv`；后端需根据 payload 自动选择解密方式：

```javascript
// 前端
<button open-type="getPhoneNumber" bindgetphonenumber="onGetPhone">
Page({
  onGetPhone(e) {
    if (e.detail.code) {
      // 新版：基础库 2.21.2+，仅传 code
      wx.request({ url: '/v1/users/me/phone', method: 'POST', data: { code: e.detail.code } })
    } else if (e.detail.encryptedData) {
      // 旧版：传 encryptedData + iv
      wx.request({ url: '/v1/users/me/phone', method: 'POST', data: { encrypted_data: e.detail.encryptedData, iv: e.detail.iv } })
    }
  }
})
```

### 2.7 用户数据迁移（localStorage 上报）

> 📌 本期实现。用户在**新设备 / 重装微信后首次登录**时，前端主动调用该接口上报 5 个 localStorage key 中的数据，后端写入对应表后返回，前端再清除本地缓存。
> 详细数据迁移流程参见 [DATABASE.md §D.5](file:///d:/Trae项目/YYG/docs/DATABASE.md)。

- **POST** `/v1/users/me/migrate-localstorage`
- 描述：用户首次登录时一次性上报本机 localStorage 数据，后端按 schema 写入对应表，返回每项迁移条数
- Header：`Idempotency-Key: <uuid>`（防重放）

**请求**：

```json
{
  "checkin_records": [
    {
      "biz_date": "2026-06-15",
      "main_checkin_completed": true,
      "reflection": "今天我选择先朗读再刷手机",
      "audio_played_seconds": 320,
      "completed_at": "2026-06-15T08:30:00+08:00",
      "tasks": [
        { "task_id": "daily-main", "completed": true }
      ]
    }
  ],
  "team": {
    "name": "妈妈先发光小队",
    "goal": "自我成长",
    "max_members": 5,
    "invite_code": "YYG2026",
    "members": [
      { "nickname": "原原妈妈", "role": "leader" }
    ]
  },
  "invite_progress": {
    "invite_progress": 2,
    "invitees": [
      { "wechat": "abc123", "registered_at": "2026-06-10T10:00:00+08:00" }
    ],
    "trial21_unlocked": false
  },
  "plan": {
    "status": "trial21",
    "started_at": "2026-06-01T00:00:00+08:00",
    "expires_at": "2026-06-22T00:00:00+08:00"
  },
  "child_profile": {
    "has_done_assessment": true,
    "grade_group": "小学低",
    "english_level": "E1",
    "core_insight": ["词汇不足", "理解困难"],
    "recommended_plan": "21d_plan"
  }
}
```

| 字段 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| `checkin_records[]` | array | 否 | 来自 `mom_english_checkin_records` |
| `team` | object | 否 | 来自 `yuanyuango_sister_growth.team` |
| `invite_progress` | object | 否 | 来自 `yuanyuango_sister_growth.inviteProgress` |
| `plan` | object | 否 | 来自 `mom_english_growth_plan_state` |
| `child_profile` | object | 否 | 来自 `mom_english_child_profile` |

**响应**：

```json
{
  "code": 0,
  "data": {
    "migrated": {
      "checkins": 12,
      "team": 1,
      "invites": 2,
      "plan": 1,
      "child_profile": 1
    },
    "skipped": {
      "checkins_duplicate": 3,
      "invites_expired": 1
    }
  },
  "trace_id": "..."
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `migrated.checkins` | int | 实际写入的打卡条数 |
| `migrated.team` | int | 写入的小队数（0 或 1） |
| `migrated.invites` | int | 写入的有效邀请数 |
| `migrated.plan` | int | 写入的计划记录数（0 或 1） |
| `migrated.child_profile` | int | 写入的画像数（0 或 1） |
| `skipped.checkins_duplicate` | int | 因 `(user_id, biz_date)` 唯一约束跳过的重复打卡 |
| `skipped.invites_expired` | int | 已过期的邀请记录 |

- **错误码**：
  - `20001` 数据格式错误（如 `biz_date` 非日期格式）
  - `20002` 重复调用（已在 24h 内迁移过）
  - `20003` 单次迁移条数超过上限（默认 500 条打卡 / 50 条邀请）

> 📌 **前端迁移完成后必须清除 5 个 localStorage key**：
> - `mom_english_checkin_records`
> - `yuanyuango_sister_growth`
> - `mom_english_growth_plan_state`
> - `mom_english_child_profile`
> - `mom_english_pending_paid_plan`（测评页临时态，不上报，清除即可）

***

## 3. 打卡与每日课程模块

> 业务码前缀 `20xxx`

### 3.1 获取今日课程

- **GET** `/v1/daily/today`
- 描述：根据用户计划状态和当前日期，返回当天的英语早操课程
- 响应 `data`：

```json
{
  "date": "2026-06-17",
  "day": 154,
  "theme": "Day 154 · 英语早操",
  "task": "完成今日 5 分钟跟读 + 1 句表达复述",
  "cover_image": "https://cdn.../day154.jpg",
  "audio_src": "https://cdn.../day154.mp3",
  "audio_title": "Day 154 · keep the ball rolling",
  "audio_subtitle": "原声音频 · 5 分钟",
  "audio_duration": "05:12",
  "quote": "Keep the ball rolling.",
  "meaning": "别停下，继续前进。",
  "copy": "再小的坚持，乘以 365 天也会发光。",
  "pronunciation": ["重音在 roll 上", "rolling 要带 /ɪŋ/ 不要吞音"],
  "speaking_examples": [
    { "en": "Keep the ball rolling on this plan.", "zh": "让这个计划继续向前推进。" }
  ],
  "definition_notes": [
    "keep the ball rolling = 让事情持续进行"
  ],
  "takeaways": [
    "今天 1 件事比昨天多坚持 1 秒"
  ],
  "translation_practice": [
    "请把 '别停下来' 翻译成英文：Don't stop ______"
  ],
  "encouragement": "今天完成就是赢。",
  "policy_impact_tasks": [
    {
      "id": "t_p_882",
      "title": "每周记录 1 次本周任务完成情况",
      "description": "用一句话写下本周最值得继续的一个习惯。",
      "frequency": "每周 1 次",
      "estimated_time": "10 分钟",
      "grade_range": ["初中"],
      "ability_tags": ["学习习惯稳定性"],
      "source_policy_id": "policy-beijing-exam-2026",
      "completed": false
    }
  ],
  "team_today_summary": {
    "team_id": "team_8e2c",
    "team_name": "原原高成长小队",
    "checked_members": 2,
    "total_members": 3
  }
}
```

### 3.2 提交每日主打卡

- **POST** `/v1/checkins/main`
- 描述：完成"今日金句跟读+反思"，主打卡记 1 元返现
- Header：`Idempotency-Key: <uuid>`
- 请求：

```json
{
  "date": "2026-06-17",
  "reflection": "今天我选择先把'再睡 5 分钟'换成'立刻坐起来朗读'。",
  "audio_played_seconds": 312
}
```

| 名称                     | 类型                 | 必填 | 描述              |
| ---------------------- | ------------------ | -- | --------------- |
| `date`                 | string(YYYY-MM-DD) | 是  | 自然日（东八区）        |
| `reflection`           | string             | 是  | 反思内容，1-500 字符   |
| `audio_played_seconds` | int                | 否  | 当日音频累计播放秒数，用于风控 |

- 响应 `data`：

```json
{
  "checkin_id": "chk_1a2b3c",
  "date": "2026-06-17",
  "main_checkin_completed": true,
  "completed_at": "2026-06-17T08:42:11+08:00",
  "cashback_earned": 100,
  "consecutive_days": 154,
  "new_badges": [
    { "id": "bdg_3", "name": "坚持勋章", "day": 7 }
  ]
}
```

> `cashback_earned` 单位为分（100 = 1.00 元）。`consecutive_days` 为连续打卡天数。

- **错误码**：
  - `20001` 当日已完成
  - `20002` 反思内容长度不达标
  - `20003` 音频播放时长过短（< 30 秒）

### 3.3 完成子任务

- **POST** `/v1/checkins/sub-tasks/{task_id}/complete`
- 描述：完成政策关联子任务或每日扩展任务
- 请求：

```json
{
  "date": "2026-06-17",
  "encouragement": "今天和孩子一起完成了 5 分钟"
}
```

- 响应：

```json
{
  "task_id": "t_p_882",
  "completed": true,
  "completed_at": "2026-06-17T09:01:00+08:00",
  "task_streak_days": 3
}
```

### 3.4 查询打卡记录（按日期）

- **GET** `/v1/checkins?date=2026-06-17`
- 响应 `data`：

```json
{
  "date": "2026-06-17",
  "main_checkin_completed": true,
  "reflection": "...",
  "tasks": [
    {
      "id": "t_p_882",
      "title": "每周记录 1 次本周任务完成情况",
      "description": "...",
      "source": "policy_impact",
      "completed": true,
      "completed_at": "2026-06-17T09:01:00+08:00"
    }
  ],
  "completed_at": "2026-06-17T08:42:11+08:00"
}
```

### 3.5 查询历史打卡日历

- **GET** `/v1/checkins/calendar?year=2026&month=6`
- 响应 `data`：

```json
{
  "year": 2026,
  "month": 6,
  "days": [
    { "date": "2026-06-01", "status": "done", "badge": "day_1" },
    { "date": "2026-06-02", "status": "done", "badge": "day_2" },
    { "date": "2026-06-03", "status": "missed" },
    { "date": "2026-06-15", "status": "done", "badge": "special", "label": "30 天蜕变" }
  ],
  "summary": {
    "checked_days": 18,
    "missed_days": 2,
    "special_days": 1
  }
}
```

### 3.6 查询连续打卡统计

- **GET** `/v1/checkins/stats`
- 响应 `data`：

```json
{
  "checked_days": 154,
  "missed_days": 6,
  "consecutive_days": 154,
  "longest_streak": 154,
  "this_month_checked": 18,
  "this_month_missed": 2
}
```

***

## 4. 返现账户与计划模块

> 业务码前缀 `21xxx`
> ⛔ **本模块中"提现（4.3）"与"付费开启计划（4.4 paid\_99 / 4.5）"本期暂不实现**，仅"返现账户（4.1）"、"返现流水（4.2）"和"邀请 3 人免费开启 21 天（4.4 invite\_3）"纳入本期开发。

### 4.1 获取返现账户

- **GET** `/v1/account/cashback`
- 响应 `data`：

```json
{
  "cashback": 15400,
  "expected_cashback": 36500,
  "remaining_days": 211,
  "checked_days": 154,
  "missed_days": 6,
  "course_unlocked": 3,
  "course_total": 5,
  "plan_status": "year365",
  "plan_started_at": "2026-01-15T00:00:00+08:00",
  "rule": {
    "title": "365 天规则",
    "items": [
      "报名费 365 元",
      "每日完成打卡，获 1 元返现资格",
      "全年满勤，返还 365 元并赠送 3980 元课程"
    ]
  }
}
```

### 4.2 返现流水

> ⛔ **本期暂不实现**（提现未开放，无需展示流水）。仅返现账户金额可见（4.1），返现积累过程不向用户展示流水列表。

- **GET** `/v1/account/cashback/records?page=1&page_size=20`
- 响应 `data`：

```json
{
  "items": [
    {
      "id": "cbr_001",
      "date": "2026-06-17",
      "amount": 100,
      "type": "earn",
      "source": "daily_checkin",
      "description": "完成 6 月 17 日打卡"
    },
    {
      "id": "cbr_002",
      "date": "2026-06-16",
      "amount": 100,
      "type": "earn",
      "source": "daily_checkin",
      "description": "完成 6 月 16 日打卡"
    }
  ],
  "total": 154,
  "page": 1,
  "page_size": 20,
  "has_next": false
}
```

### 4.3 提现申请

> ⛔ **本期暂不实现**（用户提现功能延期，返现余额仅展示，不可提现）。后续版本启用时实现此接口。

- **POST** `/v1/account/cashback/withdraw`
- 请求：

```json
{
  "amount": 5000,
  "channel": "wechat",
  "idempotency_key": "uuid-..."
}
```

| 字段                | 类型     | 必填 | 描述                      |
| ----------------- | ------ | -- | ----------------------- |
| `amount`          | int    | 是  | 提现金额（分），单笔 ≥ 100 且 ≤ 余额 |
| `channel`         | enum   | 是  | `wechat` / `alipay`     |
| `idempotency_key` | string | 是  | 幂等键，UUID                |

- 响应：

```json
{
  "withdraw_id": "wdr_001",
  "status": "processing",
  "amount": 5000,
  "estimated_arrival": "2026-06-18T12:00:00+08:00"
}
```

- **错误码**：
  - `21001` 余额不足
  - `21002` 单笔金额超限
  - `21003` 当日提现次数超限
  - `21004` 实名信息未完善

### 4.4 启用 21 天体验计划

- **POST** `/v1/plans/trial21/activate`
- 描述：本期**仅支持邀请 3 人免费解锁**。付费 trigger `paid_99` 暂不实现。
- 请求：

```json
{
  "trigger": "invite_3"
}
```

| 字段                 | 类型     | 必填     | 描述                                        |
| ------------------ | ------ | ------ | ----------------------------------------- |
| `trigger`          | enum   | 是      | ⛔ **本期只允许** **`invite_3`**；`paid_99` 暂不实现 |
| `payment_order_id` | string | ⛔ 暂不实现 | 微信支付订单号（暂不接收）                             |

- 响应：

```json
{
  "plan_id": "pln_001",
  "status": "trial21",
  "started_at": "2026-06-17T10:00:00+08:00",
  "expires_at": "2026-07-08T10:00:00+08:00"
}
```

> ⛔ **4.5 启用 365 天蜕变计划：本期不开放付费入口**。如运营需要为某用户开通 365 天计划，由后台管理员手工调用 `/admin/users/{user_id}/adjust-plan` 接口（参见 14.2）。

### 4.5 启用 365 天蜕变计划

> ⛔ **本期暂不实现**（不开放付费入口）。仅在运营后台通过 `/admin/users/{user_id}/adjust-plan` 手工开通。

- **POST** `/v1/plans/year365/activate`
- 描述：支付 ¥365 开启
- 请求：

```json
{
  "payment_order_id": "wx_2026061700123"
}
```

- 响应：

```json
{
  "plan_id": "pln_002",
  "status": "year365",
  "started_at": "2026-06-17T10:00:00+08:00",
  "expires_at": "2027-06-17T10:00:00+08:00",
  "course_reward_unlocked": true
}
```

> 📌 **业务字段约定**：
> - 用户计划状态（`user_profile.plan_status`）枚举：`none` / `trial7` / `trial21` / `21d_plan` / `100d_plan` / `year365`
> - 前端 signup 页面使用 `plan21` / `plan365` 作为按钮内部 ID；后端接口统一使用 `trial21` / `year365`
> - **`trial7` 是 7 天挽留体验**（测评完成后未立即付费时弹窗引导），仅通过 **4.5.b** 接口启用

### 4.5.b 启用 7 天挽留体验（trial7）

> **本期实现**。用于孩子在测评页 `/pages/kid-growth-assessment` 关闭主付费弹窗后，挽留用户先免费体验 7 天。

- **POST** `/v1/plans/trial7/activate`
- 描述：测评完成后未付费时引导用户进入 7 天免费体验，自动跳转到 `/pages/signup/index?id=trial7`
- 请求：

```json
{
  "trigger": "assessment_retention",
  "child_profile_id": "cp_001"
}
```

| 字段 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| `trigger` | enum | 是 | `assessment_retention`（测评挽留） |
| `child_profile_id` | string | 是 | 关联孩子画像（来自 8.2 接口） |

- 响应：

```json
{
  "plan_id": "pln_003",
  "status": "trial7",
  "started_at": "2026-06-17T10:00:00+08:00",
  "expires_at": "2026-06-24T10:00:00+08:00",
  "next_path": "/pages/daily/index"
}
```

### 4.5.c 启用 21 天习惯建立计划（21d_plan）

> ⛔ **本期暂不实现付费**（与 trial21 一致，仅运营手工开通）。名称升级为 `21d_plan` 与代码中 `kid-growth-assessment` 输出字段对齐。

- **POST** `/v1/plans/21d/activate`
- 描述：测评完成后由 21 天付费弹窗（¥99）触发，本期可经运营手工开通
- 请求：

```json
{
  "payment_order_id": null,
  "child_profile_id": "cp_001",
  "trigger": "post_assessment"
}
```

### 4.5.d 启用 100 天成长计划（100d_plan）

> ⛔ **本期暂不实现付费**。是 `kid-growth-assessment` 输出页面的"升级路径"，对应 100 天成长节点，198 元。

- **POST** `/v1/plans/100d/activate`
- 描述：测评完成后由 100 天付费弹窗（¥198）触发，本期可经运营手工开通
- 请求：

```json
{
  "payment_order_id": null,
  "child_profile_id": "cp_001",
  "trigger": "post_assessment"
}
```

### 4.6 创建支付订单

> ⛔ **本期暂不实现**（未接入微信支付商户号）。

- **POST** `/v1/payments/orders`
- 请求：

```json
{
  "product_id": "plan_year365",
  "quantity": 1
}
```

- 响应：

```json
{
  "order_id": "ord_202606170001",
  "product_id": "plan_year365",
  "amount": 36500,
  "currency": "CNY",
  "wechat_pay_params": {
    "timeStamp": "1718600000",
    "nonceStr": "5K8264ILTKCH...",
    "package": "prepay_id=wx201...",
    "signType": "RSA",
    "paySign": "oR9d8PuhnIc+Y..."
  }
}
```

### 4.7 支付回调

> ⛔ **本期暂不实现**（依赖微信支付接入）。

- **POST** `/v1/payments/wechat/callback`
- 描述：微信支付结果回调（无需鉴权，签名校验）
- 请求：微信 XML / JSON 格式
- 响应：`{ "code": "SUCCESS", "message": "成功" }`

***

## 5. 姐妹同行成长模块

> 业务码前缀 `30xxx`

### 5.1 获取我的小队详情

- **GET** `/v1/teams/me`
- 响应 `data`：

```json
{
  "id": "team_8e2c",
  "name": "原原高成长小队",
  "goal": "亲子英语",
  "max_members": 5,
  "team_consecutive_days": 28,
  "growth_value": 8640,
  "invite_code": "YYG2026",
  "created_by": "usr_2c0a1f6b8a",
  "created_at": "2026-05-20T10:00:00+08:00",
  "members": [
    {
      "user_id": "usr_2c0a1f6b8a",
      "nickname": "小雅妈妈",
      "avatar_url": "https://cdn...",
      "role": "leader",
      "today_checked": true,
      "total_checkin_days": 154
    },
    {
      "user_id": "usr_88b1c",
      "nickname": "乐乐妈妈",
      "avatar_url": "https://cdn...",
      "role": "member",
      "today_checked": true,
      "total_checkin_days": 132
    }
  ],
  "trial21_unlocked": true,
  "invite_progress": 3
}
```

### 5.2 创建小队

- **POST** `/v1/teams`
- 请求：

```json
{
  "name": "原原高成长小队",
  "goal": "亲子英语",
  "goal_options": ["情绪稳定", "亲子英语", "自我成长", "坚持打卡"]
}
```

| 字段     | 类型     | 必填 | 描述       |
| ------ | ------ | -- | -------- |
| `name` | string | 是  | 2-12 字符  |
| `goal` | enum   | 是  | 固定 4 选 1 |

- 响应：返回完整 `team` 对象（同 5.1）
- **错误码**：
  - `30001` 已在其他小队中
  - `30002` 小队名称重复

### 5.3 加入小队

- **POST** `/v1/teams/join`
- 请求：

```json
{
  "invite_code": "YYG2026"
}
```

- 响应：返回完整 `team` 对象
- **错误码**：
  - `30003` 邀请码无效
  - `30004` 小队已满
  - `30005` 已在其他小队中

### 5.4 退出小队

- **POST** `/v1/teams/me/leave`
- 请求：无
- 响应：`{ "code": 0 }`
- 副作用：若为队长，需先转让；空小队自动解散

### 5.5 转让队长

- **POST** `/v1/teams/me/transfer`
- 请求：`{ "to_user_id": "usr_88b1c" }`

### 5.6 解散小队（仅队长）

- **DELETE** `/v1/teams/me`
- 响应：`{ "code": 0 }`

### 5.7 获取今日小队动态

- **GET** `/v1/teams/me/activities/today`
- 响应 `data`：

```json
{
  "team_id": "team_8e2c",
  "date": "2026-06-17",
  "checked_members": 2,
  "total_members": 3,
  "activities": [
    {
      "id": "act_001",
      "user_id": "usr_88b1c",
      "nickname": "乐乐妈妈",
      "type": "checkin",
      "content": "今天完成了英语早操！",
      "hugged": false,
      "likes": 2,
      "encouragement": "加油！",
      "created_at": "2026-06-17T08:00:00+08:00"
    },
    {
      "id": "act_002",
      "user_id": "usr_a91bc",
      "nickname": "晴晴妈",
      "type": "pending",
      "content": "今日尚未打卡",
      "hugged": true,
      "likes": 1,
      "encouragement": null,
      "created_at": "2026-06-17T07:30:00+08:00"
    }
  ]
}
```

### 5.8 互动操作（抱抱/点赞/提醒）

- **POST** `/v1/teams/me/activities/{activity_id}/interact`
- 请求：

```json
{
  "action": "hug"  
}
```

| 字段       | 类型   | 必填 | 描述                        |
| -------- | ---- | -- | ------------------------- |
| `action` | enum | 是  | `hug` / `like` / `remind` |

- 响应：

```json
{
  "action": "hug",
  "hugged": true,
  "likes": 3
}
```

### 5.9 留言鼓励

- **POST** `/v1/teams/me/activities/{activity_id}/encourage`
- 请求：

```json
{
  "content": "今天完成就是赢"
}
```

| 字段        | 类型     | 必填 | 描述      |
| --------- | ------ | -- | ------- |
| `content` | string | 是  | 1-50 字符 |

- 响应：`{ "encouragement_id": "enc_001" }`

### 5.10 提醒未打卡姐妹

- **POST** `/v1/teams/me/remind`
- 请求：`{ "user_ids": ["usr_a91bc"] }`
- 响应：`{ "reminded_count": 1 }`

### 5.11 分享获取邀请码

- **GET** `/v1/teams/me/invite-code`
- 响应：`{ "invite_code": "YYG2026", "share_url": "https://..." }`

### 5.12 邀请进度

- **GET** `/v1/invites/progress`
- 响应 `data`：

```json
{
  "invite_progress": 2,
  "target": 3,
  "trial21_unlocked": false,
  "invitees": [
    {
      "user_id": "usr_d92f",
      "nickname": "小诺妈",
      "avatar_url": "https://cdn...",
      "first_checkin_at": "2026-06-15T08:30:00+08:00",
      "status": "confirmed"
    }
  ]
}
```

***

## 6. 蜕变广场与社交模块

> 业务码前缀 `31xxx`

### 6.1 蜕变广场动态流

- **GET** `/v1/square/feed?cursor=...&page_size=20`
- 响应 `data`：

```json
{
  "items": [
    {
      "id": "sq_001",
      "user_id": "usr_88b1c",
      "nickname": "乐乐妈妈",
      "avatar_url": "https://cdn...",
      "text": "今天忍住没吼孩子，给自己一个小小拥抱。",
      "tag": "情绪成长",
      "image_urls": [],
      "likes": 12,
      "comments": 3,
      "created_at": "2026-06-17T09:30:00+08:00"
    }
  ],
  "next_cursor": "sq_001_20260617",
  "has_next": true
}
```

### 6.2 发布动态

- **POST** `/v1/square/posts`
- 请求：

```json
{
  "text": "今天忍住没吼孩子，给自己一个小小拥抱。",
  "tag": "情绪成长",
  "image_urls": ["https://cdn.../1.jpg"]
}
```

| 字段           | 类型     | 必填 | 描述       |
| ------------ | ------ | -- | -------- |
| `text`       | string | 是  | 1-500 字符 |
| `tag`        | enum   | 否  | 预设标签     |
| `image_urls` | array  | 否  | 最多 9 张   |

- 响应：`{ "post_id": "sq_001" }`

### 6.3 点赞 / 取消点赞

- **POST** `/v1/square/posts/{post_id}/like`
- **DELETE** `/v1/square/posts/{post_id}/like`

### 6.4 评论

- **POST** `/v1/square/posts/{post_id}/comments`
- 请求：`{ "content": "太棒了" }`
- 响应：`{ "comment_id": "cm_001" }`

### 6.5 遇见认真成长的人（同频交友）

- **GET** `/v1/love-connection/profiles?page=1`
- 描述：基于用户当前 plan\_status 筛选可见资料
- 响应 `data`：

```json
{
  "items": [
    {
      "user_id": "usr_77ac",
      "nickname": "原原高 · 园园",
      "avatar_url": "https://cdn...",
      "city": "上海",
      "baby_stage": "lower",
      "tags": ["成长型交友", "同城活动", "轻松交流"],
      "bio": "想找一个愿意一起坚持的妈妈～",
      "is_unlocked": true
    }
  ],
  "unlock_tip": "完成 21 天打卡可解锁全部资料"
}
```

### 6.6 关注 / 解除关注

- **POST** `/v1/love-connection/follow/{user_id}`
- **DELETE** `/v1/love-connection/follow/{user_id}`

### 6.7 完善脱单资料

- **PUT** `/v1/love-connection/me`
- 请求：

```json
{
  "city": "上海",
  "baby_stage": "lower",
  "tags": ["成长型交友", "同城活动"],
  "bio": "想找一个愿意一起坚持的妈妈～",
  "show_real_name": false
}
```

***

## 7. 妈妈成长计划模块

> 业务码前缀 `40xxx`

### 7.1 获取我的成长曲线

- **GET** `/v1/mom-growth/me`
- 响应 `data`：

```json
{
  "user_id": "usr_2c0a1f6b8a",
  "status": "year365",
  "checkin_days": 154,
  "growth_money": 15400,
  "current_badge": "坚持勋章",
  "current_badge_level": 2,
  "next_milestone": {
    "month": 3,
    "label": "情绪更稳定",
    "days_to_go": 0
  },
  "weekly_badges": [
    { "week": 1, "name": "初心勋章", "unlocked": true, "desc": "坚持 7 天获得" },
    { "week": 2, "name": "坚持勋章", "unlocked": true, "desc": "坚持 14 天获得" }
  ],
  "milestone_node": {
    "month": 5,
    "label": "状态开始发光",
    "copy": "第 5 个月｜状态开始发光。你已经连续记录 150 天，开始重新关注自己的感受。"
  },
  "available_plans": [
    {
      "type": "trial",
      "title": "21 天打卡体验",
      "hook": "先用 21 天，把注意力慢慢还给自己。",
      "items": [
        "邀请 3 位新用户完成首次打卡，免费体验",
        "或支付 ¥99 直接开启",
        "每日成长任务、21 天打卡记录",
        "成长提醒、体验完成纪念卡",
        "最多获得 3 枚成长勋章"
      ],
      "tip": "适合第一次加入、想先试试看的妈妈。"
    },
    {
      "type": "year",
      "title": "365 天打卡蜕变",
      "hook": "365 天后，你收获的不只是返还款项，而是一套属于自己的成长系统。",
      "items": [
        "¥365 开启年度计划",
        "打卡成功 1 天，返现 1 元成长金",
        "漏打卡当天成长权益减少 1 元",
        "满 365 天赠送价值 3980 元课程训练营",
        "最多 52 枚勋章，12 个月蜕变节点"
      ],
      "tip": "适合想认真改变自己、建立长期节奏的妈妈。"
    }
  ]
}
```

### 7.2 切换计划

- **POST** `/v1/mom-growth/me/choose-plan`
- 请求：`{ "plan_type": "trial21" | "year365" }`
- 响应：

```json
{
  "status": "year365",
  "started_at": "2026-06-17T10:00:00+08:00",
  "expires_at": "2027-06-17T10:00:00+08:00"
}
```

### 7.3 蜕变节点查询

- **GET** `/v1/mom-growth/milestones?month=5`
- 响应 `data`：

```json
{
  "month": 5,
  "label": "状态开始发光",
  "badge_level": 4,
  "copy": "第 5 个月｜状态开始发光。你已经连续记录 150 天，开始重新关注自己的感受。",
  "unlocked": true,
  "required_days": 150
}
```

### 7.4 同城活动列表

- **GET** `/v1/mom-growth/offline-activities?city=上海`
- 响应 `data`：

```json
{
  "items": [
    {
      "id": "act_offline_001",
      "title": "上海·徐汇区 妈妈英语茶话会",
      "date": "2026-06-22T14:00:00+08:00",
      "location": "徐汇区某咖啡馆",
      "max_seats": 12,
      "taken_seats": 5,
      "cover": "https://cdn.../evt1.jpg"
    }
  ]
}
```

***

## 8. 孩子成长评估模块（V8 简化版）

> 业务码前缀 `50xxx`
> 📌 **本期版本**：V8 简化版（**3 题路径识别**），与 PROJECT_STATUS.md 中描述的 1-9 年级长阅读测评不同。
> 详细测评流程见 [`PROJECT_STATUS.md` 第 7.3 节](file:///d:/Trae项目/YYG/PROJECT_STATUS.md)。

### 8.0 测评流程概述

| 步骤 | 输入 | 输出 |
| --- | --- | --- |
| Step 1 | 选择年级阶段 | `grade_group`（`lower` / `upper` / `junior`） |
| Step 2 | 完成 3 个单选题 | `english_level`（E1/E2/E3）、`core_insight`（阻力标签） |
| Step 3 | 系统生成路径结果 | `primary_path` / `recommended_plan` / `hook_text` / `cta_text` |

> 📌 **字段命名约定**：本章所有响应字段统一使用 **`snake_case`**（`grade_group` / `english_level` / `core_insight` / `recommended_plan` / `primary_path` / `backup_path` / `hook_text` / `cta_text` / `child_grade` 等），与本项目其他模块保持一致。前端 `camelCase` 字段需在请求/响应拦截器中转换。

**3 个固定问题**（来自 `pages/kid-growth-assessment/kid-growth-assessment.js`）：

| key | title | options（按 A/B/C 顺序） |
| --- | --- | --- |
| `study_status` | 孩子目前英语状态 | 刚开始接触 / 兴趣阶段；学过但效果一般；能做题但不稳定 |
| `understanding` | 孩子是否需要家长翻译英语句子？ | 经常需要；偶尔需要；基本不需要 |
| `resistance` | 孩子学习英语主要问题 | 抗拒学习；学了记不住；会但不稳定 |

> 📌 **前端传入答案时统一使用 snake_case**（`study_status` / `understanding` / `resistance`）。

**年级阶段选项**（`grade_options`）：

| `grade_option` | 显示值 | 映射到 `grade_group` |
| --- | --- | --- |
| `lower` | `小学低年级（1-3年级）` | `小学低` |
| `upper` | `小学高年级（4-6年级）` | `小学高` |
| `junior` | `初中（7-9年级）` | `初中` |

**评分规则（前端已实现，可直接复用）**：

| 题目选项 | 分数 |
| --- | --- |
| `study_status`: 刚开始接触 / 兴趣阶段 | 0 |
| `study_status`: 学过但效果一般 | 1 |
| `study_status`: 能做题但不稳定 | 2 |
| `understanding`: 经常需要 | 0 |
| `understanding`: 偶尔需要 | 1 |
| `understanding`: 基本不需要 | 2 |
| `resistance`: 抗拒学习 | 0 |
| `resistance`: 学了记不住 | 1 |
| `resistance`: 会但不稳定 | 2 |

- 总分 `≤ 2` → `E1`
- 总分 `3-4` → `E2`
- 总分 `≥ 5` → `E3`

**`core_insight` 阻力标签推导规则**：

| 条件 | 标签 |
| --- | --- |
| `study_status` 含"刚开始接触" 或 `understanding` 含"经常需要" | `词汇不足` |
| `understanding` 含"经常需要" 或 "偶尔需要" | `理解困难` |
| `resistance` 含"抗拒学习" 或 "学了记不住" 或 "会但不稳定" | `学习习惯缺失` |

最终 `core_insight` 去重后取前 3 个。

### 8.1 获取测评模板

- **GET** `/v1/kid-assessment/template?variant=v8`
- 描述：返回 V8 简化版测评题（前端 `grade_options` + `questions`）
- 响应 `data`：

```json
{
  "variant": "v8",
  "steps": [
    { "step": 1, "label": "选择年级阶段", "questions": ["grade_group"] },
    { "step": 2, "label": "完成 3 题识别", "questions": ["study_status", "understanding", "resistance"] }
  ],
  "grade_options": [
    { "code": "lower",  "label": "小学低年级（1-3年级）", "grade_group": "小学低" },
    { "code": "upper",  "label": "小学高年级（4-6年级）", "grade_group": "小学高" },
    { "code": "junior", "label": "初中（7-9年级）",         "grade_group": "初中" }
  ],
  "questions": [
    { "key": "study_status",  "type": "single", "title": "孩子目前英语状态",       "options": ["刚开始接触 / 兴趣阶段", "学过但效果一般", "能做题但不稳定"] },
    { "key": "understanding","type": "single", "title": "孩子是否需要家长翻译英语句子？", "options": ["经常需要", "偶尔需要", "基本不需要"] },
    { "key": "resistance",   "type": "single", "title": "孩子学习英语主要问题",     "options": ["抗拒学习", "学了记不住", "会但不稳定"] }
  ],
  "result_plans": [
    { "plan_code": "21d_plan", "title": "21天习惯建立计划", "price_cents": 9900,  "primary": true },
    { "plan_code": "100d_plan","title": "100天成长计划",   "price_cents": 19800, "primary": false }
  ],
  "retention_plan": { "plan_code": "trial7", "title": "7天免费体验" }
}
```

### 8.2 提交测评

- **POST** `/v1/kid-assessment/submissions`
- 请求：

```json
{
  "variant": "v8",
  "grade_option": "lower",
  "answers": {
    "study_status": "刚开始接触 / 兴趣阶段",
    "understanding": "经常需要",
    "resistance": "抗拒学习"
  }
}
```

| 字段 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| `variant` | enum | 是 | 本期固定 `v8` |
| `grade_option` | enum | 是 | `lower` / `upper` / `junior` |
| `answers` | object | 是 | 3 个 key 的选择（`study_status` / `understanding` / `resistance`） |

- 响应 `data`：

```json
{
  "submission_id": "asm_v8_001",
  "child_profile_id": "cp_001",
  "result": {
    "english_level": "E1",
    "grade_group": "小学低",
    "core_insight": ["词汇不足", "理解困难", "学习习惯缺失"],
    "recommended_plan": "21d_plan",
    "primary_path": "21天习惯建立计划",
    "backup_path": "100天成长计划",
    "hook_text": "孩子的问题不是不会，而是没有进入正确学习路径",
    "cta_text": "优先建议：先做21天习惯建立"
  }
}
```

- 错误码：
  - `50001` 测评参数缺失
  - `50002` `grade_option` 取值非法
  - `50003` `answers` 不完整

### 8.3 获取孩子画像

> 📌 本期实现。V8 测评完成后立即写入本地（`mom_english_child_profile`），后端也持久化。

- **GET** `/v1/users/me/child-profile`
- 响应 `data`：

```json
{
  "id": "cp_001",
  "user_id": "usr_xxx",
  "has_done_assessment": true,
  "child_grade": "小学低",
  "english_level": "E1",
  "core_insight": ["词汇不足", "理解困难"],
  "submission_id": "asm_v8_001",
  "updated_at": "2026-06-17T10:00:00+08:00"
}
```

- 若用户未测评，返回 `404` + `code=50004`。

### 8.4 我的测评历史

- **GET** `/v1/kid-assessment/submissions?page=1&page_size=20`
- 响应 `data`：测评记录列表（按 `created_at DESC`）

### 8.5 测评后邀请解锁状态

> 📌 用于 `/pages/sister-poster/index` 的"3 位新用户注册成功后弹窗"逻辑。

- **POST** `/v1/kid-assessment/invite-unlock/check`
- 描述：测评完成、分享邀请后，客户端轮询该接口确认是否解锁
- 请求：

```json
{
  "submission_id": "asm_v8_001"
}
```

- 响应 `data`：

```json
{
  "shared": true,
  "notified": false,
  "unlocked": false,
  "trial21_unlocked": false,
  "invite_progress": 2,
  "remaining": 1
}
```

- 字段说明：
  - `shared`：是否已分享邀请卡
  - `notified`：是否已弹出过"21天任务已解锁"提示
  - `unlocked`：`trial21_unlocked || invite_progress >= 3`
  - `invite_progress`：有效邀请达成数（0-3）
  - `remaining`：距离解锁还需邀请的人数

> 当前端 `useDidShow` 触发该接口，发现 `unlocked && !notified` 时调用 `wx.showModal` 提示用户。

### 8.6 标记已通知

- **POST** `/v1/kid-assessment/invite-unlock/ack`
- 描述：前端弹窗已展示后调用，防止重复弹窗
- 请求：`{ "submission_id": "asm_v8_001" }`
- 响应：`{ "code": 0 }`

***

## 9. 课程与权益模块

> 业务码前缀 `51xxx`
> 📌 **当前课程页 `/pages/courses/index` 是引流转化页**（主推课程 + 进阶转化），点击按钮弹 toast "咨询入口待接企业微信"，**实际不进入兑换/购买流程**。

### 9.1 可兑换课程列表

- **GET** `/v1/courses?page=1&page_size=20`
- 响应 `data`：

```json
{
  "items": [
    {
      "id": "crs_001",
      "title": "亲子英语启蒙 21 讲",
      "cover": "https://cdn.../crs001.jpg",
      "tags": ["启蒙", "跟读"],
      "value": 1990,
      "required_cashback_days": 100,
      "unlocked": true
    },
    {
      "id": "crs_002",
      "title": "妈妈口语表达训练营",
      "cover": "https://cdn.../crs002.jpg",
      "tags": ["口语", "表达"],
      "value": 2980,
      "required_cashback_days": 365,
      "unlocked": false
    }
  ],
  "summary": {
    "course_unlocked": 3,
    "course_total": 5
  }
}
```

### 9.2 课程转化咨询（落地页主流程）

> 📌 本期实现。当前 `/pages/courses/index` 点击 "咨询了解" 仅 toast 提示，后端需对接企业微信。

- **POST** `/v1/courses/{course_id}/inquiries`
- 描述：用户点击 "咨询了解" 时记录一次留资线索，运营通过企业微信触达
- 请求：

```json
{
  "course_id": "crs_001",
  "from_page": "pages/courses/index",
  "contact": {
    "phone": "13800001234",
    "wechat": "可选",
    "note": "可填写咨询意向"
  }
}
```

| 字段 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| `course_id` | string | 是 | 课程 ID |
| `from_page` | string | 否 | 来源页面，默认 `pages/courses/index` |
| `contact.phone` | string | 否 | 手机号（脱敏） |
| `contact.wechat` | string | 否 | 微信号（脱敏） |
| `contact.note` | string | 否 | 备注，≤ 200 字符 |

- 响应：

```json
{
  "inquiry_id": "inq_001",
  "course_id": "crs_001",
  "status": "received",
  "follow_up_channel": "wechat_enterprise",
  "contact_hint": "运营将通过企业微信联系您"
}
```

- 错误码：
  - `51003` 课程不存在
  - `51004` 联系方式已留过 3 次（防骚扰）

### 9.3 兑换课程

- **POST** `/v1/courses/{course_id}/redeem`
- 请求：`{ "address_id": "addr_001" }`（如课程为实物）
- 响应：

```json
{
  "exchange_id": "exg_001",
  "course_id": "crs_001",
  "status": "success",
  "remaining_cashback_days": 0
}
```

- **错误码**：
  - `51001` 未达到兑换条件
  - `51002` 已兑换过

### 9.4 我的兑换记录

- **GET** `/v1/courses/exchanges?page=1`
- 响应 `data`：兑换记录

### 9.5 徽章列表

- **GET** `/v1/badges`
- 响应 `data`：

```json
{
  "items": [
    { "id": "bdg_1", "name": "初心勋章", "day": 7, "unlocked": true },
    { "id": "bdg_2", "name": "坚持勋章", "day": 21, "unlocked": true },
    { "id": "bdg_3", "name": "点亮勋章", "day": 60, "unlocked": false }
  ]
}
```

***

## 10. 政策内容 CMS 模块

> 业务码前缀 `60xxx`
> 该模块既服务 C 端用户（内容消费），也服务运营后台（编辑/审核/发布）。

### 10.1 政策列表（C 端可见）

- **GET** `/v1/policies?region=上海&stage=junior&grade=junior&domain=admission_exam&page=1`
- 查询参数支持 `region` / `stage` / `grade` / `domain` / `ability` / `task` / `user_profile` 7 类标签的多选过滤
- 响应 `data`：

```json
{
  "items": [
    {
      "id": "policy-shanghai-exam-2026",
      "title": "上海名额分配综合评价与成长记录提醒",
      "front_display_title": "上海综合评价更关注学生平时表现和过程性材料",
      "front_display_summary": "建议家长从日常打卡开始帮助孩子积累成长记录和表达成果。",
      "effective_date": "2026-09-01",
      "region": "上海",
      "stage": "初中",
      "grade_range": ["初中"],
      "tags": [
        { "type": "domain", "name": "招生考试" },
        { "type": "ability", "name": "英语阅读能力" }
      ],
      "published_at": "2026-02-20T00:00:00+08:00"
    }
  ],
  "total": 1
}
```

### 10.2 政策详情（C 端）

- **GET** `/v1/policies/{policy_id}`
- 响应 `data`：

```json
{
  "id": "policy-shanghai-exam-2026",
  "title": "...",
  "source_name": "上海市教育委员会",
  "source_url": "https://example.com/...",
  "policy_summary": "...",
  "effective_date": "2026-09-01",
  "region": "上海",
  "stage": "初中",
  "grade_range": ["初中"],
  "domains": ["quota_allocation", "comprehensive_evaluation"],
  "influence_abilities": ["英语阅读能力", "学习习惯稳定性"],
  "parent_action_suggestions": [
    "更早关注过程性成长记录，不要只在考试前集中突击。"
  ],
  "generated_tasks": [
    {
      "id": "t_p_882",
      "title": "每周记录 1 次本周任务完成情况",
      "category": "学习习惯",
      "description": "用一句话写下本周最值得继续的一个习惯。",
      "frequency": "每周 1 次",
      "estimated_time": "10 分钟",
      "grade_range": ["初中"],
      "ability_tags": ["学习习惯稳定性"]
    }
  ],
  "front_display_title": "...",
  "front_display_summary": "...",
  "impact_explanation": "...",
  "monthly_suggestions": [...],
  "weekly_task_suggestions": [...],
  "focus_directions": ["成长记录", "综合评价", "表达复述"],
  "child_impact_analysis": "...",
  "content_status": "published",
  "version": 4,
  "created_by": "policy-editor-sh",
  "reviewed_by": "reviewer-li",
  "review_comment": "口径统一，允许发布。",
  "created_at": "2026-01-15T11:20:00+08:00",
  "updated_at": "2026-05-20T10:08:00+08:00",
  "published_at": "2026-02-20",
  "published_at_system": "2026-05-20T10:18:00+08:00"
}
```

### 10.3 政策标签字典

- **GET** `/v1/policies/tags`
- 响应 `data`：

```json
{
  "groups": [
    { "type": "region", "label": "适用地区", "items": [
      { "id": "region-shanghai", "name": "上海", "enabled": true }
    ]},
    { "type": "stage", "label": "学段", "items": [
      { "id": "stage-lower", "name": "小学低年级", "enabled": true }
    ]},
    { "type": "grade", "label": "年级", "items": [] },
    { "type": "domain", "label": "领域", "items": [] },
    { "type": "ability", "label": "能力", "items": [] },
    { "type": "task", "label": "任务", "items": [] },
    { "type": "user_profile", "label": "用户画像", "items": [] }
  ]
}
```

### 10.4 政策内容生成（AI）

- **POST** `/v1/policies/ai-generate`
- 描述：调用 LLM 按既定提示词模板生成结构化政策内容
- 请求：

```json
{
  "source_text": "2026 年北京中考改革……（原文）",
  "preset_tags": {
    "region": ["region-beijing"],
    "stage": ["stage-junior"]
  }
}
```

- 响应：直接返回结构化政策内容（字段同 10.2）。

> 该接口供 CMS 后台调用，限速 5 次/分钟。

### 10.5 政策版本历史

- **GET** `/v1/policies/{policy_id}/versions`
- 响应 `data`：

```json
{
  "items": [
    {
      "version": 4,
      "title": "...",
      "change_summary": "补充了每周任务建议",
      "editor": "policy-editor-sh",
      "published_at": "2026-05-20T10:18:00+08:00"
    }
  ]
}
```

### 10.6 政策审核提交

- **POST** `/v1/policies/{policy_id}/submit-review`
- 请求：`{ "comment": "已补充每周任务建议" }`
- 响应：`{ "review_id": "rev_001", "status": "pending_review" }`

### 10.7 政策审核操作

- **POST** `/v1/policies/{policy_id}/review`
- 请求：

```json
{
  "action": "approve",
  "comment": "已补充行动建议，可发布。",
  "version": 4
}
```

| 字段        | 类型     | 必填 | 描述                                       |
| --------- | ------ | -- | ---------------------------------------- |
| `action`  | enum   | 是  | `approve` / `reject` / `request_changes` |
| `comment` | string | 是  | 审核意见                                     |
| `version` | int    | 是  | 当前版本号                                    |

- 响应：`{ "status": "published" | "pending_review" | "rejected" }`

### 10.8 政策上下架

- **POST** `/v1/policies/{policy_id}/online`
- **POST** `/v1/policies/{policy_id}/offline`
- 请求：无
- 响应：`{ "status": "published" | "offline" }`

### 10.9 标签管理

#### 创建标签

- **POST** `/v1/policies/tags`
- 请求：

```json
{
  "type": "region",
  "name": "浙江",
  "value": "浙江",
  "enabled": true
}
```

- 响应：`{ "id": "region-zhejiang" }`

#### 更新标签

- **PATCH** `/v1/policies/tags/{tag_id}`
- 请求：`{ "name": "浙江", "enabled": true }`

#### 删除标签

- **DELETE** `/v1/policies/tags/{tag_id}`

### 10.10 政策草稿

#### 列出草稿

- **GET** `/v1/policies/drafts?status=draft`

#### 保存草稿

- **POST** `/v1/policies/drafts`
- 请求：完整 policy 对象
- 响应：`{ "id": "policy_xxx" }`

***

## 11. 海报与分享模块

> 业务码前缀 `70xxx`

### 11.1 生成朋友圈海报

- **POST** `/v1/posters/daily`
- 请求：

```json
{
  "date": "2026-06-17",
  "template": "minimal_warm"
}
```

- 响应：

```json
{
  "poster_url": "https://cdn.../posters/xxx.jpg",
  "qrcode_url": "https://cdn.../qrcode/xxx.png",
  "expires_at": "2026-06-18T10:00:00+08:00"
}
```

### 11.2 生成姐妹邀请海报

- **POST** `/v1/posters/sister-invite`
- 请求：`{ "invite_code": "YYG2026" }`
- 响应：同 11.1

### 11.3 分享口令（App 内）

- **GET** `/v1/shares/app-message-config?path=/pages/sister-invite/index?inviteCode=YYG2026`
- 响应：

```json
{
  "title": "我在原原高成长小队等你一起打卡",
  "desc": "一个妈妈会走得更远，快来加入～"
}
```

***

## 12. 文件上传模块

> 业务码前缀 `80xxx`
> 📌 **客户端约束**（依据 [MINIPROGRAM_DEV.md §5.2.2](file:///d:/Trae项目/YYG/docs/MINIPROGRAM_DEV.md)）：
> - `wx.uploadFile` 必须 HTTPS；`uploadFile 合法域名` 需在微信公众平台单独配置
> - 单文件大小限制（前端）：视频 60s 时长 / 图片压缩到 1MB 内
> - 支持的文件后缀：`wxs` `png` `jpg` `jpeg` `gif` `svg` `json` `mp3` `aac` `m4a` `mp4` `wav` `ogg` `silk`（详见官方白名单）

### 12.1 获取上传凭证

- **POST** `/v1/uploads/credentials`
- 请求：

```json
{
  "scene": "avatar" | "post_image" | "poster_image" | "policy_image",
  "content_type": "image/jpeg",
  "size": 204800
}
```

| 字段 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| `scene` | enum | 是 | 上传场景 |
| `content_type` | enum | 是 | MIME 类型 |
| `size` | int | 是 | 文件大小（字节），≤ 5MB |

- 响应：

```json
{
  "upload_url": "https://upload.yuanyuangao.com/oss/...",
  "method": "PUT",
  "headers": { "Content-Type": "image/jpeg" },
  "object_key": "uploads/2026/06/17/usr_xxx.jpg",
  "cdn_url": "https://cdn.yuanyuangao.com/uploads/2026/06/17/usr_xxx.jpg"
}
```

### 12.2 上传完成回调

- **POST** `/v1/uploads/finish`
- 请求：`{ "object_key": "uploads/...", "scene": "avatar" }`
- 响应：`{ "cdn_url": "https://..." }`

### 12.3 前端 `wx.uploadFile` 完整流程

```javascript
// 1. 先调用后端获取 OSS 凭证（不要在前端生成签名）
const { data: credential } = await wx.request({
  url: 'https://api.yuanyuangao.com/v1/uploads/credentials',
  method: 'POST',
  data: { scene: 'avatar', content_type: 'image/jpeg', size: fileSize }
})

// 2. 选择本地图片
const { tempFilePaths } = await wx.chooseImage({ count: 1, sizeType: ['compressed'] })

// 3. 上传到 OSS
const uploadRes = await wx.uploadFile({
  url: credential.upload_url,
  filePath: tempFilePaths[0],
  name: 'file',
  header: credential.headers  // 必须包含 Content-Type
})

// 4. 通知后端上传完成
await wx.request({
  url: 'https://api.yuanyuangao.com/v1/uploads/finish',
  method: 'POST',
  data: { object_key: credential.object_key, scene: 'avatar' }
})
```

***

## 13. 通知与消息模块

> 业务码前缀 `90xxx`

### 13.1 系统消息列表

- **GET** `/v1/messages?type=system&unread_only=true&page=1`
- 响应 `data`：

```json
{
  "items": [
    {
      "id": "msg_001",
      "type": "system",
      "title": "今日打卡提醒",
      "content": "新的一天，从 5 分钟英语开始～",
      "unread": true,
      "created_at": "2026-06-17T08:00:00+08:00"
    }
  ],
  "unread_count": 3
}
```

### 13.2 标记已读

- **POST** `/v1/messages/{message_id}/read`
- **POST** `/v1/messages/read-all`

### 13.3 推送 token 提交

- **POST** `/v1/push-tokens`
- 请求：`{ "provider": "wechat_mp", "token": "wx_push_..." }`
- 响应：`{ "code": 0 }`

***

## 14. 后台管理模块（运营端）

> 业务码前缀 `Axxxx`（运营后台独立子域，可由 `api-admin.yuanyuangao.com/v1` 提供）
> 所有接口需 `is_admin=true` 角色鉴权

### 14.1 运营登录

- **POST** `/admin/auth/login`
- 请求：`{ "username": "...", "password": "...", "totp": "123456" }`
- 响应：返回运营 JWT

### 14.2 用户管理

| 接口     | 方法   | 路径                                       | 描述                          |
| ------ | ---- | ---------------------------------------- | --------------------------- |
| 用户列表   | GET  | `/admin/users?keyword=...&page=1`        | 多条件分页                       |
| 用户详情   | GET  | `/admin/users/{user_id}`                 | 含打卡/账户/团队                   |
| 调整用户计划 | POST | `/admin/users/{user_id}/adjust-plan`     | 本期用于运营**手工开通 365 天计划**（无支付） |
| 调整用户返现 | POST | `/admin/users/{user_id}/adjust-cashback` | ⛔ **本期暂不实现**（无提现场景）         |
| 禁用用户   | POST | `/admin/users/{user_id}/disable`         | 封禁                          |

### 14.3 订单与退款

> ⛔ **本期暂不实现**（无微信支付、无用户提现、无订单可管）。

| 接口   | 方法   | 路径                                 |
| ---- | ---- | ---------------------------------- |
| 订单列表 | GET  | `/admin/orders?status=paid&page=1` |
| 订单详情 | GET  | `/admin/orders/{order_id}`         |
| 退款   | POST | `/admin/orders/{order_id}/refund`  |

### 14.4 团队监控

| 接口   | 方法   | 路径                                |
| ---- | ---- | --------------------------------- |
| 团队列表 | GET  | `/admin/teams?keyword=...&page=1` |
| 团队详情 | GET  | `/admin/teams/{team_id}`          |
| 强制解散 | POST | `/admin/teams/{team_id}/disband`  |

### 14.5 内容审核

- 政策审核（见 10.7）
- 动态审核：

| 接口      | 方法   | 路径                                    |
| ------- | ---- | ------------------------------------- |
| 动态审核列表  | GET  | `/admin/square/posts?status=pending`  |
| 审核通过/拒绝 | POST | `/admin/square/posts/{post_id}/audit` |

### 14.6 数据看板

- **GET** `/admin/dashboard/overview`
- 响应：

```json
{
  "dau": 12345,
  "mau": 67890,
  "new_signups_today": 320,
  "active_teams": 2345,
  "publishing_policies": 56,
  "cashback_paid_today": 123400
}
```

- **GET** `/admin/dashboard/retention?start_date=...&end_date=...`
- **GET** `/admin/dashboard/funnel?step=register→first_checkin→7d→30d`

### 14.7 操作审计日志

- **GET** `/admin/audit-logs?operator=usr_admin_001&page=1`
- 响应：审计日志列表

***

## 15. 小程序平台兼容性规范（依据 [MINIPROGRAM_DEV.md](file:///d:/Trae项目/YYG/docs/MINIPROGRAM_DEV.md) 第 6 章）

> 本章约束**后端必须为前端兼容性问题提供兜底**。前端在调用 API 时若命中平台差异，期望后端能识别客户端能力并返回合适响应。

### 15.1 客户端能力探测（请求头 / 探测接口）

#### 15.1.1 请求头探测

后端按 `X-Platform-OS` + `X-SDK-Version` + `X-Device-Model` 判断能力差异（已在 [1.8.1](#181-客户端平台枚举x-platform-os-合法值) 中定义）。

#### 15.1.2 探测接口 `GET /v1/client/capability`

> 用于前端在关键路径（如打开每日打卡音频）前获取后端推荐的能力降级方案。

**请求头**：同 [1.1](#11-请求规范)

**响应**：

```json
{
  "code": 0,
  "data": {
    "audio_strategy": "mp3_then_fallback_m4a",
    "image_formats": ["webp", "jpg", "png"],
    "allow_high_perf_mode": true,
    "allow_quic": true,
    "allow_http2": true,
    "recommended_image_lazy_load": true,
    "min_storage_sync_safe": true
  },
  "trace_id": "..."
}
```

| 字段 | 取值 | 含义 |
| --- | --- | --- |
| `audio_strategy` | `mp3_only` / `m4a_only` / `mp3_then_fallback_m4a` / `hls_stream` | 音频播放策略：iOS 26.2+ 客户端返回 `m4a_only`，鸿蒙返回 `hls_stream` |
| `image_formats` | array | 后端 CDN 实际支持的图片格式 |
| `allow_high_perf_mode` | bool | Android 端是否建议开启 `useHighPerformanceMode` |
| `allow_quic` / `allow_http2` | bool | 网络能力开关 |
| `recommended_image_lazy_load` | bool | 是否建议开启图片懒加载（WebView 渲染时为 true） |
| `min_storage_sync_safe` | bool | 当前平台 `setStorageSync` 是否安全（iOS 老版本 / 纯血鸿蒙为 false） |

**后端决策规则**：

| 条件 | 返回值 |
| --- | --- |
| `X-Platform-OS == 'ios'` 且 `X-SDK-Version >= '3.0.0'` | `audio_strategy = m4a_only` |
| `X-Platform-OS == 'ohos'` 或 `X-Platform-OS == 'ohos_pc'` | `audio_strategy = hls_stream` |
| `X-Platform-OS == 'devtools'` | 所有能力默认开启，便于调试 |
| 其他 | `audio_strategy = mp3_then_fallback_m4a` |

### 15.2 平台能力差异表（与本项目相关）

#### 15.2.1 音频播放（InnerAudioContext）

| 平台 | 问题 | 后端兜底 |
| --- | --- | --- |
| iOS 26.2+ | InnerAudioContext 播放 mp3 异常 | `GET /v1/media/audio` 返回 m4a/aac 替代源（带 `format` 字段标识） |
| HarmonyOS 手机端 | InnerAudioContext 播放网络音频可能闪退 | 推荐 `HLS` 流（`format = hls`） |
| iOS | 后台播放受限 | 提示用户保持前台 |
| Android | 行为正常 | mp3 即可 |

#### 15.2.2 视频组件

| 平台 | 差异 | 后端兜底 |
| --- | --- | --- |
| iOS | 默认禁止自动播放 | 不涉及（无视频业务） |
| iOS | `enable-progress-gesture` 行为差异 | 不涉及 |

#### 15.2.3 图片

| 平台 | 差异 | 后端兜底 |
| --- | --- | --- |
| Android | webP 原生支持 | CDN 优先返回 webP |
| iOS 老旧系统 | webP 解码失败 | `Accept` 头协商，CDN 降级返回 jpg |
| `mode="top/bottom/..."` | 仅 WebView 引擎支持 | 前端按需用 `Skyline`/`WebView` 切换 |

#### 15.2.4 位置 API

| 平台 | 差异 | 后端兜底 |
| --- | --- | --- |
| iOS 14+ | 需精确位置授权 | 后端允许模糊位置降级（同城市匹配） |
| iOS | 高精度定位耗时更长 | 客户端先返回城市粗定位，再异步升级 |
| Android 12+ | 持续定位需前台服务 | 不涉及（仅一次定位） |

#### 15.2.5 网络 API

| 平台 | 差异 | 后端兜底 |
| --- | --- | --- |
| Android | `useHighPerformanceMode` 默认 `true`（3.5.0+） | 后端无需干预 |
| iOS | `useHighPerformanceMode` 默认 `false` | 同上 |
| iOS | QUIC 仅 gQUIC-Q43 | 后端网关支持 gQUIC-Q43 + h3 双协议 |
| Android | QUIC gQUIC-Q43（v8.0.54 前）/ h3（v8.0.54+） | 同上 |

### 15.3 最低基础库版本策略

| 基础库范围 | 后端兼容策略 |
| --- | --- |
| `≥ 3.0.0` | 默认方案，返回全部能力字段 |
| `2.30.0 - 2.99.99` | 响应中 `allow_skyline = false`，`enable_custom_tabbar = false` |
| `< 2.30.0` | 前端应在启动时弹窗提示升级微信（不进入主流程），后端不做兼容 |

> 后端可在 `GET /v1/client/capability` 响应中追加 `min_sdk_required` 字段，前端比对 `wx.getAppBaseInfo().SDKVersion` 决定是否进入主流程。

### 15.4 鸿蒙 OS 专项适配

| 兼容项 | 现状 | 后端建议 |
| --- | --- | --- |
| `wx.login` / `wx.checkSession` | ✅ 支持 | 无需特殊处理 |
| `wx.getLocation` | 可能需单独权限申请 | 城市定位做"上次缓存优先 + 失败降级到省" |
| `InnerAudioContext` | 播放网络音频可能闪退 | 返回 HLS 流地址 + 客户端 try-catch 兜底 |
| `wx.setStorageSync` | 纯血鸿蒙有异常 | 迁移数据走云端 + 5 个 localStorage key 异步清除 |
| `requestSubscribeMessage` | ✅ 支持 | 无差异 |
| `enhanced`（scroll-view） | 不支持 | 不影响主流程 |
| 同层渲染（cover-view 等） | 行为可能与 Android 不同 | 不影响主流程 |

### 15.5 `wx.canIUse` 兼容性速查

| 能力 | 最低基础库 | 后端在 `/v1/client/capability` 中的字段 |
| --- | --- | --- |
| `wx.openPrivacyContract` | 2.32.3 | `support_privacy_contract` |
| `wx.onNeedPrivacyAuthorization` | 2.32.3 | `support_privacy_listener` |
| `wx.getPrivacySetting` | 2.32.3 | `support_privacy_setting` |
| `button open-type="getPhoneNumber"` 新版（返回 `code`） | 2.21.2 | `support_phone_secure_v2`（影响 [2.6](#26-绑定手机号) 走旧版/新版） |
| `wx.requestSubscribeMessage` | 2.4.0 | `support_subscribe_message` |
| `wx.createInnerAudioContext` | 1.6.0 | 始终 true（但有平台差异） |

> 前端在调用前需先 `wx.canIUse('xxx')`，**后端不替代该判断**，仅在响应中给出能力开关供前端参考。

---

## 16. 前端对接规范（依据 [MINIPROGRAM_DEV.md](file:///d:/Trae项目/YYG/docs/MINIPROGRAM_DEV.md) 第 7 章）

> 本章约定**前端与后端的协作规范**。所有规范均同步自 MINIPROGRAM_DEV.md 第 7 章「最佳实践」。

### 16.1 性能优化

#### 16.1.1 启动性能

**前端要求**：

- `app.json` 开启 `lazyCodeLoading: "requiredComponents"`。
- 启动时**严禁** 大规模同步 `wx.getStorageSync`（影响首屏时间），所有本地数据读取用异步 API。
- 主包 ≤ 2 MB；总包（主包 + 分包）≤ 30 MB。

**后端要求**：

- 启动期必请求的接口（`/v1/users/me`、`/v1/config/client` 等）需 P99 < 200ms，**强烈建议启用 HTTP/2 + QUIC**。
- 启动配置接口（`/v1/config/client`）支持 `If-None-Match` / `ETag`，前端用 304 减少流量。

#### 16.1.2 渲染性能

**前端要求**：

- `setData` 合并更新，**严禁** 在循环中逐项 `setData({ [`list[${i}]`]: ... })`。
- 单页数据 ≤ 100 条；长列表使用 Skyline `list-view` 或分页加载。
- 图片开启 `lazy-load`（WebView）；优先使用 webP。

**后端要求**：

- 列表接口默认分页 `page_size = 20`；最大 100（见 [1.5](#15-分页规范)）。
- 资源 CDN 开启 `Vary: Accept`，按 `Accept` 头协商 webP / jpg。
- 列表响应中**禁止** 嵌套超过 3 层 JSON。

#### 16.1.3 网络性能

**前端要求**：

- 启用 `useHighPerformanceMode`（Android 3.5.0+）。
- 启用 `enableHttp2` 和 `enableQuic`。
- 启用 `enableCache` 利用 HTTP 缓存。
- 合理使用 `Promise.all` / `Promise.allSettled`。

**后端要求**：

- 部署层支持 HTTP/2 + QUIC（h3 + gQUIC-Q43 双协议）。
- 静态资源开启 `Cache-Control: public, max-age=31536000`（带 hash 指纹）。
- 业务 API 响应 `Cache-Control: no-store`（避免脏数据）。
- 客户端上传大文件（> 5 MB）时分片（见 [12.1](#121-获取上传凭证)）。

### 16.2 网络请求最佳实践

#### 16.2.1 通用请求封装

**前端示例**（前端在 `common.js` 中维护的请求库应至少实现）：

```javascript
function request(options) {
  return new Promise((resolve, reject) => {
    wx.request({
      ...options,
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // 触发 [2.1] 重新登录流程
          wx.removeStorageSync('token')
          reject({ code: 401, message: '未登录' })
        } else {
          reject({ code: res.statusCode, message: res.data.message })
        }
      },
      fail(err) {
        reject({ code: -1, message: '网络请求失败', err })
      }
    })
  })
}
```

**后端要求**：

- 4xx / 5xx 响应**必须** 返回与成功响应相同的 JSON 结构（`code` / `message` / `trace_id`）。
- HTTP 401 时**不要** 直接返回 401 body，由业务层在 code = 10001 中返回。
- 失败响应**不缓存**。

#### 16.2.2 并发与频率

| API | 频率限制 | 后端 429 错误码 |
| --- | --- | --- |
| `wx.login` | 每天每小程序 5 万次 | - |
| `wx.request` | 10 个并发上限；10s 内 ≤ 100 次 | 10105 |
| `wx.getLocation` | 基础库 2.17.0+ 起 5s 1 次 | 10105 |
| `wx.requestSubscribeMessage` | 每次需用户确认 | - |
| `POST /v1/checkins` | 每天每用户 1 次 | 10104（已打卡） |
| `POST /v1/users/me/phone` | 每用户 5 分钟 1 次 | 10105 |
| `POST /v1/account/cashback/withdraw` ⛔ | 每天每用户 1 次 | 10105 |

> 后端需在 429 响应中携带 `Retry-After: <秒数>` 头。

#### 16.2.3 错误处理

**前端要求**：

- 业务码 `0` 视为成功；非 0 弹 toast 提示。
- 网络层失败（`fail`）必须弹"网络异常，请重试"并触发**自动重试 1 次**（GET 请求）。
- 401 触发重新登录后，**自动重放原请求 1 次**。
- 全局 `onError` / `onUnhandledRejection` 上报到 [16.4](#164-调试与日志) 中的 `POST /v1/logs`。

**后端要求**：

- 业务码 `>= 10000` 表示业务异常；`>= 500` 表示服务端异常。
- 5xx 响应**严禁** 暴露堆栈、SQL、内部 IP；仅返回 `message` + `trace_id`。
- 数据库唯一约束冲突应返回 `code = 10104` + 友好 `message`（如"今天已打卡"）。

### 16.3 隐私合规

#### 16.3.1 `app.json` 声明

前端必须在 `app.json` 中声明所用隐私 API：

```json
{
  "requiredPrivateInfos": ["chooseImage", "getLocation"]
}
```

#### 16.3.2 隐私协议流程

**前端流程**：

1. 进入小程序时调用 `wx.getPrivacySetting`，若 `needAuthorization = true` 则**阻塞** 业务流程。
2. 注册 `wx.onNeedPrivacyAuthorization` 监听器。
3. 用户点击"同意"按钮后，调用 `wx.openPrivacyContract`，回调成功后 `res.resolve({ event: 'agree' })`。
4. 拒绝时 `res.resolve({ event: 'disagree' })`，前端关闭对应功能入口。

**后端要求**：

- 用户在 `event: 'agree'` 后**后端不感知**；可在下次业务请求的 `X-Privacy-Accepted: true` 头中透传，便于审计。
- 后端**不存储** 协议版本号，由前端在请求中以 `X-Privacy-Version: <semver>` 头传递，便于后端日志审计。
- 任何涉及 `phone` / `location` 的接口**必须** 校验 `X-Privacy-Accepted: true`，否则返回 `code = 10301 隐私未授权`。

#### 16.3.3 错误码（新增）

| code | HTTP | 含义 | 处理 |
| --- | --- | --- | --- |
| 10301 | 403 | 隐私协议未授权 | 引导用户阅读并同意隐私协议 |
| 10302 | 403 | 隐私协议版本过旧 | 前端强制更新协议 |
| 10303 | 403 | `requiredPrivateInfos` 声明缺失 | 提示用户升级小程序 |

### 16.4 调试与日志

#### 16.4.1 客户端日志

**前端要求**：

- 使用 `wx.getLogManager()` 上报本地日志（`info` / `warn` / `error`）。
- 关键路径（登录、支付、提现⛔、分享）使用 `wx.getRealtimeLogManager()` 实时上报。
- 全局 `onError` / `onUnhandledRejection` 注册到 `app.js`，捕获后**异步** 上报。

#### 16.4.2 日志上报接口 `POST /v1/logs`

**请求**：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `level` | enum | 是 | `debug` / `info` / `warn` / `error` |
| `tag` | string | 是 | 模块标签（`login` / `payment` / `checkin` / `api` ...） |
| `msg` | string | 是 | 日志内容 |
| `stack` | string | 否 | 错误堆栈 |
| `context` | object | 否 | 业务上下文（user_id / page / action） |
| `client_ts` | int | 是 | 客户端时间戳（ms） |
| `sdk_version` | string | 否 | `wx.getAppBaseInfo().SDKVersion` |
| `platform_os` | string | 否 | `wx.getDeviceInfo().platform` |
| `device_model` | string | 否 | `wx.getDeviceInfo().model` |
| `trace_id` | string | 否 | 与请求头 `X-Request-Id` 一致 |

**响应**：

```json
{ "code": 0, "data": { "log_id": "log_xxx" } }
```

**后端要求**：

- 异步落库或写 Kafka，**严禁** 同步写阻塞业务。
- 写入字段至少包含：客户端 `trace_id`、服务端 `received_at`、用户 `id`（已登录）、`level` / `tag` / `msg` / `stack`。
- `error` 级别日志需触发企业微信/钉钉告警。

#### 16.4.3 实时日志关联

- 前端 `wx.getRealtimeLogManager().info('登录成功', { openid })` 时，需携带当前 `trace_id`。
- 后端在响应头中回写 `X-Trace-Id: <uuid>`，前端在 `RealtimeDebugger` 工具中可通过该 id 串接前后端日志。

### 16.5 安全建议

#### 16.5.1 传输与存储

**前端要求**：

- 全部走 HTTPS；**严禁** 在前端硬编码密钥、AK/SK、AppSecret。
- 敏感数据（手机号、token、unionid）**禁止** 写入 `wx.setStorage`；如必须写，需经业务层 AES-256 加密 + 自定义 key 派生。
- `wx.getStorageSync('token')` 读取后**禁止** 写入日志。

**后端要求**：

- 微信 `AppSecret` 仅存在后端环境变量；调用 `jscode2session` 的代码**严禁** 出现在前端。
- JWT secret 定期轮换；access token 7 天 + refresh token 30 天。
- 用户手机号入库前 AES-256 加密；展示时由后端返回脱敏值（如 `138****1234`）。

#### 16.5.2 业务风控

| 场景 | 后端校验 |
| --- | --- |
| 登录 | `code` 单次使用，5 分钟有效；同 IP 1 分钟内 ≤ 10 次 |
| 打卡 | 同用户同日唯一；服务端校验 `biz_date` 与北京时间 |
| 提交测评 | 同用户 24 小时内 ≤ 3 次 |
| 提现⛔ | 实名 + 银行卡四要素 + 风控黑名单 |
| 政策评论 | 内容安全云（腾讯云 TMS / 阿里云内容安全）双检 |
| 邀请码 | 服务端生成，6 位数字 + 字母，30 天有效 |

#### 16.5.3 防 SQL 注入 / XSS

- 全部使用 ORM 参数化查询；**严禁** 拼接 SQL 字符串。
- 用户输入字段（评论、政策正文、昵称）入库前 `bleach` 清洗；展示时 `escape`。
- 文件上传做 MIME + 魔数双重校验（见 [12](#12-文件上传模块)）。

#### 16.5.4 登录安全

- 后端定期 `wx.checkSession`（前端配合）：连续 7 天未活跃需重新登录。
- 关键操作（修改手机号、提现⛔、注销）需二次短信验证码。
- 登录态 401 响应**严禁** 暴露 token 解析后的 payload。

### 16.6 性能与体验

| 项 | 要求 | 监控指标 |
| --- | --- | --- |
| 首屏时间 | P95 ≤ 1.5s | 启动到首页 `onReady` |
| 接口 P95 | ≤ 300ms | 所有非上传接口 |
| 接口 P99 | ≤ 1s | 同上 |
| 错误率 | < 0.5% | `code != 0` 占比 |
| JS 异常 | < 0.1% | `onError` 触发次数 / DAU |

> 上述指标接入监控告警（参考 SKILL：AI 监控与可观测性）。

---

***

## 附录 A：完整数据字典（前端 → 后端 字段映射）

> 选取项目关键对象，列出与 API 字段的对应关系，便于后端建模与前后端联调。

### A.1 用户对象 `User`

| 前端字段              | API 字段             | 类型       | 备注                                       |
| ----------------- | ------------------ | -------- | ---------------------------------------- |
| `id`              | `id`               | string   | 业务主键，前缀 `usr_`                           |
| `nickname`        | `nickname`         | string   | 微信昵称                                     |
| `avatarUrl`       | `avatar_url`       | string   | 头像 URL                                   |
| `phone`           | `phone`            | string   | 加密存储，仅展示脱敏                               |
| `role`            | `role`             | enum     | `user` / `admin` / `editor` / `reviewer` |
| `isAdmin`         | `is_admin`         | bool     | 是否后台管理员                                  |
| `planStatus`      | `plan_status`      | enum     | `none` / `trial21` / `year365`           |
| `planStartedAt`   | `plan_started_at`  | datetime | <br />                                   |
| `teamId`          | `team_id`          | string   | 所属小队 ID                                  |
| `trial21Unlocked` | `trial21_unlocked` | bool     | 21 天体验是否解锁                               |
| `inviteProgress`  | `invite_progress`  | int      | 邀请达成 0-3                                 |
| `checkedDays`     | `checked_days`     | int      | 累计打卡                                     |
| `consecutiveDays` | `consecutive_days` | int      | 连续打卡                                     |

### A.2 打卡对象 `Checkin`

| 前端字段                   | API 字段                   | 类型       | 备注                 |
| ---------------------- | ------------------------ | -------- | ------------------ |
| `date`                 | `date`                   | date     | YYYY-MM-DD（东八区自然日） |
| `mainCheckinCompleted` | `main_checkin_completed` | bool     | <br />             |
| `reflection`           | `reflection`             | text     | <br />             |
| `completedAt`          | `completed_at`           | datetime | <br />             |
| `tasks[]`              | `tasks`                  | array    | 关联子任务列表            |
| `cashbackEarned`       | `cashback_earned`        | int（分）   | <br />             |

### A.3 团队对象 `Team`

| 前端字段                  | API 字段                  | 类型     |
| --------------------- | ----------------------- | ------ |
| `name`                | `name`                  | string |
| `goal`                | `goal`                  | enum   |
| `maxMembers`          | `max_members`           | int    |
| `inviteCode`          | `invite_code`           | string |
| `teamConsecutiveDays` | `team_consecutive_days` | int    |
| `growthValue`         | `growth_value`          | int    |
| `members[]`           | `members`               | array  |

### A.4 政策对象 `Policy`

| 前端字段                        | API 字段                      | 类型             |
| --------------------------- | --------------------------- | -------------- |
| `id`                        | `id`                        | string         |
| `title`                     | `title`                     | string         |
| `sourceName`                | `source_name`               | string         |
| `sourceUrl`                 | `source_url`                | string         |
| `policySummary`             | `policy_summary`            | text           |
| `effectiveDate`             | `effective_date`            | date           |
| `region`                    | `region`                    | string         |
| `stage`                     | `stage`                     | string         |
| `gradeRange[]`              | `grade_range`               | array\[string] |
| `domains[]`                 | `domains`                   | array\[string] |
| `influenceAbilities[]`      | `influence_abilities`       | array\[string] |
| `parentActionSuggestions[]` | `parent_action_suggestions` | array\[text]   |
| `generatedTasks[]`          | `generated_tasks`           | array\[object] |
| `frontDisplayTitle`         | `front_display_title`       | string         |
| `frontDisplaySummary`       | `front_display_summary`     | string         |
| `impactExplanation`         | `impact_explanation`        | text           |
| `monthlySuggestions[]`      | `monthly_suggestions`       | array\[text]   |
| `weeklyTaskSuggestions[]`   | `weekly_task_suggestions`   | array\[object] |
| `focusDirections[]`         | `focus_directions`          | array\[string] |
| `childImpactAnalysis`       | `child_impact_analysis`     | text           |
| `contentStatus`             | `content_status`            | enum           |
| `version`                   | `version`                   | int            |
| `createdBy`                 | `created_by`                | string         |
| `reviewedBy`                | `reviewed_by`               | string         |
| `reviewComment`             | `review_comment`            | text           |
| `createdAt`                 | `created_at`                | datetime       |
| `updatedAt`                 | `updated_at`                | datetime       |
| `publishedAt`               | `published_at`              | date           |
| `publishedAtSystem`         | `published_at_system`       | datetime       |

### A.5 子任务对象 `SubTask`

| 前端字段             | API 字段             | 类型                              |
| ---------------- | ------------------ | ------------------------------- |
| `id`             | `id`               | string                          |
| `title`          | `title`            | string                          |
| `category`       | `category`         | string                          |
| `description`    | `description`      | text                            |
| `frequency`      | `frequency`        | string                          |
| `estimatedTime`  | `estimated_time`   | string                          |
| `gradeRange[]`   | `grade_range`      | array\[string]                  |
| `abilityTags[]`  | `ability_tags`     | array\[string]                  |
| `source`         | `source`           | enum（`daily` / `policy_impact`） |
| `sourcePolicyId` | `source_policy_id` | string                          |
| `completed`      | `completed`        | bool                            |
| `completedAt`    | `completed_at`     | datetime                        |

### A.6 每日课程对象 `DailyLesson`

| 前端字段                    | API 字段                 | 类型               |
| ----------------------- | ---------------------- | ---------------- |
| `day`                   | `day`                  | int              |
| `theme`                 | `theme`                | string           |
| `task`                  | `task`                 | string           |
| `coverImage`            | `cover_image`          | string           |
| `audioSrc`              | `audio_src`            | string           |
| `audioTitle`            | `audio_title`          | string           |
| `audioSubtitle`         | `audio_subtitle`       | string           |
| `audioDuration`         | `audio_duration`       | string           |
| `quote`                 | `quote`                | string           |
| `meaning`               | `meaning`              | string           |
| `copy`                  | `copy`                 | text             |
| `pronunciation[]`       | `pronunciation`        | array\[string]   |
| `speakingExamples[]`    | `speaking_examples`    | array\[{en, zh}] |
| `definitionNotes[]`     | `definition_notes`     | array\[string]   |
| `takeaways[]`           | `takeaways`            | array\[string]   |
| `translationPractice[]` | `translation_practice` | array\[string]   |
| `encouragement`         | `encouragement`        | string           |

***

## 附录 B：接口变更日志

| 版本   | 日期         | 变更内容                                                                                                | 作者    |
| ---- | ---------- | --------------------------------------------------------------------------------------------------- | ----- |
| v1.0 | 2026-06-17 | 初稿，覆盖 14 大模块共 100+ 接口                                                                              | 后端架构组 |
| v1.1 | 2026-06-17 | **1) 1.1** 新增 `X-Platform-OS` / `X-SDK-Version` / `X-Device-Model` 请求头与后端开发要求；<br/>**2) 1.8** 新增「小程序客户端约束」章节（平台枚举 / localStorage 限制 / 兼容性兜底 / 最低基础库）；<br/>**3) 2.1** 微信登录补充前端调用示例与 `wx.checkSession` 频率说明；<br/>**4) 2.6** 绑定手机号重写为基础库 2.21.2 新版流程，新增错误码 10204/10205/10206；<br/>**5) 12.1/12.3** 文件上传补充客户端约束 + credential 参数表 + 完整前端流程示例；<br/>**6) 15. 平台兼容性规范**（依据 MINIPROGRAM_DEV.md 第 6 章）：音频/视频/图片/位置/网络/鸿蒙 OS 平台差异，新增 `GET /v1/client/capability` 探测接口；<br/>**7) 16. 前端对接规范**（依据 MINIPROGRAM_DEV.md 第 7 章）：性能优化 / 网络请求 / 隐私合规 / 调试日志 / 安全建议，新增 `POST /v1/logs` 日志上报接口与错误码 10301-10303 | 后端架构组 |
| v1.2 | 2026-06-17 | **1) §2.7 新增** `POST /v1/users/me/migrate-localstorage` 用户数据迁移接口（响应 `migrated` / `skipped` 双计数器，新增错误码 20001-20003）；<br/>**2) §8.0-8.3 V8 测评字段统一 snake_case**（`grade_group` / `english_level` / `core_insight` / `recommended_plan` / `primary_path` / `hook_text` / `cta_text` / `child_grade` 等），原 §8.2 中 `gradeGroup`/`englishLevel` 等 camelCase 字段全部修正；<br/>**3) §8.1 模板响应 questions.key** `studyStatus` → `study_status`；<br/>**4) §4.5 业务字段约定补充** `plan_status` 6 值枚举（`none` / `trial7` / `trial21` / `21d_plan` / `100d_plan` / `year365`），与 DATABASE.md 双端对齐；<br/>**5) §9.2 章节号去重**（原有两个 §9.2，现依次修正为 §9.2 咨询 / §9.3 兑换 / §9.4 兑换记录 / §9.5 徽章）；<br/>**6) §2 目录细化**为 7 个子节并加锚点 | 后端架构组 |
| v1.3 | 2026-06-17 | **1) 顶部暂不实现表新增**「微信登录」行（`POST /v1/auth/wechat-login` / `refresh` / `logout`）；<br/>**2) §1.4 鉴权与签名重构**为三段式：1.4.1 本期鉴权模式（v1 可选鉴权，匿名用户行为约定 + `X-Device-Id` 推荐必填） / 1.4.2 v2 启用后的 JWT 设计（保留供后续实现） / 1.4.3 错误码本期调整（10001-10002 本期不返回）；<br/>**3) §2.1 / §2.2 / §2.3 三个章节**统一加 ⛔ 暂不实现标注 + 启用条件说明，契约完整保留；<br/>**4) MVP 替代方案表新增**「微信登录」替代做法 | 后端架构组 |

> 文档维护约定：
>
> 1. 任何破坏性变更（字段删除、类型变更、URL 移除）必须升级主版本号；
> 2. 字段新增、描述调整走小版本号；
> 3. 接口废弃需在文档中标注 `Deprecated`，并保留至少 3 个小版本周期。

***

**END OF API DOC**
