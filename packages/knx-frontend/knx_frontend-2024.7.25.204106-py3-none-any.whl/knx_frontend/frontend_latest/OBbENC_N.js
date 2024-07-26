export const id=7674;export const ids=[7674];export const modules={20678:(e,i,t)=>{t.d(i,{T:()=>s});var l=t(45081);const s=(e,i)=>{try{var t,l;return null!==(t=null===(l=a(i))||void 0===l?void 0:l.of(e))&&void 0!==t?t:e}catch(s){return e}},a=(0,l.A)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})))},54625:(e,i,t)=>{var l=t(62659),s=t(76504),a=t(80792),d=t(98597),r=t(196),n=t(33167),o=t(24517),u=t(20678);t(9484),t(96334);const p="preferred",c="last_used";(0,l.A)([(0,r.EM)("ha-assist-pipeline-picker")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"includeLastUsed",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_pipelines",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_preferredPipeline",value(){return null}},{kind:"get",key:"_default",value:function(){return this.includeLastUsed?c:p}},{kind:"method",key:"render",value:function(){var e,i;if(!this._pipelines)return d.s6;const t=null!==(e=this.value)&&void 0!==e?e:this._default;return d.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.pipeline-picker.pipeline")}
        .value=${t}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${o.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.includeLastUsed?d.qy`
              <ha-list-item .value=${c}>
                ${this.hass.localize("ui.components.pipeline-picker.last_used")}
              </ha-list-item>
            `:null}
        <ha-list-item .value=${p}>
          ${this.hass.localize("ui.components.pipeline-picker.preferred",{preferred:null===(i=this._pipelines.find((e=>e.id===this._preferredPipeline)))||void 0===i?void 0:i.name})}
        </ha-list-item>
        ${this._pipelines.map((e=>d.qy`<ha-list-item .value=${e.id}>
              ${e.name}
              (${(0,u.T)(e.language,this.hass.locale)})
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"firstUpdated",value:function(e){var i;(0,s.A)((0,a.A)(t.prototype),"firstUpdated",this).call(this,e),(i=this.hass,i.callWS({type:"assist_pipeline/pipeline/list"})).then((e=>{this._pipelines=e.pipelines,this._preferredPipeline=e.preferred_pipeline}))}},{kind:"get",static:!0,key:"styles",value:function(){return d.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const i=e.target;!this.hass||""===i.value||i.value===this.value||void 0===this.value&&i.value===this._default||(this.value=i.value===this._default?void 0:i.value,(0,n.r)(this,"value-changed",{value:this.value}))}}]}}),d.WF)},97674:(e,i,t)=>{t.r(i),t.d(i,{HaAssistPipelineSelector:()=>d});var l=t(62659),s=t(98597),a=t(196);t(54625);let d=(0,l.A)([(0,a.EM)("ha-selector-assist_pipeline")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){var e;return s.qy`
      <ha-assist-pipeline-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .includeLastUsed=${Boolean(null===(e=this.selector.assist_pipeline)||void 0===e?void 0:e.include_last_used)}
      ></ha-assist-pipeline-picker>
    `}},{kind:"field",static:!0,key:"styles",value(){return s.AH`
    ha-conversation-agent-picker {
      width: 100%;
    }
  `}}]}}),s.WF)}};
//# sourceMappingURL=OBbENC_N.js.map