export const id=5519;export const ids=[5519];export const modules={32872:(e,o,a)=>{a.d(o,{x:()=>i});const i=(e,o)=>e&&e.config.components.includes(o)},14656:(e,o,a)=>{a.d(o,{v:()=>i});const i=(e,o,a,i)=>{const[s,t,d]=e.split(".",3);return Number(s)>o||Number(s)===o&&(void 0===i?Number(t)>=a:Number(t)>a)||void 0!==i&&Number(s)===o&&Number(t)===a&&Number(d)>=i}},55519:(e,o,a)=>{a.r(o),a.d(o,{HaAddonSelector:()=>c});var i=a(62659),s=a(98597),t=a(196),d=a(32872),r=a(33167),n=a(66412),l=a(14656),u=a(12263);a(91074),a(66442),a(9484);const h=e=>s.qy`<ha-list-item twoline graphic="icon">
    <span>${e.name}</span>
    <span slot="secondary">${e.slug}</span>
    ${e.icon?s.qy`<img
          alt=""
          slot="graphic"
          .src="/api/hassio/addons/${e.slug}/icon"
        />`:""}
  </ha-list-item>`;(0,i.A)([(0,t.EM)("ha-addon-picker")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"value",value(){return""}},{kind:"field",decorators:[(0,t.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,t.wk)()],key:"_addons",value:void 0},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,t.P)("ha-combo-box")],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,t.wk)()],key:"_error",value:void 0},{kind:"method",key:"open",value:function(){var e;null===(e=this._comboBox)||void 0===e||e.open()}},{kind:"method",key:"focus",value:function(){var e;null===(e=this._comboBox)||void 0===e||e.focus()}},{kind:"method",key:"firstUpdated",value:function(){this._getAddons()}},{kind:"method",key:"render",value:function(){return this._error?s.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:this._addons?s.qy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.addon-picker.addon"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .renderer=${h}
        .items=${this._addons}
        item-value-path="slug"
        item-id-path="slug"
        item-label-path="name"
        @value-changed=${this._addonChanged}
      ></ha-combo-box>
    `:s.s6}},{kind:"method",key:"_getAddons",value:async function(){try{if((0,d.x)(this.hass,"hassio")){const e=await(async e=>(0,l.v)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/addons",method:"get"}):(0,u.PS)(await e.callApi("GET","hassio/addons")))(this.hass);this._addons=e.addons.filter((e=>e.version)).sort(((e,o)=>(0,n.x)(e.name,o.name,this.hass.locale.language)))}else this._error=this.hass.localize("ui.components.addon-picker.error.no_supervisor")}catch(e){this._error=this.hass.localize("ui.components.addon-picker.error.fetch_addons")}}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_addonChanged",value:function(e){e.stopPropagation();const o=e.detail.value;o!==this._value&&this._setValue(o)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,r.r)(this,"value-changed",{value:e}),(0,r.r)(this,"change")}),0)}}]}}),s.WF);let c=(0,i.A)([(0,t.EM)("ha-selector-addon")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",decorators:[(0,t.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,t.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return s.qy`<ha-addon-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      allow-custom-entity
    ></ha-addon-picker>`}},{kind:"field",static:!0,key:"styles",value(){return s.AH`
    ha-addon-picker {
      width: 100%;
    }
  `}}]}}),s.WF)},12263:(e,o,a)=>{a.d(o,{PS:()=>i,VR:()=>s});const i=e=>e.data,s=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])}};
//# sourceMappingURL=Sz8729Eh.js.map