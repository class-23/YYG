"use strict";
(wx["webpackJsonp"]=wx["webpackJsonp"]||[]).push([[1582],{6707:function(e,s,n){
var t=n(2180),o=n(7294),R=n(2954),a=n.n(R),l=n(1515),i=n(8970),c=n(5893);
var gradeOptions=["小学低年级（1-3年级）","小学高年级（4-6年级）","初中（7-9年级）"];
var questions=[
  {key:"studyStatus",title:"孩子目前英语状态",options:["刚开始接触 / 兴趣阶段","学过但效果一般","能做题但不稳定"]},
  {key:"understanding",title:"孩子是否需要家长翻译英语句子？",options:["经常需要","偶尔需要","基本不需要"]},
  {key:"resistance",title:"孩子学习英语主要问题",options:["抗拒学习","学了记不住","会但不稳定"]}
];
var emptyAnswers={studyStatus:"",understanding:"",resistance:""};
function shortGrade(e){return e.indexOf("低年级")>-1?"小学低":e.indexOf("高年级")>-1?"小学高":"初中"}
function unique(e){return e.filter(function(s,n){return e.indexOf(s)===n})}
function getLevel(e){
  var s=0;
  "刚开始接触 / 兴趣阶段"===e.studyStatus?s+=0:"学过但效果一般"===e.studyStatus?s+=1:s+=2;
  "经常需要"===e.understanding?s+=0:"偶尔需要"===e.understanding?s+=1:s+=2;
  "抗拒学习"===e.resistance?s+=0:"学了记不住"===e.resistance?s+=1:s+=2;
  return s<=2?"E1":s<=4?"E2":"E3"
}
function getInsight(e){
  var s=[];
  ("刚开始接触 / 兴趣阶段"===e.studyStatus||"经常需要"===e.understanding)&&s.push("词汇不足");
  ("经常需要"===e.understanding||"偶尔需要"===e.understanding)&&s.push("理解困难");
  ("抗拒学习"===e.resistance||"学了记不住"===e.resistance||"会但不稳定"===e.resistance)&&s.push("学习习惯缺失");
  return unique(s).slice(0,3)
}
function buildResult(e,s){
  var n=getLevel(s),t=getInsight(s);
  return {
    englishLevel:n,
    gradeGroup:shortGrade(e),
    coreInsight:t,
    recommendedPlan:"21d_plan",
    primaryPath:"21天习惯建立计划",
    backupPath:"100天成长计划",
    hookText:"孩子的问题不是不会，而是没有进入正确学习路径",
    ctaText:"优先建议：先做21天习惯建立"
  }
}
function updateUserProfile(e){
  var s="mom_english_child_profile",n=a().getStorageSync(s)||{};
  a().setStorageSync(s,Object.assign({},n,{
    hasDoneAssessment:!0,
    childGrade:e.gradeGroup,
    englishLevel:e.englishLevel,
    coreInsight:e.coreInsight,
    updatedAt:(new Date).toISOString()
  }))
}
function go(e){a().navigateTo({url:e})}
function jumpToDay1(){a().switchTab({url:"/pages/daily/index"})}
function savePaidPlan(e){a().setStorageSync("mom_english_pending_paid_plan",{plan:e,status:"paid",paidAt:(new Date).toISOString(),nextPath:"/pages/daily/index"})}
function P(){
  var e=(0,o.useState)(1),s=e[0],n=e[1],t=(0,o.useState)(""),r=t[0],P=t[1],d=(0,o.useState)(emptyAnswers),u=d[0],x=d[1],m=(0,o.useState)(null),h=m[0],g=m[1],p=(0,o.useState)(!1),f=p[0],v=p[1],q=(0,o.useState)(""),L=q[0],O=q[1],w=(0,o.useState)(Date.now()),j=w[0],b=function(e,s){x(Object.assign({},u,(function(e,s){var n={};return n[e]=s,n})(e,s)))},y=function(){if(!r)return(0,i.A)("先选择孩子所在年级"),!1;return!0},k=function(){if(!y())return;var e=questions.every(function(e){return u[e.key]});if(!e)return(0,i.A)("完成3个问题后就能生成路径"),!1;return!0},N=function(){if(!y())return;n(2),a().pageScrollTo({scrollTop:0,duration:200})},S=function(){if(!k())return;var e=buildResult(r,u);g(e),updateUserProfile(e),n(3),a().pageScrollTo({scrollTop:0,duration:200})},T=function(){n(1),P(""),x(emptyAnswers),g(null),v(!1),O(""),w(Date.now())},E=function(){v(!0)},M=function(e){O(e),a().setStorageSync("mom_english_pending_paid_plan",{plan:e,status:"pending",createdAt:(new Date).toISOString(),nextPath:"/pages/daily/index"}),(0,i.A)("支付完成后将进入第1天打卡"),setTimeout(function(){savePaidPlan(e),O(""),(0,i.A)("支付成功，进入第1天"),setTimeout(jumpToDay1,500)},700)},G=function(){M("21d_plan")},C=function(){M("100d_plan")},D=function(){go("/pages/sister-poster/index?from=assessment&inviteCode=YYG2026")},B=function(){v(!1);go("/pages/signup/index?id=trial7")};
  (0,R.useUnload)(function(){Date.now()-j<8e3&&!h&&v(!0)});
  (0,R.useDidHide)(function(){Date.now()-j<8e3&&!h&&v(!0)});
  return (0,c.jsxs)(l.G7,{className:"page kid-growth-page v8-page",children:[
    (0,c.jsxs)(l.G7,{className:"v8-hero warm-card",children:[
      (0,c.jsx)(l.xv,{className:"eyebrow",children:"Path Check"}),
      (0,c.jsx)(l.G7,{className:"h1",children:"1分钟英语学习路径识别"}),
      (0,c.jsx)(l.G7,{className:"hero-sub",children:"不做长阅读题，只用3个问题判断孩子英语水平 E1 / E2 / E3，并直接给出下一步学习路径。"}),
      (0,c.jsxs)(l.G7,{className:"v8-goal",children:[
        (0,c.jsx)(l.xv,{children:"英语水平分层"}),
        (0,c.jsx)(l.xv,{children:"学习阻力识别"}),
        (0,c.jsx)(l.xv,{children:"21天优先推荐"})
      ]}),
      (0,c.jsx)(l.G7,{className:"step-strip",children:[1,2,3].map(function(e){return(0,c.jsx)(l.G7,{className:"step-dot ".concat(s>=e?"is-active":""),children:"0"+e},e)})})
    ]}),
    1===s?(0,c.jsxs)(l.G7,{className:"v8-card card",children:[
      (0,c.jsx)(l.xv,{className:"eyebrow",children:"Step 1"}),
      (0,c.jsx)(l.G7,{className:"h2",children:"先选孩子所在阶段"}),
      (0,c.jsx)(l.G7,{className:"section-copy",children:"年级只用于判断路径难度，不再进入复杂分层阅读题。"}),
      (0,c.jsx)(l.G7,{className:"option-list",children:gradeOptions.map(function(e){return(0,c.jsx)(l.G7,{className:"option-pill ".concat(r===e?"is-selected":""),onClick:function(){return P(e)},children:e},e)})}),
      (0,c.jsx)(l.zx,{className:"btn btn-primary submit-btn",onClick:N,children:"开始3题识别"}),
      (0,c.jsx)(l.zx,{className:"btn btn-link",onClick:E,children:"先不测，看看体验"})
    ]}):null,
    2===s?(0,c.jsxs)(l.G7,{className:"v8-card card",children:[
      (0,c.jsx)(l.xv,{className:"eyebrow",children:"Step 2"}),
      (0,c.jsx)(l.G7,{className:"h2",children:"完成3个问题"}),
      (0,c.jsx)(l.G7,{className:"section-copy",children:"选最接近孩子真实状态的一项，系统会生成 E1 / E2 / E3 分层结果。"}),
      questions.map(function(e,s){return(0,c.jsxs)(l.G7,{className:"question-block",children:[
        (0,c.jsxs)(l.G7,{className:"field-title",children:[s+1,". ",e.title]}),
        (0,c.jsx)(l.G7,{className:"option-list",children:e.options.map(function(s,n){return(0,c.jsxs)(l.G7,{className:"option-card ".concat(u[e.key]===s?"is-selected":""),onClick:function(){return b(e.key,s)},children:[
          (0,c.jsx)(l.xv,{children:["A","B","C"][n]}),
          (0,c.jsx)(l.G7,{children:s})
        ]},s)})})
      ]},e.key)}),
      (0,c.jsxs)(l.G7,{className:"action-row",children:[
        (0,c.jsx)(l.zx,{className:"btn btn-ghost",onClick:function(){return n(1)},children:"返回"}),
        (0,c.jsx)(l.zx,{className:"btn btn-primary",onClick:S,children:"生成学习路径"})
      ]})
    ]}):null,
    3===s&&h?(0,c.jsxs)(l.G7,{className:"result-card warm-card",children:[
      (0,c.jsx)(l.xv,{className:"eyebrow",children:"Result"}),
      (0,c.jsxs)(l.G7,{className:"level-row",children:[
        (0,c.jsx)(l.G7,{className:"level-badge",children:h.englishLevel}),
        (0,c.jsxs)(l.G7,{children:[
          (0,c.jsx)(l.G7,{className:"h2",children:"孩子当前路径判断"}),
          (0,c.jsx)(l.G7,{className:"result-copy",children:h.hookText})
        ]})
      ]}),
      (0,c.jsxs)(l.G7,{className:"result-grid",children:[
        (0,c.jsxs)(l.G7,{className:"result-item",children:[(0,c.jsx)(l.xv,{children:"年级阶段"}),(0,c.jsx)(l.G7,{children:h.gradeGroup})]}),
        (0,c.jsxs)(l.G7,{className:"result-item",children:[(0,c.jsx)(l.xv,{children:"推荐路径"}),(0,c.jsx)(l.G7,{children:h.primaryPath})]})
      ]}),
      (0,c.jsxs)(l.G7,{className:"result-block",children:[
        (0,c.jsx)(l.xv,{children:"核心阻力"}),
        (0,c.jsx)(l.G7,{className:"keyword-list",children:h.coreInsight.map(function(e){return(0,c.jsx)(l.xv,{children:e},e)})})
      ]}),
      (0,c.jsx)(l.G7,{className:"hook-card",children:h.ctaText}),
      (0,c.jsxs)(l.G7,{className:"plan-card primary-plan",children:[
        (0,c.jsx)(l.xv,{className:"plan-tag",children:"主推荐"}),
        (0,c.jsx)(l.G7,{className:"plan-title",children:"21天习惯建立计划"}),
        (0,c.jsx)(l.G7,{className:"plan-copy",children:"每天10分钟，先帮孩子把英语学习节奏稳下来。\n先愿意开始，再慢慢学会坚持。"}),
        (0,c.jsxs)(l.G7,{className:"plan-actions",children:[
          (0,c.jsx)(l.zx,{className:"btn btn-primary",onClick:G,children:"支付99元并进入Day1"}),
          (0,c.jsx)(l.zx,{className:"btn btn-ghost",onClick:D,children:"邀请三个姐妹同行"})
        ]})
      ]}),
      (0,c.jsxs)(l.G7,{className:"plan-card",children:[
        (0,c.jsx)(l.xv,{className:"plan-tag",children:"升级路径"}),
        (0,c.jsx)(l.G7,{className:"plan-title",children:"100天成长计划"}),
        (0,c.jsx)(l.G7,{className:"plan-copy",children:"198元成长系统，适合已经完成基础习惯后继续拉长训练周期。支付完成后同样从第1天打卡开始。"}),
        (0,c.jsx)(l.zx,{className:"btn btn-ghost",onClick:C,children:"支付198元并进入Day1"})
      ]}),
      (0,c.jsxs)(l.G7,{className:"action-row",children:[
        (0,c.jsx)(l.zx,{className:"btn btn-ghost",onClick:T,children:"重新测评"}),
        (0,c.jsx)(l.zx,{className:"btn btn-link",onClick:E,children:"暂时退出"})
      ]})
    ]}):null,
    f?(0,c.jsx)(l.G7,{className:"retention-mask",children:(0,c.jsxs)(l.G7,{className:"retention-popup",children:[
      (0,c.jsx)(l.xv,{className:"eyebrow",children:"7天挽留体验"}),
      (0,c.jsx)(l.G7,{className:"h2",children:"先免费体验7天"}),
      (0,c.jsx)(l.G7,{className:"result-copy",children:"还没准备好进入21天也没关系。先用7天看看孩子真实学习状态，再决定要不要继续。"}),
      (0,c.jsx)(l.zx,{className:"btn btn-primary",onClick:B,children:"7天免费体验"}),
      (0,c.jsx)(l.zx,{className:"btn btn-ghost",onClick:function(){return v(!1)},children:"继续留在测评页"})
    ]})}):null
    ,L?(0,c.jsx)(l.G7,{className:"payment-mask",children:(0,c.jsxs)(l.G7,{className:"payment-popup",children:[
      (0,c.jsx)(l.xv,{className:"eyebrow",children:"Payment"}),
      (0,c.jsx)(l.G7,{className:"h2",children:"支付确认中"}),
      (0,c.jsx)(l.G7,{className:"result-copy",children:"支付成功后，会自动进入第1天英语早操打卡内容。"})
    ]})}):null
  ]})
}
var d={navigationBarTitleText:"英语路径识别"};
Page((0,t.createPageConfig)(P,"pages/kid-growth-assessment/kid-growth-assessment",{root:{cn:[]}},d||{}))
}},function(e){var s=function(s){return e(e.s=s)};e.O(0,[2107,1216,8592],function(){return s(6707)});e.O()}]);
