export const id=6805;export const ids=[6805];export const modules={6805:(e,i,t)=>{t.r(i);var a=t(62659),s=t(98597),l=t(196),n=t(33167),o=(t(32694),t(32283),t(59373),t(43799));(0,a.A)([(0,l.EM)("ha-input_number-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_max",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_min",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_mode",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_step",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_unit_of_measurement",value:void 0},{kind:"set",key:"item",value:function(e){var i,t,a;(this._item=e,e)?(this._name=e.name||"",this._icon=e.icon||"",this._max=null!==(i=e.max)&&void 0!==i?i:100,this._min=null!==(t=e.min)&&void 0!==t?t:0,this._mode=e.mode||"slider",this._step=null!==(a=e.step)&&void 0!==a?a:1,this._unit_of_measurement=e.unit_of_measurement):(this._item={min:0,max:100},this._name="",this._icon="",this._max=100,this._min=0,this._mode="slider",this._step=1)}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}},{kind:"method",key:"render",value:function(){var e;return this.hass?s.qy`
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
          .value=${this._min}
          .configValue=${"min"}
          type="number"
          step="any"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.min")}
        ></ha-textfield>
        <ha-textfield
          .value=${this._max}
          .configValue=${"max"}
          type="number"
          step="any"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.max")}
        ></ha-textfield>
        ${null!==(e=this.hass.userData)&&void 0!==e&&e.showAdvanced?s.qy`
              <div class="layout horizontal center justified">
                ${this.hass.localize("ui.dialogs.helper_settings.input_number.mode")}
                <ha-formfield
                  .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.slider")}
                >
                  <ha-radio
                    name="mode"
                    value="slider"
                    .checked=${"slider"===this._mode}
                    @change=${this._modeChanged}
                  ></ha-radio>
                </ha-formfield>
                <ha-formfield
                  .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.box")}
                >
                  <ha-radio
                    name="mode"
                    value="box"
                    .checked=${"box"===this._mode}
                    @change=${this._modeChanged}
                  ></ha-radio>
                </ha-formfield>
              </div>
              <ha-textfield
                .value=${this._step}
                .configValue=${"step"}
                type="number"
                step="any"
                @input=${this._valueChanged}
                .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.step")}
              ></ha-textfield>

              <ha-textfield
                .value=${this._unit_of_measurement||""}
                .configValue=${"unit_of_measurement"}
                @input=${this._valueChanged}
                .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.unit_of_measurement")}
              ></ha-textfield>
            `:""}
      </div>
    `:s.s6}},{kind:"method",key:"_modeChanged",value:function(e){(0,n.r)(this,"value-changed",{value:{...this._item,mode:e.target.value}})}},{kind:"method",key:"_valueChanged",value:function(e){var i;if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target,a=t.configValue,s="number"===t.type?Number(t.value):(null===(i=e.detail)||void 0===i?void 0:i.value)||t.value;if(this[`_${a}`]===s)return;const l={...this._item};void 0===s||""===s?delete l[a]:l[a]=s,(0,n.r)(this,"value-changed",{value:l})}},{kind:"get",static:!0,key:"styles",value:function(){return[o.RF,s.AH`
        .form {
          color: var(--primary-text-color);
        }

        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
      `]}}]}}),s.WF)}};
//# sourceMappingURL=H6dBQWUJ.js.map