/*! For license information please see Va9IKhwx.js.LICENSE.txt */
export const id=4987;export const ids=[4987];export const modules={94090:(e,t,i)=>{var r=i(62659),a=(i(23981),i(98597)),s=i(196),o=i(12506),c=i(66534),l=i(33167),n=i(24517);i(96334),i(9484);(0,r.A)([(0,s.EM)("ha-color-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"defaultColor",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"method",key:"_valueSelected",value:function(e){const t=e.target.value;t&&(0,l.r)(this,"value-changed",{value:"default"!==t?t:void 0})}},{kind:"method",key:"render",value:function(){return a.qy`
      <ha-select
        .icon=${Boolean(this.value)}
        .label=${this.label}
        .value=${this.value||"default"}
        .helper=${this.helper}
        .disabled=${this.disabled}
        @closed=${n.d}
        @selected=${this._valueSelected}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.value?a.qy`
              <span slot="icon">
                ${this.renderColorCircle(this.value||"grey")}
              </span>
            `:a.s6}
        ${this.defaultColor?a.qy` <ha-list-item value="default">
              ${this.hass.localize("ui.components.color-picker.default_color")}
            </ha-list-item>`:a.s6}
        ${Array.from(c.l).map((e=>a.qy`
            <ha-list-item .value=${e} graphic="icon">
              ${this.hass.localize(`ui.components.color-picker.colors.${e}`)||e}
              <span slot="graphic">${this.renderColorCircle(e)}</span>
            </ha-list-item>
          `))}
      </ha-select>
    `}},{kind:"method",key:"renderColorCircle",value:function(e){return a.qy`
      <span
        class="circle-color"
        style=${(0,o.W)({"--circle-color":(0,c.M)(e)})}
      ></span>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      .circle-color {
        display: block;
        background-color: var(--circle-color);
        border-radius: 10px;
        width: 20px;
        height: 20px;
      }
      ha-select {
        width: 100%;
      }
    `}}]}}),a.WF)},13442:(e,t,i)=>{var r=i(62659),a=i(76504),s=i(80792),o=i(76513),c=(i(86395),i(5789)),l=i(71086),n=i(16584),d=i(90523),h=i(4943),u={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},p={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"};const m=function(e){function t(i){return e.call(this,(0,o.Cl)((0,o.Cl)({},t.defaultAdapter),i))||this}return(0,o.C6)(t,e),Object.defineProperty(t,"strings",{get:function(){return p},enumerable:!1,configurable:!0}),Object.defineProperty(t,"cssClasses",{get:function(){return u},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),t.prototype.setChecked=function(e){this.adapter.setNativeControlChecked(e),this.updateAriaChecked(e),this.updateCheckedStyling(e)},t.prototype.setDisabled=function(e){this.adapter.setNativeControlDisabled(e),e?this.adapter.addClass(u.DISABLED):this.adapter.removeClass(u.DISABLED)},t.prototype.handleChange=function(e){var t=e.target;this.updateAriaChecked(t.checked),this.updateCheckedStyling(t.checked)},t.prototype.updateCheckedStyling=function(e){e?this.adapter.addClass(u.CHECKED):this.adapter.removeClass(u.CHECKED)},t.prototype.updateAriaChecked=function(e){this.adapter.setNativeControlAttr(p.ARIA_CHECKED_ATTR,""+!!e)},t}(h.I);var v=i(98597),b=i(196),k=i(79278);class _ extends l.O{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=m,this.rippleHandlers=new d.I((()=>(this.shouldRenderRipple=!0,this.ripple)))}changeHandler(e){this.mdcFoundation.handleChange(e),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},(0,l.i)(this.mdcRoot)),{setNativeControlChecked:e=>{this.formElement.checked=e},setNativeControlDisabled:e=>{this.formElement.disabled=e},setNativeControlAttr:(e,t)=>{this.formElement.setAttribute(e,t)}})}renderRipple(){return this.shouldRenderRipple?v.qy`
        <mwc-ripple
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const e=this.formElement;e&&(this.rippleHandlers.startFocus(),e.focus())}blur(){const e=this.formElement;e&&(this.rippleHandlers.endFocus(),e.blur())}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}render(){return v.qy`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              aria-label="${(0,k.J)(this.ariaLabel)}"
              aria-labelledby="${(0,k.J)(this.ariaLabelledBy)}"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,o.Cg)([(0,b.MZ)({type:Boolean}),(0,n.P)((function(e){this.mdcFoundation.setChecked(e)}))],_.prototype,"checked",void 0),(0,o.Cg)([(0,b.MZ)({type:Boolean}),(0,n.P)((function(e){this.mdcFoundation.setDisabled(e)}))],_.prototype,"disabled",void 0),(0,o.Cg)([c.T,(0,b.MZ)({attribute:"aria-label"})],_.prototype,"ariaLabel",void 0),(0,o.Cg)([c.T,(0,b.MZ)({attribute:"aria-labelledby"})],_.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,b.P)(".mdc-switch")],_.prototype,"mdcRoot",void 0),(0,o.Cg)([(0,b.P)("input")],_.prototype,"formElement",void 0),(0,o.Cg)([(0,b.nJ)("mwc-ripple")],_.prototype,"ripple",void 0),(0,o.Cg)([(0,b.wk)()],_.prototype,"shouldRenderRipple",void 0),(0,o.Cg)([(0,b.Ls)({passive:!0})],_.prototype,"handleRippleMouseDown",null),(0,o.Cg)([(0,b.Ls)({passive:!0})],_.prototype,"handleRippleTouchStart",null);const y=v.AH`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`;var f=i(33167);(0,r.A)([(0,b.EM)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,b.MZ)({type:Boolean})],key:"haptic",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){(0,a.A)((0,s.A)(i.prototype),"firstUpdated",this).call(this),this.addEventListener("change",(()=>{var e;this.haptic&&(e="light",(0,f.r)(window,"haptic",e))}))}},{kind:"field",static:!0,key:"styles",value(){return[y,v.AH`
      :host {
        --mdc-theme-secondary: var(--switch-checked-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
        background-color: var(--switch-checked-button-color);
        border-color: var(--switch-checked-button-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__track {
        background-color: var(--switch-checked-track-color);
        border-color: var(--switch-checked-track-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
        background-color: var(--switch-unchecked-button-color);
        border-color: var(--switch-unchecked-button-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
        background-color: var(--switch-unchecked-track-color);
        border-color: var(--switch-unchecked-track-color);
      }
    `]}}]}}),_)},64987:(e,t,i)=>{i.r(t);var r=i(62659),a=(i(58068),i(98597)),s=i(196),o=i(33167),c=(i(91074),i(88762)),l=(i(32694),i(13442),i(59373),i(77984),i(94090),i(43799));(0,r.A)([(0,s.EM)("dialog-label-detail")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_color",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_description",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_submitting",value(){return!1}},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._error=void 0,this._params.entry?(this._name=this._params.entry.name||"",this._icon=this._params.entry.icon||"",this._color=this._params.entry.color||"",this._description=this._params.entry.description||""):(this._name=this._params.suggestedName||"",this._icon="",this._color="",this._description=""),document.body.addEventListener("keydown",this._handleKeyPress)}},{kind:"field",key:"_handleKeyPress",value(){return e=>{"Escape"===e.key&&e.stopPropagation()}}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,o.r)(this,"dialog-closed",{dialog:this.localName}),document.body.removeEventListener("keydown",this._handleKeyPress)}},{kind:"method",key:"render",value:function(){return this._params?a.qy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        .heading=${(0,c.l)(this.hass,this._params.entry?this._params.entry.name||this._params.entry.label_id:this.hass.localize("ui.panel.config.labels.detail.new_label"))}
      >
        <div>
          ${this._error?a.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
          <div class="form">
            <ha-textfield
              dialogInitialFocus
              .value=${this._name}
              .configValue=${"name"}
              @input=${this._input}
              .label=${this.hass.localize("ui.panel.config.labels.detail.name")}
              .validationMessage=${this.hass.localize("ui.panel.config.labels.detail.required_error_msg")}
              required
            ></ha-textfield>
            <ha-icon-picker
              .value=${this._icon}
              .hass=${this.hass}
              .configValue=${"icon"}
              @value-changed=${this._valueChanged}
              .label=${this.hass.localize("ui.panel.config.labels.detail.icon")}
            ></ha-icon-picker>
            <ha-color-picker
              .value=${this._color}
              .configValue=${"color"}
              .hass=${this.hass}
              @value-changed=${this._valueChanged}
              .label=${this.hass.localize("ui.panel.config.labels.detail.color")}
            ></ha-color-picker>
            <ha-textarea
              .value=${this._description}
              .configValue=${"description"}
              @input=${this._input}
              .label=${this.hass.localize("ui.panel.config.labels.detail.description")}
            ></ha-textarea>
          </div>
        </div>
        ${this._params.entry&&this._params.removeEntry?a.qy`
              <mwc-button
                slot="secondaryAction"
                class="warning"
                @click=${this._deleteEntry}
                .disabled=${this._submitting}
              >
                ${this.hass.localize("ui.panel.config.labels.detail.delete")}
              </mwc-button>
            `:a.s6}
        <mwc-button
          slot="primaryAction"
          @click=${this._updateEntry}
          .disabled=${this._submitting||!this._name}
        >
          ${this._params.entry?this.hass.localize("ui.panel.config.labels.detail.update"):this.hass.localize("ui.panel.config.labels.detail.create")}
        </mwc-button>
      </ha-dialog>
    `:a.s6}},{kind:"method",key:"_input",value:function(e){const t=e.target,i=t.configValue;this._error=void 0,this[`_${i}`]=t.value}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.target.configValue;this._error=void 0,this[`_${t}`]=e.detail.value||""}},{kind:"method",key:"_updateEntry",value:async function(){let e;this._submitting=!0;try{const t={name:this._name.trim(),icon:this._icon.trim()||null,color:this._color.trim()||null,description:this._description.trim()||null};e=this._params.entry?await this._params.updateEntry(t):await this._params.createEntry(t),this.closeDialog()}catch(t){this._error=t?t.message:"Unknown error"}finally{this._submitting=!1}return e}},{kind:"method",key:"_deleteEntry",value:async function(){this._submitting=!0;try{await this._params.removeEntry()&&(this._params=void 0)}finally{this._submitting=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[l.nA,a.AH`
        a {
          color: var(--primary-color);
        }
        ha-textarea,
        ha-textfield,
        ha-icon-picker,
        ha-color-picker {
          display: block;
        }
        ha-color-picker,
        ha-textarea {
          margin-top: 16px;
        }
      `]}}]}}),a.WF)}};
//# sourceMappingURL=Va9IKhwx.js.map