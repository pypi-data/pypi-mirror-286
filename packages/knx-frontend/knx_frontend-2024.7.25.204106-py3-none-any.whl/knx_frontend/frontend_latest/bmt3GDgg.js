export const id=1670;export const ids=[1670];export const modules={20678:(e,a,t)=>{t.d(a,{T:()=>i});var l=t(45081);const i=(e,a)=>{try{var t,l;return null!==(t=null===(l=s(a))||void 0===l?void 0:l.of(e))&&void 0!==t?t:e}catch(i){return e}},s=(0,l.A)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})))},24110:(e,a,t)=>{var l={};t.r(l);var i=t(62659),s=t(76504),n=t(80792),o=t(98597),u=t(196),d=t(45081),r=t(33167),v=t(24517),h=t(20678),c=t(66412);t(9484),t(96334);(0,i.A)([(0,u.EM)("ha-language-picker")],(function(e,a){class t extends a{constructor(...a){super(...a),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,u.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,u.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,u.MZ)({type:Array})],key:"languages",value:void 0},{kind:"field",decorators:[(0,u.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,u.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,u.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,u.MZ)({type:Boolean})],key:"nativeName",value(){return!1}},{kind:"field",decorators:[(0,u.MZ)({type:Boolean})],key:"noSort",value(){return!1}},{kind:"field",decorators:[(0,u.wk)()],key:"_defaultLanguages",value(){return[]}},{kind:"field",decorators:[(0,u.P)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,s.A)((0,n.A)(t.prototype),"firstUpdated",this).call(this,e),this._computeDefaultLanguageOptions()}},{kind:"method",key:"updated",value:function(e){(0,s.A)((0,n.A)(t.prototype),"updated",this).call(this,e);const a=e.has("hass")&&this.hass&&e.get("hass")&&e.get("hass").locale.language!==this.hass.locale.language;if(e.has("languages")||e.has("value")||a){var l,i;if(this._select.layoutOptions(),this._select.value!==this.value&&(0,r.r)(this,"value-changed",{value:this._select.value}),!this.value)return;const e=this._getLanguagesOptions(null!==(l=this.languages)&&void 0!==l?l:this._defaultLanguages,this.nativeName,null===(i=this.hass)||void 0===i?void 0:i.locale).findIndex((e=>e.value===this.value));-1===e&&(this.value=void 0),a&&this._select.select(e)}}},{kind:"field",key:"_getLanguagesOptions",value(){return(0,d.A)(((e,a,t)=>{let i=[];if(a){const a=l.translationMetadata.translations;i=e.map((e=>{var t;let l=null===(t=a[e])||void 0===t?void 0:t.nativeName;if(!l)try{l=new Intl.DisplayNames(e,{type:"language",fallback:"code"}).of(e)}catch(i){l=e}return{value:e,label:l}}))}else t&&(i=e.map((e=>({value:e,label:(0,h.T)(e,t)}))));return!this.noSort&&t&&i.sort(((e,a)=>(0,c.S)(e.label,a.label,t.language))),i}))}},{kind:"method",key:"_computeDefaultLanguageOptions",value:function(){this._defaultLanguages=Object.keys(l.translationMetadata.translations)}},{kind:"method",key:"render",value:function(){var e,a,t,l,i,s,n;const u=this._getLanguagesOptions(null!==(e=this.languages)&&void 0!==e?e:this._defaultLanguages,this.nativeName,null===(a=this.hass)||void 0===a?void 0:a.locale),d=null!==(t=this.value)&&void 0!==t?t:this.required?null===(l=u[0])||void 0===l?void 0:l.value:this.value;return o.qy`
      <ha-select
        .label=${null!==(i=this.label)&&void 0!==i?i:(null===(s=this.hass)||void 0===s?void 0:s.localize("ui.components.language-picker.language"))||"Language"}
        .value=${d||""}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${v.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${0===u.length?o.qy`<ha-list-item value=""
              >${(null===(n=this.hass)||void 0===n?void 0:n.localize("ui.components.language-picker.no_languages"))||"No languages"}</ha-list-item
            >`:u.map((e=>o.qy`
                <ha-list-item .value=${e.value}
                  >${e.label}</ha-list-item
                >
              `))}
      </ha-select>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const a=e.target;""!==a.value&&a.value!==this.value&&(this.value=a.value,(0,r.r)(this,"value-changed",{value:this.value}))}}]}}),o.WF)},71670:(e,a,t)=>{t.r(a),t.d(a,{HaLanguageSelector:()=>n});var l=t(62659),i=t(98597),s=t(196);t(24110);let n=(0,l.A)([(0,s.EM)("ha-selector-language")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){var e,a,t;return i.qy`
      <ha-language-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .languages=${null===(e=this.selector.language)||void 0===e?void 0:e.languages}
        .nativeName=${Boolean(null===(a=this.selector)||void 0===a||null===(a=a.language)||void 0===a?void 0:a.native_name)}
        .noSort=${Boolean(null===(t=this.selector)||void 0===t||null===(t=t.language)||void 0===t?void 0:t.no_sort)}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-language-picker>
    `}},{kind:"field",static:!0,key:"styles",value(){return i.AH`
    ha-language-picker {
      width: 100%;
    }
  `}}]}}),i.WF)}};
//# sourceMappingURL=bmt3GDgg.js.map