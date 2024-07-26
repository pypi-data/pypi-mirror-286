export const id=2292;export const ids=[2292];export const modules={82292:(e,i,t)=>{t.r(i),t.d(i,{HaFormFloat:()=>r});var a=t(62659),d=t(98597),o=t(196),l=t(33167);t(59373);let r=(0,a.A)([(0,o.EM)("ha-form-float")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"localize",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.P)("ha-textfield")],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){var e,i;return d.qy`
      <ha-textfield
        type="numeric"
        inputMode="decimal"
        .label=${this.label}
        .helper=${this.helper}
        helperPersistent
        .value=${void 0!==this.data?this.data:""}
        .disabled=${this.disabled}
        .required=${this.schema.required}
        .autoValidate=${this.schema.required}
        .suffix=${null===(e=this.schema.description)||void 0===e?void 0:e.suffix}
        .validationMessage=${this.schema.required?null===(i=this.localize)||void 0===i?void 0:i.call(this,"ui.common.error_required"):void 0}
        @input=${this._valueChanged}
      ></ha-textfield>
    `}},{kind:"method",key:"updated",value:function(e){e.has("schema")&&this.toggleAttribute("own-margin",!!this.schema.required)}},{kind:"method",key:"_valueChanged",value:function(e){const i=e.target,t=i.value.replace(",",".");let a;if(!t.endsWith(".")&&"-"!==t)if(""!==t&&(a=parseFloat(t),isNaN(a)&&(a=void 0)),this.data!==a)(0,l.r)(this,"value-changed",{value:a});else{const e=void 0===a?"":String(a);i.value!==e&&(i.value=e)}}},{kind:"field",static:!0,key:"styles",value(){return d.AH`
    :host([own-margin]) {
      margin-bottom: 5px;
    }
    ha-textfield {
      display: block;
    }
  `}}]}}),d.WF)}};
//# sourceMappingURL=K2z7K0Ge.js.map