(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-3628040a"],{9262:function(e,n,t){"use strict";t.r(n);var a=function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("v-expansion-panels",e._l(e.items,(function(n,a){return t("v-expansion-panel",{key:a},[t("v-expansion-panel-header",[e._v(e._s(n.position))]),t("v-expansion-panel-content",[t("v-card-text",[t("p",[e._v(e._s(n.rank))]),t("p",{staticStyle:{"font-size":"120%"}},[e._v(e._s(n.name))])]),t("v-img",{staticStyle:{"margin-top":"-20px"},attrs:{src:n.image}})],1)],1)})),1)},i=[],s=(t("b64b"),{data:function(){return{items:[{name:"Ивановский Владимир Сергеевич",rank:"Генерал-лейтенант",position:'Начальник ВИТ "ЭРА',image:"/images/chieff/Vladimir_Ivanovsky.jpg",data:[]},{name:"Морозов Андрей Владимирович",rank:"Полковник",position:'Заместитель начальника ВИТ "ЭРА" по НОД',image:"",data:[]},{name:"Морозов Андрей Владимирович",rank:"Полковник",position:'Заместитель начальника ВИТ "ЭРА" по НОД',image:"",data:[]},{name:"Морозов Андрей Владимирович",rank:"Полковник",position:'Заместитель начальника ВИТ "ЭРА" по НОД',image:"",data:[]}]}},mounted:function(){this.$store.state.user&&0!=Object.keys(this.$store.state.user).length||this.$fire({title:"Уведомление",text:"Необходимо авторизоваться!",type:"error"}).then(this.$router.push("/howtouse")),document.title='Технополис "ЭРА" | Руководство',this.$emit("update:title","Руководство")}}),o=s,r=t("2877"),c=t("6544"),l=t.n(c),p=t("99d9"),d=t("cd55"),u=t("49e2"),h=t("c865"),v=t("0393"),m=t("adda"),x=Object(r["a"])(o,a,i,!1,null,null,null);n["default"]=x.exports;l()(x,{VCardText:p["b"],VExpansionPanel:d["a"],VExpansionPanelContent:u["a"],VExpansionPanelHeader:h["a"],VExpansionPanels:v["a"],VImg:m["a"]})},c865:function(e,n,t){"use strict";var a=t("5530"),i=t("0789"),s=t("9d26"),o=t("a9ad"),r=t("3206"),c=t("5607"),l=t("80d2"),p=t("58df"),d=Object(p["a"])(o["a"],Object(r["a"])("expansionPanel","v-expansion-panel-header","v-expansion-panel"));n["a"]=d.extend().extend({name:"v-expansion-panel-header",directives:{ripple:c["a"]},props:{disableIconRotate:Boolean,expandIcon:{type:String,default:"$expand"},hideActions:Boolean,ripple:{type:[Boolean,Object],default:!1}},data:function(){return{hasMousedown:!1}},computed:{classes:function(){return{"v-expansion-panel-header--active":this.isActive,"v-expansion-panel-header--mousedown":this.hasMousedown}},isActive:function(){return this.expansionPanel.isActive},isDisabled:function(){return this.expansionPanel.isDisabled},isReadonly:function(){return this.expansionPanel.isReadonly}},created:function(){this.expansionPanel.registerHeader(this)},beforeDestroy:function(){this.expansionPanel.unregisterHeader()},methods:{onClick:function(e){this.$emit("click",e)},genIcon:function(){var e=Object(l["l"])(this,"actions")||[this.$createElement(s["a"],this.expandIcon)];return this.$createElement(i["c"],[this.$createElement("div",{staticClass:"v-expansion-panel-header__icon",class:{"v-expansion-panel-header__icon--disable-rotate":this.disableIconRotate},directives:[{name:"show",value:!this.isDisabled}]},e)])}},render:function(e){var n=this;return e("button",this.setBackgroundColor(this.color,{staticClass:"v-expansion-panel-header",class:this.classes,attrs:{tabindex:this.isDisabled?-1:null,type:"button"},directives:[{name:"ripple",value:this.ripple}],on:Object(a["a"])(Object(a["a"])({},this.$listeners),{},{click:this.onClick,mousedown:function(){return n.hasMousedown=!0},mouseup:function(){return n.hasMousedown=!1}})}),[Object(l["l"])(this,"default",{open:this.isActive},!0),this.hideActions||this.genIcon()])}})}}]);
//# sourceMappingURL=chunk-3628040a.634b5cb4.js.map