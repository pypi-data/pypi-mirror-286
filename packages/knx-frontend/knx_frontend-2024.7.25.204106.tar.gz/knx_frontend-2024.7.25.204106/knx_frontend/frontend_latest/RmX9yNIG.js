export const id=1240;export const ids=[1240];export const modules={71240:(e,i,t)=>{t.r(i);var a=t(62659),o=t(98597),s=t(196),r=t(33167),l=(t(19887),t(32694),t(59373),t(43799));(0,a.A)([(0,s.EM)("ha-timer-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_duration",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_restore",value:void 0},{kind:"set",key:"item",value:function(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._duration=e.duration||"00:00:00",this._restore=e.restore||!1):(this._name="",this._icon="",this._duration="00:00:00",this._restore=!1)}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}},{kind:"method",key:"render",value:function(){return this.hass?o.qy`
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
        <ha-textfield
          .configValue=${"duration"}
          .value=${this._duration}
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.timer.duration")}
        ></ha-textfield>
        <ha-formfield
          .label=${this.hass.localize("ui.dialogs.helper_settings.timer.restore")}
        >
          <ha-checkbox
            .configValue=${"restore"}
            .checked=${this._restore}
            @click=${this._toggleRestore}
          >
          </ha-checkbox>
        </ha-formfield>
      </div>
    `:o.s6}},{kind:"method",key:"_valueChanged",value:function(e){var i;if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target.configValue,a=(null===(i=e.detail)||void 0===i?void 0:i.value)||e.target.value;if(this[`_${t}`]===a)return;const o={...this._item};a?o[t]=a:delete o[t],(0,r.r)(this,"value-changed",{value:o})}},{kind:"method",key:"_toggleRestore",value:function(){this._restore=!this._restore,(0,r.r)(this,"value-changed",{value:{...this._item,restore:this._restore}})}},{kind:"get",static:!0,key:"styles",value:function(){return[l.RF,o.AH`
        .form {
          color: var(--primary-text-color);
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
      `]}}]}}),o.WF)}};
//# sourceMappingURL=RmX9yNIG.js.map