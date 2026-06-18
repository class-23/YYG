"use strict";
(wx["webpackJsonp"]=wx["webpackJsonp"]||[]).push([[1820],{2035:function(e,s,a){
var n=a(2180),r=a(7294),l=a(2954),o=a.n(l),c=a(1515),t=a(9570),i=a(8970),d=a(5893),P="checkinPosterCanvas";
function m(){
  var e=o().getStorageSync("mom_english_latest_checkin_poster")||{};
  return{day:e.day||t.z7.day,theme:e.theme||t.z7.theme,quote:e.quote||t.z7.quote,meaning:e.insight||t.z7.meaning,copy:e.focus?"\u6211\u4eca\u5929\u63a8\u8fdb\u4e86\uff1a".concat(e.focus,"\u3002\u6bcf\u592910\u5206\u949f\uff0c\u5148\u628a\u8282\u594f\u7a33\u4e0b\u6765\u3002"):"\u6211\u4eca\u5929\u5b8c\u6210\u4e8610\u5206\u949f\u82f1\u8bed\u65e9\u64cd\u3002\u5988\u5988\u5148\u575a\u6301\uff0c\u5b69\u5b50\u624d\u76f8\u4fe1\u575a\u6301\u3002"}
}
function h(e,s,n,r,l,o){
  var c=e.measureText?e.measureText(s).width:s.length*l*.58;if(c<=o)return e.fillText(s,n,r),r+l;
  for(var t="",i=0,d=0;d<s.length;d++){var m=t+s[d],h=e.measureText?e.measureText(m).width:m.length*l*.58;if(h>o&&t){e.fillText(t,n,r),r+=l,i++,t=s[d]}else t=m}
  return t&&e.fillText(t,n,r),r+l
}
function p(e,s,n,r,l,o,c){
  e.beginPath(),e.moveTo(s+c,n),e.lineTo(s+l-c,n),e.quadraticCurveTo(s+l,n,s+l,n+c),e.lineTo(s+l,n+o-c),e.quadraticCurveTo(s+l,n+o,s+l-c,n+o),e.lineTo(s+c,n+o),e.quadraticCurveTo(s,n+o,s,n+o-c),e.lineTo(s,n+c),e.quadraticCurveTo(s,n,s+c,n),e.closePath()
}
function g(e,s){
  var a=o().createCanvasContext(P);
  a.setFillStyle("#fffaf6"),a.fillRect(0,0,600,900);
  a.setFillStyle("#ffffff"),p(a,42,40,516,820,30),a.fill();
  a.setFillStyle("#c2641a"),a.setFontSize(26),a.setTextAlign("left"),a.fillText("\u5b9d\u5988\u82f1\u8bed\u65e9\u64cd \xb7 Day ".concat(e.day),72,94);
  a.setFillStyle("#1a211d"),a.setFontSize(42),h(a,e.theme,72,154,50,456);
  a.setFillStyle("#fff2e4"),p(a,72,220,456,190,22),a.fill();
  a.setFillStyle("#1a211d"),a.setFontSize(42),h(a,e.quote,96,286,50,408);
  a.setFillStyle("#6f6259"),a.setFontSize(26);var n=h(a,e.meaning,72,470,38,456);
  a.setFillStyle("#f7eadb"),p(a,72,n+16,456,150,20),a.fill();
  a.setFillStyle("#5f5148"),a.setFontSize(25),h(a,e.copy,96,n+62,36,408);
  a.setFillStyle("#ffffff"),p(a,72,708,150,150,18),a.fill();
  a.setStrokeStyle("#f0b36e"),a.setLineWidth(3),p(a,72,708,150,150,18),a.stroke();
  a.setFillStyle("#c2641a"),a.setFontSize(26),a.setTextAlign("center"),a.fillText("\u5c0f\u7a0b\u5e8f\u7801",147,790);
  a.setTextAlign("left"),a.setFillStyle("#7d6d63"),a.setFontSize(24),a.fillText("\u6bcf\u592910\u5206\u949f",252,748),a.setFillStyle("#1a211d"),a.setFontSize(30),h(a,"\u5148\u7a33\u4f4f\u81ea\u5df1\uff0c\u518d\u966a\u5b69\u5b50\u5f80\u524d\u8d70\u3002",252,795,38,260);
  a.draw(!1,function(){
    setTimeout(function(){
      o().canvasToTempFilePath({canvasId:P,width:600,height:900,destWidth:1200,destHeight:1800,success:function(e){s(e.tempFilePath)},fail:function(){o().hideLoading(),(0,i.A)("\u6d77\u62a5\u751f\u6210\u5931\u8d25\uff0c\u8bf7\u91cd\u8bd5")}})
    },120)
  })
}
function y(e){
  o().showLoading({title:"\u6b63\u5728\u751f\u6210"});
  g(e,function(e){
    o().saveImageToPhotosAlbum({filePath:e,success:function(){o().hideLoading(),(0,i.A)("\u5df2\u4fdd\u5b58\u5230\u76f8\u518c")},fail:function(e){o().hideLoading();var s=(null===e||void 0===e?void 0:e.errMsg)||"";s.indexOf("auth")>-1?o().showModal({title:"\u9700\u8981\u76f8\u518c\u6743\u9650",content:"\u8bf7\u5141\u8bb8\u4fdd\u5b58\u5230\u76f8\u518c\uff0c\u624d\u80fd\u751f\u6210\u670b\u53cb\u5708\u6d77\u62a5\u3002",confirmText:"\u53bb\u8bbe\u7f6e",success:function(e){e.confirm&&o().openSetting({})}}):(0,i.A)("\u4fdd\u5b58\u5931\u8d25\uff0c\u8bf7\u91cd\u8bd5")}})
  })
}
function x(){
  var e=(0,r.useState)(m()),s=e[0],a=e[1],n=(0,l.useRouter)(),R=(0,r.useRef)(!1);
  (0,l.useDidShow)(function(){var e=m();a(e),"1"===(null===n||void 0===n?void 0:n.params.autoSave)&&!R.current&&(R.current=!0,setTimeout(function(){return y(e)},300))});
  return(0,d.jsxs)(c.G7,{className:"page poster-page",children:[
    (0,d.jsx)(c.xv,{className:"eyebrow",children:"Poster"}),
    (0,d.jsx)(c.G7,{className:"h1",children:"\u751f\u6210\u4eca\u65e5\u670b\u53cb\u5708\u5361\u7247"}),
    (0,d.jsx)(c.G7,{className:"muted intro",children:"\u8fd9\u5f20\u5361\u7247\u4f1a\u4f18\u5148\u4f7f\u7528\u4f60\u521a\u521a\u5199\u4e0b\u7684\u6253\u5361\u53cd\u9988\uff0c\u5e76\u751f\u6210\u53ef\u4fdd\u5b58\u7684\u670b\u53cb\u5708\u56fe\u7247\u3002"}),
    (0,d.jsxs)(c.G7,{className:"poster warm-card",children:[
      (0,d.jsxs)(c.G7,{className:"poster-top",children:["\u5b9d\u5988\u82f1\u8bed\u65e9\u64cd \xb7 Day ",s.day]}),
      (0,d.jsx)(c.G7,{className:"poster-theme",children:s.theme}),
      (0,d.jsx)(c.G7,{className:"poster-quote",children:s.quote}),
      (0,d.jsx)(c.G7,{className:"poster-meaning",children:s.meaning}),
      (0,d.jsx)(c.G7,{className:"poster-copy",children:s.copy}),
      (0,d.jsx)(c.G7,{className:"qr",children:"\u5c0f\u7a0b\u5e8f\u7801"})
    ]}),
    (0,d.jsx)("canvas",{"canvas-id":P,canvasId:P,className:"poster-canvas",style:"width:600px;height:900px;"}),
    (0,d.jsx)(c.zx,{className:"btn btn-primary",onClick:function(){return y(s)},children:"\u751f\u6210\u5e76\u4fdd\u5b58\u670b\u53cb\u5708\u6d77\u62a5"})
  ]})
}
var u={navigationBarTitleText:"\u670b\u53cb\u5708\u6d77\u62a5"};Page((0,n.createPageConfig)(x,"pages/poster/index",{root:{cn:[]}},u||{}))
}},function(e){var s=function(s){return e(e.s=s)};e.O(0,[2107,1216,8592],function(){return s(2035)});e.O()}]);
