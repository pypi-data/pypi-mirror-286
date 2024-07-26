/*! For license information please see kvTiw1h3.js.LICENSE.txt */
export const id=3971;export const ids=[3971];export const modules={13442:(e,t,i)=>{var r=i(62659),c=i(76504),s=i(80792),o=i(76513),a=(i(86395),i(5789)),d=i(71086),n=i(16584),l=i(90523),h=i(4943),u={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},p={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"};const m=function(e){function t(i){return e.call(this,(0,o.Cl)((0,o.Cl)({},t.defaultAdapter),i))||this}return(0,o.C6)(t,e),Object.defineProperty(t,"strings",{get:function(){return p},enumerable:!1,configurable:!0}),Object.defineProperty(t,"cssClasses",{get:function(){return u},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),t.prototype.setChecked=function(e){this.adapter.setNativeControlChecked(e),this.updateAriaChecked(e),this.updateCheckedStyling(e)},t.prototype.setDisabled=function(e){this.adapter.setNativeControlDisabled(e),e?this.adapter.addClass(u.DISABLED):this.adapter.removeClass(u.DISABLED)},t.prototype.handleChange=function(e){var t=e.target;this.updateAriaChecked(t.checked),this.updateCheckedStyling(t.checked)},t.prototype.updateCheckedStyling=function(e){e?this.adapter.addClass(u.CHECKED):this.adapter.removeClass(u.CHECKED)},t.prototype.updateAriaChecked=function(e){this.adapter.setNativeControlAttr(p.ARIA_CHECKED_ATTR,""+!!e)},t}(h.I);var v=i(98597),b=i(196),_=i(79278);class k extends d.O{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=m,this.rippleHandlers=new l.I((()=>(this.shouldRenderRipple=!0,this.ripple)))}changeHandler(e){this.mdcFoundation.handleChange(e),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},(0,d.i)(this.mdcRoot)),{setNativeControlChecked:e=>{this.formElement.checked=e},setNativeControlDisabled:e=>{this.formElement.disabled=e},setNativeControlAttr:(e,t)=>{this.formElement.setAttribute(e,t)}})}renderRipple(){return this.shouldRenderRipple?v.qy`
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
              aria-label="${(0,_.J)(this.ariaLabel)}"
              aria-labelledby="${(0,_.J)(this.ariaLabelledBy)}"
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
      </div>`}handleRippleMouseDown(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,o.Cg)([(0,b.MZ)({type:Boolean}),(0,n.P)((function(e){this.mdcFoundation.setChecked(e)}))],k.prototype,"checked",void 0),(0,o.Cg)([(0,b.MZ)({type:Boolean}),(0,n.P)((function(e){this.mdcFoundation.setDisabled(e)}))],k.prototype,"disabled",void 0),(0,o.Cg)([a.T,(0,b.MZ)({attribute:"aria-label"})],k.prototype,"ariaLabel",void 0),(0,o.Cg)([a.T,(0,b.MZ)({attribute:"aria-labelledby"})],k.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,b.P)(".mdc-switch")],k.prototype,"mdcRoot",void 0),(0,o.Cg)([(0,b.P)("input")],k.prototype,"formElement",void 0),(0,o.Cg)([(0,b.nJ)("mwc-ripple")],k.prototype,"ripple",void 0),(0,o.Cg)([(0,b.wk)()],k.prototype,"shouldRenderRipple",void 0),(0,o.Cg)([(0,b.Ls)({passive:!0})],k.prototype,"handleRippleMouseDown",null),(0,o.Cg)([(0,b.Ls)({passive:!0})],k.prototype,"handleRippleTouchStart",null);const f=v.AH`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`;var w=i(33167);(0,r.A)([(0,b.EM)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,b.MZ)({type:Boolean})],key:"haptic",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){(0,c.A)((0,s.A)(i.prototype),"firstUpdated",this).call(this),this.addEventListener("change",(()=>{var e;this.haptic&&(e="light",(0,w.r)(window,"haptic",e))}))}},{kind:"field",static:!0,key:"styles",value(){return[f,v.AH`
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
    `]}}]}}),k)},3971:(e,t,i)=>{i.r(t);var r=i(62659),c=i(98597),s=i(196),o=i(33167),a=(i(13442),i(59373),i(43799));(0,r.A)([(0,s.EM)("ha-counter-form")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_maximum",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_minimum",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_restore",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_initial",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_step",value:void 0},{kind:"set",key:"item",value:function(e){var t,i,r,c,s;(this._item=e,e)?(this._name=e.name||"",this._icon=e.icon||"",this._maximum=null!==(t=e.maximum)&&void 0!==t?t:void 0,this._minimum=null!==(i=e.minimum)&&void 0!==i?i:void 0,this._restore=null===(r=e.restore)||void 0===r||r,this._step=null!==(c=e.step)&&void 0!==c?c:1,this._initial=null!==(s=e.initial)&&void 0!==s?s:0):(this._name="",this._icon="",this._maximum=void 0,this._minimum=void 0,this._restore=!0,this._step=1,this._initial=0)}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}},{kind:"method",key:"render",value:function(){var e;return this.hass?c.qy`
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
          .value=${this._minimum}
          .configValue=${"minimum"}
          type="number"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.counter.minimum")}
        ></ha-textfield>
        <ha-textfield
          .value=${this._maximum}
          .configValue=${"maximum"}
          type="number"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.counter.maximum")}
        ></ha-textfield>
        <ha-textfield
          .value=${this._initial}
          .configValue=${"initial"}
          type="number"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.counter.initial")}
        ></ha-textfield>
        ${null!==(e=this.hass.userData)&&void 0!==e&&e.showAdvanced?c.qy`
              <ha-textfield
                .value=${this._step}
                .configValue=${"step"}
                type="number"
                @input=${this._valueChanged}
                .label=${this.hass.localize("ui.dialogs.helper_settings.counter.step")}
              ></ha-textfield>
              <div class="row">
                <ha-switch
                  .checked=${this._restore}
                  .configValue=${"restore"}
                  @change=${this._valueChanged}
                >
                </ha-switch>
                <div>
                  ${this.hass.localize("ui.dialogs.helper_settings.counter.restore")}
                </div>
              </div>
            `:""}
      </div>
    `:c.s6}},{kind:"method",key:"_valueChanged",value:function(e){var t;if(!this.new&&!this._item)return;e.stopPropagation();const i=e.target,r=i.configValue,c="number"===i.type?""!==i.value?Number(i.value):void 0:"ha-switch"===i.localName?e.target.checked:(null===(t=e.detail)||void 0===t?void 0:t.value)||i.value;if(this[`_${r}`]===c)return;const s={...this._item};void 0===c||""===c?delete s[r]:s[r]=c,(0,o.r)(this,"value-changed",{value:s})}},{kind:"get",static:!0,key:"styles",value:function(){return[a.RF,c.AH`
        .form {
          color: var(--primary-text-color);
        }
        .row {
          margin-top: 12px;
          margin-bottom: 12px;
          color: var(--primary-text-color);
          display: flex;
          align-items: center;
        }
        .row div {
          margin-left: 16px;
          margin-inline-start: 16px;
          margin-inline-end: initial;
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
      `]}}]}}),c.WF)}};
//# sourceMappingURL=kvTiw1h3.js.map