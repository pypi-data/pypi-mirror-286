export const id=1940;export const ids=[1940];export const modules={1940:(e,i,t)=>{t.r(i),t.d(i,{HaTTSVoiceSelector:()=>l});var s=t(62659),a=t(98597),d=t(196);t(75973);let l=(0,s.A)([(0,d.EM)("ha-selector-tts_voice")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,i,t,s;return a.qy`<ha-tts-voice-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .language=${(null===(e=this.selector.tts_voice)||void 0===e?void 0:e.language)||(null===(i=this.context)||void 0===i?void 0:i.language)}
      .engineId=${(null===(t=this.selector.tts_voice)||void 0===t?void 0:t.engineId)||(null===(s=this.context)||void 0===s?void 0:s.engineId)}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-tts-voice-picker>`}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    ha-tts-picker {
      width: 100%;
    }
  `}}]}}),a.WF)},75973:(e,i,t)=>{var s=t(62659),a=t(76504),d=t(80792),l=t(98597),o=t(196),n=t(33167),u=t(24517),r=t(11355),v=t(6933);t(9484),t(96334);const c="__NONE_OPTION__";(0,s.A)([(0,o.EM)("ha-tts-voice-picker")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,o.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"engineId",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_voices",value:void 0},{kind:"field",decorators:[(0,o.P)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"render",value:function(){var e,i;if(!this._voices)return l.s6;const t=null!==(e=this.value)&&void 0!==e?e:this.required?null===(i=this._voices[0])||void 0===i?void 0:i.voice_id:c;return l.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.tts-voice-picker.voice")}
        .value=${t}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${u.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?l.s6:l.qy`<ha-list-item .value=${c}>
              ${this.hass.localize("ui.components.tts-voice-picker.none")}
            </ha-list-item>`}
        ${this._voices.map((e=>l.qy`<ha-list-item .value=${e.voice_id}>
              ${e.name}
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,a.A)((0,d.A)(t.prototype),"willUpdate",this).call(this,e),this.hasUpdated?(e.has("language")||e.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}},{kind:"field",key:"_debouncedUpdateVoices",value(){return(0,r.s)((()=>this._updateVoices()),500)}},{kind:"method",key:"_updateVoices",value:async function(){this.engineId&&this.language?(this._voices=(await(0,v.z3)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((e=>e.voice_id===this.value))||(this.value=void 0,(0,n.r)(this,"value-changed",{value:this.value})))):this._voices=void 0}},{kind:"method",key:"updated",value:function(e){var i,s,l;((0,a.A)((0,d.A)(t.prototype),"updated",this).call(this,e),e.has("_voices")&&(null===(i=this._select)||void 0===i?void 0:i.value)!==this.value)&&(null===(s=this._select)||void 0===s||s.layoutOptions(),(0,n.r)(this,"value-changed",{value:null===(l=this._select)||void 0===l?void 0:l.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return l.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const i=e.target;!this.hass||""===i.value||i.value===this.value||void 0===this.value&&i.value===c||(this.value=i.value===c?void 0:i.value,(0,n.r)(this,"value-changed",{value:this.value}))}}]}}),l.WF)},6933:(e,i,t)=>{t.d(i,{EF:()=>d,Xv:()=>l,ni:()=>a,u1:()=>o,z3:()=>n});const s="media-source://tts/",a=e=>e.startsWith(s),d=e=>e.substring(19),l=(e,i,t)=>e.callWS({type:"tts/engine/list",language:i,country:t}),o=(e,i)=>e.callWS({type:"tts/engine/get",engine_id:i}),n=(e,i,t)=>e.callWS({type:"tts/engine/voices",engine_id:i,language:t})}};
//# sourceMappingURL=QRyGvG-A.js.map