import{aP as p,aZ as s,b2 as h,a7 as b,o as u,a as f,h as c,aN as l,ar as y,c as m,f as g,n as k,aX as v}from"./BSpKbMoe.js";var C=`
@layer primevue {
    .p-checkbox {
        position: relative;
        display: inline-flex;
        user-select: none;
        vertical-align: bottom;
    }

    .p-checkbox-input {
        cursor: pointer;
    }

    .p-checkbox-box {
        display: flex;
        justify-content: center;
        align-items: center;
    }
}
`,x={root:function(t){var n=t.instance,r=t.props;return["p-checkbox p-component",{"p-highlight":n.checked,"p-disabled":r.disabled}]},box:"p-checkbox-box",input:"p-checkbox-input",icon:"p-checkbox-icon"},S=p.extend({name:"checkbox",css:C,classes:x}),B={name:"BaseCheckbox",extends:v,props:{value:null,modelValue:null,binary:Boolean,name:{type:String,default:null},trueValue:{type:null,default:!0},falseValue:{type:null,default:!1},disabled:{type:Boolean,default:!1},readonly:{type:Boolean,default:!1},required:{type:Boolean,default:!1},tabindex:{type:Number,default:null},inputId:{type:String,default:null},inputClass:{type:[String,Object],default:null},inputStyle:{type:Object,default:null},ariaLabelledby:{type:String,default:null},ariaLabel:{type:String,default:null}},style:S,provide:function(){return{$parentInstance:this}}};function V(e){return T(e)||O(e)||I(e)||A()}function A(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function I(e,t){if(e){if(typeof e=="string")return i(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);if(n==="Object"&&e.constructor&&(n=e.constructor.name),n==="Map"||n==="Set")return Array.from(e);if(n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return i(e,t)}}function O(e){if(typeof Symbol<"u"&&e[Symbol.iterator]!=null||e["@@iterator"]!=null)return Array.from(e)}function T(e){if(Array.isArray(e))return i(e)}function i(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var P={name:"Checkbox",extends:B,emits:["update:modelValue","change","focus","blur"],methods:{getPTOptions:function(t){return this.ptm(t,{context:{checked:this.checked,disabled:this.disabled}})},onChange:function(t){var n=this;if(!this.disabled&&!this.readonly){var r;this.binary?r=this.checked?this.falseValue:this.trueValue:this.checked?r=this.modelValue.filter(function(o){return!s.equals(o,n.value)}):r=this.modelValue?[].concat(V(this.modelValue),[this.value]):[this.value],this.$emit("update:modelValue",r),this.$emit("change",t)}},onFocus:function(t){this.$emit("focus",t)},onBlur:function(t){this.$emit("blur",t)}},computed:{checked:function(){return this.binary?this.modelValue===this.trueValue:s.contains(this.value,this.modelValue)}},components:{CheckIcon:h}},j=["data-p-highlight","data-p-disabled"],q=["id","value","name","checked","tabindex","disabled","readonly","required","aria-labelledby","aria-label"];function F(e,t,n,r,o,a){var d=b("CheckIcon");return u(),f("div",l({class:e.cx("root")},a.getPTOptions("root"),{"data-pc-name":"checkbox","data-p-highlight":a.checked,"data-p-disabled":e.disabled}),[c("input",l({id:e.inputId,type:"checkbox",class:[e.cx("input"),e.inputClass],style:e.inputStyle,value:e.value,name:e.name,checked:a.checked,tabindex:e.tabindex,disabled:e.disabled,readonly:e.readonly,required:e.required,"aria-labelledby":e.ariaLabelledby,"aria-label":e.ariaLabel,onFocus:t[0]||(t[0]=function(){return a.onFocus&&a.onFocus.apply(a,arguments)}),onBlur:t[1]||(t[1]=function(){return a.onBlur&&a.onBlur.apply(a,arguments)}),onChange:t[2]||(t[2]=function(){return a.onChange&&a.onChange.apply(a,arguments)})},a.getPTOptions("input")),null,16,q),c("div",l({class:e.cx("box")},a.getPTOptions("box")),[y(e.$slots,"icon",{checked:a.checked,class:k(e.cx("icon"))},function(){return[a.checked?(u(),m(d,l({key:0,class:e.cx("icon")},a.getPTOptions("icon")),null,16,["class"])):g("",!0)]})],16)],16,j)}P.render=F;export{P as default};
