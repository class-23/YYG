# 宝妈英语早操小程序项目说明

更新时间：2026-06-16

## 1. 项目定位

本项目是一个面向宝妈群体的微信小程序，当前名称为「宝妈英语早操」。产品核心不是单纯的英语学习工具，而是围绕“妈妈先成长、孩子再被带动”的亲子英语与女性成长平台。

当前小程序已经具备以下方向的原型能力：

- 每日英语早操打卡：每天 10 分钟，通过音频、金句、表达拆解和打卡记录帮助妈妈建立学习节奏。
- 妈妈成长计划：提供 21 天体验计划和 365 天成长计划，强调连续打卡、成长金、徽章和阶段性蜕变。
- 孩子阅读能力测评：通过 1-9 年级分层阅读任务，输出孩子阅读画像、英语等级、语文阅读状态、薄弱标签和训练建议。
- 姐妹同行成长区：支持创建或加入成长小队，模拟邀请、打卡陪伴、点赞、鼓励、提醒等社群互动。
- 蜕变广场与权益承接：承载用户成长展示、社交连接、权益页、课程转化页等后续商业闭环。
- 政策知识库后台原型：内置教育政策内容、标签、版本、审核、列表、编辑等页面，用于后续把教育政策转化为家长可执行的成长任务。

当前代码是 Taro 编译后的微信小程序产物，适合直接导入微信开发者工具预览。它不是原始 Taro 源码目录，因此业务逻辑已被 webpack 打包到各页面 JS 和公共 JS 中。

## 2. 当前项目状态

项目当前属于「可演示的小程序前端原型 / MVP 产物」：

- 可以在微信开发者工具中以小程序项目打开。
- 页面路由、tabBar、样式、静态素材、音频播放、本地打卡、本地小队状态等已经存在。
- 目前没有接入真实后端服务，没有发现实际 `wx.request` 业务接口调用。
- 多数业务数据是前端静态数据或本地存储模拟数据。
- 支付、邀请有效性、审核发布、政策新增编辑等动作当前多为前端模拟或按钮占位。
- 当前 `project.config.json` 使用 `touristappid`，正式发布前需要替换为真实小程序 AppID。

## 3. 技术栈

### 3.1 前端框架

- Taro 3.6.40
- React 风格组件写法，经 Taro 编译为微信小程序运行时代码
- 微信小程序原生运行环境

### 3.2 构建产物特征

目录中的文件是编译后的 dist：

- `app.js`：小程序入口运行时代码。
- `app.json`：页面路由、窗口样式、tabBar 配置。
- `app.wxss` / `common.wxss` / 页面 `.wxss`：全局与页面样式。
- `runtime.js`、`taro.js`、`vendors.js`、`common.js`：webpack/Taro/runtime/公共业务模块。
- `pages/**/index.js`：各页面编译后的业务逻辑和渲染函数。
- `base.wxml`、`comp.*`：Taro 统一模板和组件适配层。

### 3.3 微信小程序能力使用情况

当前代码已使用或预留的微信能力包括：

- 页面跳转：`navigateTo`、`switchTab`、`pageScrollTo`
- 本地存储：`getStorageSync`、`setStorageSync`
- 音频播放：`createInnerAudioContext`
- 分享：`useShareAppMessage`、按钮 `openType="share"`
- 剪贴板：`setClipboardData`
- Toast 提示：`showToast`

当前未发现真实业务网络请求：

- 未发现 `wx.request` / `Taro.request` 调用真实接口。
- 未发现 `wx.login` 登录流程。
- 未发现 `uploadFile` 文件上传流程。
- 未发现微信支付调用。

## 4. 运行与开发说明

### 4.1 当前目录

```text
/Users/uu/Documents/Codex/2026-06-03/ip/outputs/mom-english-taro/dist
```

### 4.2 微信开发者工具打开方式

1. 打开微信开发者工具。
2. 选择「导入项目」。
3. 项目目录选择当前 `dist` 目录。
4. AppID 当前为 `touristappid`，可先用测试号或游客模式预览。
5. 正式联调时把 `project.config.json` 中的 `appid` 替换为真实小程序 AppID。

### 4.3 注意事项

当前目录是编译后产物，不建议在这里长期做业务开发。后续如果要持续迭代，建议恢复或建立原始 Taro 源码工程，目录通常包括：

```text
src/
  app.config.ts
  app.tsx
  pages/
  components/
  services/
  stores/
  assets/
```

然后用 Taro 构建生成当前 `dist`。

## 5. 目录结构说明

```text
dist/
  app.json                         小程序页面、窗口、tabBar 配置
  project.config.json              微信开发者工具项目配置
  app.js                           小程序入口
  app.wxss                         全局样式
  common.js                        公共业务数据与工具模块打包产物
  vendors.js                       第三方依赖打包产物
  runtime.js                       webpack 运行时代码
  taro.js                          Taro 运行时
  assets/
    yuanyuangao-portrait.jpg       首页人物图
    daily/
      day1-keep-the-ball-rolling.jpg
      day1-keep-the-ball-rolling.mp3
  pages/
    home/                          首页
    daily/                         今日打卡
    transformation-square/         蜕变广场
    rewards/                       我的成长权益
    mom-growth-plan/               妈妈成长打卡计划
    sister-growth/                 姐妹同行成长区
    sister-invite/                 姐妹邀请落地页
    sister-poster/                 姐妹邀请海报
    love-connection/               脱单交友区
    growth/                        阅读成长路径
    kid-growth-assessment/         阅读能力测评
    policy-admin/                  政策知识库后台入口
    policy-admin/list/             政策内容列表
    policy-admin/editor/           新增/编辑政策内容
    policy-admin/tags/             政策标签管理
    policy-admin/versions/         政策版本记录
    policy-admin/review/           内容发布审核
    signup/                        活动报名
    account/                       返现账户
    calendar/                      成长日历
    poster/                        朋友圈海报
    content/                       宝妈成长内容
    courses/                       课程转化
```

## 6. 页面路由与功能说明

页面配置来自 `app.json`。

### 6.1 TabBar 页面

| 页面 | 路由 | 功能 |
| --- | --- | --- |
| 首页 | `pages/home/index` | 品牌入口，展示原原高 English Morning、妈妈成长入口、孩子成长入口、蜕变广场入口、今日英语早操摘要 |
| 打卡 | `pages/daily/index` | 今日英语早操、音频播放、学习拆解、反思输入、完成打卡、政策关联任务、小队提醒 |
| 蜕变广场 | `pages/transformation-square/index` | 成长展示和社交承接入口，连接姐妹同行、交友、成长故事等方向 |
| 权益 | `pages/rewards/index` | 成长权益、返现、计划权益、课程权益承接 |

### 6.2 成长与转化页面

| 页面 | 路由 | 功能 |
| --- | --- | --- |
| 妈妈成长计划 | `pages/mom-growth-plan/mom-growth-plan` | 21 天体验、365 天计划、成长曲线、徽章、成长金、姐妹同行入口、交友权益入口 |
| 姐妹同行成长区 | `pages/sister-growth/index` | 创建小队、加入小队、查看小队状态、点赞、抱抱、留言鼓励、邀请进度 |
| 姐妹邀请 | `pages/sister-invite/index` | 通过邀请码进入小队邀请流程 |
| 姐妹邀请海报 | `pages/sister-poster/index` | 生成邀请海报展示页 |
| 朋友圈海报 | `pages/poster/index` | 打卡后生成朋友圈卡片 |
| 活动报名 | `pages/signup/index` | 活动或课程报名承接 |
| 课程转化 | `pages/courses/index` | 课程购买/转化承接 |
| 返现账户 | `pages/account/index` | 成长金、返现账户展示 |
| 成长日历 | `pages/calendar/index` | 打卡日历和成长轨迹展示 |
| 宝妈成长内容 | `pages/content/index` | 内容阅读、成长文章或课程内容承接 |
| 脱单交友区 | `pages/love-connection/love-connection` | 成长型交友、同城活动、情感陪伴权益说明 |

### 6.3 孩子阅读页面

| 页面 | 路由 | 功能 |
| --- | --- | --- |
| 阅读成长路径 | `pages/growth/index` | 孩子英语阅读成长路线、卡点与路径说明 |
| 阅读能力测评 | `pages/kid-growth-assessment/kid-growth-assessment` | 1-9 年级阅读测评，生成孩子阅读画像 JSON |

### 6.4 政策后台页面

| 页面 | 路由 | 功能 |
| --- | --- | --- |
| 政策知识库 | `pages/policy-admin/index` | 政策后台首页，展示内容库、标签、审核、版本等入口 |
| 政策列表 | `pages/policy-admin/list/index` | 按地区、学段、状态筛选政策内容 |
| 新增/编辑政策 | `pages/policy-admin/editor/index` | 展示政策录入字段、政策解读字段、生成提示词预留 |
| 标签管理 | `pages/policy-admin/tags/index` | 管理地区、学段、年级、政策领域、能力、任务、人群等标签 |
| 版本记录 | `pages/policy-admin/versions/index` | 展示政策内容版本、更新记录 |
| 发布审核 | `pages/policy-admin/review/index` | 展示待审核政策、审核意见、发布提示 |

## 7. 核心业务模块说明

### 7.1 每日英语早操打卡

入口页面：`pages/daily/index`

业务目标：

- 让妈妈每天用 10 分钟完成一次英语早操。
- 用音频、金句、发音重点、口语例句、表达理解、短语提炼、翻译练习组成一个轻量学习单元。
- 支持填写今日反思并完成打卡。
- 完成后可生成朋友圈卡片或邀请姐妹一起打卡。

当前数据来源：

- 今日课程内容来自公共模块中的 `dailyLesson` 类静态数据。
- 当前已接入真实本地素材：
  - `assets/daily/day1-keep-the-ball-rolling.jpg`
  - `assets/daily/day1-keep-the-ball-rolling.mp3`

关键行为：

- 创建 `InnerAudioContext` 播放今日音频。
- 监听音频播放进度，更新进度条和当前时间。
- 用户输入反思后保存到本地存储。
- 点击完成打卡后，把今日主任务标记为完成。

本地存储：

```text
mom_english_checkin_records
```

存储结构大致为：

```json
[
  {
    "date": "2026-06-16",
    "tasks": [
      {
        "id": "daily-main-2026-06-16",
        "date": "2026-06-16",
        "title": "Day 1 英语早操",
        "description": "今日任务文案",
        "category": "daily_main",
        "source": "daily",
        "completed": true,
        "completedAt": "ISO 时间"
      }
    ],
    "mainCheckinCompleted": true,
    "reflection": "用户填写的今日反思",
    "completedAt": "ISO 时间"
  }
]
```

当前限制：

- 打卡数据只存在本机微信小程序本地缓存中。
- 换设备、清缓存或重新安装后数据会丢失。
- 没有用户登录、云端同步、补卡规则、反作弊规则。

### 7.2 妈妈成长计划

入口页面：`pages/mom-growth-plan/mom-growth-plan`

业务目标：

- 把用户从单次打卡引导到 21 天体验或 365 天成长计划。
- 用成长曲线、徽章、成长金、阶段节点形成长期激励。
- 通过姐妹同行和蜕变广场形成社群与商业闭环。

计划类型：

| 类型 | 当前页面文案 | 当前状态 |
| --- | --- | --- |
| 21 天体验 | 邀请 3 位新用户完成首次打卡免费体验，或支付 ¥99 开启 | 前端模拟开启 |
| 365 天计划 | ¥365 开启，打卡成功 1 天返还 1 元成长金，漏打减少权益 | 前端模拟开启 |

主要展示字段：

- `status`：用户当前计划状态，如 `none`、`trial21`、`year365`
- `checkinDays`：累计打卡天数
- `todayChecked`：今日是否打卡
- `growthMoney`：成长金
- `weeklyBadges`：周徽章
- `monthlyMilestones`：月度蜕变节点

当前限制：

- 支付为模拟逻辑，没有调用微信支付。
- 成长金为前端展示概念，没有真实账户系统。
- 计划开通状态应在后续接入用户账户和订单系统。

### 7.3 孩子阅读能力测评

入口页面：`pages/kid-growth-assessment/kid-growth-assessment`

业务目标：

- 面向小学 1 年级到初中 9 年级孩子。
- 通过基础信息、分层阅读任务、阅读习惯问卷生成可用于后续推荐的阅读画像。

测评流程：

1. 基础信息卡
   - 当前年级：`1-2年级`、`3-4年级`、`5-6年级`、`7-9年级`
   - 英语阅读自评
   - 每天阅读时间
   - 阅读兴趣类型

2. 阅读任务卡
   - 根据年级展示不同英文短文。
   - 每个年级 5 道题。
   - 题型包括细节、主旨、动作词、推理、词汇、长句理解等。

3. 阅读习惯小问卷
   - 兴趣类型：故事追光型、知识采集型、任务闯关型、安静沉浸型。
   - 阻力原因：词汇压力、长句断线、考试抗拒、兴趣驱动弱。
   - 专注时长：3 分钟、5-8 分钟、10-15 分钟、15 分钟以上。
   - 激励方式：夸奖、徽章积分、讲给别人听、看到自己读懂。

4. 生成阅读画像
   - 阅读角色画像
   - 英语阅读分：0-10 分
   - 英语等级：`E1` 到 `E5`
   - 语文阅读状态：`C1` 到 `C5`
   - 薄弱标签
   - 推荐书单方向
   - 每日任务
   - 训练重点

结果 JSON 示例：

```json
{
  "grade_level": "3-4年级",
  "chinese_level": "C3",
  "english_level": "E4",
  "interest_type": "故事追光型：喜欢角色和情节",
  "reading_tolerance": "10-15分钟",
  "weakness_tags": ["长句断线", "短文主旨抓取", "关键词定位"],
  "recommendation": {
    "starter_books": ["英文分级读物：L2-L3 校园任务类"],
    "daily_task": "3-4年级每日任务：每天 1 篇短文...",
    "training_focus": ["短文主旨抓取", "关键词定位"]
  }
}
```

当前限制：

- 测评结果只在当前页面状态中生成。
- 页面提供“复制 JSON 结果”，但没有保存到用户档案。
- 后续应接入测评记录接口、书单推荐接口和任务下发接口。

### 7.4 姐妹同行成长区

入口页面：`pages/sister-growth/index`

业务目标：

- 让妈妈以 2-5 人小队形式一起打卡。
- 通过邀请、今日小队打卡、点赞、抱抱、留言鼓励、提醒打卡提升留存。
- 邀请 3 位新用户完成首次打卡后解锁 21 天体验权益。

核心功能：

- 创建小队
  - 小队名称：2 到 12 个字
  - 小队目标：情绪稳定、亲子英语、自我成长、坚持打卡
  - 最大人数：页面文案为 5 人

- 加入小队
  - 输入邀请码
  - 当前原型阶段输入任意邀请码都可模拟加入

- 小队状态
  - 小队人数
  - 今日打卡人数
  - 连续同行天数
  - 成长值

- 小队互动
  - 点赞
  - 抱抱她
  - 提醒打卡
  - 留言鼓励
  - 快捷鼓励语

- 分享邀请
  - 使用小程序分享能力
  - 可复制邀请码
  - 可跳转邀请海报页

当前限制：

- 小队、成员、邀请进度均为本地模拟。
- 没有真实邀请关系、用户身份、分享回流归因、有效邀请校验。
- 没有服务端社群数据同步。

### 7.5 政策知识库后台

入口页面：`pages/policy-admin/index`

业务目标：

- 管理教育政策内容。
- 将政策从“原文摘要”转成“影响方向、家长行动建议、打卡任务”。
- 为后续用户测评报告、成长建议和每周任务提供内容来源。

当前预置内容：

- 北京中考指标分配与综合素质评价提醒
- 上海名额分配综合评价与成长记录提醒
- 广东中考统一命题与学科基础能力提醒
- 以及其他教育政策内容

政策内容字段：

```json
{
  "id": "policy-beijing-exam-2026",
  "title": "政策标题",
  "sourceName": "政策来源名称",
  "sourceUrl": "政策来源链接",
  "policySummary": "政策摘要",
  "effectiveDate": "生效时间",
  "region": "适用地区",
  "stage": "适用学段",
  "gradeRange": ["适用年级"],
  "domains": ["政策领域"],
  "influenceAbilities": ["影响能力标签"],
  "parentActionSuggestions": ["家长行动建议"],
  "generatedTasks": ["可生成打卡任务"],
  "frontDisplayTitle": "前端展示标题",
  "frontDisplaySummary": "前端展示摘要",
  "impactExplanation": "政策影响说明",
  "monthlySuggestions": ["本月成长建议"],
  "weeklyTaskSuggestions": ["本周打卡建议"],
  "focusDirections": ["关注方向"],
  "childImpactAnalysis": "对孩子影响分析",
  "contentStatus": "内容状态",
  "version": 3,
  "createdBy": "创建人",
  "reviewedBy": "审核人",
  "reviewComment": "审核意见",
  "createdAt": "创建时间",
  "updatedAt": "更新时间",
  "publishedAt": "发布时间"
}
```

政策状态枚举：

| 值 | 含义 |
| --- | --- |
| `draft` | 草稿 |
| `pending_review` | 待审核 |
| `published` | 已发布 |
| `offline` | 已下架 |
| `archived` | 已归档 |

政策领域枚举：

| 值 | 含义 |
| --- | --- |
| `admission_exam` | 招生考试 |
| `quota_allocation` | 名额分配 / 指标到校 |
| `comprehensive_evaluation` | 综合评价 |
| `science_education` | 科学教育 |
| `ai_education` | AI 教育 |
| `comprehensive_quality` | 综合素养 |
| `english_reading` | 英语阅读 |
| `english_listening_speaking` | 英语听说 |
| `learning_habit` | 学习习惯 |
| `family_education` | 家庭教育 |
| `project_learning` | 项目学习 |
| `growth_record` | 成长记录 |
| `evaluation_reform` | 评价改革 |
| `school_planning` | 升学规划 |
| `strong_base_training` | 强基 / 拔尖培养 |

当前后台能力状态：

- 列表页可按地区、学段、状态筛选 mock 政策。
- 编辑页展示完整字段结构，但没有真实表单保存。
- 审核页展示待审核流程和审核按钮，但按钮为占位。
- 标签管理和版本记录为后台能力原型。
- 目前没有服务端数据库，也没有管理端权限控制。

## 8. 当前“接口”说明

这里的“接口”分为三类：页面路由接口、本地存储接口、后续应实现的后端接口。当前代码没有真实 HTTP API。

### 8.1 页面路由接口

项目中页面跳转使用公共跳转工具包装 Taro/微信导航能力。业务上可理解为以下路由接口。

| 入口 | 目标路由 | 用途 |
| --- | --- | --- |
| 首页妈妈成长卡片 | `/pages/mom-growth-plan/mom-growth-plan` | 进入妈妈成长计划 |
| 首页孩子成长卡片 | `/pages/growth/index` | 进入孩子阅读成长路径 |
| 首页蜕变广场入口 | `/pages/transformation-square/index` | 进入蜕变广场 tab |
| 打卡页生成卡片 | `/pages/poster/index` | 生成朋友圈打卡卡片 |
| 打卡页邀请姐妹 | `/pages/sister-growth/index` | 进入姐妹同行成长区 |
| 妈妈成长页姐妹入口 | `/pages/sister-growth/index` | 创建或加入成长小队 |
| 妈妈成长页交友权益 | `/pages/transformation-square/index` | 进入蜕变广场 |
| 姐妹成长页完成打卡 | `/pages/daily/index` | 跳转今日打卡 tab |
| 姐妹成长页邀请海报 | `/pages/sister-poster/index?inviteCode=xxx` | 生成小队邀请海报 |
| 姐妹分享路径 | `/pages/sister-invite/index?inviteCode=xxx` | 好友通过邀请码进入邀请页 |
| 成长计划页继续打卡 | `/pages/daily/index` | 回到今日打卡 |

### 8.2 本地存储接口

#### 8.2.1 每日打卡记录

存储键：

```text
mom_english_checkin_records
```

用途：

- 保存每天的打卡任务。
- 保存用户今日反思。
- 保存任务完成状态。

读写方式：

- `getStorageSync(key)`
- `setStorageSync(key, records)`

建议后续服务端接口：

```http
GET /api/checkins/today
POST /api/checkins
PATCH /api/checkins/{id}/tasks/{taskId}
GET /api/checkins/calendar
```

#### 8.2.2 妈妈成长计划记录

用途：

- 保存当前计划状态。
- 保存累计打卡天数、成长金、徽章、今日是否完成等。

当前状态来源：

- 公共模块中的本地状态工具，页面通过类似 `getGrowthRecord()`、`startTrial()`、`startYearPlan()` 的逻辑读取和更新。

建议后续服务端接口：

```http
GET /api/growth-plan/me
POST /api/growth-plan/trial21/start
POST /api/growth-plan/year365/start
POST /api/growth-plan/checkin
GET /api/growth-plan/badges
GET /api/growth-plan/milestones
```

#### 8.2.3 姐妹小队状态

用途：

- 保存用户是否加入小队。
- 保存小队成员、邀请码、活动流、邀请进度、是否解锁 21 天体验。

当前状态来源：

- 公共模块中的本地模拟团队工具，页面通过类似 `getSisterState()`、`createTeam()`、`joinTeam()`、`updateActivity()`、`confirmInvite()` 的逻辑更新。

建议后续服务端接口：

```http
GET /api/sister-team/me
POST /api/sister-team
POST /api/sister-team/join
POST /api/sister-team/invite/confirm
POST /api/sister-team/activities/{activityId}/like
POST /api/sister-team/activities/{activityId}/hug
POST /api/sister-team/activities/{activityId}/comment
POST /api/sister-team/members/remind
```

### 8.3 后续后端 API 设计建议

#### 用户与登录

当前缺失：

- 微信登录
- openid/unionid
- 用户资料
- 会员状态
- 设备间同步

建议接口：

```http
POST /api/auth/wechat-login
GET /api/users/me
PATCH /api/users/me
GET /api/users/me/profile
PATCH /api/users/me/profile
```

#### 每日课程内容

当前缺失：

- 每天课程动态下发。
- 音频、封面、文案后台管理。

建议接口：

```http
GET /api/daily-lessons/today
GET /api/daily-lessons/{day}
POST /api/admin/daily-lessons
PATCH /api/admin/daily-lessons/{id}
```

建议数据结构：

```json
{
  "day": 1,
  "theme": "Keep the ball rolling",
  "quote": "Keep the ball rolling.",
  "meaning": "让事情继续推进。",
  "audioTitle": "Day 1 英语早操",
  "audioSubtitle": "今日表达",
  "audioDuration": "02:35",
  "audioSrc": "https://cdn.example.com/audio/day1.mp3",
  "coverImage": "https://cdn.example.com/image/day1.jpg",
  "pronunciation": ["发音重点"],
  "speakingExamples": [
    {
      "en": "Let's keep the ball rolling.",
      "zh": "我们继续推进吧。"
    }
  ],
  "definitionNotes": ["表达理解"],
  "takeaways": ["短语提炼"],
  "translationPractice": ["翻译练习"],
  "task": "今日打卡任务",
  "encouragement": "鼓励文案"
}
```

#### 阅读测评

当前缺失：

- 测评记录保存。
- 用户历史测评。
- 书单和任务动态推荐。

建议接口：

```http
GET /api/reading-assessments/questions?gradeLevel=3-4
POST /api/reading-assessments
GET /api/reading-assessments/{id}
GET /api/reading-assessments/me/latest
POST /api/reading-assessments/{id}/copy-report
```

建议提交结构：

```json
{
  "basicInfo": {
    "gradeLevel": "3-4年级",
    "englishSelf": "能读懂简单短文",
    "dailyReadingTime": "10-20分钟",
    "readingInterest": "科普发现"
  },
  "answers": {
    "g34-q1": "周三午饭后"
  },
  "behaviorAnswers": {
    "interest_type": "故事追光型：喜欢角色和情节",
    "resistance_reason": "句子太长，容易读着读着断线",
    "reading_tolerance": "10-15分钟",
    "motivation_type": "能讲给别人听"
  }
}
```

建议返回结构：

```json
{
  "id": "assessment_123",
  "readingRole": {
    "title": "3-4年级 · 故事追光者",
    "desc": "孩子更容易被人物和情节带进去..."
  },
  "englishScore": 8,
  "reportJson": {
    "grade_level": "3-4年级",
    "chinese_level": "C3",
    "english_level": "E4",
    "weakness_tags": ["长句断线"],
    "recommendation": {
      "starter_books": [],
      "daily_task": "每天 1 篇短文...",
      "training_focus": []
    }
  }
}
```

#### 政策知识库

当前缺失：

- 政策内容真实 CRUD。
- 审核流。
- 标签管理。
- 与测评报告联动。

建议接口：

```http
GET /api/policies
GET /api/policies/{id}
POST /api/admin/policies
PATCH /api/admin/policies/{id}
DELETE /api/admin/policies/{id}
POST /api/admin/policies/{id}/submit-review
POST /api/admin/policies/{id}/approve
POST /api/admin/policies/{id}/reject
POST /api/admin/policies/{id}/offline
POST /api/admin/policies/{id}/archive
GET /api/admin/policies/{id}/versions
GET /api/admin/policy-tags
POST /api/admin/policy-tags
PATCH /api/admin/policy-tags/{id}
```

政策列表查询参数建议：

```text
keyword      政策标题、摘要、标签关键词
region       地区，如 北京、上海、广东、全国通用
stage        学段，如 幼儿园、小学低年级、小学高年级、初中
status       draft / pending_review / published / offline / archived
domain       政策领域
ability      影响能力
page         页码
pageSize     每页数量
```

#### 邀请与小队

当前缺失：

- 邀请码真实生成和校验。
- 分享回流归因。
- 新用户首打卡有效性校验。
- 小队成员真实关系。

建议接口：

```http
POST /api/invites
GET /api/invites/{code}
POST /api/invites/{code}/accept
POST /api/invites/{code}/complete-first-checkin
GET /api/invites/me/progress
```

#### 支付与权益

当前缺失：

- 21 天体验支付。
- 365 天计划支付。
- 成长金账户。
- 权益发放。

建议接口：

```http
POST /api/orders
GET /api/orders/{id}
POST /api/payments/wechat/prepay
POST /api/payments/wechat/notify
GET /api/rewards/me
GET /api/account/cashback
POST /api/account/withdraw
```

## 9. 数据模型建议

### 9.1 User

```json
{
  "id": "user_123",
  "openid": "wechat_openid",
  "unionid": "wechat_unionid",
  "nickname": "用户昵称",
  "avatarUrl": "头像",
  "phone": "手机号",
  "createdAt": "2026-06-16T00:00:00.000Z",
  "updatedAt": "2026-06-16T00:00:00.000Z"
}
```

### 9.2 GrowthPlan

```json
{
  "userId": "user_123",
  "status": "trial21",
  "checkinDays": 5,
  "todayChecked": false,
  "growthMoney": 5,
  "startedAt": "2026-06-01",
  "expiresAt": "2026-06-22",
  "weeklyBadges": [],
  "monthlyMilestones": []
}
```

### 9.3 CheckinRecord

```json
{
  "id": "checkin_123",
  "userId": "user_123",
  "date": "2026-06-16",
  "lessonId": "lesson_day_1",
  "reflection": "今日反思",
  "tasks": [],
  "completedAt": "2026-06-16T08:30:00.000Z"
}
```

### 9.4 SisterTeam

```json
{
  "id": "team_123",
  "name": "原原高成长小队",
  "goal": "坚持打卡",
  "inviteCode": "YYG2026",
  "maxMembers": 5,
  "members": [],
  "teamConsecutiveDays": 3,
  "growthValue": 120
}
```

### 9.5 Policy

```json
{
  "id": "policy_123",
  "title": "政策标题",
  "sourceName": "来源名称",
  "sourceUrl": "来源链接",
  "policySummary": "政策摘要",
  "region": "北京",
  "stage": "初中",
  "gradeRange": ["初中"],
  "domains": ["admission_exam"],
  "influenceAbilities": ["英语阅读能力"],
  "parentActionSuggestions": [],
  "generatedTasks": [],
  "contentStatus": "published",
  "version": 1
}
```

## 10. 当前风险与待补齐事项

### 10.1 技术风险

- 当前只有编译产物，没有原始源码时，后续维护成本较高。
- 业务数据写在前端包内，更新课程、政策、测评题都需要重新发版。
- 本地存储不能保证数据安全、同步和长期保留。
- 没有用户体系，无法识别用户、设备和邀请关系。
- 没有真实支付、订单和权益系统。
- 没有后台权限，政策后台页面不能直接上线给运营使用。

### 10.2 产品风险

- 365 天返现和成长金涉及资金承诺，正式上线前需要明确规则、风控、财务和合规。
- 邀请 3 人解锁权益需要防刷机制。
- 教育政策内容需要来源真实性和审核机制。
- 阅读测评如果用于学习建议，需要在页面明确“非诊断、非标准化考试”的边界。
- 脱单交友区涉及用户资料、社交安全、隐私保护和内容审核，正式上线需要单独设计合规机制。

### 10.3 下一步建议

优先级 1：

- 找回或重建原始 Taro 源码工程。
- 建立用户登录与云端用户档案。
- 把每日打卡记录从本地存储迁到后端。
- 建立课程内容接口，支持每日课程动态下发。

优先级 2：

- 接入阅读测评记录保存。
- 接入姐妹小队真实邀请、成员、互动、有效邀请校验。
- 接入 21 天和 365 天计划的订单与权益状态。

优先级 3：

- 建立政策知识库管理后台。
- 将政策内容与阅读测评报告、每周任务推荐联动。
- 完善蜕变广场、交友区、课程转化和权益账户。

## 11. 给技术人员或 AI 的接手提示

如果你要继续开发本项目，请先判断你拿到的是哪种代码：

- 如果只有当前 `dist`：这是微信小程序编译产物，适合预览、逆向理解和临时小改，不适合长期开发。
- 如果有原始 Taro 源码：优先在源码中改动，然后重新构建到 `dist`。

当前最关键的业务判断：

- 产品主线是“每日打卡 + 成长计划 + 姐妹同行 + 孩子阅读测评 + 政策知识库”。
- 当前没有真实后端接口，所有“接口说明”应理解为后续后端化的设计方向。
- 每日打卡和姐妹小队是留存核心。
- 阅读测评和政策知识库是内容与个性化建议核心。
- 21 天体验、365 天计划、成长金和课程转化是商业化核心。

如果要把它从原型推进到可上线版本，建议不要直接在编译产物上继续堆功能，而是拆成：

```text
前端小程序：Taro + React
后端 API：用户、打卡、课程、测评、小队、政策、订单、权益
管理后台：课程内容、政策内容、用户运营、订单权益、风控审核
文件存储/CDN：音频、封面、海报素材
数据分析：留存、打卡、邀请、转化、课程完成率
```

