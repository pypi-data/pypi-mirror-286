export const id=8387;export const ids=[8387];export const modules={68873:(e,t,r)=>{r.d(t,{a:()=>n});var a=r(6601),i=r(19263);function n(e,t){const r=(0,i.m)(e.entity_id),n=void 0!==t?t:null==e?void 0:e.state;if(["button","event","input_button","scene"].includes(r))return n!==a.Hh;if((0,a.g0)(n))return!1;if(n===a.KF&&"alert"!==r)return!1;switch(r){case"alarm_control_panel":return"disarmed"!==n;case"alert":return"idle"!==n;case"cover":case"valve":return"closed"!==n;case"device_tracker":case"person":return"not_home"!==n;case"lawn_mower":return["mowing","error"].includes(n);case"lock":return"locked"!==n;case"media_player":return"standby"!==n;case"vacuum":return!["idle","docked","paused"].includes(n);case"plant":return"problem"===n;case"group":return["on","home","open","locked","problem"].includes(n);case"timer":return"active"===n;case"camera":return"streaming"===n}return!0}},93259:(e,t,r)=>{var a=r(62659),i=r(76504),n=r(80792),o=r(98597),s=r(196),l=r(90662),d=r(33167);r(91074),r(52631);const u={boolean:()=>r.e(7150).then(r.bind(r,47150)),constant:()=>r.e(3908).then(r.bind(r,73908)),float:()=>r.e(2292).then(r.bind(r,82292)),grid:()=>r.e(6880).then(r.bind(r,96880)),expandable:()=>r.e(6048).then(r.bind(r,66048)),integer:()=>r.e(3172).then(r.bind(r,73172)),multi_select:()=>r.e(5494).then(r.bind(r,95494)),positive_time_period_dict:()=>r.e(8590).then(r.bind(r,38590)),select:()=>r.e(3644).then(r.bind(r,73644)),string:()=>r.e(9345).then(r.bind(r,39345))},c=(e,t)=>e?t.name?e[t.name]:e:null;(0,a.A)([(0,s.EM)("ha-form")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof o.mN&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{var t;"selector"in e||null===(t=u[e.type])||void 0===t||t.call(u)}))}},{kind:"method",key:"render",value:function(){return o.qy`
      <div class="root" part="root">
        ${this.error&&this.error.base?o.qy`
              <ha-alert alert-type="error">
                ${this._computeError(this.error.base,this.schema)}
              </ha-alert>
            `:""}
        ${this.schema.map((e=>{var t;const r=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),a=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return o.qy`
            ${r?o.qy`
                  <ha-alert own-margin alert-type="error">
                    ${this._computeError(r,e)}
                  </ha-alert>
                `:a?o.qy`
                    <ha-alert own-margin alert-type="warning">
                      ${this._computeWarning(a,e)}
                    </ha-alert>
                  `:""}
            ${"selector"in e?o.qy`<ha-selector
                  .schema=${e}
                  .hass=${this.hass}
                  .name=${e.name}
                  .selector=${e.selector}
                  .value=${c(this.data,e)}
                  .label=${this._computeLabel(e,this.data)}
                  .disabled=${e.disabled||this.disabled||!1}
                  .placeholder=${e.required?"":e.default}
                  .helper=${this._computeHelper(e)}
                  .localizeValue=${this.localizeValue}
                  .required=${e.required||!1}
                  .context=${this._generateContext(e)}
                ></ha-selector>`:(0,l._)(this.fieldElementName(e.type),{schema:e,data:c(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:null===(t=this.hass)||void 0===t?void 0:t.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,context:this._generateContext(e),...this.getFormProperties()})}
          `}))}
      </div>
    `}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[r,a]of Object.entries(e.context))t[r]=this.data[a];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,i.A)((0,n.A)(r.prototype),"createRenderRoot",this).call(this);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const r=t.name?{[t.name]:e.detail.value}:e.detail.value;this.data={...this.data,...r},(0,d.r)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?o.qy`<ul>
        ${e.map((e=>o.qy`<li>
              ${this.computeError?this.computeError(e,t):e}
            </li>`))}
      </ul>`:this.computeError?this.computeError(e,t):e}},{kind:"method",key:"_computeWarning",value:function(e,t){return this.computeWarning?this.computeWarning(e,t):e}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      .root > * {
        display: block;
      }
      .root > *:not([own-margin]):not(:last-child) {
        margin-bottom: 24px;
      }
      ha-alert[own-margin] {
        margin-bottom: 4px;
      }
    `}}]}}),o.WF)},6601:(e,t,r)=>{r.d(t,{Hh:()=>i,KF:()=>o,g0:()=>d,s7:()=>s});var a=r(79592);const i="unavailable",n="unknown",o="off",s=[i,n],l=[i,n,o],d=(0,a.g)(s);(0,a.g)(l)}};
//# sourceMappingURL=W_vmeJr2.js.map