export const id=6928;export const ids=[6928];export const modules={6928:(e,t,i)=>{i.r(t),i.d(t,{HaSelectorUiStateContent:()=>H});var s=i(62659),a=i(98597),n=i(196),o=i(28226),l=i(66580),r=i(45081),d=i(96041),u=i(33167),c=i(19263),h=i(80085),v=i(76504),_=i(80792),p=i(3139),m=i(1695);(0,s.A)([(0,n.EM)("ha-relative-time")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"datetime",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"capitalize",value(){return!1}},{kind:"field",key:"_interval",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,v.A)((0,_.A)(i.prototype),"disconnectedCallback",this).call(this),this._clearInterval()}},{kind:"method",key:"connectedCallback",value:function(){(0,v.A)((0,_.A)(i.prototype),"connectedCallback",this).call(this),this.datetime&&this._startInterval()}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"firstUpdated",value:function(e){(0,v.A)((0,_.A)(i.prototype),"firstUpdated",this).call(this,e),this._updateRelative()}},{kind:"method",key:"update",value:function(e){(0,v.A)((0,_.A)(i.prototype),"update",this).call(this,e),this._updateRelative()}},{kind:"method",key:"_clearInterval",value:function(){this._interval&&(window.clearInterval(this._interval),this._interval=void 0)}},{kind:"method",key:"_startInterval",value:function(){this._clearInterval(),this._interval=window.setInterval((()=>this._updateRelative()),6e4)}},{kind:"method",key:"_updateRelative",value:function(){if(this.datetime){const e=(0,p.K)(new Date(this.datetime),this.hass.locale);this.innerHTML=this.capitalize?(0,m.Z)(e):e}else this.innerHTML=this.hass.localize("ui.components.relative_time.never")}}]}}),a.mN);var k=i(6601),f=i(33496),y=i(2503);i(28368);const b=["button","input_button","scene"],g=["remaining_time","install_status"],$={timer:["remaining_time"],update:["install_status"]},M={valve:["current_position"],cover:["current_position"],fan:["percentage"],light:["brightness"]},S={climate:["state","current_temperature"],cover:["state","current_position"],fan:"percentage",humidifier:["state","current_humidity"],light:"brightness",timer:"remaining_time",update:"install_status",valve:["state","current_position"]};(0,s.A)([(0,n.EM)("state-display")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"content",value:void 0},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"get",key:"_content",value:function(){var e,t;const i=(0,h.t)(this.stateObj);return null!==(e=null!==(t=this.content)&&void 0!==t?t:S[i])&&void 0!==e?e:"state"}},{kind:"method",key:"_computeContent",value:function(e){var t,s;const n=this.stateObj,o=(0,h.t)(n);if("state"===e)return n.attributes.device_class!==f.Sn&&!b.includes(o)||(0,k.g0)(n.state)?this.hass.formatEntityState(n):a.qy`
          <hui-timestamp-display
            .hass=${this.hass}
            .ts=${new Date(n.state)}
            format="relative"
            capitalize
          ></hui-timestamp-display>
        `;if("last_changed"===e||"last-changed"===e)return a.qy`
        <ha-relative-time
          .hass=${this.hass}
          .datetime=${n.last_changed}
        ></ha-relative-time>
      `;if("last_updated"===e||"last-updated"===e)return a.qy`
        <ha-relative-time
          .hass=${this.hass}
          .datetime=${n.last_updated}
        ></ha-relative-time>
      `;if("last_triggered"===e)return a.qy`
        <ha-relative-time
          .hass=${this.hass}
          .datetime=${n.attributes.last_triggered}
        ></ha-relative-time>
      `;if((null!==(t=$[o])&&void 0!==t?t:[]).includes(e)){if("install_status"===e)return a.qy`
          ${(0,y.A_)(n,this.hass)}
        `;if("remaining_time"===e)return i.e(1126).then(i.bind(i,61126)),a.qy`
          <ha-timer-remaining-time
            .hass=${this.hass}
            .stateObj=${n}
          ></ha-timer-remaining-time>
        `}const l=n.attributes[e];return null==l||null!==(s=M[o])&&void 0!==s&&s.includes(e)&&!l?void 0:this.hass.formatEntityAttributeValue(n,e)}},{kind:"method",key:"render",value:function(){const e=this.stateObj,t=(0,d.e)(this._content).map((e=>this._computeContent(e))).filter(Boolean);return t.length?a.qy`
      ${t.map(((e,t,i)=>a.qy`${e}${t<i.length-1?" ⸱ ":a.s6}`))}
    `:a.qy`${this.hass.formatEntityState(e)}`}}]}}),a.WF);i(66442);const V=["access_token","available_modes","battery_icon","battery_level","code_arm_required","code_format","color_modes","device_class","editable","effect_list","entity_id","entity_picture","event_types","fan_modes","fan_speed_list","friendly_name","frontend_stream_type","has_date","has_time","hvac_modes","icon","id","max_color_temp_kelvin","max_mireds","max_temp","max","min_color_temp_kelvin","min_mireds","min_temp","min","mode","operation_list","options","percentage_step","precipitation_unit","preset_modes","pressure_unit","remaining","sound_mode_list","source_list","state_class","step","supported_color_modes","supported_features","swing_modes","target_temp_step","temperature_unit","token","unit_of_measurement","visibility_unit","wind_speed_unit"];(0,s.A)([(0,n.EM)("ha-entity-state-content-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"entityId",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,n.P)("ha-combo-box",!0)],key:"_comboBox",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return!(!e.has("_opened")&&this._opened)}},{kind:"field",key:"options",value(){return(0,r.A)(((e,t)=>{var i;const s=e?(0,c.m)(e):void 0;return[{label:this.hass.localize("ui.components.state-content-picker.state"),value:"state"},{label:this.hass.localize("ui.components.state-content-picker.last_changed"),value:"last_changed"},{label:this.hass.localize("ui.components.state-content-picker.last_updated"),value:"last_updated"},...s?g.filter((e=>{var t;return null===(t=$[s])||void 0===t?void 0:t.includes(e)})).map((e=>({label:this.hass.localize(`ui.components.state-content-picker.${e}`),value:e}))):[],...Object.keys(null!==(i=null==t?void 0:t.attributes)&&void 0!==i?i:{}).filter((e=>!V.includes(e))).map((e=>({value:e,label:this.hass.formatEntityAttributeName(t,e)})))]}))}},{kind:"field",key:"_filter",value(){return""}},{kind:"method",key:"render",value:function(){if(!this.hass)return a.s6;const e=this._value,t=this.entityId?this.hass.states[this.entityId]:void 0,i=this.options(this.entityId,t),s=i.filter((e=>!this._value.includes(e.value)));return a.qy`
      ${null!=e&&e.length?a.qy`
            <ha-sortable
              no-style
              @item-moved=${this._moveItem}
              .disabled=${this.disabled}
            >
              <ha-chip-set>
                ${(0,l.u)(this._value,(e=>e),((e,t)=>{var s;const n=(null===(s=i.find((t=>t.value===e)))||void 0===s?void 0:s.label)||e;return a.qy`
                      <ha-input-chip
                        .idx=${t}
                        @remove=${this._removeItem}
                        .label=${n}
                        selected
                      >
                        <ha-svg-icon
                          slot="icon"
                          .path=${"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"}
                          data-handle
                        ></ha-svg-icon>

                        ${n}
                      </ha-input-chip>
                    `}))}
              </ha-chip-set>
            </ha-sortable>
          `:a.s6}

      <ha-combo-box
        item-value-path="value"
        item-label-path="label"
        .hass=${this.hass}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required&&!e.length}
        .value=${""}
        .items=${s}
        allow-custom-value
        @filter-changed=${this._filterChanged}
        @value-changed=${this._comboBoxValueChanged}
        @opened-changed=${this._openedChanged}
      ></ha-combo-box>
    `}},{kind:"get",key:"_value",value:function(){return this.value?(0,d.e)(this.value):[]}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_filterChanged",value:function(e){var t;this._filter=(null==e?void 0:e.detail.value)||"";const i=null===(t=this._comboBox.items)||void 0===t?void 0:t.filter((e=>{var t;return(e.label||e.value).toLowerCase().includes(null===(t=this._filter)||void 0===t?void 0:t.toLowerCase())}));this._filter&&(null==i||i.unshift({label:this._filter,value:this._filter})),this._comboBox.filteredItems=i}},{kind:"method",key:"_moveItem",value:async function(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail,s=this._value.concat(),a=s.splice(t,1)[0];s.splice(i,0,a),this._setValue(s),await this.updateComplete,this._filterChanged()}},{kind:"method",key:"_removeItem",value:async function(e){e.stopPropagation();const t=[...this._value];t.splice(e.target.idx,1),this._setValue(t),await this.updateComplete,this._filterChanged()}},{kind:"method",key:"_comboBoxValueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(this.disabled||""===t)return;const i=this._value;i.includes(t)||(setTimeout((()=>{this._filterChanged(),this._comboBox.setInputValue("")}),0),this._setValue([...i,t]))}},{kind:"method",key:"_setValue",value:function(e){const t=0===e.length?void 0:1===e.length?e[0]:e;this.value=t,(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    :host {
      position: relative;
    }

    ha-chip-set {
      padding: 8px 0;
    }

    .sortable-fallback {
      display: none;
      opacity: 0;
    }

    .sortable-ghost {
      opacity: 0.4;
    }

    .sortable-drag {
      cursor: grabbing;
    }
  `}}]}}),a.WF);let H=(0,s.A)([(0,n.EM)("ha-selector-ui_state_content")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,t;return a.qy`
      <ha-entity-state-content-picker
        .hass=${this.hass}
        .entityId=${(null===(e=this.selector.ui_state_content)||void 0===e?void 0:e.entity_id)||(null===(t=this.context)||void 0===t?void 0:t.filter_entity)}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-entity-state-content-picker>
    `}}]}}),(0,o.E)(a.WF))},2503:(e,t,i)=>{i.d(t,{A_:()=>o,Jy:()=>n});i(93758);var s=i(60222);i(66412);let a=function(e){return e[e.INSTALL=1]="INSTALL",e[e.SPECIFIC_VERSION=2]="SPECIFIC_VERSION",e[e.PROGRESS=4]="PROGRESS",e[e.BACKUP=8]="BACKUP",e[e.RELEASE_NOTES=16]="RELEASE_NOTES",e}({});const n=e=>(e=>(0,s.$)(e,a.PROGRESS)&&"number"==typeof e.attributes.in_progress)(e)||!!e.attributes.in_progress,o=(e,t)=>{const i=e.state,o=e.attributes;if("off"===i){return o.latest_version&&o.skipped_version===o.latest_version?o.latest_version:t.formatEntityState(e)}if("on"===i&&n(e)){return(0,s.$)(e,a.PROGRESS)&&"number"==typeof o.in_progress?t.localize("ui.card.update.installing_with_progress",{progress:o.in_progress}):t.localize("ui.card.update.installing")}return t.formatEntityState(e)}},28226:(e,t,i)=>{i.d(t,{E:()=>l});var s=i(62659),a=i(76504),n=i(80792),o=i(196);const l=e=>(0,s.A)(null,(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.A)((0,n.A)(i.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,a.A)((0,n.A)(i.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){if((0,a.A)((0,n.A)(i.prototype),"updated",this).call(this,e),e.has("hass"))this.__checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const t of e.keys())if(this.hassSubscribeRequiredHostProps.includes(t))return void this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){var e;void 0!==this.__unsubs||!this.isConnected||void 0===this.hass||null!==(e=this.hassSubscribeRequiredHostProps)&&void 0!==e&&e.some((e=>void 0===this[e]))||(this.__unsubs=this.hassSubscribe())}}]}}),e)}};
//# sourceMappingURL=LHehD9uw.js.map