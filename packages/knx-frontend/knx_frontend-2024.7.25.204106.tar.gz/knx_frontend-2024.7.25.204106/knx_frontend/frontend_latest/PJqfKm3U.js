/*! For license information please see PJqfKm3U.js.LICENSE.txt */
export const id=1301;export const ids=[1301];export const modules={73133:(e,t,i)=>{i.r(t),i.d(t,{HaEntitySelector:()=>y});var s=i(62659),n=i(76504),r=i(80792),l=i(98597),a=i(196),d=i(96041),u=i(33167),o=i(88502),c=i(36831),h=i(45081),v=i(18889);i(85067);(0,s.A)([(0,a.EM)("ha-entities-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"include-unit-of-measurement"})],key:"includeUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"include-entities"})],key:"includeEntities",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"exclude-entities"})],key:"excludeEntities",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:"picked-entity-label"})],key:"pickedEntityLabel",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:"pick-entity-label"})],key:"pickEntityLabel",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array})],key:"createDomains",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return l.s6;const e=this._currentEntities;return l.qy`
      ${e.map((e=>l.qy`
          <div>
            <ha-entity-picker
              allow-custom-entity
              .curValue=${e}
              .hass=${this.hass}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeEntities=${this.includeEntities}
              .excludeEntities=${this.excludeEntities}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
              .entityFilter=${this._getEntityFilter(this.value,this.entityFilter)}
              .value=${e}
              .label=${this.pickedEntityLabel}
              .disabled=${this.disabled}
              .createDomains=${this.createDomains}
              @value-changed=${this._entityChanged}
            ></ha-entity-picker>
          </div>
        `))}
      <div>
        <ha-entity-picker
          allow-custom-entity
          .hass=${this.hass}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeEntities=${this.includeEntities}
          .excludeEntities=${this.excludeEntities}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
          .entityFilter=${this._getEntityFilter(this.value,this.entityFilter)}
          .label=${this.pickEntityLabel}
          .helper=${this.helper}
          .disabled=${this.disabled}
          .createDomains=${this.createDomains}
          .required=${this.required&&!e.length}
          @value-changed=${this._addEntity}
        ></ha-entity-picker>
      </div>
    `}},{kind:"field",key:"_getEntityFilter",value(){return(0,h.A)(((e,t)=>i=>(!e||!e.includes(i.entity_id))&&(!t||t(i))))}},{kind:"get",key:"_currentEntities",value:function(){return this.value||[]}},{kind:"method",key:"_updateEntities",value:async function(e){this.value=e,(0,u.r)(this,"value-changed",{value:e})}},{kind:"method",key:"_entityChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t||void 0!==i&&!(0,v.n)(i))return;const s=this._currentEntities;i&&!s.includes(i)?this._updateEntities(s.map((e=>e===t?i:e))):this._updateEntities(s.filter((e=>e!==t)))}},{kind:"method",key:"_addEntity",value:async function(e){e.stopPropagation();const t=e.detail.value;if(!t)return;if(e.currentTarget.value="",!t)return;const i=this._currentEntities;i.includes(t)||this._updateEntities([...i,t])}},{kind:"field",static:!0,key:"styles",value(){return l.AH`
    div {
      margin-top: 8px;
    }
  `}}]}}),l.WF);let y=(0,s.A)([(0,a.EM)("ha-selector-entity")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,a.wk)()],key:"_createDomains",value:void 0},{kind:"method",key:"_hasIntegration",value:function(e){var t;return(null===(t=e.entity)||void 0===t?void 0:t.filter)&&(0,d.e)(e.entity.filter).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){var t,i;e.has("selector")&&void 0!==this.value&&(null!==(t=this.selector.entity)&&void 0!==t&&t.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,u.r)(this,"value-changed",{value:this.value})):null!==(i=this.selector.entity)&&void 0!==i&&i.multiple||!Array.isArray(this.value)||(this.value=this.value[0],(0,u.r)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"render",value:function(){var e,t,i;return this._hasIntegration(this.selector)&&!this._entitySources?l.s6:null!==(e=this.selector.entity)&&void 0!==e&&e.multiple?l.qy`
      ${this.label?l.qy`<label>${this.label}</label>`:""}
      <ha-entities-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .includeEntities=${this.selector.entity.include_entities}
        .excludeEntities=${this.selector.entity.exclude_entities}
        .entityFilter=${this._filterEntities}
        .createDomains=${this._createDomains}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-entities-picker>
    `:l.qy`<ha-entity-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .includeEntities=${null===(t=this.selector.entity)||void 0===t?void 0:t.include_entities}
        .excludeEntities=${null===(i=this.selector.entity)||void 0===i?void 0:i.exclude_entities}
        .entityFilter=${this._filterEntities}
        .createDomains=${this._createDomains}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-entity
      ></ha-entity-picker>`}},{kind:"method",key:"updated",value:function(e){(0,n.A)((0,r.A)(i.prototype),"updated",this).call(this,e),e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,o.c)(this.hass).then((e=>{this._entitySources=e})),e.has("selector")&&(this._createDomains=(0,c.Lo)(this.selector))}},{kind:"field",key:"_filterEntities",value(){return e=>{var t;return null===(t=this.selector)||void 0===t||null===(t=t.entity)||void 0===t||!t.filter||(0,d.e)(this.selector.entity.filter).some((t=>(0,c.Ru)(t,e,this._entitySources)))}}}]}}),l.WF)},86625:(e,t,i)=>{i.d(t,{T:()=>h});var s=i(34078),n=i(3982),r=i(3267);class l{constructor(e){this.G=e}disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}}class a{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var e;null!==(e=this.Y)&&void 0!==e||(this.Y=new Promise((e=>this.Z=e)))}resume(){var e;null===(e=this.Z)||void 0===e||e.call(this),this.Y=this.Z=void 0}}var d=i(2154);const u=e=>!(0,n.sO)(e)&&"function"==typeof e.then,o=1073741823;class c extends r.Kq{constructor(){super(...arguments),this._$C_t=o,this._$Cwt=[],this._$Cq=new l(this),this._$CK=new a}render(...e){var t;return null!==(t=e.find((e=>!u(e))))&&void 0!==t?t:s.c0}update(e,t){const i=this._$Cwt;let n=i.length;this._$Cwt=t;const r=this._$Cq,l=this._$CK;this.isConnected||this.disconnected();for(let s=0;s<t.length&&!(s>this._$C_t);s++){const e=t[s];if(!u(e))return this._$C_t=s,e;s<n&&e===i[s]||(this._$C_t=o,n=0,Promise.resolve(e).then((async t=>{for(;l.get();)await l.get();const i=r.deref();if(void 0!==i){const s=i._$Cwt.indexOf(e);s>-1&&s<i._$C_t&&(i._$C_t=s,i.setValue(t))}})))}return s.c0}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const h=(0,d.u$)(c)}};
//# sourceMappingURL=PJqfKm3U.js.map