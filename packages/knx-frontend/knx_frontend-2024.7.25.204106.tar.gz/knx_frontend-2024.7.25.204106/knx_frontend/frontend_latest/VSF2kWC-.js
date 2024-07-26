export const id=8136;export const ids=[8136];export const modules={88136:(e,t,i)=>{i.r(t),i.d(t,{HaSelectorAttribute:()=>n});var a=i(62659),o=i(76504),d=i(80792),s=i(98597),l=i(196),r=i(33167),u=i(44540);i(66442);(0,a.A)([(0,l.EM)("ha-entity-attribute-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"entityId",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Array,attribute:"hide-attributes"})],key:"hideAttributes",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean,attribute:"allow-custom-value"})],key:"allowCustomValue",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,l.P)("ha-combo-box",!0)],key:"_comboBox",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return!(!e.has("_opened")&&this._opened)}},{kind:"method",key:"updated",value:function(e){if(e.has("_opened")&&this._opened){const e=this.entityId?this.hass.states[this.entityId]:void 0;this._comboBox.items=e?Object.keys(e.attributes).filter((e=>{var t;return!(null!==(t=this.hideAttributes)&&void 0!==t&&t.includes(e))})).map((t=>({value:t,label:(0,u.R)(this.hass.localize,e,this.hass.entities,t)}))):[]}}},{kind:"method",key:"render",value:function(){var e;return this.hass?s.qy`
      <ha-combo-box
        .hass=${this.hass}
        .value=${this.value?(0,u.R)(this.hass.localize,this.hass.states[this.entityId],this.hass.entities,this.value):""}
        .autofocus=${this.autofocus}
        .label=${null!==(e=this.label)&&void 0!==e?e:this.hass.localize("ui.components.entity.entity-attribute-picker.attribute")}
        .disabled=${this.disabled||!this.entityId}
        .required=${this.required}
        .helper=${this.helper}
        .allowCustomValue=${this.allowCustomValue}
        item-value-path="value"
        item-label-path="label"
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
      </ha-combo-box>
    `:s.s6}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){this.value=e.detail.value}}]}}),s.WF);let n=(0,a.A)([(0,l.EM)("ha-selector-attribute")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,t,i;return s.qy`
      <ha-entity-attribute-picker
        .hass=${this.hass}
        .entityId=${(null===(e=this.selector.attribute)||void 0===e?void 0:e.entity_id)||(null===(t=this.context)||void 0===t?void 0:t.filter_entity)}
        .hideAttributes=${null===(i=this.selector.attribute)||void 0===i?void 0:i.hide_attributes}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-value
      ></ha-entity-attribute-picker>
    `}},{kind:"method",key:"updated",value:function(e){var t;if((0,o.A)((0,d.A)(i.prototype),"updated",this).call(this,e),!this.value||null!==(t=this.selector.attribute)&&void 0!==t&&t.entity_id||!e.has("context"))return;const a=e.get("context");if(!this.context||!a||a.filter_entity===this.context.filter_entity)return;let s=!1;if(this.context.filter_entity){const e=this.hass.states[this.context.filter_entity];e&&this.value in e.attributes||(s=!0)}else s=void 0!==this.value;s&&(0,r.r)(this,"value-changed",{value:void 0})}}]}}),s.WF)}};
//# sourceMappingURL=VSF2kWC-.js.map