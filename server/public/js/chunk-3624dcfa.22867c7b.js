(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-3624dcfa"],{2469:function(e,n,a){"use strict";a.r(n);var t=function(){var e=this,n=e.$createElement,a=e._self._c||n;return a("v-container",[a("v-expansion-panels",{attrs:{disabled:e.disabled,multiple:"",flat:"",tile:""},model:{value:e.panel,callback:function(n){e.panel=n},expression:"panel"}},[a("v-expansion-panel",[a("v-expansion-panel-header",[e._v("Как войти в систему?")]),a("v-expansion-panel-content",[e._v(" Чтобы войти в систему необходимо отсканировать QR код с оборотной стороны бэйджа "),a("v-row",{staticStyle:{"margin-top":"10px"},attrs:{align:"center",justify:"center"}},[a("v-img",{attrs:{"max-width":"200",src:"https://pro-markirovku.ru/wp-content/uploads/2019/12/pro-markirovku-290.png"}})],1)],1)],1),a("v-expansion-panel",[a("v-expansion-panel-header",[e._v("Что такое АИСС?")]),a("v-expansion-panel-content",[e._v(" Чтобы войти в систему необходимо отсканировать QR код с оборотной стороны бэйджа ")])],1),a("v-expansion-panel",[a("v-expansion-panel-header",[e._v("Что такое технополис")]),a("v-expansion-panel-content",[e._v(" Чтобы войти в систему необходимо отсканировать QR код с оборотной стороны бэйджа ")])],1)],1)],1)},i=[],s={data:function(){return{panel:[0],disabled:!1}},mounted:function(){document.title='Технополис "ЭРА" | Информация',this.$emit("update:title","Информация")}},o=s,l=a("2877"),r=a("6544"),c=a.n(r),p=a("a523"),d=a("cd55"),u=a("49e2"),h=a("c865"),v=a("0393"),x=a("adda"),f=a("0fd9"),b=Object(l["a"])(o,t,i,!1,null,null,null);n["default"]=b.exports;c()(b,{VContainer:p["a"],VExpansionPanel:d["a"],VExpansionPanelContent:u["a"],VExpansionPanelHeader:h["a"],VExpansionPanels:v["a"],VImg:x["a"],VRow:f["a"]})},c865:function(e,n,a){"use strict";var t=a("5530"),i=a("0789"),s=a("9d26"),o=a("a9ad"),l=a("3206"),r=a("5607"),c=a("80d2"),p=a("58df"),d=Object(p["a"])(o["a"],Object(l["a"])("expansionPanel","v-expansion-panel-header","v-expansion-panel"));n["a"]=d.extend().extend({name:"v-expansion-panel-header",directives:{ripple:r["a"]},props:{disableIconRotate:Boolean,expandIcon:{type:String,default:"$expand"},hideActions:Boolean,ripple:{type:[Boolean,Object],default:!1}},data:function(){return{hasMousedown:!1}},computed:{classes:function(){return{"v-expansion-panel-header--active":this.isActive,"v-expansion-panel-header--mousedown":this.hasMousedown}},isActive:function(){return this.expansionPanel.isActive},isDisabled:function(){return this.expansionPanel.isDisabled},isReadonly:function(){return this.expansionPanel.isReadonly}},created:function(){this.expansionPanel.registerHeader(this)},beforeDestroy:function(){this.expansionPanel.unregisterHeader()},methods:{onClick:function(e){this.$emit("click",e)},genIcon:function(){var e=Object(c["l"])(this,"actions")||[this.$createElement(s["a"],this.expandIcon)];return this.$createElement(i["c"],[this.$createElement("div",{staticClass:"v-expansion-panel-header__icon",class:{"v-expansion-panel-header__icon--disable-rotate":this.disableIconRotate},directives:[{name:"show",value:!this.isDisabled}]},e)])}},render:function(e){var n=this;return e("button",this.setBackgroundColor(this.color,{staticClass:"v-expansion-panel-header",class:this.classes,attrs:{tabindex:this.isDisabled?-1:null,type:"button"},directives:[{name:"ripple",value:this.ripple}],on:Object(t["a"])(Object(t["a"])({},this.$listeners),{},{click:this.onClick,mousedown:function(){return n.hasMousedown=!0},mouseup:function(){return n.hasMousedown=!1}})}),[Object(c["l"])(this,"default",{open:this.isActive},!0),this.hideActions||this.genIcon()])}})}}]);
//# sourceMappingURL=chunk-3624dcfa.22867c7b.js.map