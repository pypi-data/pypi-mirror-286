/*! For license information please see W5Rc0CG1.js.LICENSE.txt */
export const id=8709;export const ids=[8709];export const modules={18709:(e,t,i)=>{i.r(t),i.d(t,{HaIconSelector:()=>a});var s=i(62659),o=i(98597),n=i(196),r=i(86625),d=i(33167),l=i(74538);i(45063);let a=(0,s.A)([(0,n.EM)("ha-selector-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,t,i,s;const n=null===(e=this.context)||void 0===e?void 0:e.icon_entity,d=n?this.hass.states[n]:void 0,a=(null===(t=this.selector.icon)||void 0===t?void 0:t.placeholder)||(null==d?void 0:d.attributes.icon)||d&&(0,r.T)((0,l.fq)(this.hass,d));return o.qy`
      <ha-icon-picker
        .hass=${this.hass}
        .label=${this.label}
        .value=${this.value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .placeholder=${null!==(i=null===(s=this.selector.icon)||void 0===s?void 0:s.placeholder)&&void 0!==i?i:a}
        @value-changed=${this._valueChanged}
      >
        ${!a&&d?o.qy`
              <ha-state-icon
                slot="fallback"
                .hass=${this.hass}
                .stateObj=${d}
              ></ha-state-icon>
            `:o.s6}
      </ha-icon-picker>
    `}},{kind:"method",key:"_valueChanged",value:function(e){(0,d.r)(this,"value-changed",{value:e.detail.value})}}]}}),o.WF)},86625:(e,t,i)=>{i.d(t,{T:()=>u});var s=i(34078),o=i(3982),n=i(3267);class r{constructor(e){this.G=e}disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}}class d{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var e;null!==(e=this.Y)&&void 0!==e||(this.Y=new Promise((e=>this.Z=e)))}resume(){var e;null===(e=this.Z)||void 0===e||e.call(this),this.Y=this.Z=void 0}}var l=i(2154);const a=e=>!(0,o.sO)(e)&&"function"==typeof e.then,c=1073741823;class h extends n.Kq{constructor(){super(...arguments),this._$C_t=c,this._$Cwt=[],this._$Cq=new r(this),this._$CK=new d}render(...e){var t;return null!==(t=e.find((e=>!a(e))))&&void 0!==t?t:s.c0}update(e,t){const i=this._$Cwt;let o=i.length;this._$Cwt=t;const n=this._$Cq,r=this._$CK;this.isConnected||this.disconnected();for(let s=0;s<t.length&&!(s>this._$C_t);s++){const e=t[s];if(!a(e))return this._$C_t=s,e;s<o&&e===i[s]||(this._$C_t=c,o=0,Promise.resolve(e).then((async t=>{for(;r.get();)await r.get();const i=n.deref();if(void 0!==i){const s=i._$Cwt.indexOf(e);s>-1&&s<i._$C_t&&(i._$C_t=s,i.setValue(t))}})))}return s.c0}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const u=(0,l.u$)(h)}};
//# sourceMappingURL=W5Rc0CG1.js.map