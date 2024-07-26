export const id=1546;export const ids=[1546];export const modules={31546:(e,i,t)=>{t.r(i),t.d(i,{HaSTTSelector:()=>g});var s=t(62659),a=t(98597),n=t(196),d=t(76504),l=t(80792),u=t(33167),r=t(24517),o=t(91330),h=t(11355);t(9484),t(96334);const v="__NONE_OPTION__",c={cloud:"Home Assistant Cloud"};(0,s.A)([(0,n.EM)("ha-stt-picker")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_engines",value:void 0},{kind:"method",key:"render",value:function(){var e;if(!this._engines)return a.s6;const i=null!==(e=this.value)&&void 0!==e?e:this.required?this._engines.find((e=>{var i;return 0!==(null===(i=e.supported_languages)||void 0===i?void 0:i.length)})):v;return a.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.stt-picker.stt")}
        .value=${i}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${r.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?a.s6:a.qy`<ha-list-item .value=${v}>
              ${this.hass.localize("ui.components.stt-picker.none")}
            </ha-list-item>`}
        ${this._engines.map((e=>{var i;let t=e.engine_id;if(e.engine_id.includes(".")){const i=this.hass.states[e.engine_id];t=i?(0,o.u)(i):e.engine_id}else e.engine_id in c&&(t=c[e.engine_id]);return a.qy`<ha-list-item
            .value=${e.engine_id}
            .disabled=${0===(null===(i=e.supported_languages)||void 0===i?void 0:i.length)}
          >
            ${t}
          </ha-list-item>`}))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,d.A)((0,l.A)(t.prototype),"willUpdate",this).call(this,e),this.hasUpdated?e.has("language")&&this._debouncedUpdateEngines():this._updateEngines()}},{kind:"field",key:"_debouncedUpdateEngines",value(){return(0,h.s)((()=>this._updateEngines()),500)}},{kind:"method",key:"_updateEngines",value:async function(){var e,i,t,s;if(this._engines=(await(i=this.hass,t=this.language,s=this.hass.config.country||void 0,i.callWS({type:"stt/engine/list",language:t,country:s}))).providers,!this.value)return;const a=this._engines.find((e=>e.engine_id===this.value));(0,u.r)(this,"supported-languages-changed",{value:null==a?void 0:a.supported_languages}),a&&0!==(null===(e=a.supported_languages)||void 0===e?void 0:e.length)||(this.value=void 0,(0,u.r)(this,"value-changed",{value:this.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){var i;const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===v||(this.value=t.value===v?void 0:t.value,(0,u.r)(this,"value-changed",{value:this.value}),(0,u.r)(this,"supported-languages-changed",{value:null===(i=this._engines.find((e=>e.engine_id===this.value)))||void 0===i?void 0:i.supported_languages}))}}]}}),a.WF);let g=(0,s.A)([(0,n.EM)("ha-selector-stt")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,i;return a.qy`<ha-stt-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .language=${(null===(e=this.selector.stt)||void 0===e?void 0:e.language)||(null===(i=this.context)||void 0===i?void 0:i.language)}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-stt-picker>`}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    ha-stt-picker {
      width: 100%;
    }
  `}}]}}),a.WF)}};
//# sourceMappingURL=h2l4Z-AA.js.map