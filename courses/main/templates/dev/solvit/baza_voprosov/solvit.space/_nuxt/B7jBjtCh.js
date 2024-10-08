import{aP as p,aZ as r,b0 as c,ae as b,o as i,a as s,h as u,aN as o,a4 as g,ar as f,f as h,n as m,D as y,aX as v}from"./BSpKbMoe.js";var B=`
@layer primevue {
    .p-togglebutton {
        position: relative;
        display: inline-flex;
        user-select: none;
        vertical-align: bottom;
    }

    .p-togglebutton-input {
        cursor: pointer;
    }

    .p-togglebutton .p-button {
        flex: 1 1 auto;
    }
}
`,S={root:function(t){var a=t.instance,l=t.props;return["p-togglebutton p-component",{"p-disabled":l.disabled,"p-highlight":a.active}]},input:"p-togglebutton-input",box:function(t){var a=t.instance;return["p-button p-component",{"p-button-icon-only":a.hasIcon&&!a.hasLabel}]},icon:function(t){var a=t.instance,l=t.props;return["p-button-icon",{"p-button-icon-left":l.iconPos==="left"&&a.label,"p-button-icon-right":l.iconPos==="right"&&a.label}]},label:"p-button-label"},I=p.extend({name:"togglebutton",css:B,classes:S}),L={name:"BaseToggleButton",extends:v,props:{modelValue:Boolean,onIcon:String,offIcon:String,onLabel:{type:String,default:"Yes"},offLabel:{type:String,default:"No"},iconPos:{type:String,default:"left"},disabled:{type:Boolean,default:!1},readonly:{type:Boolean,default:!1},tabindex:{type:Number,default:null},inputId:{type:String,default:null},inputClass:{type:[String,Object],default:null},inputStyle:{type:Object,default:null},ariaLabelledby:{type:String,default:null},ariaLabel:{type:String,default:null}},style:I,provide:function(){return{$parentInstance:this}}},P={name:"ToggleButton",extends:L,emits:["update:modelValue","change","focus","blur"],methods:{getPTOptions:function(t){return this.ptm(t,{context:{active:this.active,disabled:this.disabled}})},onChange:function(t){!this.disabled&&!this.readonly&&(this.$emit("update:modelValue",!this.modelValue),this.$emit("change",t))},onFocus:function(t){this.$emit("focus",t)},onBlur:function(t){this.$emit("blur",t)}},computed:{active:function(){return this.modelValue===!0},hasLabel:function(){return r.isNotEmpty(this.onLabel)&&r.isNotEmpty(this.offLabel)},hasIcon:function(){return this.$slots.icon||this.onIcon&&this.offIcon},label:function(){return this.hasLabel?this.modelValue?this.onLabel:this.offLabel:"&nbsp;"}},directives:{ripple:c}},V=["data-p-highlight","data-p-disabled"],O=["id","value","checked","tabindex","disabled","readonly","aria-labelledby","aria-label"];function T(e,t,a,l,C,n){var d=b("ripple");return i(),s("div",o({class:e.cx("root")},n.getPTOptions("root"),{"data-pc-name":"togglebutton","data-p-highlight":n.active,"data-p-disabled":e.disabled}),[u("input",o({id:e.inputId,type:"checkbox",role:"switch",class:[e.cx("input"),e.inputClass],style:e.inputStyle,value:e.modelValue,checked:n.active,tabindex:e.tabindex,disabled:e.disabled,readonly:e.readonly,"aria-labelledby":e.ariaLabelledby,"aria-label":e.ariaLabel,onFocus:t[0]||(t[0]=function(){return n.onFocus&&n.onFocus.apply(n,arguments)}),onBlur:t[1]||(t[1]=function(){return n.onBlur&&n.onBlur.apply(n,arguments)}),onChange:t[2]||(t[2]=function(){return n.onChange&&n.onChange.apply(n,arguments)})},n.getPTOptions("input")),null,16,O),g((i(),s("div",o({class:e.cx("box")},n.getPTOptions("box")),[f(e.$slots,"icon",{value:e.modelValue,class:m(e.cx("icon"))},function(){return[e.onIcon||e.offIcon?(i(),s("span",o({key:0,class:[e.cx("icon"),e.modelValue?e.onIcon:e.offIcon]},n.getPTOptions("icon")),null,16)):h("",!0)]}),u("span",o({class:e.cx("label")},n.getPTOptions("label")),y(n.label),17)],16)),[[d]])],16,V)}P.render=T;export{P as default};
