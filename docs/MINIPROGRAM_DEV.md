# 微信小程序开发技术体系文档

> **项目代号**：mom-english-taro
> **文档版本**：v1.0
> **最后更新**：2026-06-17
> **文档定位**：系统性整理微信小程序开发技术体系，覆盖开发框架、组件、API、兼容性及最佳实践，为后续小程序功能开发提供技术指导和参考依据
> **主要参考**：微信官方文档（`https://developers.weixin.qq.com/miniprogram/dev/`）

---

## 目录

- [第 1 章 技术架构概述](#第-1-章-技术架构概述)
  - [1.1 微信小程序简介](#11-微信小程序简介)
  - [1.2 小程序的运行环境](#12-小程序的运行环境)
  - [1.3 渲染层与逻辑层](#13-渲染层与逻辑层)
  - [1.4 双线程通信模型](#14-双线程通信模型)
  - [1.5 渲染引擎（WebView / Skyline）](#15-渲染引擎webview--skyline)
- [第 2 章 开发环境搭建](#第-2-章-开发环境搭建)
  - [2.1 微信开发者工具](#21-微信开发者工具)
  - [2.2 项目结构](#22-项目结构)
  - [2.3 全局配置（app.json）](#23-全局配置appjson)
  - [2.4 页面配置（页面 json）](#24-页面配置页面-json)
  - [2.5 调试与发布](#25-调试与发布)
- [第 3 章 开发框架选型](#第-3-章-开发框架选型)
  - [3.1 原生小程序框架（MINA）](#31-原生小程序框架mina)
  - [3.2 Taro 3 框架](#32-taro-3-框架)
  - [3.3 uni-app 框架](#33-uni-app-框架)
  - [3.4 三大框架对比](#34-三大框架对比)
  - [3.5 本项目框架选型](#35-本项目框架选型)
- [第 4 章 核心组件参考手册](#第-4-章-核心组件参考手册)
  - [4.1 视图容器](#41-视图容器)
  - [4.2 基础内容](#42-基础内容)
  - [4.3 表单组件](#43-表单组件)
  - [4.4 导航组件](#44-导航组件)
  - [4.5 媒体组件](#45-媒体组件)
  - [4.6 地图与画布](#46-地图与画布)
  - [4.7 开放能力](#47-开放能力)
  - [4.8 Skyline 专属组件](#48-skyline-专属组件)
  - [4.9 组件兼容性速查表](#49-组件兼容性速查表)
- [第 5 章 API 接口手册](#第-5-章-api-接口手册)
  - [5.1 基础 API（系统/更新/调试/性能）](#51-基础-api系统更新调试性能)
  - [5.2 网络 API](#52-网络-api)
  - [5.3 媒体 API（音频/视频/图片）](#53-媒体-api音频视频图片)
  - [5.4 位置 API](#54-位置-api)
  - [5.5 设备 API（蓝牙/网络/屏幕等）](#55-设备-api蓝牙网络屏幕等)
  - [5.6 界面 API（交互/导航/tabBar/菜单）](#56-界面-api交互导航tabbar菜单)
  - [5.7 数据缓存 API](#57-数据缓存-api)
  - [5.8 开放能力 API（登录/支付/分享/订阅等）](#58-开放能力-api登录支付分享订阅等)
  - [5.9 分包加载与预下载 API](#59-分包加载与预下载-api)
  - [5.10 加密 API](#510-加密-api)
- [第 6 章 兼容性说明](#第-6-章-兼容性说明)
  - [6.1 兼容性策略总览](#61-兼容性策略总览)
  - [6.2 版本号比较规范](#62-版本号比较规范)
  - [6.3 API 存在判断与 wx.canIUse](#63-api-存在判断与-wxcaniuse)
  - [6.4 最低基础库版本设置](#64-最低基础库版本设置)
  - [6.5 Android 与 iOS 平台差异](#65-android-与-ios-平台差异)
  - [6.6 鸿蒙 OS 平台支持](#66-鸿蒙-os-平台支持)
  - [6.7 各组件 API 兼容性矩阵](#67-各组件-api-兼容性矩阵)
- [第 7 章 最佳实践](#第-7-章-最佳实践)
  - [7.1 性能优化](#71-性能优化)
  - [7.2 包体积控制](#72-包体积控制)
  - [7.3 网络请求最佳实践](#73-网络请求最佳实践)
  - [7.4 数据缓存策略](#74-数据缓存策略)
  - [7.5 用户体验与可访问性](#75-用户体验与可访问性)
  - [7.6 安全建议](#76-安全建议)
  - [7.7 调试与日志](#77-调试与日志)
  - [7.8 鸿蒙与多端适配](#78-鸿蒙与多端适配)
- [附录 A：参考链接](#附录-a参考链接)
- [附录 B：术语表](#附录-b术语表)

---

## 第 1 章 技术架构概述

### 1.1 微信小程序简介

微信小程序是一种**不需要下载安装即可使用**的应用，它实现了"触手可及"的梦想。用户扫一扫或搜一下即可打开应用，体现了"用完即走"的理念，同时具备了原生 APP 的体验。

小程序提供了**简单、高效的应用开发框架**和**丰富的组件及 API**，帮助开发者在微信中开发具有原生 APP 体验的服务。

小程序的核心优势：

- **开发成本低**：使用 WXML、WXSS、JS 等前端技术栈，学习曲线平缓
- **跨平台**：一次开发，可运行于 Android、iOS、Windows、macOS、鸿蒙 OS
- **生态完善**：依托微信生态，可调用微信支付、登录、分享等能力
- **分发便利**：扫码、搜索、好友分享、公众号关联等多种入口

### 1.2 小程序的运行环境

我们称微信客户端给小程序所提供的环境为**宿主环境**。小程序借助宿主环境提供的能力，可以完成许多普通网页无法完成的功能。

宿主环境主要包括以下几部分：

| 组成 | 说明 |
| --- | --- |
| 通信模型 | 渲染层与逻辑层的通信机制 |
| 运行机制 | 小程序启动、页面加载、销毁的生命周期 |
| 组件系统 | 视图层提供的基础组件（view、button、image 等） |
| API 库 | 逻辑层提供的微信原生能力（网络、媒体、位置等） |
| 渲染引擎 | WebView（默认）或 Skyline（新一代） |

### 1.3 渲染层与逻辑层

小程序的运行环境分成**渲染层**和**逻辑层**：

- **渲染层**：WXML 模板和 WXSS 样式工作在渲染层，负责界面的渲染
- **逻辑层**：JS 脚本工作在逻辑层，负责业务逻辑的处理

这两个线程的管理方式：

- **渲染层**：界面使用 WebView 进行渲染，因为一个小程序存在多个界面，所以渲染层存在**多个 WebView 线程**
- **逻辑层**：采用 JsCore 线程运行 JS 脚本，**整个小程序只有一个逻辑层线程**

### 1.4 双线程通信模型

渲染层和逻辑层的两个线程之间的通信会经由微信客户端（Native）做中转，逻辑层发送网络请求也经由 Native 转发。

```
┌────────────────┐         ┌─────────────┐         ┌────────────────┐
│    渲染层       │  ←→→→  │  Native     │  ←→→→→  │    逻辑层       │
│  （WebView）    │         │  微信客户端   │         │   （JsCore）   │
└────────────────┘         └─────────────┘         └────────────────┘
       ↑                                                    ↑
       │                                                    │
       └──────── setData / 事件 ────────── wx API ─────────┘
```

**核心通信方式**：

1. **逻辑层 → 渲染层**：`this.setData()`（会合并异步执行）
2. **渲染层 → 逻辑层**：通过事件（`bindtap`、`bindinput` 等）

### 1.5 渲染引擎（WebView / Skyline）

小程序支持两种渲染引擎，可在 `app.json` 或页面配置中切换：

| 引擎 | 说明 | 特点 |
| --- | --- | --- |
| **WebView** | 默认渲染引擎 | 兼容性好，标准 Web 渲染 |
| **Skyline** | 新一代渲染引擎（基础库 2.27.0+） | 性能更优、原生体验更佳、支持更多高级特性 |

Skyline 渲染引擎的显著优势：

- 滚动长列表性能大幅提升（支持 `list-view`、`grid-view` 虚拟列表）
- 支持更精细的手势系统（双击、重按、横向滑动等）
- 共享元素动画、转场动画
- worklet 动画系统

在 `app.json` 中开启 Skyline：

```json
{
  "lazyCodeLoading": "requiredComponents",
  "renderer": "skyline"
}
```

或在单个页面配置：

```json
{
  "renderer": "skyline"
}
```

> **提示**：Skyline 模式与 WebView 模式有部分 API 差异，使用 Skyline 专属组件时需确认目标客户端基础库版本支持。

---

## 第 2 章 开发环境搭建

### 2.1 微信开发者工具

微信开发者工具是小程序的官方 IDE，提供代码编辑、调试、预览、上传等功能。

**下载地址**：`https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html`

**核心功能**：

| 功能 | 说明 |
| --- | --- |
| 代码编辑 | 支持 WXML/WXSS/JS/JSON 语法高亮、智能提示 |
| 模拟器 | 模拟不同设备、不同基础库版本的运行环境 |
| 真机调试 | 通过 USB 或网络连接真机调试 |
| 调试器 | 包含 Console、Network、Storage、Wxml 等调试工具 |
| 性能分析 | 启动性能、运行时性能、网络性能分析 |
| 上传发布 | 上传代码到微信后台，进行版本管理 |

**最低系统要求**：

- Windows：Windows 7 及以上（推荐 Windows 10/11）
- macOS：macOS 10.13 及以上
- 推荐配置：8GB+ 内存，1080P+ 分辨率

### 2.2 项目结构

小程序包含一个描述整体程序的 `app` 和多个描述各自页面的 `page`。

**一个小程序主体部分由三个文件组成，必须放在项目的根目录**：

| 文件 | 必需 | 作用 |
| --- | --- | --- |
| `app.js` | 是 | 小程序逻辑 |
| `app.json` | 是 | 小程序公共配置 |
| `app.wxss` | 否 | 小程序公共样式表 |

**一个小程序页面由四个文件组成**：

| 文件类型 | 必需 | 作用 |
| --- | --- | --- |
| `js` | 是 | 页面逻辑 |
| `wxml` | 是 | 页面结构 |
| `json` | 否 | 页面配置 |
| `wxss` | 否 | 页面样式表 |

> **注意**：描述页面的四个文件必须具有相同的路径与文件名。

**典型项目结构**：

```
miniprogram/
├── app.js                    # 小程序主逻辑
├── app.json                  # 小程序公共配置
├── app.wxss                  # 小程序公共样式
├── project.config.json       # 项目配置
├── sitemap.json              # 站点地图
├── pages/                    # 页面目录
│   ├── home/
│   │   ├── home.js
│   │   ├── home.json
│   │   ├── home.wxml
│   │   └── home.wxss
│   └── daily/
│       └── ...
├── components/               # 自定义组件
├── utils/                    # 工具函数
├── images/                   # 图片资源
└── lib/                      # 第三方库
```

**允许上传的文件类型**：

项目目录中，以下文件会经过编译，上传之后无法直接访问到：`.js`、`app.json`、`.wxml`、`*.wxss`。

除此之外，只有后缀名在白名单内的文件可以被上传：

- `wxs`、`png`、`jpg`、`jpeg`、`gif`、`svg`、`json`、`cer`
- `mp3`、`aac`、`m4a`、`mp4`、`wav`、`ogg`、`silk`
- `wasm`、`br`、`cert`

### 2.3 全局配置（app.json）

`app.json` 是小程序的全局配置，包括小程序的所有页面路径、窗口表现、底部 tabBar、网络超时时间等。

**完整配置项**：

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs"
  ],
  "window": {
    "backgroundTextStyle": "light",
    "navigationBarBackgroundColor": "#fff",
    "navigationBarTitleText": "小程序标题",
    "navigationBarTextStyle": "black",
    "backgroundColor": "#f8f8f8",
    "enablePullDownRefresh": false
  },
  "tabBar": {
    "color": "#8a7568",
    "selectedColor": "#d56d1c",
    "backgroundColor": "#ffffff",
    "borderStyle": "white",
    "list": [
      {
        "pagePath": "pages/home/index",
        "text": "首页"
      }
    ]
  },
  "networkTimeout": {
    "request": 10000,
    "downloadFile": 10000,
    "connectSocket": 10000,
    "uploadFile": 10000
  },
  "debug": false,
  "permission": {
    "scope.userLocation": {
      "desc": "你的位置信息将用于定位附近的小队"
    }
  },
  "requiredPrivateInfos": [
    "getLocation",
    "chooseLocation"
  ],
  "lazyCodeLoading": "requiredComponents",
  "renderer": "skyline",
  "sitemapLocation": "sitemap.json"
}
```

**关键字段说明**：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `pages` | 是 | 页面路径列表，第一项为首页 |
| `window` | 否 | 全局窗口表现 |
| `tabBar` | 否 | 底部 tabBar 表现（至少 2 个、最多 5 个 tab） |
| `networkTimeout` | 否 | 网络请求超时时间 |
| `permission` | 否 | 授权相关配置 |
| `requiredPrivateInfos` | 否 | 必填隐私接口声明（2022.7.14 后新发布必填） |
| `lazyCodeLoading` | 否 | 是否开启组件按需注入 |
| `renderer` | 否 | 全局渲染引擎（skyline / webview） |

### 2.4 页面配置（页面 json）

每个页面的 `.json` 文件用于配置本页面的窗口表现，会覆盖 `app.json` 中的 `window` 配置。

**示例**：

```json
{
  "navigationBarTitleText": "页面标题",
  "navigationBarBackgroundColor": "#ffffff",
  "navigationBarTextStyle": "black",
  "backgroundColor": "#f8f8f8",
  "enablePullDownRefresh": true,
  "usingComponents": {
    "my-component": "/components/my-component/index"
  },
  "disableScroll": false,
  "reachBottomDistance": 50,
  "initialNavigationBar": {
    "backgroundColor": "#ffffff"
  }
}
```

### 2.5 调试与发布

**调试流程**：

1. **本地调试**：在开发者工具中点击"编译"，使用模拟器调试
2. **真机调试**：点击"真机调试"扫码，手机上预览效果
3. **预览**：点击"预览"扫码，可在不同设备上快速验证
4. **性能分析**：使用 Audits 面板、Trace 工具进行性能分析

**发布流程**：

1. 点击"上传"按钮，填写版本号和项目备注
2. 登录微信公众平台（mp.weixin.qq.com）进入"版本管理"
3. 提交审核（需选择类目、标签）
4. 审核通过后点击"发布"，生效到正式版

**版本号规范**：

- 建议采用 `Major.Minor.Patch`（如 `1.2.3`）
- 每次发版递增，遵循语义化版本规范

---

## 第 3 章 开发框架选型

### 3.1 原生小程序框架（MINA）

微信官方提供的小程序开发框架，称为 MINA 框架。MINA 通过尽可能简单、高效的方式让开发者可以在微信中开发具有原生 APP 体验的服务。

**核心特性**：

- **响应式数据绑定**：核心是响应的数据绑定系统，数据与视图保持同步
- **页面路由管理**：框架管理整个小程序的页面路由，做到页面间无缝切换
- **基础组件**：自带微信风格样式和特殊逻辑的基础组件
- **丰富 API**：提供微信原生 API（用户信息、本地存储、支付等）

**目录结构**：

```
pages/
├── index/
│   ├── index.js       # 页面逻辑
│   ├── index.json     # 页面配置
│   ├── index.wxml     # 页面结构
│   └── index.wxss     # 页面样式
```

**优点**：

- 无需额外编译，原生性能最佳
- 体积最小，无第三方依赖
- 与微信官方文档完全对齐
- 调试支持最完善

**缺点**：

- 组件化、模块化能力弱（需要自行实现）
- 缺乏 TypeScript、SCSS、ESLint 等现代开发体验
- 代码复用、状态管理、路由管理需自行搭建
- 不支持跨端

### 3.2 Taro 3 框架

Taro 是京东凹凸实验室推出的多端统一开发框架，支持使用 React/Vue/Nerv 等框架开发微信/京东/百度/支付宝/字节跳动/QQ/飞书/钉钉小程序、H5、React Native 等多个端。

**核心特性**：

- **多端编译**：一套代码，多端运行
- **React 风格**：使用 React/Vue 语法开发
- **现代化工具链**：原生支持 TypeScript、Sass/Less、ESLint
- **组件库生态**：taro-ui、NutUI 等丰富组件库
- **跨端能力**：可同时输出小程序、H5、React Native

**目录结构**：

```
src/
├── app.config.ts
├── app.tsx
├── pages/
│   └── index/
│       └── index.tsx
├── components/
├── services/
├── stores/
└── assets/
```

**优点**：

- 现代化开发体验（TypeScript + React）
- 多端复用，节省开发成本
- 生态丰富，社区活跃
- 与现代前端工具链无缝集成

**缺点**：

- 编译产物有额外开销
- 部分 API 兼容性需注意
- 调试链路较长
- 学习成本略高

**本项目状态**：当前是 Taro 3.6.40 编译后的微信小程序产物。

### 3.3 uni-app 框架

uni-app 是 DCloud 推出的多端统一开发框架，使用 Vue.js 开发所有前端应用。一套代码，可发布到 iOS、Android、鸿蒙 Next、Web，以及各种小程序（微信/支付宝/百度/抖音/飞书/QQ/快手/钉钉/淘宝/京东/小红书）、快应用、鸿蒙元服务等多个平台。

**核心特性**：

- **Vue 语法**：基于 Vue.js，学习成本低
- **跨端能力极强**：支持十几种平台
- **原生渲染**：App 端支持原生渲染（uni-app x）
- **性能优秀**：小程序端性能优于市场其他框架
- **周边生态**：数千款插件，70+ 微信/QQ 群
- **HBuilderX IDE**：专为 uni-app 定制的高效 IDE

**优点**：

- 跨端平台最多
- Vue 语法对前端开发者友好
- 性能表现优秀
- 插件市场丰富

**缺点**：

- 部分平台特性需用条件编译处理
- 与原生小程序存在少量差异
- IDE 强依赖 HBuilderX（非必需，但推荐）

### 3.4 三大框架对比

| 维度 | 原生 MINA | Taro 3 | uni-app |
| --- | --- | --- | --- |
| 语法 | WXML + WXSS + JS | React / Vue | Vue |
| 多端支持 | 仅微信 | 微信 + 多端 | 微信 + 10+ 端 |
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 体积 | 最小 | 中等 | 中等 |
| TypeScript | 需自行配置 | 原生支持 | 原生支持 |
| 组件库 | 需自行建设 | taro-ui / NutUI | uni-ui |
| 学习成本 | 低 | 中 | 中 |
| 调试体验 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 社区生态 | 官方 | 京东出品，活跃 | DCloud 出品，活跃 |
| 包体积 | 最小 | 略大 | 略大 |
| 渲染引擎 | WebView / Skyline | WebView（默认） | WebView（默认） |

### 3.5 本项目框架选型

**当前项目**（mom-english-taro）：

- **框架**：Taro 3.6.40
- **业务代码**：React 风格组件
- **当前状态**：Taro 编译产物（dist 目录），不是源码
- **运行平台**：仅微信小程序

**建议**：

- 如果**只做微信小程序**：原生 MINA 是最简洁、性能最好的选择
- 如果**需要多端**：Taro 3（React 生态）或 uni-app（Vue 生态）
- 如果**长期维护**：建议恢复 Taro 源码工程结构，而不是直接修改编译产物

---

## 第 4 章 核心组件参考手册

微信小程序提供丰富的基础组件，按功能可分为以下几类。

### 4.1 视图容器

视图容器是构建页面布局的基础组件。

| 组件 | 功能 | 最低版本 |
| --- | --- | --- |
| `view` | 视图容器（相当于 div） | 1.0.0 |
| `scroll-view` | 可滚动视图区域 | 1.0.0 |
| `swiper` | 滑块视图容器 | 1.0.0 |
| `swiper-item` | 仅可放置在 swiper 组件中 | 1.0.0 |
| `movable-view` | 可移动的视图容器 | 1.2.0 |
| `movable-area` | movable-view 的可移动区域 | 1.2.0 |
| `cover-view` | 覆盖在原生组件之上的文本视图 | 1.0.0 |
| `cover-image` | 覆盖在原生组件之上的图片视图 | 1.0.0 |
| `page-container` | 页面容器（弹出层） | 2.13.0 |
| `root-portal` | 使子树从页面脱离（fixed 效果） | 2.32.1 |
| `match-media` | media query 匹配检测节点 | 2.11.0 |

**view 组件示例**：

```xml
<view class="container" hover-class="hover-style" hover-stay-time="400">
  <view class="content">内容</view>
</view>
```

**view 属性**：

| 属性 | 类型 | 默认值 | 必填 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- | --- |
| `hover-class` | string | none | 否 | 指定按下去的样式类 | 1.0.0 |
| `hover-stop-propagation` | boolean | false | 否 | 是否阻止祖先节点出现点击态 | 1.5.0 |
| `hover-start-time` | number | 50 | 否 | 按住后多久出现点击态（ms） | 1.0.0 |
| `hover-stay-time` | number | 400 | 否 | 手指松开后点击态保留时间（ms） | 1.0.0 |

**scroll-view 组件关键属性**：

| 属性 | 类型 | 默认值 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- |
| `scroll-x` | boolean | false | 允许横向滚动 | 1.0.0 |
| `scroll-y` | boolean | false | 允许纵向滚动 | 1.0.0 |
| `upper-threshold` | number | 50 | 距顶部/左边多远触发 scrolltoupper | 1.0.0 |
| `lower-threshold` | number | 50 | 距底部/右边多远触发 scrolltolower | 1.0.0 |
| `scroll-top` | number | - | 设置竖向滚动条位置 | 1.0.0 |
| `scroll-left` | number | - | 设置横向滚动条位置 | 1.0.0 |
| `scroll-into-view` | string | - | 值应为某子元素 id | 1.0.0 |
| `scroll-with-animation` | boolean | false | 设置滚动条位置时使用动画过渡 | 1.0.0 |
| `refresher-enabled` | boolean | false | 开启自定义下拉刷新 | 2.10.1 |
| `bindscrolltoupper` | eventhandle | - | 滚动到顶部/左边时触发 | 1.0.0 |
| `bindscrolltolower` | eventhandle | - | 滚动到底部/右边时触发 | 1.0.0 |
| `bindscroll` | eventhandle | - | 滚动时触发 | 1.0.0 |

**scroll-view 注意事项**：

1. 使用竖向滚动时，需要给 scroll-view 一个固定高度，通过 WXSS 设置 height
2. 横向滚动需打开 `enable-flex` 以兼容 WebView
3. 基础库 2.4.0 以下不支持嵌套 textarea、map、canvas、video 组件
4. 在滚动 scroll-view 时会阻止页面回弹
5. Skyline 渲染引擎有 `type`（list/custom/nested）等特有属性

**swiper 组件属性**：

| 属性 | 类型 | 默认值 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- |
| `indicator-dots` | boolean | false | 是否显示面板指示点 | 1.0.0 |
| `indicator-color` | color | rgba(0,0,0,.3) | 指示点颜色 | 1.1.0 |
| `indicator-active-color` | color | #000000 | 当前选中指示点颜色 | 1.1.0 |
| `autoplay` | boolean | false | 是否自动切换 | 1.0.0 |
| `current` | number | 0 | 当前所在滑块的 index | 1.0.0 |
| `interval` | number | 5000 | 自动切换时间间隔（ms） | 1.0.0 |
| `duration` | number | 500 | 滑动动画时长（ms） | 1.0.0 |
| `circular` | boolean | false | 是否采用衔接滑动 | 1.0.0 |
| `vertical` | boolean | false | 滑动方向是否为纵向 | 1.0.0 |
| `display-multiple-items` | number | 1 | 同时显示的滑块数量 | 1.9.0 |
| `previous-margin` | string | 0px | 前边距 | 1.9.0 |
| `next-margin` | string | 0px | 后边距 | 1.9.0 |

**cover-view / cover-image 组件**：

仅在以下原生组件上有效：`video`、`map`、`canvas`、`live-player`、`live-pusher`、`web-view`。可覆盖在原生组件之上，常用于视频播放页加弹幕、加按钮等场景。

```xml
<video src="...">
  <cover-view class="controls">
    <cover-image src="..." bindtap="onPlay"></cover-image>
  </cover-view>
</video>
```

### 4.2 基础内容

| 组件 | 功能 | 最低版本 |
| --- | --- | --- |
| `text` | 文本组件（用于内联文本） | 1.0.0 |
| `icon` | 图标组件 | 1.0.0 |
| `progress` | 进度条 | 1.0.0 |
| `rich-text` | 富文本 | 1.0.0 |
| `selection` | 局部文本选区 | 3.7.0 |

**text 组件关键属性**：

| 属性 | 类型 | 默认值 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- |
| `selectable` | boolean | false | 文本是否可选（已废弃） | 1.1.0 |
| `user-select` | boolean | false | 文本是否可选 | 2.12.1 |
| `space` | string | - | 显示连续空格（ensp/emsp/nbsp） | 1.4.0 |
| `decode` | boolean | false | 是否解码 | 1.4.0 |

**text 组件使用注意**：

1. 内联文本只能用 text 组件，不能用 view
2. text 组件内只支持 text 嵌套
3. decode 可解析的字符：`&nbsp;` `&lt;` `&gt;` `&amp;` `&apos;` `&ensp;` `&emsp;`

**rich-text 组件**：

支持将 HTML 字符串渲染为小程序节点，但仅支持有限的标签和属性，且不支持 JS。

```xml
<rich-text nodes="{{htmlContent}}"></rich-text>
```

```javascript
this.setData({
  htmlContent: '<div class="title">Hello</div><p>这是富文本</p>'
})
```

**progress 组件属性**：

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `percent` | number | - | 百分比 0-100 |
| `show-info` | boolean | false | 在进度条右侧显示百分比 |
| `stroke-width` | number | 6 | 进度条宽度（px） |
| `color` | color | #09BB07 | 进度条颜色 |
| `active-color` | color | - | 已选择的进度条颜色 |
| `background-color` | color | - | 未选择的进度条颜色 |
| `active` | boolean | false | 进度条从左往右的动画 |
| `active-mode` | string | backwards | backwards:动画从头播 / forwards:动画从上次结束点续播 |

**icon 组件**：

微信提供了一套常用图标，type 值必须为预设值。详见官方 icon 文档。

### 4.3 表单组件

表单组件用于构建用户输入界面。

| 组件 | 功能 | 最低版本 |
| --- | --- | --- |
| `button` | 按钮 | 1.0.0 |
| `form` | 表单 | 1.0.0 |
| `input` | 输入框 | 1.0.0 |
| `textarea` | 多行输入框 | 1.0.0 |
| `checkbox` | 多选项目 | 1.0.0 |
| `checkbox-group` | 多项选择器 | 1.0.0 |
| `radio` | 单选项目 | 1.0.0 |
| `radio-group` | 单项选择器 | 1.0.0 |
| `switch` | 开关选择器 | 1.0.0 |
| `slider` | 滑动选择器 | 1.0.0 |
| `picker` | 从底部弹起的滚动选择器 | 1.0.0 |
| `picker-view` | 嵌入页面的滚动选择器 | 1.0.0 |
| `picker-view-column` | 滚动选择器子项 | 1.0.0 |
| `label` | 用来改进表单组件的可用性 | 1.0.0 |
| `editor` | 富文本编辑器 | 2.7.0 |
| `editor-portal` | editor 自定义区块渲染 | 3.6.0 |
| `keyboard-accessory` | input / textarea 聚焦时键盘上方工具栏 | 2.13.0 |

**button 组件**：

按钮是小程序中最特殊的组件之一，因为它承载了多种**微信开放能力**。

| 属性 | 类型 | 默认值 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- |
| `size` | string | default | default / mini | 1.0.0 |
| `type` | string | default | primary / default / warn | 1.0.0 |
| `plain` | boolean | false | 按钮是否镂空 | 1.0.0 |
| `disabled` | boolean | false | 是否禁用 | 1.0.0 |
| `loading` | boolean | false | 名称前是否带 loading 图标 | 1.0.0 |
| `form-type` | string | - | submit / reset / submitToGroup | 1.0.0 |
| `open-type` | string | - | 微信开放能力 | 1.1.0 |
| `hover-class` | string | button-hover | 指定按下去的样式类 | 1.0.0 |
| `hover-start-time` | number | 20 | 按住后多久出现点击态（ms） | 1.0.0 |
| `hover-stay-time` | number | 70 | 手指松开后点击态保留时间（ms） | 1.0.0 |

**open-type 合法值**：

| 值 | 说明 | 最低版本 | 备注 |
| --- | --- | --- | --- |
| `contact` | 打开客服会话 | 1.1.0 | 鸿蒙 OS 暂不支持 |
| `share` | 触发用户转发 | 1.2.0 | 需阅读转发使用指引 |
| `getPhoneNumber` | 手机号快速验证 | 1.2.0 | 已升级，需后台接口换号 |
| `getRealtimePhoneNumber` | 手机号实时验证 | 2.24.4 | |
| `getUserInfo` | 获取用户信息 | 1.3.0 | 推荐使用头像昵称填写 |
| `launchApp` | 打开 APP | 1.9.5 | |
| `openSetting` | 打开授权设置页 | 2.0.7 | |
| `feedback` | 打开意见反馈页面 | 2.1.0 | |
| `chooseAvatar` | 获取用户头像 | 2.21.2 | |
| `agreePrivacyAuthorization` | 用户同意隐私协议 | 2.32.3 | |
| `liveActivity` | 一次性订阅消息 | 2.26.2 | |

**input 组件**：

| 属性 | 类型 | 默认值 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- |
| `value` | string | - | 输入框的初始内容 | 1.0.0 |
| `type` | string | text | text / number / idcard / digit / safe-password / nickname | 1.0.0 |
| `password` | boolean | false | 是否是密码类型 | 1.0.0 |
| `placeholder` | string | - | 输入框为空时占位符 | 1.0.0 |
| `placeholder-class` | string | input-placeholder | 占位符样式类 | 1.0.0 |
| `placeholder-style` | string | - | 占位符样式 | 1.0.0 |
| `disabled` | boolean | false | 是否禁用 | 1.0.0 |
| `maxlength` | number | 140 | 最大输入长度 | 1.0.0 |
| `cursor-spacing` | number | 0 | 指定光标与键盘的距离 | 1.0.0 |
| `auto-focus` | boolean | false | 自动聚焦 | 1.0.0 |
| `focus` | boolean | false | 获取焦点 | 1.0.0 |
| `confirm-type` | string | done | send / search / next / go / done | 1.0.0 |
| `always-embed` | boolean | false | 强制 input 处于同层 | 2.10.2 |
| `confirm-hold` | boolean | false | 点击键盘完成按钮时是否保持键盘不收起 | 1.6.0 |
| `cursor` | number | - | 指定 focus 时光标位置 | 1.5.0 |
| `selection-start` | number | -1 | 光标起始位置 | 1.5.0 |
| `selection-end` | number | -1 | 光标结束位置 | 1.5.0 |
| `adjust-position` | boolean | true | 键盘弹起时是否自动上推页面 | 1.5.0 |
| `hold-keyboard` | boolean | false | focus 时点击不收起键盘 | 1.6.0 |
| `bindinput` | eventhandle | - | 键盘输入时触发 | 1.0.0 |
| `bindfocus` | eventhandle | - | 聚焦时触发 | 1.0.0 |
| `bindblur` | eventhandle | - | 失焦时触发 | 1.0.0 |
| `bindconfirm` | eventhandle | - | 点击完成按钮时触发 | 1.0.0 |
| `bindkeyboardheightchange` | eventhandle | - | 键盘高度变化时触发 | 2.7.0 |

**picker 组件**：从底部弹起的滚动选择器，支持五种选择器模式：

- `mode="selector"`：普通选择器
- `mode="multiSelector"`：多列选择器
- `mode="time"`：时间选择器
- `mode="date"`：日期选择器
- `mode="region"`：省市区选择器

**switch 组件**：

```xml
<switch checked="{{isSwitch}}" bindchange="onSwitchChange" color="#d56d1c" />
```

**slider 组件**：

```xml
<slider 
  min="0" 
  max="100" 
  value="{{progress}}"
  step="1"
  show-value
  activeColor="#d56d1c"
  block-size="20"
  bindchange="onSliderChange"
  bindchanging="onSliderChanging"
/>
```

**editor 组件**：

富文本编辑器，可以对图片、文字进行编辑。基础库 2.7.0+。

### 4.4 导航组件

| 组件 | 功能 | 最低版本 |
| --- | --- | --- |
| `navigator` | 页面链接 | 1.0.0 |
| `functional-page-navigator` | 仅在插件中有效，跳转到插件功能页 | 2.1.0 |

**navigator 组件属性**：

| 属性 | 类型 | 默认值 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- |
| `url` | string | - | 应用内的跳转链接 | 1.0.0 |
| `open-type` | string | navigate | 跳转方式 | 1.0.0 |
| `delta` | number | 1 | 当 open-type 为 navigateBack 时生效 | 1.0.0 |
| `hover-class` | string | navigator-hover | 指定按下去的样式类 | 1.0.0 |
| `hover-stop-propagation` | boolean | false | 指定是否阻止祖先节点出现点击态 | 1.5.0 |
| `hover-start-time` | number | 50 | 按住后多久出现点击态（ms） | 1.0.0 |
| `hover-stay-time` | number | 600 | 手指松开后点击态保留时间（ms） | 1.0.0 |
| `target` | string | self | 在哪个目标上发生跳转（self/miniProgram） | 2.0.7 |
| `app-id` | string | - | 当 target="miniProgram" 时有效，要打开的小程序 appId | 2.0.7 |
| `path` | string | - | 当 target="miniProgram" 时有效，打开的页面路径 | 2.0.7 |
| `extra-data` | object | - | 当 target="miniProgram" 时有效，需要传递给目标小程序的数据 | 2.0.7 |
| `version` | string | release | 当 target="miniProgram" 时有效，要打开的小程序版本 | 2.0.7 |
| `short-link` | string | - | 当 target="miniProgram" 时有效，小程序短链 | 2.13.0 |

**navigator open-type 合法值**：

| 值 | 说明 | 最低版本 |
| --- | --- | --- |
| `navigate` | 保留当前页面，跳转到应用内的某个页面 | 1.0.0 |
| `redirect` | 关闭当前页面，跳转到应用内的某个页面 | 1.0.0 |
| `switchTab` | 跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面 | 1.0.0 |
| `reLaunch` | 关闭所有页面，打开到应用内的某个页面 | 1.0.0 |
| `navigateBack` | 关闭当前页面，返回上一页面或多级页面 | 1.0.0 |
| `exit` | 退出小程序 | 2.1.0 |

**navigator 使用注意**：

- `navigate` 只能打开非 tabBar 页面
- `switchTab` 只能打开 tabBar 页面
- 跳转页面栈最多 10 层
- URL 路径必须以 `/` 开头

**示例**：

```xml
<!-- 普通跳转 -->
<navigator url="/pages/detail/index?id=1" open-type="navigate">跳转详情</navigator>

<!-- 跳转到 tabBar 页面 -->
<navigator url="/pages/home/index" open-type="switchTab">回到首页</navigator>

<!-- 重定向（关闭当前页） -->
<navigator url="/pages/login/index" open-type="redirect">去登录</navigator>

<!-- 打开其他小程序 -->
<navigator target="miniProgram" app-id="wx1234567890" path="pages/index/index">打开其他小程序</navigator>
```

### 4.5 媒体组件

| 组件 | 功能 | 最低版本 |
| --- | --- | --- |
| `audio` | 音频 | 1.0.0 |
| `image` | 图片 | 1.0.0 |
| `video` | 视频 | 1.0.0 |
| `camera` | 系统相机 | 1.0.0 |
| `live-player` | 实时音视频播放 | 1.7.0 |
| `live-pusher` | 实时音视频录制 | 1.7.0 |
| `voip-room` | 多人音视频对话 | 2.11.0 |
| `channel-live` | 视频号直播 | 2.21.2 |
| `channel-video` | 视频号视频 | 2.21.2 |

**image 组件属性**：

| 属性 | 类型 | 默认值 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- |
| `src` | string | - | 图片资源地址 | 1.0.0 |
| `mode` | string | scaleToFill | 图片裁剪、缩放模式 | 1.0.0 |
| `show-menu-by-longpress` | boolean | false | 长按图片显示菜单 | 2.7.0 |
| `lazy-load` | boolean | false | 图片懒加载（WebView） | 1.5.0 |
| `webp` | boolean | false | 是否解析 webP 格式（WebView） | 2.9.0 |
| `forceHttps` | boolean | false | 自动将 http 替换为 https | 3.9.1 |
| `binderror` | eventhandle | - | 当错误发生时触发 | 1.0.0 |
| `bindload` | eventhandle | - | 当图片载入完毕时触发 | 1.0.0 |

**image mode 合法值**：

| 值 | 说明 |
| --- | --- |
| `scaleToFill` | 不保持纵横比缩放，使图片完全适应 |
| `aspectFit` | 保持纵横比缩放，长边能完全显示 |
| `aspectFill` | 保持纵横比缩放，短边能完全显示（可能截取） |
| `widthFix` | 宽度不变，高度自动变化 |
| `heightFix` | 高度不变，宽度自动变化 |
| `top / bottom / center / left / right` | 裁剪模式（仅 WebView） |
| `top left / top right / bottom left / bottom right` | 裁剪模式（仅 WebView） |

**image 注意事项**：

- 默认宽度 320px、高度 240px
- 支持 JPG、PNG、SVG、WEBP、GIF
- 自 2.3.0 起支持云文件 ID
- svg 格式不支持百分比单位
- svg 格式不支持 `<style>` element
- 使用 svg 格式且 mode=scaleToFill 时，WebView 会居中，Skyline 会撑满

**video 组件关键属性**：

| 属性 | 类型 | 默认值 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- |
| `src` | string | - | 视频资源地址 | 1.0.0 |
| `initial-time` | number | - | 视频初始播放位置（秒） | 1.0.0 |
| `duration` | number | - | 指定视频时长（秒） | 1.1.0 |
| `controls` | boolean | true | 是否显示默认播放控件 | 1.0.0 |
| `autoplay` | boolean | false | 是否自动播放 | 1.0.0 |
| `loop` | boolean | false | 是否循环播放 | 1.0.0 |
| `muted` | boolean | false | 是否静音播放 | 1.0.0 |
| `object-fit` | string | contain | contain / fill / cover | 1.0.0 |
| `poster` | string | - | 视频封面的图片网络资源地址 | 1.0.0 |
| `show-fullscreen-btn` | boolean | true | 是否显示全屏按钮 | 1.0.0 |
| `show-play-btn` | boolean | true | 是否显示视频底部控制栏的播放按钮 | 1.0.0 |
| `show-center-play-btn` | boolean | true | 是否显示视频中间的播放按钮 | 1.0.0 |
| `enable-progress-gesture` | boolean | true | 是否开启控制进度的手势 | 1.0.0 |
| `vslide-gesture` | boolean | false | 在非全屏模式下，是否开启亮度与音量调节手势 | 1.0.0 |
| `vslide-gesture-in-fullscreen` | boolean | true | 在全屏模式下，是否开启亮度与音量调节手势 | 1.0.0 |
| `enable-play-gesture` | boolean | false | 是否开启播放手势，即双击切换播放/暂停 | 2.4.0 |
| `picture-in-picture-mode` | string | - | 小窗模式（push/ pop） | 2.11.0 |
| `bindplay` | eventhandle | - | 开始/继续播放时触发 | 1.0.0 |
| `bindpause` | eventhandle | - | 暂停播放时触发 | 1.0.0 |
| `bindended` | eventhandle | - | 播放到末尾时触发 | 1.0.0 |
| `binderror` | eventhandle | - | 视频播放出错时触发 | 1.0.0 |
| `bindwaiting` | eventhandle | - | 视频出现缓冲时触发 | 1.7.0 |
| `bindprogress` | eventhandle | - | 加载进度变化时触发 | 2.13.0 |

**camera 组件**：

需要用户授权 `scope.camera`，可实现扫码、拍摄等功能。

```xml
<camera 
  device-position="back" 
  flash="off" 
  bindstop="onCameraStop"
  binderror="onCameraError"
  style="width: 100%; height: 300px;"
></camera>
```

### 4.6 地图与画布

**map 组件**：

地图组件使用腾讯地图 SDK（`qqmap-wx-jssdk`），基础库 2.7.0 起支持同层渲染。

| 属性 | 类型 | 说明 | 最低版本 |
| --- | --- | --- | --- |
| `longitude` | number | 中心经度 | 1.0.0 |
| `latitude` | number | 中心纬度 | 1.0.0 |
| `scale` | number | 缩放级别（3-20） | 1.0.0 |
| `markers` | Array | 标记点 | 1.0.0 |
| `polyline` | Array | 路线 | 1.0.0 |
| `polygons` | Array | 多边形 | 1.0.0 |
| `circles` | Array | 圆 | 1.0.0 |
| `controls` | Array | 控件 | 1.0.0 |
| `show-location` | boolean | 显示当前定位点 | 1.0.0 |
| `show-compass` | boolean | 显示指南针 | 1.0.0 |
| `enable-3D` | boolean | 开启 3D 效果 | 1.0.0 |
| `enable-traffic` | boolean | 开启实时路况 | 1.0.0 |
| `enable-poi` | boolean | 是否展示 POI 点 | 2.14.0 |

**canvas 组件**：

画布组件，用于绘制图形、生成海报、处理图像。

| 属性 | 类型 | 说明 | 最低版本 |
| --- | --- | --- | --- |
| `canvas-id` | string | canvas 组件标识 | 1.0.0 |
| `type` | string | canvas 类型（2d / webgl） | 1.0.0 |
| `disable-scroll` | boolean | 禁止屏幕滚动以及下拉刷新 | 1.0.0 |
| `bindtouchstart` | eventhandle | 手指触摸动作开始 | 1.0.0 |
| `bindtouchmove` | eventhandle | 手指触摸后移动 | 1.0.0 |
| `bindtouchend` | eventhandle | 手指触摸动作结束 | 1.0.0 |
| `bindtouchcancel` | eventhandle | 手指触摸动作被打断 | 1.0.0 |
| `binderror` | eventhandle | 当发生错误时触发 | 1.0.0 |

**canvas 渲染模式**：

- **传统模式**：使用 `canvas-id`（基础库 1.0.0+）
- **新版类型**：使用 `type="2d"`，通过 `wx.createSelectorQuery().select('#canvas')` 获取渲染上下文（基础库 1.0.0+）

**推荐使用新版 type="2d"**，性能和 API 都更优。

### 4.7 开放能力

| 组件 | 功能 | 最低版本 |
| --- | --- | --- |
| `web-view` | 承载网页的容器 | 1.0.0 |
| `ad` | Banner 广告 | 2.10.0 |
| `ad-custom` | 原生模板广告 | 2.21.2 |
| `official-account` | 公众号关注组件 | 2.3.0 |
| `open-data` | 用于展示微信开放的数据 | 1.0.0 |
| `store-coupon` | 微信小店优惠券 | 2.31.0 |
| `store-gift` | 微信送礼物 | 2.32.0 |
| `store-home` | 微信小店首页 | 2.31.0 |
| `store-product` | 微信小店商品 | 2.31.0 |

**web-view 组件**：

承载网页的容器，会自动铺满整个小程序页面。**个人类型小程序不支持使用**。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `src` | string | 网页链接 |
| `bindmessage` | eventhandle | 网页向小程序 postMessage 时触发 |
| `bindload` | eventhandle | 网页加载成功时触发 |
| `binderror` | eventhandle | 网页加载失败时触发 |

**web-view 使用限制**：

- 仅支持 https 链接
- 网页内 iframe 不支持
- 网页应做好屏幕适配
- 需要在后台配置业务域名

**open-data 组件**：

用于展示微信开放的数据（如群名称、用户昵称等），基础库 1.4.0 起支持开放能力升级。

### 4.8 Skyline 专属组件

Skyline 渲染引擎提供了大量增强组件，**仅在 Skyline 渲染引擎下可用**。

**手势系统**（基础库 2.14.0+）：

| 组件 | 功能 |
| --- | --- |
| `tap-gesture-handler` | 点击时触发手势 |
| `double-tap-gesture-handler` | 双击时触发手势 |
| `long-press-gesture-handler` | 长按时触发手势 |
| `horizontal-drag-gesture-handler` | 横向滑动时触发手势 |
| `vertical-drag-gesture-handler` | 纵向滑动时触发手势 |
| `pan-gesture-handler` | 拖动（横向/纵向）时触发手势 |
| `scale-gesture-handler` | 多指缩放时触发手势 |
| `force-press-gesture-handler` | iPhone 设备重按时触发手势 |

**布局增强组件**（基础库 2.25.0+）：

| 组件 | 功能 |
| --- | --- |
| `draggable-sheet` | 半屏可拖拽组件 |
| `grid-builder` | 网格构造器 |
| `grid-view` | 网格布局容器、瀑布流 |
| `list-builder` | 列表构造器 |
| `list-view` | 列表布局容器 |
| `nested-scroll-body` | 嵌套 scroll-view 的里层节点 |
| `nested-scroll-header` | 嵌套 scroll-view 的外层节点 |
| `open-container` | 容器转场动画组件 |
| `open-data-item` | 展示微信开放数据 |
| `open-data-list` | 展示微信开放数据列表 |
| `share-element` | 共享元素 |
| `snapshot` | 截图组件 |
| `span` | 用于支持内联文本和 image / navigator 混排 |
| `sticky-header` | 吸顶布局容器 |
| `sticky-section` | 吸顶布局容器 |

### 4.9 组件兼容性速查表

| 组件 | Android | iOS | 鸿蒙 OS | Windows | macOS | 开发者工具 |
| --- | --- | --- | --- | --- | --- | --- |
| view | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| scroll-view | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| swiper | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| image | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| button | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| input | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| video | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| map | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| canvas | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| web-view | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| live-player | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| live-pusher | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| ad | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Skyline 系列 | ✅ | ✅ | ✅ | 部分 | 部分 | ✅ |

> **注意**：
> - `live-player` 和 `live-pusher` 在 PC 端（Windows/macOS）暂不支持
> - Skyline 渲染引擎需基础库 2.27.0+，鸿蒙 OS 上需使用鸿蒙版微信
> - PC 端能力比移动端少，建议在 PC 端做功能降级处理

---

## 第 5 章 API 接口手册

小程序提供丰富的 API，按功能可分为以下几类。

### 5.1 基础 API（系统/更新/调试/性能）

#### 5.1.1 系统信息

**wx.getSystemInfo / wx.getSystemInfoSync**

> 从基础库 2.20.1 开始，本接口停止维护，请使用：
> - `wx.getSystemSetting`
> - `wx.getAppAuthorizeSetting`
> - `wx.getDeviceInfo`
> - `wx.getWindowInfo`
> - `wx.getAppBaseInfo`

**wx.getSystemInfo 返回参数**：

| 属性 | 类型 | 说明 | 最低版本 |
| --- | --- | --- | --- |
| `brand` | string | 设备品牌 | 1.5.0 |
| `model` | string | 设备型号 | - |
| `pixelRatio` | number | 设备像素比 | - |
| `screenWidth` | number | 屏幕宽度（px） | 1.1.0 |
| `screenHeight` | number | 屏幕高度（px） | 1.1.0 |
| `windowWidth` | number | 可使用窗口宽度（px） | - |
| `windowHeight` | number | 可使用窗口高度（px） | - |
| `statusBarHeight` | number | 状态栏高度（px） | 1.9.0 |
| `language` | string | 微信设置的语言 | - |
| `version` | string | 微信版本号 | - |
| `system` | string | 操作系统及版本 | - |
| `platform` | string | 客户端平台 | - |
| `fontSizeSetting` | number | 用户字体大小（px） | 1.5.0 |
| `SDKVersion` | string | 客户端基础库版本 | 1.1.0 |
| `benchmarkLevel` | number | 设备性能等级（仅 Android） | 1.8.0 |
| `albumAuthorized` | boolean | 允许微信使用相册的开关（仅 iOS） | 2.6.0 |
| `cameraAuthorized` | boolean | 允许微信使用摄像头的开关 | 2.6.0 |
| `locationAuthorized` | boolean | 允许微信使用定位的开关 | 2.6.0 |
| `microphoneAuthorized` | boolean | 允许微信使用麦克风的开关 | 2.6.0 |
| `notificationAuthorized` | boolean | 允许微信通知的开关 | 2.6.0 |
| `bluetoothEnabled` | boolean | 蓝牙的系统开关 | 2.6.0 |
| `locationEnabled` | boolean | 地理位置的系统开关 | 2.6.0 |
| `wifiEnabled` | boolean | Wi-Fi 的系统开关 | 2.6.0 |
| `safeArea` | Object | 安全区域 | 2.7.0 |
| `theme` | string | 系统当前主题（light / dark） | 2.11.0 |
| `host` | Object | 当前小程序运行的宿主环境 | 2.12.3 |
| `enableDebug` | boolean | 是否已打开调试 | 2.15.0 |
| `deviceOrientation` | string | 设备方向（portrait / landscape） | - |

**platform 合法值**：

- `ios`：iOS 微信（包含 iPhone、iPad）
- `android`：Android 微信
- `ohos`：HarmonyOS 手机端微信
- `ohos_pc`：HarmonyOS PC 微信
- `windows`：Windows 微信
- `mac`：macOS 微信
- `devtools`：微信开发者工具

**wx.getDeviceInfo**（推荐使用，2.20.1+）：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `model` | string | 设备型号 |
| `brand` | string | 设备品牌 |
| `platform` | string | 客户端平台 |
| `system` | string | 操作系统及版本 |
| `abi` | string | 设备 abi（仅 Android） |
| `benchmarkLevel` | number | 设备性能等级（仅 Android） |

**wx.getWindowInfo**（推荐使用，2.20.1+）：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `pixelRatio` | number | 设备像素比 |
| `screenWidth` | number | 屏幕宽度（px） |
| `screenHeight` | number | 屏幕高度（px） |
| `windowWidth` | number | 可使用窗口宽度（px） |
| `windowHeight` | number | 可使用窗口高度（px） |
| `statusBarHeight` | number | 状态栏高度（px） |
| `safeArea` | Object | 安全区域 |

**wx.getAppBaseInfo**（推荐使用，2.20.1+）：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `SDKVersion` | string | 客户端基础库版本 |
| `version` | string | 微信版本号 |
| `language` | string | 微信设置的语言 |
| `theme` | string | 系统当前主题 |
| `host` | Object | 当前小程序运行的宿主环境 |

**wx.getSystemSetting**：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `bluetoothEnabled` | boolean | 蓝牙的系统开关 |
| `locationEnabled` | boolean | 地理位置的系统开关 |
| `wifiEnabled` | boolean | Wi-Fi 的系统开关 |
| `deviceOrientation` | string | 设备方向 |

**wx.getAppAuthorizeSetting**：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `albumAuthorized` | boolean | 允许微信使用相册（仅 iOS） |
| `cameraAuthorized` | boolean | 允许微信使用摄像头 |
| `locationAuthorized` | boolean | 允许微信使用定位 |
| `microphoneAuthorized` | boolean | 允许微信使用麦克风 |
| `notificationAuthorized` | boolean | 允许微信通知 |
| `phoneCalendarAuthorized` | boolean | 允许微信使用日历 |

#### 5.1.2 生命周期 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.getLaunchOptionsSync` | 获取小程序启动时的参数 | - |
| `wx.getEnterOptionsSync` | 获取本次小程序启动时的参数 | - |
| `wx.getApiCategory` | 获取当前 API 类别 | - |
| `wx.onApiCategoryChange` | 监听 API 类别变化事件 | - |
| `wx.onAppShow` | 监听小程序切前台事件 | - |
| `wx.onAppHide` | 监听小程序切后台事件 | - |
| `wx.onError` | 监听小程序错误事件 | - |
| `wx.onUnhandledRejection` | 监听未处理的 Promise 拒绝事件 | - |
| `wx.onPageNotFound` | 监听小程序要打开的页面不存在事件 | - |
| `wx.onThemeChange` | 监听系统主题改变事件 | - |
| `wx.onAudioInterruptionBegin` | 监听音频中断开始事件 | - |
| `wx.onAudioInterruptionEnd` | 监听音频中断结束事件 | - |
| `wx.onLazyLoadError` | 监听小程序异步组件加载失败事件 | - |

#### 5.1.3 更新 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.getUpdateManager` | 获取全局唯一的版本更新管理器 | - |
| `wx.updateWeChatApp` | 更新客户端版本 | - |

**UpdateManager 方法**：

- `applyUpdate()`：强制小程序重启并使用新版本
- `onCheckForUpdate(callback)`：监听向微信后台请求检查更新结果事件
- `onUpdateReady(callback)`：监听小程序有版本更新事件
- `onUpdateFailed(callback)`：监听小程序更新失败事件

**使用流程**：

```javascript
const updateManager = wx.getUpdateManager()

updateManager.onCheckForUpdate(function (res) {
  // 请求完新版本信息的回调
  console.log(res.hasUpdate)
})

updateManager.onUpdateReady(function () {
  wx.showModal({
    title: '更新提示',
    content: '新版本已经准备好，是否重启应用？',
    success(res) {
      if (res.confirm) {
        updateManager.applyUpdate()
      }
    }
  })
})

updateManager.onUpdateFailed(function () {
  // 新版本下载失败
})
```

#### 5.1.4 调试 API

| API | 说明 |
| --- | --- |
| `wx.setEnableDebug` | 设置是否打开调试开关 |
| `wx.getRealtimeLogManager` | 获取实时日志管理器对象 |
| `wx.getLogManager` | 获取日志管理器对象 |
| `console.debug` / `console.log` / `console.info` / `console.warn` / `console.error` | 控制台日志 |

**LogManager 方法**：

- `LogManager.debug()`：写 debug 日志
- `LogManager.info()`：写 info 日志
- `LogManager.log()`：写 log 日志
- `LogManager.warn()`：写 warn 日志

**RealtimeLogManager 方法**：

- `info()` / `warn()` / `error()`：写日志
- `setFilterMsg()`：设置过滤关键字
- `addFilterMsg()`：添加过滤关键字
- `tag()`：获取给定标签的日志管理器实例

#### 5.1.5 性能 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.getPerformance` | 获取当前小程序性能相关的信息 | 2.13.0 |
| `wx.reportPerformance` | 小程序测速上报 | 2.13.0 |
| `wx.requestIdleCallback` | 注册一个空闲时期被调用的函数 | - |
| `wx.cancelIdleCallback` | 取消之前注册的指定回调函数 | - |
| `wx.preloadWebview` | 预加载下个页面的 WebView | - |
| `wx.preloadSkylineView` | 预加载下个页面的 Skyline 运行环境 | - |
| `wx.preloadAssets` | 为视图层预加载媒体资源文件 | - |

**Performance API 使用**：

```javascript
const performance = wx.getPerformance()
const observer = performance.createObserver((list) => {
  list.getEntries().forEach((entry) => {
    console.log(entry.name, entry.entryType, entry.duration)
  })
})
observer.observe({ entryTypes: ['render', 'script', 'navigation'] })
```

### 5.2 网络 API

#### 5.2.1 wx.request（核心 API）

**功能**：发起 HTTPS 网络请求。

**最低版本**：1.0.0

**Object 参数**：

| 属性 | 类型 | 默认值 | 必填 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- | --- |
| `url` | string | - | 是 | 开发者服务器接口地址 | - |
| `data` | string/object/ArrayBuffer | - | 否 | 请求的参数 | - |
| `header` | Object | - | 否 | 请求的 header，header 中不能设置 Referer | - |
| `timeout` | number | 60000 | 否 | 超时时间（ms） | 2.10.0 |
| `method` | string | GET | 否 | HTTP 请求方法 | - |
| `dataType` | string | json | 否 | 返回的数据格式 | - |
| `responseType` | string | text | 否 | 响应的数据类型（text / arraybuffer） | 1.7.0 |
| `useHighPerformanceMode` | boolean | true | 否 | 使用高性能模式（Android 默认开启） | 3.3.3 |
| `enableHttp2` | boolean | false | 否 | 开启 http2 | 2.10.4 |
| `enableProfile` | boolean | true | 否 | 是否开启 profile（iOS/Android） | - |
| `enableQuic` | boolean | false | 否 | 是否开启 Quic/h3 协议 | 2.10.4 |
| `enableCache` | boolean | false | 否 | 开启 Http 缓存 | 2.10.4 |
| `enableHttpDNS` | boolean | false | 否 | 是否开启 HttpDNS 服务 | 2.19.1 |
| `httpDNSServiceId` | string | - | 否 | HttpDNS 服务商 Id | 2.19.1 |
| `httpDNSTimeout` | number | 60000 | 否 | HttpDNS 超时时间（ms） | 3.8.9 |
| `httpDNSFallback` | boolean | true | 否 | 是否开启 HttpDNS 兜底 | 3.16.2 |
| `enableChunked` | boolean | false | 否 | 开启 transfer-encoding chunked | 2.20.2 |
| `forceCellularNetwork` | boolean | false | 否 | 强制使用蜂窝网络发送请求 | 2.21.0 |
| `redirect` | string | follow | 否 | 重定向拦截策略 | 3.2.2 |
| `success` | function | - | 否 | 接口调用成功的回调函数 | - |
| `fail` | function | - | 否 | 接口调用失败的回调函数 | - |
| `complete` | function | - | 否 | 接口调用结束的回调函数 | - |

**HTTP 请求方法合法值**：

`OPTIONS` `GET` `HEAD` `POST` `PUT` `DELETE` `TRACE` `CONNECT`

**data 参数说明**：

- 对于 `GET` 方法，会将数据转换成 query string
- 对于 `POST` + `application/json`，会对数据进行 JSON 序列化
- 对于 `POST` + `application/x-www-form-urlencoded`，会转换成 query string

**响应参数**：

| 属性 | 类型 | 说明 | 最低版本 |
| --- | --- | --- | --- |
| `data` | string/Object/Arraybuffer | 开发者服务器返回的数据 | - |
| `statusCode` | number | HTTP 状态码 | - |
| `header` | Object | HTTP Response Header | 1.2.0 |
| `cookies` | Array.<string> | cookies，格式为字符串数组 | 2.10.0 |
| `profile` | Object | 网络请求调试信息（仅 iOS/Android） | 2.10.4 |

**网络使用限制**：

1. **必须使用 HTTPS**：所有小程序网络请求必须使用 HTTPS 协议
2. **需要在后台配置 request 合法域名**：在微信公众平台配置
3. **跳过域名校验**：开发阶段可在开发者工具中勾选"不校验合法域名"
4. **并发限制**：默认 10 个并发请求
5. **频率限制**：详见 [接口调用频率规范](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/api-frequency.html)

**示例代码**：

```javascript
wx.request({
  url: 'https://api.yuanyuangao.com/v1/users/me',
  method: 'GET',
  header: {
    'content-type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  timeout: 10000,
  success(res) {
    if (res.statusCode === 200) {
      console.log(res.data)
    }
  },
  fail(err) {
    console.error('请求失败', err)
  }
})
```

#### 5.2.2 上传与下载

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.uploadFile` | 上传文件到服务器 | 1.0.0 |
| `wx.downloadFile` | 下载文件到本地 | 1.0.0 |
| `FileSystemManager.readFile` | 读取本地文件 | 1.0.0 |
| `FileSystemManager.writeFile` | 写入本地文件 | 1.0.0 |

**wx.uploadFile 参数**：

| 属性 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `url` | string | 是 | 开发者服务器地址 |
| `filePath` | string | 是 | 要上传文件资源的路径 |
| `name` | string | 是 | 文件对应的 key |
| `header` | Object | 否 | HTTP 请求 Header |
| `formData` | Object | 否 | HTTP 请求中其他额外的 form data |
| `timeout` | number | 否 | 超时时间（ms），默认 60000 |
| `success` | function | 否 | 接口调用成功的回调函数 |

**wx.downloadFile 参数**：

| 属性 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `url` | string | 是 | 下载资源的 url |
| `header` | Object | 否 | HTTP 请求 Header |
| `timeout` | number | 否 | 超时时间（ms），默认 60000 |
| `success` | function | 否 | 接口调用成功的回调函数 |

#### 5.2.3 WebSocket

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.connectSocket` | 创建一个 WebSocket 连接 | 1.0.0 |
| `SocketTask` | WebSocket 任务 | 1.0.0 |
| `wx.sendSocketMessage` | 通过 WebSocket 连接发送数据 | 1.0.0 |
| `wx.closeSocket` | 关闭 WebSocket 连接 | 1.0.0 |
| `wx.onSocketOpen` | 监听 WebSocket 连接打开事件 | 1.0.0 |
| `wx.onSocketError` | 监听 WebSocket 错误事件 | 1.0.0 |
| `wx.onSocketMessage` | 监听 WebSocket 接受到服务器的消息事件 | 1.0.0 |
| `wx.onSocketClose` | 监听 WebSocket 关闭事件 | 1.0.0 |

**注意**：推荐使用 `SocketTask` 实例方法（`send`、`close`、`onOpen`、`onMessage`、`onError`、`onClose`），不要再使用旧版的 `wx.sendSocketMessage` 等。

#### 5.2.4 mDNS / UDP / TCP

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.createUDPSocket` | 创建一个 UDP Socket 实例 | 2.9.0 |
| `wx.createTCPSocket` | 创建一个 TCP Socket 实例 | 2.18.0 |

#### 5.2.5 网络状态

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.getNetworkType` | 获取网络类型 | 1.0.0 |
| `wx.onNetworkStatusChange` | 监听网络状态变化 | 1.0.0 |
| `wx.getLocalIPAddress` | 获取局域网 IP | 2.16.0 |

**网络类型合法值**：`wifi` `2g` `3g` `4g` `5g` `ethernet` `unknown` `none`

### 5.3 媒体 API（音频/视频/图片）

#### 5.3.1 音频 API

**wx.createInnerAudioContext**

> 基础库 1.6.0 开始支持

创建内部 audio 上下文 InnerAudioContext 对象。

```javascript
const innerAudioContext = wx.createInnerAudioContext({
  useWebAudioImplement: false // 短音频建议开启
})
innerAudioContext.src = 'https://cdn.yuanyuangao.com/audio/day1.mp3'
innerAudioContext.play()
```

**InnerAudioContext 属性**：

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `src` | string | - | 音频资源的地址 |
| `startTime` | number | 0 | 音频开始播放的位置（秒） |
| `autoplay` | boolean | false | 是否自动开始播放 |
| `loop` | boolean | false | 是否循环播放 |
| `obeyMuteSwitch` | boolean | false | 是否遵循系统静音开关 |
| `volume` | number | 1 | 音量，范围 0-1 |
| `playbackRate` | number | 1 | 播放速度，范围 0.5-2.0 |
| `currentTime` | number | - | 当前音频的播放位置（秒） |
| `duration` | number | - | 当前音频的长度（秒） |
| `paused` | boolean | - | 当前是否暂停或停止 |
| `buffered` | number | - | 音频缓冲的时间点 |

**InnerAudioContext 方法**：

- `play()`：播放
- `pause()`：暂停
- `stop()`：停止
- `seek(position)`：跳转到指定位置
- `destroy()`：释放音频资源
- `onCanplay(callback)`：音频进入可以播放状态
- `onPlay(callback)`：音频播放事件
- `onPause(callback)`：音频暂停事件
- `onStop(callback)`：音频停止事件
- `onEnded(callback)`：音频自然播放结束事件
- `onTimeUpdate(callback)`：音频播放进度更新事件
- `onError(callback)`：音频播放错误事件
- `onWaiting(callback)`：音频加载中事件

**注意事项**：

- 音频资源不会自动释放，及时调用 `destroy()` 释放资源
- 单个小程序最多同时存在 30 个 InnerAudioContext
- iOS 26.2 上有 InnerAudioContext 播放 mp3 异常问题
- 鸿蒙手机微信小程序 InnerAudioContext 播放网络音频可能导致闪退

**其他音频 API**：

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.createMediaAudioContext` | 创建媒体音频播放上下文 | 2.13.0 |
| `wx.getAvailableAudioSources` | 获取当前支持的音频输入源 | 1.0.0 |
| `wx.startRecord` | 开始录音 | 1.0.0 |
| `wx.stopRecord` | 停止录音 | 1.0.0 |
| `RecorderManager` | 录音管理器 | 1.6.0 |
| `wx.playVoice` | 播放语音（即将废弃） | 1.0.0 |

#### 5.3.2 视频 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.chooseMedia` | 拍摄或从手机相册中选择图片或视频 | 2.10.0 |
| `wx.chooseVideo` | 拍摄或从手机相册中选择视频（即将废弃） | 1.0.0 |
| `wx.chooseImage` | 从本地相册选择图片或拍照 | 1.0.0 |
| `wx.saveImageToPhotosAlbum` | 保存图片到系统相册 | 1.0.0 |
| `wx.saveVideoToPhotosAlbum` | 保存视频到系统相册 | 1.0.0 |
| `wx.getVideoInfo` | 获取视频详细信息 | 2.11.0 |
| `wx.compressVideo` | 压缩视频接口 | 2.11.0 |
| `wx.openVideoEditor` | 打开视频编辑器 | 2.12.0 |
| `VideoContext` | 视频上下文 | 1.0.0 |

#### 5.3.3 图片 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.chooseImage` | 从本地相册选择图片或拍照 | 1.0.0 |
| `wx.chooseMedia` | 拍摄或从手机相册中选择图片或视频 | 2.10.0 |
| `wx.previewMedia` | 预览图片和视频 | 2.10.0 |
| `wx.previewImage` | 预览图片 | 1.0.0 |
| `wx.saveImageToPhotosAlbum` | 保存图片到系统相册 | 1.0.0 |
| `wx.getImageInfo` | 获取图片信息 | 1.0.0 |
| `wx.compressImage` | 压缩图片接口 | 2.10.0 |
| `wx.cropImage` | 裁剪图片 | 2.26.0 |

#### 5.3.4 相机与实时音视频

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.createCameraContext` | 创建 camera 上下文 | 1.0.0 |
| `CameraContext` | 相机上下文 | 1.0.0 |
| `wx.createLivePlayerContext` | 创建 live-player 上下文 | 1.7.0 |
| `wx.createLivePusherContext` | 创建 live-pusher 上下文 | 1.7.0 |
| `LivePlayerContext` | 直播播放器上下文 | 1.7.0 |
| `LivePusherContext` | 直播推流上下文 | 1.7.0 |

### 5.4 位置 API

#### 5.4.1 wx.getLocation

> 基础库 2.17.0 起增加调用频率限制
>
> 2022.7.14 后发布的小程序，需在 `app.json` 中声明 `requiredPrivateInfos: ["getLocation"]`

**用户授权**：需要 `scope.userLocation`

**Object 参数**：

| 属性 | 类型 | 默认值 | 必填 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- | --- |
| `type` | string | wgs84 | 否 | wgs84 返回 gps 坐标；gcj02 返回可用于 wx.openLocation 的坐标 | - |
| `altitude` | boolean | false | 否 | 传入 true 会返回高度信息 | 1.6.0 |
| `isHighAccuracy` | boolean | false | 否 | 开启高精度定位 | 2.9.0 |
| `highAccuracyExpireTime` | number | - | 否 | 高精度定位超时时间（ms） | 2.9.0 |
| `success` | function | - | 否 | 接口调用成功的回调函数 | - |
| `fail` | function | - | 否 | 接口调用失败的回调函数 | - |
| `complete` | function | - | 否 | 接口调用结束的回调函数 | - |

**success 回调参数**：

| 属性 | 类型 | 说明 | 最低版本 |
| --- | --- | --- | --- |
| `latitude` | number | 纬度，范围为 -90~90 | - |
| `longitude` | number | 经度，范围为 -180~180 | - |
| `speed` | number | 速度（m/s） | - |
| `accuracy` | number | 位置精确度 | - |
| `altitude` | number | 高度（m） | 1.2.0 |
| `verticalAccuracy` | number | 垂直精度（m），Android 返回 0 | 1.2.0 |
| `horizontalAccuracy` | number | 水平精度（m） | 1.2.0 |

**类目限制**：

`wx.getLocation` 接口仅对部分开放类目的小程序开放，需要在微信公众平台「开发-开发管理-接口设置」中自助开通该接口权限。

**开放类目**：电商平台、商家自营、医疗服务、交通服务、生活服务、物流服务、餐饮服务、工具、金融、旅游、汽车服务、IT科技、房地产服务、政务民生等。

**使用示例**：

```javascript
wx.getLocation({
  type: 'gcj02',
  isHighAccuracy: true,
  highAccuracyExpireTime: 5000,
  success(res) {
    console.log('纬度:', res.latitude)
    console.log('经度:', res.longitude)
  },
  fail(err) {
    console.error('获取位置失败', err)
  }
})
```

#### 5.4.2 其他位置 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.chooseLocation` | 打开地图选择位置 | 1.0.0 |
| `wx.openLocation` | 使用微信内置地图查看位置 | 1.0.0 |
| `wx.onLocationChange` | 监听实时地理位置变化事件 | 2.9.0 |
| `wx.offLocationChange` | 移除实时地理位置变化事件的监听函数 | 2.9.0 |
| `wx.startLocationUpdate` | 开启小程序进入前台时接收位置消息 | 2.9.0 |
| `wx.stopLocationUpdate` | 关闭监听实时位置变化 | 2.9.0 |
| `wx.startLocationUpdateBackground` | 开始监听实时位置变化（前后台） | 2.9.0 |
| `wx.getFuzzyLocation` | 获取当前的模糊地理位置 | 2.26.0 |
| `wx.getLocationPrivacySetting` | 查询小程序地理位置相关隐私设置 | 3.13.0 |

### 5.5 设备 API（蓝牙/网络/屏幕等）

#### 5.5.1 蓝牙 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.openBluetoothAdapter` | 初始化蓝牙模块 | 1.1.0 |
| `wx.closeBluetoothAdapter` | 关闭蓝牙模块 | 1.1.0 |
| `wx.getBluetoothAdapterState` | 获取本机蓝牙适配器状态 | 1.1.0 |
| `wx.onBluetoothAdapterStateChange` | 监听蓝牙适配器状态变化事件 | 1.1.0 |
| `wx.startBluetoothDevicesDiscovery` | 开始搜寻附近的蓝牙外围设备 | 1.1.0 |
| `wx.stopBluetoothDevicesDiscovery` | 停止搜寻附近的蓝牙外围设备 | 1.1.0 |
| `wx.getBluetoothDevices` | 获取在蓝牙模块生效期间所有已发现的蓝牙设备 | 1.1.0 |
| `wx.getConnectedBluetoothDevices` | 根据 uuid 获取处于已连接状态的设备 | 1.1.0 |
| `wx.createBLEConnection` | 连接低功耗蓝牙设备 | 1.1.0 |
| `wx.closeBLEConnection` | 断开与低功耗蓝牙设备的连接 | 1.1.0 |
| `wx.getBLEDeviceServices` | 获取蓝牙设备所有 service（服务） | 1.1.0 |
| `wx.getBLEDeviceCharacteristics` | 获取蓝牙设备某个 service 的所有 characteristic | 1.1.0 |
| `wx.readBLECharacteristicValue` | 读取低功耗蓝牙设备的特征值的二进制数据值 | 1.1.0 |
| `wx.writeBLECharacteristicValue` | 向低功耗蓝牙设备特征值写入二进制数据 | 1.1.0 |
| `wx.notifyBLECharacteristicValueChange` | 启用低功耗蓝牙设备特征值变化时的 notify 功能 | 1.1.0 |
| `wx.onBLECharacteristicValueChange` | 监听低功耗蓝牙设备的特征值变化事件 | 1.1.0 |
| `wx.onBLEConnectionStateChange` | 监听低功耗蓝牙连接状态的改变事件 | 1.1.0 |

#### 5.5.2 Wi-Fi / NFC API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.startWifi` | 初始化 Wi-Fi 模块 | 1.6.0 |
| `wx.stopWifi` | 关闭 Wi-Fi 模块 | 1.6.0 |
| `wx.getWifiList` | 请求获取 Wi-Fi 列表 | 1.6.0 |
| `wx.onGetWifiList` | 监听获取到 Wi-Fi 列表数据事件 | 1.6.0 |
| `wx.connectWifi` | 连接 Wi-Fi | 1.6.0 |
| `wx.getConnectedWifi` | 获取已连接中的 Wi-Fi 信息 | 1.6.0 |
| `wx.onWifiConnected` | 监听连接上 Wi-Fi 事件 | 1.6.0 |
| `wx.onWifiConnectedWithPartialInfo` | 监听连接上 Wi-Fi 事件（部分信息） | 2.13.0 |
| `wx.getLocalIPAddress` | 获取局域网 IP | 2.16.0 |
| `wx.startHCE` | 初始化 NFC 模块 | 1.7.0 |
| `wx.stopHCE` | 关闭 NFC 模块 | 1.7.0 |
| `wx.onHCEMessage` | 监听接收 NFC 设备消息事件 | 1.7.0 |
| `wx.sendHCEMessage` | 发送 NFC 消息 | 1.7.0 |

#### 5.5.3 屏幕与亮度

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.setScreenBrightness` | 设置屏幕亮度 | 1.2.0 |
| `wx.getScreenBrightness` | 获取屏幕亮度 | 1.2.0 |
| `wx.setKeepScreenOn` | 设置是否保持常亮状态 | 1.4.0 |
| `wx.onUserCaptureScreen` | 监听用户主动截屏事件 | 1.4.0 |
| `wx.onScreenLockStateChange` | 监听屏幕锁定状态变化事件 | 2.16.1 |

#### 5.5.4 振动与触感反馈

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.vibrateShort` | 使手机发生较短时间的振动（15ms） | 1.2.0 |
| `wx.vibrateLong` | 使手机发生较长时间的振动（400ms） | 1.2.0 |

#### 5.5.5 加速度计 / 罗盘 / 陀螺仪

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.startAccelerometer` | 开始监听加速度数据 | 1.1.0 |
| `wx.stopAccelerometer` | 停止监听加速度数据 | 1.1.0 |
| `wx.onAccelerometerChange` | 监听加速度数据事件 | 1.1.0 |
| `wx.startCompass` | 开始监听罗盘数据 | 1.1.0 |
| `wx.stopCompass` | 停止监听罗盘数据 | 1.1.0 |
| `wx.onCompassChange` | 监听罗盘数据事件 | 1.1.0 |
| `wx.startGyroscope` | 开始监听陀螺仪数据 | 2.3.0 |
| `wx.stopGyroscope` | 停止监听陀螺仪数据 | 2.3.0 |
| `wx.onGyroscopeChange` | 监听陀螺仪数据事件 | 2.3.0 |

#### 5.5.6 扫码 / 二维码

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.scanCode` | 调起客户端扫码界面进行扫码 | 1.0.0 |

**scanCode 回调参数**：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `result` | string | 所扫码的内容 |
| `scanType` | string | 扫码类型 |
| `charSet` | string | 扫码所识别的字符集 |
| `path` | string | 当所扫的码为小程序码时，会返回此字段 |
| `rawData` | string | 原始数据，base64 编码 |

### 5.6 界面 API（交互/导航/tabBar/菜单）

#### 5.6.1 交互反馈

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.showToast` | 显示消息提示框 | 1.0.0 |
| `wx.hideToast` | 隐藏消息提示框 | 1.0.0 |
| `wx.showModal` | 显示模态对话框 | 1.0.0 |
| `wx.showLoading` | 显示 loading 提示框 | 1.0.0 |
| `wx.hideLoading` | 隐藏 loading 提示框 | 1.0.0 |
| `wx.showActionSheet` | 显示操作菜单 | 1.0.0 |
| `wx.enableAlertBeforeUnload` | 开启小程序页面返回询问对话框 | 2.12.0 |
| `wx.disableAlertBeforeUnload` | 关闭小程序页面返回询问对话框 | 2.12.0 |

**showToast 参数**：

| 属性 | 类型 | 默认值 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `title` | string | - | 是 | 提示的内容 |
| `icon` | string | success | 否 | success / error / loading / none |
| `image` | string | - | 否 | 自定义图标的本地路径 |
| `duration` | number | 1500 | 否 | 提示的延迟时间（ms） |
| `mask` | boolean | false | 否 | 是否显示透明蒙层 |
| `position` | string | - | 否 | top / center / bottom |

#### 5.6.2 导航

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.navigateTo` | 保留当前页面，跳转到应用内的某个页面 | 1.0.0 |
| `wx.redirectTo` | 关闭当前页面，跳转到应用内的某个页面 | 1.0.0 |
| `wx.switchTab` | 跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面 | 1.0.0 |
| `wx.reLaunch` | 关闭所有页面，打开到应用内的某个页面 | 1.0.0 |
| `wx.navigateBack` | 关闭当前页面，返回上一页面或多级页面 | 1.0.0 |
| `wx.exitMiniProgram` | 退出小程序 | 2.1.0 |

**页面跳转 API 对比**：

| API | 是否关闭当前页 | 是否可跳 tabBar | 页面栈变化 |
| --- | --- | --- | --- |
| `navigateTo` | 否 | 否 | 页面栈 +1（最多 10 层） |
| `redirectTo` | 是 | 否 | 替换当前页 |
| `switchTab` | 是 | 是 | 跳转到 tabBar 页面 |
| `reLaunch` | 是 | 是 | 关闭所有页，重新打开 |
| `navigateBack` | - | - | 页面栈 -n |

#### 5.6.3 TabBar

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.setTabBarItem` | 动态设置 tabBar 某一项的内容 | 1.9.0 |
| `wx.setTabBarStyle` | 动态设置 tabBar 的整体样式 | 1.9.0 |
| `wx.hideTabBar` | 隐藏 tabBar | 1.9.0 |
| `wx.showTabBar` | 显示 tabBar | 1.9.0 |
| `wx.setTabBarBadge` | 为 tabBar 某一项的右上角添加文本 | 1.9.0 |
| `wx.removeTabBarBadge` | 移除 tabBar 某一项右上角的文本 | 1.9.0 |
| `wx.showTabBarRedDot` | 显示 tabBar 某一项的右上角的红点 | 1.9.0 |
| `wx.hideTabBarRedDot` | 隐藏 tabBar 某一项的右上角的红点 | 1.9.0 |
| `wx.onTabBarMidButtonTap` | 监听中间按钮的点击事件 | 2.5.0 |

#### 5.6.4 导航栏

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.setNavigationBarTitle` | 动态设置当前页面的标题 | 1.4.0 |
| `wx.setNavigationBarColor` | 设置页面导航条颜色 | 1.4.0 |
| `wx.showNavigationBarLoading` | 在当前页面显示导航条加载动画 | 1.0.0 |
| `wx.hideNavigationBarLoading` | 在当前页面隐藏导航条加载动画 | 1.0.0 |
| `wx.setNavigationBarLoading` | 设置导航条加载动画（鸿蒙） | - |

#### 5.6.5 菜单

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.showShareMenu` | 显示分享按钮 | 1.0.0 |
| `wx.hideShareMenu` | 隐藏分享按钮 | 1.0.0 |
| `wx.showMore` | 显示右上角菜单 | 3.0.0 |
| `wx.showFavoriteGuide` | 显示收藏引导 | 2.13.0 |

#### 5.6.6 滚动与动画

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.pageScrollTo` | 将页面滚动到目标位置 | 1.0.0 |
| `wx.createAnimation` | 创建一个动画实例 animation | 1.0.0 |
| `Animation` | 动画实例 | 1.0.0 |
| `wx.createSelectorQuery` | 返回一个 SelectorQuery 对象实例 | 1.4.0 |
| `SelectorQuery` | 选择器查询 | 1.4.0 |

#### 5.6.7 键盘与输入

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.hideKeyboard` | 隐藏键盘 | 1.1.0 |
| `wx.onKeyboardHeightChange` | 监听键盘高度变化事件 | 2.4.0 |
| `wx.offKeyboardHeightChange` | 移除键盘高度变化事件的监听函数 | 2.4.0 |

#### 5.6.8 窗口

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.setWindowSize` | 改变窗口大小（仅 PC） | - |
| `wx.checkIsPictureInPictureSupported` | 检查当前设备是否支持画中画 | 3.0.1 |
| `wx.setVisualEffectOnCapture` | 设置截屏/录屏时是否隐藏系统能力 UI | 3.4.7 |
| `wx.setVisualEffectOnUserCapture` | 设置用户截屏/录屏时是否隐藏页面 | 3.10.0 |

### 5.7 数据缓存 API

#### 5.7.1 同步缓存 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.setStorageSync` | 将数据存储在本地缓存中指定的 key 中 | 1.0.0 |
| `wx.getStorageSync` | 从本地缓存中同步获取指定 key 的内容 | 1.0.0 |
| `wx.removeStorageSync` | 从本地缓存中同步移除指定 key | 1.0.0 |
| `wx.clearStorageSync` | 同步清理本地数据缓存 | 1.0.0 |
| `wx.getStorageInfoSync` | 同步获取当前 storage 的相关信息 | 1.0.0 |

**wx.setStorageSync 参数**：

- `key`：本地缓存中指定的 key
- `data`：需要存储的内容。只支持原生类型、Date、及能够通过 JSON.stringify 序列化的对象

**存储限制**：

- 单个 key 允许存储的最大数据长度为 **1MB**
- 所有数据存储上限为 **10MB**
- 启动过程中过多的同步读写存储，会显著影响启动耗时

#### 5.7.2 异步缓存 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.setStorage` | 将数据存储在本地缓存中指定的 key 中 | 1.0.0 |
| `wx.getStorage` | 从本地缓存中异步获取指定 key 的内容 | 1.0.0 |
| `wx.removeStorage` | 从本地缓存中异步移除指定 key | 1.0.0 |
| `wx.clearStorage` | 异步清理本地数据缓存 | 1.0.0 |
| `wx.getStorageInfo` | 异步获取当前 storage 的相关信息 | 1.0.0 |

**wx.setStorage 参数**：

| 属性 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `key` | string | 是 | 本地缓存中指定的 key |
| `data` | any | 是 | 需要存储的内容 |
| `success` | function | 否 | 接口调用成功的回调函数 |
| `fail` | function | 否 | 接口调用失败的回调函数 |
| `complete` | function | 否 | 接口调用结束的回调函数 |

**注意事项**：

- storage 应只用来进行数据的持久化存储，不应用于运行时的数据传递或全局状态管理
- 异步 API 在大部分场景下都优于同步 API（不阻塞渲染线程）
- `wx.setStorageSync` 在部分苹果微信客户端的本地数据库有损坏问题
- `wx.setStorageSync` 在纯血鸿蒙系统中有异常问题

#### 5.7.3 缓存策略

**存储隔离**：

- 不同小程序的 storage 相互隔离
- 同一个小程序不同用户（不同 openid）的 storage 是隔离的
- 同一用户在同一设备上不同小程序的 storage 是隔离的

**存储建议**：

1. 关键数据使用异步 API，避免阻塞
2. 大量数据写入时使用异步 API
3. 启动时尽量减少同步 API 的调用
4. 敏感数据（密码、token）应做加密处理
5. 设置数据应有过期机制

### 5.8 开放能力 API（登录/支付/分享/订阅等）

#### 5.8.1 登录

**wx.login**

> 基础库 1.0.0

调用接口获取登录凭证（code），有效期 5 分钟。开发者需要在开发者服务器后台调用 `code2Session`，使用 code 换取 openid、unionid、session_key 等信息。

**Object 参数**：

| 属性 | 类型 | 必填 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- |
| `timeout` | number | 否 | 超时时间（ms） | 1.9.90 |
| `success` | function | 否 | 接口调用成功的回调函数 | - |
| `fail` | function | 否 | 接口调用失败的回调函数 | - |
| `complete` | function | 否 | 接口调用结束的回调函数 | - |

**success 回调参数**：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `code` | string | 用户登录凭证（有效期 5 分钟） |

**示例代码**：

```javascript
wx.login({
  success(res) {
    if (res.code) {
      // 发起网络请求
      wx.request({
        url: 'https://api.yuanyuangao.com/v1/auth/wechat-login',
        method: 'POST',
        data: {
          code: res.code
        },
        success(loginRes) {
          // 登录成功，获取 JWT
          const token = loginRes.data.access_token
          wx.setStorageSync('token', token)
        }
      })
    } else {
      console.log('登录失败！' + res.errMsg)
    }
  }
})
```

**其他登录 API**：

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.checkSession` | 检查登录态是否过期 | 1.0.0 |
| `wx.login` | 调用接口获取登录凭证 | 1.0.0 |

**手机号授权**：

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `button open-type="getPhoneNumber"` | 手机号快速验证 | 1.2.0 |
| `button open-type="getRealtimePhoneNumber"` | 手机号实时验证 | 2.24.4 |

> **注意**：从 2.21.2 起，`getPhoneNumber` 接口进行了安全升级，`bindgetphonenumber` 返回的信息中增加 `code` 参数，开发者拿到 `code` 后需调用微信后台接口换取手机号。

#### 5.8.2 支付

**wx.requestPayment**

> 基础库 1.0.0

发起微信支付。调用前需在小程序微信公众平台-功能-微信支付入口申请接入微信支付。

**Object 参数**：

| 属性 | 类型 | 默认值 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `timeStamp` | string | - | 是 | 时间戳（秒） |
| `nonceStr` | string | - | 是 | 随机字符串，长度为 32 个字符以下 |
| `package` | string | - | 是 | 统一下单接口返回的 prepay_id 参数值，提交格式如：prepay_id=*** |
| `signType` | string | MD5 | 否 | 签名算法（MD5/HMAC-SHA256/RSA） |
| `paySign` | string | - | 是 | 签名 |
| `success` | function | - | 否 | 接口调用成功的回调函数 |
| `fail` | function | - | 否 | 接口调用失败的回调函数 |
| `complete` | function | - | 否 | 接口调用结束的回调函数 |

**signType 合法值**：

- `MD5`：仅在 v2 版本接口适用
- `HMAC-SHA256`：仅在 v2 版本接口适用
- `RSA`：仅在 v3 版本接口适用

**示例代码**：

```javascript
wx.requestPayment({
  timeStamp: '1718600000',
  nonceStr: '5K8264ILTKCH16CQ2502SI8ZNMTM67VS',
  package: 'prepay_id=wx201...',
  signType: 'RSA',
  paySign: 'oR9d8PuhnIc+Y...',
  success(res) {
    console.log('支付成功', res)
  },
  fail(err) {
    console.error('支付失败', err)
  }
})
```

**使用云开发的支付**：

```javascript
wx.cloud.callFunction({
  name: 'pay',
  data: { /* ... */ },
  success: res => {
    const payment = res.result.payment
    wx.requestPayment({
      ...payment,
      success: console.log,
      fail: console.error
    })
  }
})
```

#### 5.8.3 分享

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `button open-type="share"` | 触发用户转发 | 1.2.0 |
| `Page.onShareAppMessage` | 用户点击右上角转发按钮时触发 | 1.0.0 |
| `Page.onShareTimeline` | 用户点击右上角分享到朋友圈时触发 | 1.4.0 |
| `wx.showShareMenu` | 显示分享按钮 | 1.0.0 |
| `wx.hideShareMenu` | 隐藏分享按钮 | 1.0.0 |
| `wx.updateAppMessageShareData` | 更新应用分享信息 | 1.2.0 |
| `wx.updateTimelineShareData` | 更新应用分享到朋友圈信息 | 1.4.0 |
| `wx.getShareInfo` | 获取转发详细信息 | 1.1.0 |

#### 5.8.4 订阅消息

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.requestSubscribeMessage` | 调起客户端小程序订阅消息界面 | 2.4.4 |
| `wx.requestSubscribeDeviceMessage` | 订阅设备消息 | 2.13.0 |
| `wx.requestLiveActivity` | 拉起一次性订阅消息界面（liveActivity） | 2.26.2 |

#### 5.8.5 用户信息与隐私

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.getUserProfile` | 获取用户信息 | 2.10.4 |
| `wx.getUserInfo` | 获取用户信息（旧版接口） | 1.0.0 |
| `wx.chooseMedia` | 拍摄或从手机相册中选择图片或视频 | 2.10.0 |
| `wx.chooseImage` | 从本地相册选择图片或拍照 | 1.0.0 |
| `button open-type="chooseAvatar"` | 获取用户头像 | 2.21.2 |
| `wx.getPrivacySetting` | 查询小程序隐私协议 | 2.32.3 |
| `wx.onNeedPrivacyAuthorization` | 监听需要用户授权隐私协议 | 2.32.3 |
| `wx.openPrivacyContract` | 跳转至微信隐私协议页面 | 2.32.3 |
| `wx.requirePrivacyAuthorize` | 模拟隐私协议授权 | 2.32.3 |

#### 5.8.6 客服与意见反馈

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `button open-type="contact"` | 打开客服会话 | 1.1.0 |
| `button open-type="feedback"` | 打开意见反馈页面 | 2.1.0 |
| `wx.openCustomerServiceChat` | 打开微信客服（半屏） | 3.2.1 |

#### 5.8.7 微信卡券 / 小店

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.openCard` | 打开小程序内的微信卡券 | 1.0.0 |
| `wx.addCard` | 批量添加卡券 | 1.0.0 |
| `wx.openStoreCouponDetail` | 打开微信小店优惠券详情 | 2.31.0 |
| `wx.openStoreHome` | 打开微信小店首页 | 2.31.0 |
| `wx.openStoreProduct` | 打开微信小店商品 | 2.31.0 |
| `wx.openStoreOrder` | 打开微信小店订单 | 2.31.0 |

#### 5.8.8 跳转其他小程序 / App

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.navigateToMiniProgram` | 打开另一个小程序 | 1.3.0 |
| `wx.navigateBackMiniProgram` | 返回到上一个小程序 | 1.3.0 |
| `wx.exitMiniProgram` | 退出小程序 | 2.1.0 |
| `navigator target="miniProgram"` | 通过组件打开其他小程序 | 2.0.7 |
| `button open-type="launchApp"` | 打开 APP | 1.9.5 |

#### 5.8.9 数据上报与监测

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.reportMonitor` | 自定义业务数据监控上报 | 2.0.1 |
| `wx.reportAnalytics` | 自定义分析数据上报 | 2.13.0 |
| `wx.reportPerformance` | 小程序测速上报 | 2.13.0 |
| `wx.getExptInfo` | 获取实验信息 | 2.17.0 |
| `wx.reportEvent` | 上报事件 | 3.7.5 |

### 5.9 分包加载与预下载 API

#### 5.9.1 分包配置

小程序支持分包加载，将代码分成多个包，按需加载。

**app.json 配置**：

```json
{
  "subpackages": [
    {
      "root": "packageA",
      "name": "A",
      "pages": [
        "pages/cat/cat",
        "pages/dog/dog"
      ],
      "independent": false
    }
  ],
  "preloadRule": {
    "pages": ["pages/index/index"],
    "packages": ["A"]
  }
}
```

**分包预下载规则**：

```json
{
  "preloadRule": {
    "pages": ["pages/index/index"],
    "network": "all",
    "packages": ["important"]
  }
}
```

#### 5.9.2 分包 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.preDownloadSubpackage` | 触发分包预下载 | 2.17.0 |
| `PreDownloadSubpackageTask` | 预下载分包任务实例 | 2.17.0 |

**示例**：

```javascript
wx.preDownloadSubpackage({
  name: 'A',
  success(res) {
    console.log('分包预下载成功', res)
  }
})
```

**分包限制**：

- 整个小程序所有分包大小不超过 **30MB**（主包 + 分包）
- 单个分包/主包大小不能超过 **2MB**
- 主包用于放置默认页面和公共资源

### 5.10 加密 API

| API | 说明 | 最低版本 |
| --- | --- | --- |
| `wx.getUserCryptoManager` | 获取用户加密模块 | 2.17.0 |
| `UserCryptoManager` | 用户加密模块 | 2.17.0 |
| `UserCryptoManager.getLatestUserKey` | 获取最新的用户加密密钥 | 2.17.0 |
| `UserCryptoManager.getRandomValues` | 获取密码学安全随机数 | 2.17.0 |

**使用示例**：

```javascript
const crypto = wx.getUserCryptoManager()

// 获取用户加密密钥
crypto.getLatestUserKey({
  success(res) {
    const { encryptKey, iv, signature } = res
    // 使用 encryptKey 加密数据
  }
})

// 获取密码学安全随机数
const randomValues = new Uint8Array(16)
crypto.getRandomValues({
  data: randomValues
})
```

---

## 第 6 章 兼容性说明

### 6.1 兼容性策略总览

小程序的功能不断增强，但旧版本的微信客户端并不支持新功能，所以在使用这些新能力时需要做兼容。

**主要兼容策略**：

1. **版本号比较**：获取当前基础库版本号，与所需最低版本号比较
2. **API 存在判断**：通过 `if (wx.xxx)` 判断 API 是否存在
3. **wx.canIUse**：检查 API、回调、参数、组件等是否在当前基础库版本可用
4. **最低基础库版本设置**：在小程序管理后台设置最低基础库版本

### 6.2 版本号比较规范

微信客户端和小程序基础库的版本号风格为 `Major.Minor.Patch`（主版本号.次版本号.修订版本号）。

**正确的版本号比较函数**：

```javascript
function compareVersion(v1, v2) {
  v1 = v1.split('.')
  v2 = v2.split('.')
  const len = Math.max(v1.length, v2.length)
  
  while (v1.length < len) {
    v1.push('0')
  }
  while (v2.length < len) {
    v2.push('0')
  }
  
  for (let i = 0; i < len; i++) {
    const num1 = parseInt(v1[i])
    const num2 = parseInt(v2[i])
    if (num1 > num2) {
      return 1
    } else if (num1 < num2) {
      return -1
    }
  }
  return 0
}

// 使用示例
const version = wx.getAppBaseInfo().SDKVersion
if (compareVersion(version, '1.1.0') >= 0) {
  // 支持的特性
} else {
  wx.showModal({
    title: '提示',
    content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
  })
}
```

> **注意**：不可以直接使用字符串比较的方法进行版本号比较。例如 `'2.29.1' > '2.3.0'` 是 `false` 的。

### 6.3 API 存在判断与 wx.canIUse

#### 6.3.1 API 存在判断

对于新增的 API，可以通过判断该 API 是否存在来判断是否支持用户使用的基础库版本。

```javascript
if (wx.openBluetoothAdapter) {
  wx.openBluetoothAdapter()
} else {
  wx.showModal({
    title: '提示',
    content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
  })
}
```

#### 6.3.2 wx.canIUse

通过 `wx.canIUse` 来判断是否可以在该基础库版本下直接使用。

**API 参数或返回值**：

```javascript
wx.showModal({
  success: function(res) {
    if (wx.canIUse('showModal.success.cancel')) {
      console.log(res.cancel)
    }
  }
})
```

**组件**：

```javascript
Page({
  data: {
    canIUse: wx.canIUse('cover-view')
  }
})
```

```xml
<video controls="{{!canIUse}}">
  <cover-view wx:if="{{canIUse}}">play</cover-view>
</video>
```

> canIUse 的数据文件随基础库进行更新，新版本中的新功能可能出现遗漏的情况，建议开发者在使用时提前测试。

### 6.4 最低基础库版本设置

> 需要 iOS 6.5.8 / 安卓 6.5.7 及以上版本微信客户端支持

为便于开发者解决低版本基础库无法兼容小程序的新功能的问题，开发者可设置小程序最低基础库版本要求。

**设置方式**：

1. 登录小程序管理后台
2. 进入「设置 - 基本设置 - 基础库最低版本设置」
3. 在配置前，可查看近 30 天内访问当前小程序的用户所使用的基础库版本占比
4. 设置后，若用户基础库版本低于设置值，则无法正常打开小程序，并提示用户更新客户端版本

### 6.5 Android 与 iOS 平台差异

虽然小程序大部分 API 行为在 Android 和 iOS 上保持一致，但仍存在一些平台差异，需要特别关注。

#### 6.5.1 系统信息差异

| 属性 | Android | iOS |
| --- | --- | --- |
| `platform` | `android` | `ios` |
| `system` | Android 14、Android 13 等 | iOS 17.0、iOS 18.0 等 |
| `benchmarkLevel` | 设备性能等级（-2/0/-1/1+） | 不返回 |
| `abi` | 设备 abi（armeabi-v7a / arm64-v8a） | 不返回 |
| `safeArea` | 顶部状态栏 + 底部导航栏 | 顶部刘海屏 + 底部 Home Indicator |
| `verticalAccuracy` | 始终返回 0 | 实际垂直精度 |
| `locationReducedAccuracy` | 不支持 | true / false |

#### 6.5.2 媒体 API 差异

**音频播放（InnerAudioContext）**：

- iOS 26.2 上有 InnerAudioContext 播放 mp3 异常问题
- 鸿蒙手机微信小程序 InnerAudioContext 播放网络音频可能导致闪退
- iOS 端音频后台播放受到更多限制

**视频（video）**：

- iOS 端默认禁止视频自动播放（需用户交互后）
- Android 端部分浏览器内核在小程序 webview 中对视频编解码支持不同
- iOS 上 video 组件的 `enable-progress-gesture` 默认行为与 Android 略有不同

**图片（image）**：

- Android 端对 webP 格式的支持更原生
- iOS 端部分老旧 iOS 系统的 webP 解码可能失败
- `mode="top/bottom/left/right/center/..."` 仅 WebView 渲染引擎支持

#### 6.5.3 网络 API 差异

| 特性 | Android | iOS |
| --- | --- | --- |
| `useHighPerformanceMode` 默认值 | `true`（基础库 3.5.0+） | `false` |
| HttpDNS | 支持 | 支持 |
| QUIC | gQUIC-Q43（v8.0.54 前） / h3（v8.0.54+） | gQUIC-Q43 |
| HTTP/2 | 支持 | 支持 |
| `enableProfile` | 支持 | 支持 |
| 强制蜂窝网络 `forceCellularNetwork` | 支持 | 支持 |

#### 6.5.4 位置 API 差异

- iOS 上 `wx.getLocation` 高精度定位耗时更长
- iOS 14+ 要求精确位置授权，否则只能返回模糊位置
- Android 12+ 需要前台服务才能持续定位

#### 6.5.5 蓝牙 API 差异

- iOS 上 BLE 广播包格式与 Android 不同
- Android 上 `notifyBLECharacteristicValueChange` 需要 MTU 协商
- iOS 上后台蓝牙连接受限

#### 6.5.6 UI 行为差异

- iOS 端 `input` 的 `cursor-spacing` 在不同系统版本表现不同
- iOS 端 `scroll-view` 的弹性滚动（bounces）需要开启 enhanced 属性
- Android 端 `cover-view` 在原生组件上的渲染有部分限制

### 6.6 鸿蒙 OS 平台支持

**鸿蒙 OS 支持情况**：

| 客户端 | 支持情况 |
| --- | --- |
| HarmonyOS 手机端微信 | ✅ 支持（platform: `ohos`） |
| HarmonyOS PC 微信 | ✅ 支持（platform: `ohos_pc`） |

**鸿蒙 OS 上的兼容性提示**：

- `getLocation` 在鸿蒙 OS 上可能需要单独的权限申请
- `InnerAudioContext` 在鸿蒙 OS 上播放网络音频可能导致闪退
- `setStorageSync` 在纯血鸿蒙系统中有异常问题
- 部分原生组件在鸿蒙 OS 上的同层渲染行为可能与 Android 不同
- 鸿蒙 OS 暂不支持 `enhanced` 及其相关的属性和方法（scroll-view）

**鸿蒙适配建议**：

- 关键路径加 try-catch 兜底
- 通过 `wx.getSystemInfoSync().platform` 判断鸿蒙系统后做特定处理
- 持续关注微信官方对鸿蒙 OS 的支持更新

### 6.7 各组件 API 兼容性矩阵

#### 6.7.1 组件基础库要求

| 组件 | 最低基础库 | 备注 |
| --- | --- | --- |
| view, scroll-view, swiper, swiper-item | 1.0.0 | - |
| text, image, button, input, textarea, icon, progress | 1.0.0 | - |
| form, radio, radio-group, checkbox, checkbox-group | 1.0.0 | - |
| switch, slider, picker, label | 1.0.0 | - |
| navigator | 1.0.0 | - |
| audio, video, camera, map, canvas | 1.0.0 | - |
| web-view, open-data | 1.0.0 | - |
| movable-view, movable-area | 1.2.0 | - |
| cover-view, cover-image | 1.0.0 | - |
| rich-text | 1.0.0 | - |
| functional-page-navigator | 2.1.0 | 仅插件 |
| live-player, live-pusher | 1.7.0 | - |
| editor | 2.7.0 | - |
| ad | 2.10.0 | - |
| page-container | 2.13.0 | - |
| ad-custom, channel-live, channel-video | 2.21.2 | - |
| keyboard-accessory | 2.13.0 | - |
| match-media | 2.11.0 | - |
| grid-view, list-view, sticky-header, sticky-section | 2.25.0+ | Skyline |
| snapshot, open-container | 2.27.0+ | Skyline |
| list-builder, grid-builder | 2.29.0+ | Skyline |
| root-portal | 2.32.1 | - |
| nested-scroll-body, nested-scroll-header | 3.0.0+ | Skyline |
| span, selection | 3.7.0+ | - |
| editor-portal | 3.6.0+ | - |

#### 6.7.2 平台能力支持矩阵

| 能力 | iOS | Android | 鸿蒙 OS | Windows | macOS |
| --- | --- | --- | --- | --- | --- |
| wx.login | ✅ | ✅ | ✅ | ✅ | ✅ |
| wx.checkSession | ✅ | ✅ | ✅ | ✅ | ✅ |
| wx.getUserInfo | ✅ | ✅ | ✅ | ✅ | ✅ |
| wx.getUserProfile | ✅ | ✅ | ✅ | ✅ | ✅ |
| wx.requestPayment | ✅ | ✅ | ✅ | ✅ | ✅ |
| wx.chooseMedia | ✅ | ✅ | ✅ | ✅ | ✅ |
| wx.scanCode | ✅ | ✅ | ✅ | ✅ | ✅ |
| wx.getLocation | ✅ | ✅ | ✅ | ✅ | ✅ |
| wx.startLocationUpdate | ✅ | ✅ | ✅ | ❌ | ❌ |
| wx.requestSubscribeMessage | ✅ | ✅ | ✅ | ❌ | ❌ |
| wx.openBluetoothAdapter | ✅ | ✅ | ✅ | ❌ | ❌ |
| wx.startWifi | ✅ | ✅ | ✅ | ❌ | ❌ |
| wx.startHCE | ✅（部分支持） | ✅ | ❌ | ❌ | ❌ |
| InnerAudioContext | ✅ | ✅ | ⚠️ 有问题 | ✅ | ✅ |
| video 组件 | ✅ | ✅ | ✅ | ✅ | ✅ |
| live-player/live-pusher | ✅ | ✅ | ✅ | ❌ | ❌ |
| map 组件 | ✅ | ✅ | ✅ | ✅ | ✅ |
| canvas 组件 | ✅ | ✅ | ✅ | ✅ | ✅ |
| web-view 组件 | ✅ | ✅ | ✅ | ✅ | ✅ |
| ad 广告 | ✅ | ✅ | ✅ | ❌ | ❌ |
| Skyline 渲染 | ✅ | ✅ | ✅ | 部分 | 部分 |
| 半屏小程序 | ✅ | ✅ | ✅ | ❌ | ❌ |
| 视频号组件 | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## 第 7 章 最佳实践

### 7.1 性能优化

#### 7.1.1 启动性能

**优化策略**：

1. **按需注入**：

```json
{
  "lazyCodeLoading": "requiredComponents"
}
```

2. **精简主包**：将非首屏使用的页面放入分包
3. **移除无用代码**：及时清理未使用的文件、组件、依赖
4. **预加载分包**：使用 `preloadRule` 预加载即将使用的分包
5. **避免启动时大量同步存储读取**：启动时尽量使用异步 API

#### 7.1.2 渲染性能

**setData 优化**：

```javascript
// 不推荐：频繁调用、数据量大
for (let i = 0; i < 100; i++) {
  this.setData({ [`list[${i}]`]: newData[i] })
}

// 推荐：合并更新
this.setData({ list: newData })
```

**长列表优化**：

- 单页数据控制在 100 条以内
- 使用 Skyline 渲染引擎 + list-view 组件实现虚拟列表
- WebView 渲染引擎下可使用 `recycle-view` 等方案

**图片优化**：

- 使用 CDN 图片，避免本地大图
- 启用 `lazy-load`（WebView）
- 优先使用 webP 格式
- 适当压缩图片大小
- 雪碧图 / 字体图标

**避免频繁事件触发**：

```javascript
// scroll 事件节流
let lastCall = 0
onScroll(e) {
  const now = Date.now()
  if (now - lastCall < 16) return // 60 FPS
  lastCall = now
  // 处理滚动
}
```

#### 7.1.3 运行性能

- 减少 setData 次数和数据量
- 避免在 JS 中执行大量同步逻辑
- 将复杂计算放到 `requestIdleCallback` 中执行
- 使用 WebAssembly 处理计算密集型任务

#### 7.1.4 网络性能

- 启用 `useHighPerformanceMode`（Android 端）
- 启用 `enableHttp2` 和 `enableQuic`
- 启用 `enableCache` 利用 HTTP 缓存
- 大文件使用分片上传
- 图片懒加载

### 7.2 包体积控制

**主包限制**：

- 主包大小 **≤ 2MB**
- 总包（主包 + 分包）≤ **30MB**

**优化策略**：

1. **图片资源压缩**：
   - 使用 webP 格式
   - 适当压缩 JPG/PNG
   - 大图采用渐进式加载

2. **代码优化**：
   - 移除 console.log
   - 删除未使用代码
   - 压缩 JavaScript 代码
   - 避免引入过大的第三方库

3. **分包加载**：
   - 将非首屏页面放入分包
   - 按业务域划分分包
   - 设置合理的 preloadRule

4. **资源懒加载**：
   - 图片 lazy-load
   - 组件 lazy-code-loading

### 7.3 网络请求最佳实践

#### 7.3.1 域名配置

- **必须使用 HTTPS**
- 在微信公众平台配置 request 合法域名
- 开发阶段可在开发者工具中勾选"不校验合法域名"

#### 7.3.2 并发控制

- 默认 10 个并发请求上限
- 使用请求队列控制并发数
- 合理使用 `Promise.all` / `Promise.allSettled`

#### 7.3.3 错误处理

```javascript
function request(options) {
  return new Promise((resolve, reject) => {
    wx.request({
      ...options,
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // 未登录，跳转登录
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

#### 7.3.4 请求频率限制

详见 [接口调用频率规范](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/api-frequency.html)：

- `wx.login`：每个小程序每天调用次数有限
- `wx.request`：默认 10 个并发，10s 内最多 100 次
- `wx.getLocation`：基础库 2.17.0 起增加调用频率限制
- `wx.requestSubscribeMessage`：每次触发需要用户手动确认

### 7.4 数据缓存策略

#### 7.4.1 使用原则

1. **不要把 storage 当全局变量用**：storage 应只用来进行数据的持久化存储
2. **避免启动时大量同步读取**：影响启动耗时
3. **异步优先**：尽量使用异步 API
4. **设置过期时间**：业务数据应有过期机制

#### 7.4.2 实践建议

```javascript
// 封装带过期时间的 storage
const Storage = {
  set(key, value, expire = 0) {
    const data = {
      value,
      expire: expire > 0 ? Date.now() + expire : 0
    }
    wx.setStorageSync(key, data)
  },
  
  get(key) {
    const data = wx.getStorageSync(key)
    if (!data) return null
    if (data.expire > 0 && Date.now() > data.expire) {
      wx.removeStorageSync(key)
      return null
    }
    return data.value
  }
}

// 使用
Storage.set('userInfo', userInfo, 24 * 60 * 60 * 1000) // 24小时过期
const userInfo = Storage.get('userInfo')
```

#### 7.4.3 敏感信息处理

- 密码、token 等敏感信息应加密存储
- 不要在 storage 中存储明文密码
- 注意 storage 中的数据可能在其他场景被读取

### 7.5 用户体验与可访问性

#### 7.5.1 加载体验

- 合理使用 loading 提示
- 避免空白页面，使用骨架屏
- 图片懒加载
- 关键路径预加载

#### 7.5.2 错误处理

- 网络异常：友好提示重试
- 接口错误：明确错误信息
- 表单校验：实时反馈
- 全局错误监听：

```javascript
// app.js
App({
  onError(err) {
    console.error('全局错误', err)
    // 上报错误
  },
  onUnhandledRejection(err) {
    console.error('未处理 Promise 错误', err)
    // 上报错误
  }
})
```

#### 7.5.3 可访问性

- 提供合适的 `aria-label`
- 支持屏幕阅读器
- 颜色对比度符合 WCAG 标准
- 支持键盘操作
- 详细的 [aria-component 文档](https://developers.weixin.qq.com/miniprogram/dev/component/aria-component.html)

### 7.6 安全建议

#### 7.6.1 网络安全

- 全部使用 HTTPS
- 后端接口做好鉴权
- 防止 SQL 注入、XSS
- 敏感数据加密传输

#### 7.6.2 客户端安全

- 不在客户端存储敏感信息
- 业务逻辑放在服务端
- 防调试、防反编译
- 重要操作二次验证

#### 7.6.3 隐私合规

- 在 `app.json` 中声明 `requiredPrivateInfos`
- 使用 `wx.getPrivacySetting` 检查隐私协议授权
- 使用 `wx.onNeedPrivacyAuthorization` 监听隐私协议授权
- 在涉及用户隐私的 API 调用前先获得用户同意

```javascript
// 隐私协议处理
if (wx.getPrivacySetting) {
  wx.getPrivacySetting({
    success(res) {
      if (res.needAuthorization) {
        // 需要用户授权
        wx.onNeedPrivacyAuthorization(res => {
          // 用户点击"同意"按钮
          wx.showModal({
            title: '用户隐私保护提示',
            content: '为了正常访问位置信息，请阅读并同意《用户隐私保护指引》',
            success(modalRes) {
              if (modalRes.confirm) {
                wx.openPrivacyContract({
                  success: () => {
                    res.resolve({ event: 'agree' })
                  }
                })
              } else {
                res.resolve({ event: 'disagree' })
              }
            }
          })
        })
      }
    }
  })
}
```

#### 7.6.4 登录安全

- 定期校验 session_key 有效性（`wx.checkSession`）
- 后端使用 `code` 兑换 `session_key`，避免在前端处理
- 关键操作进行二次验证

### 7.7 调试与日志

#### 7.7.1 调试工具

- **Console**：查看日志
- **Network**：查看网络请求
- **Storage**：查看 storage 数据
- **Wxml**：查看页面结构
- **Performance**：性能分析
- **Audits**：质量审计
- **Trace**：运行轨迹

#### 7.7.2 日志上报

```javascript
const logger = wx.getLogManager()

logger.info({ tag: 'login', msg: '用户登录' })
logger.warn({ tag: 'payment', msg: '支付警告' })
logger.error({ tag: 'api', msg: 'API 错误' })
```

#### 7.7.3 实时日志

```javascript
const realtimeLogger = wx.getRealtimeLogManager()
realtimeLogger.info('关键操作')
realtimeLogger.error('错误信息')
realtimeLogger.warn('警告信息')
```

### 7.8 鸿蒙与多端适配

#### 7.8.1 平台判断

```javascript
const { platform, system } = wx.getSystemInfoSync()

if (platform === 'ios') {
  // iOS 特定处理
} else if (platform === 'android') {
  // Android 特定处理
} else if (platform === 'ohos') {
  // 鸿蒙 OS 特定处理
}
```

#### 7.8.2 性能降级

```javascript
const { benchmarkLevel } = wx.getSystemInfoSync()

if (benchmarkLevel < 0) {
  // 低性能设备，降低动画复杂度
} else if (benchmarkLevel >= 5) {
  // 高性能设备，启用高级效果
}
```

#### 7.8.3 兼容性兜底

```javascript
// 关键 API 兼容性检查
if (wx.requestSubscribeMessage) {
  wx.requestSubscribeMessage({ /* ... */ })
} else {
  // 降级方案
  wx.showModal({
    title: '提示',
    content: '请升级微信到最新版本'
  })
}
```

---

## 附录 A：参考链接

### 官方文档

- [微信小程序开发文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [小程序组件参考](https://developers.weixin.qq.com/miniprogram/dev/component/)
- [小程序 API 参考](https://developers.weixin.qq.com/miniprogram/dev/api/)
- [小程序服务端 API](https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/)
- [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
- [微信开放社区](https://developers.weixin.qq.com/community/)
- [微信支付开发文档](https://pay.weixin.qq.com/doc/v3/partner/4012069852)

### 兼容性文档

- [基础库兼容性](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html)
- [接口调用频率规范](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/api-frequency.html)
- [网络使用说明](https://developers.weixin.qq.com/miniprogram/dev/framework/ability/network.html)
- [存储策略](https://developers.weixin.qq.com/miniprogram/dev/framework/ability/storage.html)
- [Errno 错误码](https://developers.weixin.qq.com/miniprogram/dev/framework/usability/PublicErrno.html)

### Skyline 渲染引擎

- [Skyline 介绍](https://developers.weixin.qq.com/miniprogram/dev/framework/runtime/skyline/introduction.html)
- [Skyline 迁移起步](https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/glass-easel/migration.html)

### 框架文档

- [Taro 文档](https://docs.taro.zone/)
- [uni-app 文档](https://uniapp.dcloud.net.cn/)
- [Taro UI 组件库](https://taro-ui.jd.com/)

### 隐私与合规

- [小程序隐私协议开发指南](https://developers.weixin.qq.com/miniprogram/dev/framework/user-privacy/PrivacyAuthorize.html)
- [小程序用户隐私保护规范](https://developers.weixin.qq.com/miniprogram/dev/framework/user-privacy/)

---

## 附录 B：术语表

| 术语 | 解释 |
| --- | --- |
| **MINA** | 微信官方小程序开发框架的总称 |
| **基础库** | 微信客户端内置的、提供小程序运行所需 API 和能力的库 |
| **AppID** | 小程序的唯一标识符，在微信公众平台申请 |
| **WXML** | 微信标记语言（WeiXin Markup Language），类似 HTML |
| **WXSS** | 微信样式表（WeiXin Style Sheet），类似 CSS，支持 rpx 单位 |
| **JS** | 小程序的逻辑层脚本语言 |
| **JSON** | 小程序的配置文件格式 |
| **rpx** | 响应式像素（responsive pixel），750rpx = 屏幕宽度 |
| **WXS** | 微信脚本语言（WeiXin Script），在 WXML 中使用的脚本 |
| **Component** | 小程序自定义组件 |
| **Page** | 小程序页面 |
| **App** | 小程序应用实例 |
| **WebView** | 小程序默认的渲染引擎 |
| **Skyline** | 微信新一代小程序渲染引擎 |
| **worklet** | Skyline 引擎下的动画脚本 |
| **openid** | 用户的唯一标识，同一用户在不同小程序中 openid 不同 |
| **unionid** | 同一用户在同一微信开放平台下所有应用的统一标识 |
| **session_key** | 微信小程序会话密钥，用于数据加解密 |
| **prepay_id** | 微信支付预支付会话标识 |
| **scope** | 微信权限作用域，如 scope.userLocation |
| **API 类别** | 微信 API 的分类标识（default / functional / sensitive） |

---

**END OF MINIPROGRAM DEV DOC**
