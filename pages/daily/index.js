"use strict";
(wx["webpackJsonp"]=wx["webpackJsonp"]||[]).push([[6673],{6518:function(e,s,n){
var a=n(2180),c=n(1413),t=n(9439),i=n(7294),r=n(1515),l=n(2954),o=n.n(l),d=n(9570),u=n(8970),m=n(3433),x=n(8145),h="mom_english_checkin_records";
function j(){return(0,x.s)()}
function p(){return o().getStorageSync(h)||[]}
function f(e){return o().setStorageSync(h,e),e}
function N(){return{id:"daily-main-".concat(j()),date:j(),title:"Day ".concat(d.z7.day," \u82f1\u8bed\u65e9\u64cd"),description:d.z7.task,category:"daily_main",source:"daily",completed:!1}}
function G(e){return e||{date:j(),tasks:[N()],mainCheckinCompleted:!1,reflection:"",completedAt:""}}
function g(){var e=p(),s=e.find(function(e){return e.date===j()});return G(s)}
function v(e){var s=p(),n=G(e),a=s.some(function(e){return e.date===n.date}),c=a?s.map(function(e){return e.date===n.date?n:e}):[n].concat((0,m.Z)(s));return f(c),n}
function k(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"",s=g();if(s.mainCheckinCompleted)return s;var n=(0,c.Z)((0,c.Z)({},s),{},{mainCheckinCompleted:!0,reflection:e,completedAt:(new Date).toISOString(),tasks:s.tasks.map(function(e){return"daily"===e.source?(0,c.Z)((0,c.Z)({},e),{},{completed:!0,completedAt:(new Date).toISOString()}):e})});return v(n)}
function y(e){var s=g(),n=(0,c.Z)((0,c.Z)({},s),{},{tasks:s.tasks.map(function(s){return s.id===e?(0,c.Z)((0,c.Z)({},s),{},{completed:!0,completedAt:(new Date).toISOString()}):s})});return v(n)}
function L(e){
  var s=(e||"").replace(/\s+/g," ").trim(),n=s||"\u4eca\u5929\u613f\u610f\u5f00\u59cb",a=(n.split(/[，。,.、；;！!？?]/).filter(Boolean)[0]||n).trim();
  a=a.length>18?a.slice(0,18)+"...":a;
  return{focus:a,insight:s?"\u4f60\u4eca\u5929\u5199\u4e0b\u7684\u91cd\u70b9\u662f\u300c".concat(a,"\u300d\u3002\u628a\u5b83\u8bf4\u51fa\u6765\uff0c\u884c\u52a8\u5c31\u6709\u4e86\u65b9\u5411\u3002"):"\u4f60\u4eca\u5929\u5b8c\u6210\u4e8610\u5206\u949f\u82f1\u8bed\u65e9\u64cd\u3002\u5148\u5b8c\u6210\u4e00\u6b21\uff0c\u8282\u594f\u5c31\u5f00\u59cb\u56de\u6765\u3002",quote:s?"\u628a\u300c".concat(a,"\u300d\u5f80\u524d\u63a8\u4e00\u70b9\uff0c\u4eca\u5929\u5c31\u6ca1\u6709\u767d\u8d70\u3002"):"\u613f\u610f\u5f00\u59cb\uff0c\u5c31\u662f\u4eca\u5929\u6700\u4eae\u7684\u8fdb\u6b65\u3002"}
}
var z=n(5678),S=n(9646),b=n(5893);
function C(){
  var e=(0,i.useState)(g()),s=(0,t.Z)(e,2),n=s[0],a=s[1],
    m=(0,i.useState)(""),x=(0,t.Z)(m,2),h=x[0],j=x[1],
    p=(0,i.useState)((0,S.um)()),f=(0,t.Z)(p,2),N=f[0],G=f[1],
    C=(0,i.useState)(!1),w=(0,t.Z)(C,2),Z=w[0],A=w[1],
    D=(0,i.useState)(0),I=(0,t.Z)(D,2),O=I[0],T=I[1],
    _=(0,i.useState)("00:00"),E=(0,t.Z)(_,2),P=E[0],q=E[1],
    V=(0,i.useState)(null),X=(0,t.Z)(V,2),Y=X[0],K=X[1],
    J=(0,i.useRef)(null);
  (0,i.useEffect)(function(){if(d.z7.audioSrc){var e=o().createInnerAudioContext();return e.src=d.z7.audioSrc,J.current=e,e.onTimeUpdate(function(){var s=e.duration||0,n=e.currentTime||0;T(s?n/s*100:0);var a=String(Math.floor(n/60)).padStart(2,"0"),c=String(Math.floor(n%60)).padStart(2,"0");q("".concat(a,":").concat(c))}),e.onEnded(function(){A(!1),T(100)}),function(){e.destroy(),J.current=null}}},[]);
  (0,l.useDidShow)(function(){var e=g();a(e),j(e.reflection||""),G((0,S.um)())});
  var Q=n.tasks.filter(function(e){return"policy_impact"===e.source}),B=N.team,F=(null===B||void 0===B?void 0:B.members.filter(function(e){return e.todayChecked}).length)||0,
    R=function(){
      n.mainCheckinCompleted||(0,z.n7)();
      var e=k(h),s=L(h);
      o().setStorageSync("mom_english_latest_checkin_poster",(0,c.Z)((0,c.Z)({},s),{},{day:d.z7.day,theme:d.z7.theme,createdAt:(new Date).toISOString()}));
      a(e),K(s),(0,u.A)("\u4eca\u65e5\u6253\u5361\u6210\u529f")
    },
    U=function(e){a(y(e)),(0,u.A)("\u4efb\u52a1\u5df2\u5b8c\u6210")},
    H=function(){if(d.z7.audioSrc&&J.current){if(Z)return J.current.pause(),void A(!1);J.current.play(),A(!0)}else(0,u.A)("\u4eca\u65e5\u97f3\u9891\u5f85\u66f4\u65b0")},
    ee=function(){Y&&o().setStorageSync("mom_english_latest_checkin_poster",(0,c.Z)((0,c.Z)({},Y),{},{day:d.z7.day,theme:d.z7.theme,createdAt:(new Date).toISOString()})),K(null),(0,u.go)("/pages/poster/index?from=daily&autoSave=1")},
    se=function(){K(null),(0,u.go)("/pages/sister-poster/index?from=daily&inviteCode=YYG2026")};
  return(0,b.jsxs)(r.G7,{className:"page daily-page",children:[
    (0,b.jsxs)(r.G7,{className:"today-card warm-card",children:[
      (0,b.jsxs)(r.xv,{className:"eyebrow",children:["Day ",d.z7.day]}),
      (0,b.jsx)(r.G7,{className:"h1",children:d.z7.theme}),
      (0,b.jsx)(r.G7,{className:"muted",children:"\u4eca\u5929\u53ea\u9700\u898110\u5206\u949f\u3002\u522b\u7b49\u5b69\u5b50\u81ea\u5f8b\uff0c\u5988\u5988\u5148\u505a\u7ed9\u5b69\u5b50\u770b\u3002"})
    ]}),
    (0,b.jsxs)(r.G7,{className:"lesson-card card",children:[
      d.z7.coverImage?(0,b.jsx)(r.Ee,{className:"lesson-cover",src:d.z7.coverImage,mode:"widthFix"}):null,
      (0,b.jsxs)(r.G7,{className:"audio-player-card",children:[
        (0,b.jsxs)(r.G7,{className:"audio-player-top",children:[
          (0,b.jsxs)(r.G7,{children:[
            (0,b.jsx)(r.xv,{children:"\u82f1\u8bed\u65e9\u64cd"}),
            (0,b.jsx)(r.G7,{children:d.z7.audioTitle}),
            (0,b.jsx)(r.G7,{className:"audio-subtitle",children:d.z7.audioSubtitle})
          ]}),
          (0,b.jsx)(r.zx,{className:"mini-btn",onClick:H,children:Z?"\u6682\u505c":"\u64ad\u653e"})
        ]}),
        (0,b.jsx)(r.G7,{className:"audio-progress-track",children:(0,b.jsx)(r.G7,{className:"audio-progress-fill",style:{width:"".concat(O,"%")}})}),
        (0,b.jsxs)(r.G7,{className:"audio-meta-row",children:[(0,b.jsx)(r.xv,{children:P}),(0,b.jsx)(r.xv,{children:d.z7.audioDuration})]}),
        (0,b.jsx)(r.G7,{className:"audio-tip",children:d.z7.audioSrc?"\u8fd9\u4e00\u671f\u5df2\u63a5\u5165\u771f\u5b9e\u97f3\u9891\u6587\u4ef6\uff0c\u540e\u7eed\u6bcf\u5929\u53ea\u8981\u66ff\u6362\u5bf9\u5e94 day \u7684\u7d20\u6750\u5373\u53ef\u3002":"\u5f53\u524d\u672a\u63a5\u5165\u4eca\u65e5\u97f3\u9891\u6587\u4ef6\uff0c\u540e\u7eed\u63d0\u4f9b\u97f3\u9891\u5730\u5740\u540e\u53ef\u76f4\u63a5\u64ad\u653e\u3002"})
      ]}),
      (0,b.jsxs)(r.G7,{className:"quote-box",children:[
        (0,b.jsx)(r.xv,{children:"\u4eca\u65e5\u91d1\u53e5"}),
        (0,b.jsx)(r.G7,{children:d.z7.quote}),
        (0,b.jsx)(r.xv,{className:"meaning",children:d.z7.meaning})
      ]}),
      (0,b.jsx)(r.G7,{className:"copy",children:d.z7.copy})
    ]}),
    (0,b.jsxs)(r.G7,{className:"task-card card",children:[
      (0,b.jsx)(r.G7,{className:"h2",children:"\u4eca\u65e5\u62c6\u89e3"}),
      (0,b.jsxs)(r.G7,{className:"lesson-section",children:[(0,b.jsx)(r.xv,{className:"lesson-section-title",children:"\u53d1\u97f3\u91cd\u70b9"}),d.z7.pronunciation.map(function(e){return(0,b.jsx)(r.G7,{className:"lesson-bullet",children:e},e)})]}),
      (0,b.jsxs)(r.G7,{className:"lesson-section",children:[(0,b.jsx)(r.xv,{className:"lesson-section-title",children:"\u53e3\u8bed\u4f8b\u53e5"}),d.z7.speakingExamples.map(function(e){return(0,b.jsxs)(r.G7,{className:"lesson-example",children:[(0,b.jsx)(r.xv,{children:e.en}),(0,b.jsx)(r.G7,{children:e.zh})]},e.en)})]}),
      (0,b.jsxs)(r.G7,{className:"lesson-section",children:[(0,b.jsx)(r.xv,{className:"lesson-section-title",children:"\u8868\u8fbe\u7406\u89e3"}),d.z7.definitionNotes.map(function(e){return(0,b.jsx)(r.G7,{className:"lesson-bullet",children:e},e)})]}),
      (0,b.jsxs)(r.G7,{className:"lesson-section",children:[(0,b.jsx)(r.xv,{className:"lesson-section-title",children:"\u77ed\u8bed\u63d0\u70bc"}),d.z7.takeaways.map(function(e){return(0,b.jsx)(r.G7,{className:"lesson-bullet",children:e},e)})]}),
      (0,b.jsxs)(r.G7,{className:"lesson-section",children:[(0,b.jsx)(r.xv,{className:"lesson-section-title",children:"\u7ffb\u8bd1\u7ec3\u4e60"}),d.z7.translationPractice.map(function(e){return(0,b.jsx)(r.G7,{className:"lesson-bullet",children:e},e)})]})
    ]}),
    (0,b.jsxs)(r.G7,{className:"task-card card",children:[
      (0,b.jsx)(r.G7,{className:"h2",children:"\u4eca\u65e5\u6253\u5361\u4efb\u52a1"}),
      (0,b.jsx)(r.G7,{className:"muted",children:d.z7.task}),
      (0,b.jsx)(r.gx,{className:"reflection",value:h,onInput:function(e){var s=e.detail.value;j(s),v((0,c.Z)((0,c.Z)({},n),{},{reflection:s}))},placeholder:"\u5199\u4e0b\u4eca\u5929\u6700\u60f3\u6539\u53d8\u7684\u4e00\u4ef6\u4e8b..."}),
      (0,b.jsx)(r.G7,{className:"encouragement",children:d.z7.encouragement}),
      (0,b.jsx)(r.zx,{className:"btn btn-primary",onClick:R,children:"\u4eca\u65e5\u5df2\u5b8c\u6210"})
    ]}),
    Q.length?(0,b.jsxs)(r.G7,{className:"task-card card",children:[
      (0,b.jsx)(r.G7,{className:"h2",children:"\u653f\u7b56\u5173\u8054\u4efb\u52a1"}),
      (0,b.jsx)(r.G7,{className:"muted",children:"\u8fd9\u4e9b\u4efb\u52a1\u6765\u81ea\u4f60\u5df2\u89e3\u9501\u7684\u653f\u7b56\u5f71\u54cd\u5206\u6790\uff0c\u4f1a\u540c\u6b65\u8fdb\u5165\u672c\u5468\u6253\u5361\u8282\u594f\u3002"}),
      (0,b.jsx)(r.G7,{className:"policy-task-list",children:Q.map(function(e){return(0,b.jsxs)(r.G7,{className:"policy-task-item",children:[(0,b.jsxs)(r.xv,{children:["\u653f\u7b56\u5173\u8054\u4efb\u52a1\uff5c",e.title]}),(0,b.jsx)(r.G7,{children:e.description}),(0,b.jsx)(r.zx,{className:"mini-action",onClick:function(){return U(e.id)},children:e.completed?"\u5df2\u5b8c\u6210":"\u5b8c\u6210\u4efb\u52a1"})]},e.id)})})
    ]}):null,
    B?(0,b.jsxs)(r.G7,{className:"task-card card",children:[
      (0,b.jsx)(r.G7,{className:"h2",children:"\u59d0\u59b9\u540c\u884c\u63d0\u9192"}),
      (0,b.jsxs)(r.G7,{className:"muted",children:["\u4eca\u65e5\u5c0f\u961f\u6253\u5361 ",F,"/",B.members.length]}),
      (0,b.jsx)(r.G7,{className:"policy-task-list",children:(0,b.jsxs)(r.G7,{className:"policy-task-item",children:[(0,b.jsx)(r.xv,{children:"\u63d0\u9192\u59d0\u59b9\u6253\u5361"}),(0,b.jsx)(r.G7,{children:"\u628a\u4eca\u5929\u7684\u5c0f\u8fdb\u5ea6\u4e5f\u5206\u4eab\u7ed9\u961f\u53cb\uff0c\u4e00\u8d77\u628a\u8282\u594f\u7a33\u4f4f\u3002"})]})}),
      (0,b.jsx)(r.zx,{className:"btn btn-ghost",onClick:function(){return(0,u.go)("/pages/sister-growth/index")},children:"\u53bb\u59d0\u59b9\u5c0f\u961f"})
    ]}):null,
    Y?(0,b.jsx)(r.G7,{className:"poster-mask",children:(0,b.jsxs)(r.G7,{className:"checkin-poster",children:[
      (0,b.jsx)(r.zx,{className:"poster-close",onClick:function(){return K(null)},children:"\xd7"}),
      (0,b.jsx)(r.xv,{className:"poster-eyebrow",children:"\u4eca\u65e5\u6253\u5361\u6d77\u62a5"}),
      (0,b.jsxs)(r.G7,{className:"poster-title",children:["Day ",d.z7.day," \xb7 ",d.z7.theme]}),
      (0,b.jsxs)(r.G7,{className:"poster-focus",children:[(0,b.jsx)(r.xv,{children:"\u6211\u4eca\u5929\u63a8\u8fdb\u4e86"}),(0,b.jsx)(r.G7,{children:Y.focus})]}),
      (0,b.jsx)(r.G7,{className:"poster-insight",children:Y.insight}),
      (0,b.jsx)(r.G7,{className:"poster-quote",children:Y.quote}),
      (0,b.jsxs)(r.G7,{className:"poster-actions",children:[
        (0,b.jsx)(r.zx,{className:"btn btn-primary",onClick:ee,children:"\u53d1\u670b\u53cb\u5708"}),
        (0,b.jsx)(r.zx,{className:"btn btn-ghost",onClick:se,children:"\u9080\u8bf7\u59d0\u59b9"})
      ]})
    ]})}):null
  ]})
}
var W={navigationBarTitleText:"\u4eca\u65e5\u6253\u5361"};Page((0,a.createPageConfig)(C,"pages/daily/index",{root:{cn:[]}},W||{}))
}},function(e){var s=function(s){return e(e.s=s)};e.O(0,[2107,1216,8592],function(){return s(6518)});e.O()}]);
