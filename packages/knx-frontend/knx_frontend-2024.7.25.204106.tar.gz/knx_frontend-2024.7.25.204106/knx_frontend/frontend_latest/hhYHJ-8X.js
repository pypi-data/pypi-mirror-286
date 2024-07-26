export const id=3266;export const ids=[3266];export const modules={53266:(e,i,t)=>{t.r(i);var a=t(62659),o=t(98597),n=t(196),s=t(33167),l=(t(59373),t(43799));(0,a.A)([(0,n.EM)("ha-input_boolean-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_icon",value:void 0},{kind:"set",key:"item",value:function(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||""):(this._name="",this._icon="")}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}},{kind:"method",key:"render",value:function(){return this.hass?o.qy`
      <div class="form">
        <ha-textfield
          .value=${this._name}
          .configValue=${"name"}
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.name")}
          autoValidate
          required
          .validationMessage=${this.hass.localize("ui.dialogs.helper_settings.required_error_msg")}
          dialogInitialFocus
        ></ha-textfield>
        <ha-icon-picker
          .hass=${this.hass}
          .value=${this._icon}
          .configValue=${"icon"}
          @value-changed=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.icon")}
        ></ha-icon-picker>
      </div>
    `:o.s6}},{kind:"method",key:"_valueChanged",value:function(e){var i;if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target.configValue,a=(null===(i=e.detail)||void 0===i?void 0:i.value)||e.target.value;if(this[`_${t}`]===a)return;const o={...this._item};a?o[t]=a:delete o[t],(0,s.r)(this,"value-changed",{value:o})}},{kind:"get",static:!0,key:"styles",value:function(){return[l.RF,o.AH`
        .form {
          color: var(--primary-text-color);
        }
        .row {
          padding: 16px 0;
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
      `]}}]}}),o.WF)}};
//# sourceMappingURL=hhYHJ-8X.js.map