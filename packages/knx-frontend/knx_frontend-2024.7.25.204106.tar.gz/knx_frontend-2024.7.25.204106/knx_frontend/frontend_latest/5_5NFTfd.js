export const id=5853;export const ids=[5853];export const modules={95853:(e,i,t)=>{t.r(i),t.d(i,{HaAreaSelector:()=>k});var s=t(62659),a=t(98597),r=t(196),d=t(45081),l=t(96041),n=t(71378),o=t(33167),u=t(88502),c=t(81407),h=t(36831),v=(t(57046),t(28226));(0,s.A)([(0,r.EM)("ha-areas-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"no-add"})],key:"noAdd",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:"picked-area-label"})],key:"pickedAreaLabel",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:"pick-area-label"})],key:"pickAreaLabel",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"method",key:"render",value:function(){if(!this.hass)return a.s6;const e=this._currentAreas;return a.qy`
      ${e.map((e=>a.qy`
          <div>
            <ha-area-picker
              .curValue=${e}
              .noAdd=${this.noAdd}
              .hass=${this.hass}
              .value=${e}
              .label=${this.pickedAreaLabel}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .deviceFilter=${this.deviceFilter}
              .entityFilter=${this.entityFilter}
              .disabled=${this.disabled}
              @value-changed=${this._areaChanged}
            ></ha-area-picker>
          </div>
        `))}
      <div>
        <ha-area-picker
          .noAdd=${this.noAdd}
          .hass=${this.hass}
          .label=${this.pickAreaLabel}
          .helper=${this.helper}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .deviceFilter=${this.deviceFilter}
          .entityFilter=${this.entityFilter}
          .disabled=${this.disabled}
          .placeholder=${this.placeholder}
          .required=${this.required&&!e.length}
          @value-changed=${this._addArea}
          .excludeAreas=${e}
        ></ha-area-picker>
      </div>
    `}},{kind:"get",key:"_currentAreas",value:function(){return this.value||[]}},{kind:"method",key:"_updateAreas",value:async function(e){this.value=e,(0,o.r)(this,"value-changed",{value:e})}},{kind:"method",key:"_areaChanged",value:function(e){e.stopPropagation();const i=e.currentTarget.curValue,t=e.detail.value;if(t===i)return;const s=this._currentAreas;t&&!s.includes(t)?this._updateAreas(s.map((e=>e===i?t:e))):this._updateAreas(s.filter((e=>e!==i)))}},{kind:"method",key:"_addArea",value:function(e){e.stopPropagation();const i=e.detail.value;if(!i)return;e.currentTarget.value="";const t=this._currentAreas;t.includes(i)||this._updateAreas([...t,i])}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    div {
      margin-top: 8px;
    }
  `}}]}}),(0,v.E)(a.WF));let k=(0,s.A)([(0,r.EM)("ha-selector-area")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,r.wk)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_configEntries",value:void 0},{kind:"field",key:"_deviceIntegrationLookup",value(){return(0,d.A)(n.fk)}},{kind:"method",key:"_hasIntegration",value:function(e){var i,t;return(null===(i=e.area)||void 0===i?void 0:i.entity)&&(0,l.e)(e.area.entity).some((e=>e.integration))||(null===(t=e.area)||void 0===t?void 0:t.device)&&(0,l.e)(e.area.device).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){var i,t;e.has("selector")&&void 0!==this.value&&(null!==(i=this.selector.area)&&void 0!==i&&i.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,o.r)(this,"value-changed",{value:this.value})):null!==(t=this.selector.area)&&void 0!==t&&t.multiple||!Array.isArray(this.value)||(this.value=this.value[0],(0,o.r)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"updated",value:function(e){e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,u.c)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,c.VN)(this.hass).then((e=>{this._configEntries=e})))}},{kind:"method",key:"render",value:function(){var e,i,t,s,r;return this._hasIntegration(this.selector)&&!this._entitySources?a.s6:null!==(e=this.selector.area)&&void 0!==e&&e.multiple?a.qy`
      <ha-areas-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .pickAreaLabel=${this.label}
        no-add
        .deviceFilter=${null!==(i=this.selector.area)&&void 0!==i&&i.device?this._filterDevices:void 0}
        .entityFilter=${null!==(t=this.selector.area)&&void 0!==t&&t.entity?this._filterEntities:void 0}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-areas-picker>
    `:a.qy`
        <ha-area-picker
          .hass=${this.hass}
          .value=${this.value}
          .label=${this.label}
          .helper=${this.helper}
          no-add
          .deviceFilter=${null!==(s=this.selector.area)&&void 0!==s&&s.device?this._filterDevices:void 0}
          .entityFilter=${null!==(r=this.selector.area)&&void 0!==r&&r.entity?this._filterEntities:void 0}
          .disabled=${this.disabled}
          .required=${this.required}
        ></ha-area-picker>
      `}},{kind:"field",key:"_filterEntities",value(){return e=>{var i;return null===(i=this.selector.area)||void 0===i||!i.entity||(0,l.e)(this.selector.area.entity).some((i=>(0,h.Ru)(i,e,this._entitySources)))}}},{kind:"field",key:"_filterDevices",value(){return e=>{var i;if(null===(i=this.selector.area)||void 0===i||!i.device)return!0;const t=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,l.e)(this.selector.area.device).some((i=>(0,h.vX)(i,e,t)))}}}]}}),a.WF)},88502:(e,i,t)=>{t.d(i,{c:()=>r});const s=async(e,i,t,a,r,...d)=>{const l=r,n=l[e],o=n=>a&&a(r,n.result)!==n.cacheKey?(l[e]=void 0,s(e,i,t,a,r,...d)):n.result;if(n)return n instanceof Promise?n.then(o):o(n);const u=t(r,...d);return l[e]=u,u.then((t=>{l[e]={result:t,cacheKey:null==a?void 0:a(r,t)},setTimeout((()=>{l[e]=void 0}),i)}),(()=>{l[e]=void 0})),u},a=e=>e.callWS({type:"entity/source"}),r=e=>s("_entitySources",3e4,a,(e=>Object.keys(e.states).length),e)},28226:(e,i,t)=>{t.d(i,{E:()=>l});var s=t(62659),a=t(76504),r=t(80792),d=t(196);const l=e=>(0,s.A)(null,(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.A)((0,r.A)(t.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,a.A)((0,r.A)(t.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){if((0,a.A)((0,r.A)(t.prototype),"updated",this).call(this,e),e.has("hass"))this.__checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const i of e.keys())if(this.hassSubscribeRequiredHostProps.includes(i))return void this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){var e;void 0!==this.__unsubs||!this.isConnected||void 0===this.hass||null!==(e=this.hassSubscribeRequiredHostProps)&&void 0!==e&&e.some((e=>void 0===this[e]))||(this.__unsubs=this.hassSubscribe())}}]}}),e)}};
//# sourceMappingURL=5_5NFTfd.js.map