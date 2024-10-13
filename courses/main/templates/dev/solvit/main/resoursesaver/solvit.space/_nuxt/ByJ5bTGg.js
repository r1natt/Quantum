import{aP as r,aZ as o,o as s,a as u,h as l,aN as i,aX as p}from"./BSpKbMoe.js";var b=`
@layer primevue {
    .p-radiobutton {
        position: relative;
        display: inline-flex;
        user-select: none;
        vertical-align: bottom;
    }

    .p-radiobutton-input {
        cursor: pointer;
    }

    .p-radiobutton-box {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .p-radiobutton-icon {
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        transform: translateZ(0) scale(.1);
        border-radius: 50%;
        visibility: hidden;
    }

    .p-radiobutton.p-highlight .p-radiobutton-icon {
        transform: translateZ(0) scale(1.0, 1.0);
        visibility: visible;
    }
}
`,c={root:function(n){var t=n.instance,d=n.props;return["p-radiobutton p-component",{"p-highlight":t.checked,"p-disabled":d.disabled}]},box:"p-radiobutton-box",input:"p-radiobutton-input",icon:"p-radiobutton-icon"},h=r.extend({name:"radiobutton",css:b,classes:c}),y={name:"BaseRadioButton",extends:p,props:{value:null,modelValue:null,binary:Boolean,name:{type:String,default:null},disabled:{type:Boolean,default:!1},readonly:{type:Boolean,default:!1},tabindex:{type:Number,default:null},inputId:{type:String,default:null},inputClass:{type:[String,Object],default:null},inputStyle:{type:Object,default:null},ariaLabelledby:{type:String,default:null},ariaLabel:{type:String,default:null}},style:h,provide:function(){return{$parentInstance:this}}},m={name:"RadioButton",extends:y,emits:["update:modelValue","change","focus","blur"],methods:{getPTOptions:function(n){return this.ptm(n,{context:{checked:this.checked,disabled:this.disabled}})},onChange:function(n){if(!this.disabled&&!this.readonly){var t=this.binary?!this.checked:this.value;this.$emit("update:modelValue",t),this.$emit("change",n)}},onFocus:function(n){this.$emit("focus",n)},onBlur:function(n){this.$emit("blur",n)}},computed:{checked:function(){return this.modelValue!=null&&(this.binary?!!this.modelValue:o.equals(this.modelValue,this.value))}}},f=["data-p-highlight","data-p-disabled"],g=["id","value","name","checked","tabindex","disabled","readonly","aria-labelledby","aria-label"];function v(e,n,t,d,B,a){return s(),u("div",i({class:e.cx("root")},a.getPTOptions("root"),{"data-pc-name":"radiobutton","data-p-highlight":a.checked,"data-p-disabled":e.disabled}),[l("input",i({id:e.inputId,type:"radio",class:[e.cx("input"),e.inputClass],style:e.inputStyle,value:e.value,name:e.name,checked:a.checked,tabindex:e.tabindex,disabled:e.disabled,readonly:e.readonly,"aria-labelledby":e.ariaLabelledby,"aria-label":e.ariaLabel,onFocus:n[0]||(n[0]=function(){return a.onFocus&&a.onFocus.apply(a,arguments)}),onBlur:n[1]||(n[1]=function(){return a.onBlur&&a.onBlur.apply(a,arguments)}),onChange:n[2]||(n[2]=function(){return a.onChange&&a.onChange.apply(a,arguments)})},a.getPTOptions("input")),null,16,g),l("div",i({class:e.cx("box")},a.getPTOptions("box")),[l("div",i({class:e.cx("icon")},a.getPTOptions("icon")),null,16)],16)],16,f)}m.render=v;export{m as default};
