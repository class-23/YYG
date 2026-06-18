"use strict";
(wx["webpackJsonp"]=wx["webpackJsonp"]||[]).push([[1311],{7280:function(s,e,r){
var a=r(2180),R=r(7294),T=r(2954),w=r.n(T),c=r(1515),n=r(8970),l=r.p+"assets/yuanyuangao-portrait.jpg",x=r(9570),g=r(5678),i=r(5893);
function getHomeLesson(){
  var s=(0,g.uE)(),e=Math.max(1,Number(s.checkinDays||0)+1);
  return{day:e,quote:x.z7.quote,theme:x.z7.theme,checkinDays:Number(s.checkinDays||0)}
}
function o(){
  var s=(0,R.useState)(getHomeLesson()),e=s[0],r=s[1];
  (0,T.useDidShow)(function(){r(getHomeLesson())});
  var openDaily=function(){
    w().setStorageSync("mom_english_selected_lesson_day",e.day);
    w().setStorageSync("mom_english_selected_lesson_source","home_listen_card");
    w().setStorageSync("mom_english_current_lesson_snapshot",{day:e.day,quote:e.quote,theme:e.theme,from:"home",updatedAt:(new Date).toISOString()});
    (0,n.n)("/pages/daily/index")
  };
  return(0,i.jsxs)(c.G7,{className:"page home-page",children:[
    (0,i.jsxs)(c.G7,{className:"intro-hero",children:[
      (0,i.jsx)(c.Ee,{className:"hero-portrait",src:l,mode:"aspectFill"}),
      (0,i.jsxs)(c.G7,{className:"hero-content",children:[
        (0,i.jsx)(c.xv,{className:"eyebrow",children:"\u539f\u539f\u9ad8 \xb7 English Morning"}),
        (0,i.jsx)(c.G7,{className:"h1",children:"\u5988\u5988\u5148\u5f00\u53e3\uff0c\u5b69\u5b50\u624d\u6562\u5f80\u524d\u8d70"}),
        (0,i.jsx)(c.G7,{className:"hero-copy",children:"\u6bcf\u592910\u5206\u949f\uff0c\u966a\u5b69\u5b50\u8f7b\u677e\u5f00\u53e3\u3002"}),
        (0,i.jsxs)(c.G7,{className:"hero-proof",children:[
          (0,i.jsx)(c.xv,{children:"200\u4e07\u7c89\u4e1d"}),
          (0,i.jsx)(c.xv,{children:"\u96c5\u601d8\u5206"}),
          (0,i.jsx)(c.xv,{children:"\u6559\u5b6610\u5e74"})
        ]})
      ]})
    ]}),
    (0,i.jsxs)(c.G7,{className:"module-section",children:[
      (0,i.jsxs)(c.G7,{className:"module-card card module-mom",onClick:function(){return(0,n.go)("/pages/mom-growth-plan/mom-growth-plan")},children:[
        (0,i.jsxs)(c.G7,{children:[
          (0,i.jsx)(c.xv,{className:"eyebrow",children:"Her Growth"}),
          (0,i.jsx)(c.G7,{className:"module-title",children:"\u5988\u5988\u4e5f\u8981\u53d1\u5149"}),
          (0,i.jsx)(c.G7,{className:"module-copy",children:"\u4e0d\u662f\u4e3a\u4e86\u6210\u4e3a\u5b8c\u7f8e\u5988\u5988\uff0c\u800c\u662f\u91cd\u65b0\u6210\u4e3a\u81ea\u5df1\u3002"})
        ]}),
        (0,i.jsx)(c.zx,{className:"btn btn-primary",children:"\u70b9\u4eae\u81ea\u5df1"})
      ]}),
      (0,i.jsxs)(c.G7,{className:"module-card card module-child",onClick:function(){return(0,n.go)("/pages/growth/index")},children:[
        (0,i.jsxs)(c.G7,{children:[
          (0,i.jsx)(c.xv,{className:"eyebrow",children:"Kid Path"}),
          (0,i.jsx)(c.G7,{className:"module-title",children:"\u770b\u89c1\u5b69\u5b50\u7684\u8def"}),
          (0,i.jsx)(c.G7,{className:"module-copy",children:"\u4ece\u5361\u70b9\u5230\u7a81\u7834\uff0c\u627e\u5230\u9002\u5408\u5b69\u5b50\u7684\u82f1\u8bed\u6210\u957f\u8def\u5f84\u3002"})
        ]}),
        (0,i.jsx)(c.zx,{className:"btn btn-primary",children:"\u70b9\u4eae\u5b9d\u8d1d"})
      ]})
    ]}),
    (0,i.jsxs)(c.G7,{className:"sister-entry",onClick:function(){return(0,n.n)("/pages/transformation-square/index")},children:[
      (0,i.jsxs)(c.G7,{className:"sister-entry-avatars",children:[
        (0,i.jsx)(c.xv,{children:"\u59d0"}),
        (0,i.jsx)(c.xv,{children:"\u4f34"}),
        (0,i.jsx)(c.xv,{children:"\u9047"})
      ]}),
      (0,i.jsxs)(c.G7,{className:"sister-entry-copy",children:[
        (0,i.jsx)(c.xv,{className:"eyebrow",children:"Grow Together"}),
        (0,i.jsx)(c.G7,{className:"sister-entry-title",children:"\u8715\u53d8\u5e7f\u573a"}),
        (0,i.jsx)(c.G7,{children:"\u59d0\u59b9\u540c\u884c\u3001\u540c\u9891\u8fde\u63a5\uff0c\u90fd\u5728\u8fd9\u91cc\u3002"})
      ]}),
      (0,i.jsx)(c.xv,{className:"sister-entry-arrow",children:"\u203a"})
    ]}),
    (0,i.jsxs)(c.G7,{className:"listen-card",onClick:openDaily,children:[
      (0,i.jsxs)(c.G7,{className:"player-top",children:[
        (0,i.jsx)(c.xv,{}),
        (0,i.jsxs)(c.G7,{children:["\u82f1\u8bed\u65e9\u64cd \xb7 Day ",e.day]})
      ]}),
      (0,i.jsx)(c.G7,{className:"quote",children:e.quote}),
      (0,i.jsxs)(c.G7,{className:"waveform",children:[
        (0,i.jsx)(c.xv,{}),(0,i.jsx)(c.xv,{}),(0,i.jsx)(c.xv,{}),(0,i.jsx)(c.xv,{}),(0,i.jsx)(c.xv,{}),
        (0,i.jsx)(c.xv,{}),(0,i.jsx)(c.xv,{}),(0,i.jsx)(c.xv,{}),(0,i.jsx)(c.xv,{}),(0,i.jsx)(c.xv,{})
      ]}),
      (0,i.jsxs)(c.G7,{className:"listen-hint",children:["\u8fdb\u5165\u7b2c ",e.day,"\u5929\u6253\u5361\u5185\u5bb9"]})
    ]})
  ]})
}
var t={navigationBarTitleText:"\u5b9d\u5988\u82f1\u8bed\u65e9\u64cd"};Page((0,a.createPageConfig)(o,"pages/home/index",{root:{cn:[]}},t||{}))
}},function(s){var e=function(e){return s(s.s=e)};s.O(0,[2107,1216,8592],function(){return e(7280)});s.O()}]);
