export const id=3172;export const ids=[3172];export const modules={73172:(e,i,a)=>{a.r(i),a.d(i,{HaFormInteger:()=>h});var t=a(62659),s=a(98597),d=a(196),l=a(33167);a(53335);let h=(0,t.A)([(0,d.EM)("ha-form-integer")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"localize",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.P)("ha-textfield ha-slider")],key:"_input",value:void 0},{kind:"field",key:"_lastValue",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){var e,i;return void 0!==this.schema.valueMin&&void 0!==this.schema.valueMax&&this.schema.valueMax-this.schema.valueMin<256?s.qy`
        <div>
          ${this.label}
          <div class="flex">
            ${this.schema.required?"":s.qy`
                  <ha-checkbox
                    @change=${this._handleCheckboxChange}
                    .checked=${void 0!==this.data}
                    .disabled=${this.disabled}
                  ></ha-checkbox>
                `}
            <ha-slider
              labeled
              .value=${this._value}
              .min=${this.schema.valueMin}
              .max=${this.schema.valueMax}
              .disabled=${this.disabled||void 0===this.data&&!this.schema.required}
              @change=${this._valueChanged}
            ></ha-slider>
          </div>
          ${this.helper?s.qy`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
        </div>
      `:s.qy`
      <ha-textfield
        type="number"
        inputMode="numeric"
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
    `}},{kind:"method",key:"updated",value:function(e){e.has("schema")&&this.toggleAttribute("own-margin",!("valueMin"in this.schema&&"valueMax"in this.schema||!this.schema.required))}},{kind:"get",key:"_value",value:function(){var e,i;return void 0!==this.data?this.data:this.schema.required?void 0!==(null===(e=this.schema.description)||void 0===e?void 0:e.suggested_value)&&null!==(null===(i=this.schema.description)||void 0===i?void 0:i.suggested_value)||this.schema.default||this.schema.valueMin||0:this.schema.valueMin||0}},{kind:"method",key:"_handleCheckboxChange",value:function(e){let i;if(e.target.checked)for(const t of[this._lastValue,null===(a=this.schema.description)||void 0===a?void 0:a.suggested_value,this.schema.default,0]){var a;if(void 0!==t){i=t;break}}else this._lastValue=this.data;(0,l.r)(this,"value-changed",{value:i})}},{kind:"method",key:"_valueChanged",value:function(e){const i=e.target,a=i.value;let t;if(""!==a&&(t=parseInt(String(a))),this.data!==t)(0,l.r)(this,"value-changed",{value:t});else{const e=void 0===t?"":String(t);i.value!==e&&(i.value=e)}}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`
      :host([own-margin]) {
        margin-bottom: 5px;
      }
      .flex {
        display: flex;
      }
      ha-slider {
        flex: 1;
      }
      ha-textfield {
        display: block;
      }
    `}}]}}),s.WF)}};
//# sourceMappingURL=3O7t2-C8.js.map