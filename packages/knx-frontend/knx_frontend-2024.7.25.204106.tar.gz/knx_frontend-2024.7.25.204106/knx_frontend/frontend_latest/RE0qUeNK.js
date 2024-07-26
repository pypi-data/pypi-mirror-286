export const id=6038;export const ids=[6038];export const modules={32872:(e,t,i)=>{i.d(t,{x:()=>a});const a=(e,t)=>e&&e.config.components.includes(t)},14656:(e,t,i)=>{i.d(t,{v:()=>a});const a=(e,t,i,a)=>{const[o,r,n]=e.split(".",3);return Number(o)>t||Number(o)===t&&(void 0===a?Number(r)>=i:Number(r)>i)||void 0!==a&&Number(o)===t&&Number(r)===i&&Number(n)>=a}},20678:(e,t,i)=>{i.d(t,{T:()=>o});var a=i(45081);const o=(e,t)=>{try{var i,a;return null!==(i=null===(a=r(t))||void 0===a?void 0:a.of(e))&&void 0!==i?i:e}catch(o){return e}},r=(0,a.A)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})))},4449:(e,t,i)=>{function a(e,t,i){return t.reduce(((e,t,a,o)=>{if(void 0!==e){if(!e[t]&&i){const i=o[a+1];e[t]=void 0===i||"number"==typeof i?[]:{}}return e[t]}}),e)}function o(e,t,i,o,r){const n=Array.isArray(e)?[...e]:{...e},s=o?a(n,o):n,l=r?a(n,r,!0):n;if(!Array.isArray(s)||!Array.isArray(l))return e;const d=s.splice(t,1)[0];return l.splice(i,0,d),n}i.d(t,{w:()=>o})},57162:(e,t,i)=>{i.d(t,{l:()=>a});const a=async e=>{if(navigator.clipboard)try{return void(await navigator.clipboard.writeText(e))}catch(i){}const t=document.createElement("textarea");t.value=e,document.body.appendChild(t),t.select(),document.execCommand("copy"),document.body.removeChild(t)}},54625:(e,t,i)=>{var a=i(62659),o=i(76504),r=i(80792),n=i(98597),s=i(196),l=i(33167),d=i(24517),c=i(20678);i(9484),i(96334);const u="preferred",h="last_used";(0,a.A)([(0,s.EM)("ha-assist-pipeline-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"includeLastUsed",value(){return!1}},{kind:"field",decorators:[(0,s.wk)()],key:"_pipelines",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_preferredPipeline",value(){return null}},{kind:"get",key:"_default",value:function(){return this.includeLastUsed?h:u}},{kind:"method",key:"render",value:function(){var e,t;if(!this._pipelines)return n.s6;const i=null!==(e=this.value)&&void 0!==e?e:this._default;return n.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.pipeline-picker.pipeline")}
        .value=${i}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${d.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.includeLastUsed?n.qy`
              <ha-list-item .value=${h}>
                ${this.hass.localize("ui.components.pipeline-picker.last_used")}
              </ha-list-item>
            `:null}
        <ha-list-item .value=${u}>
          ${this.hass.localize("ui.components.pipeline-picker.preferred",{preferred:null===(t=this._pipelines.find((e=>e.id===this._preferredPipeline)))||void 0===t?void 0:t.name})}
        </ha-list-item>
        ${this._pipelines.map((e=>n.qy`<ha-list-item .value=${e.id}>
              ${e.name}
              (${(0,c.T)(e.language,this.hass.locale)})
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"firstUpdated",value:function(e){var t;(0,o.A)((0,r.A)(i.prototype),"firstUpdated",this).call(this,e),(t=this.hass,t.callWS({type:"assist_pipeline/pipeline/list"})).then((e=>{this._pipelines=e.pipelines,this._preferredPipeline=e.preferred_pipeline}))}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===this._default||(this.value=t.value===this._default?void 0:t.value,(0,l.r)(this,"value-changed",{value:this.value}))}}]}}),n.WF)},51029:(e,t,i)=>{var a=i(62659),o=i(76504),r=i(80792),n=i(98597),s=i(196),l=i(45081),d=i(33167),c=i(24517);const u={key:"Mod-s",run:e=>((0,d.r)(e.dom,"editor-save"),!0)},h=e=>{const t=document.createElement("ha-icon");return t.icon=e.label,t};(0,a.A)([(0,s.EM)("ha-code-editor")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"mode",value(){return"yaml"}},{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"readOnly",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"linewrap",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean,attribute:"autocomplete-entities"})],key:"autocompleteEntities",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean,attribute:"autocomplete-icons"})],key:"autocompleteIcons",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"error",value(){return!1}},{kind:"field",decorators:[(0,s.wk)()],key:"_value",value(){return""}},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"field",key:"_iconList",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;const e=this._loadedCodeMirror.highlightingFor(this.codemirror.state,[this._loadedCodeMirror.tags.comment]);return!!this.renderRoot.querySelector(`span.${e}`)}},{kind:"method",key:"connectedCallback",value:function(){(0,o.A)((0,r.A)(a.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this.requestUpdate(),this.addEventListener("keydown",c.d),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.A)((0,r.A)(a.prototype),"disconnectedCallback",this).call(this),this.removeEventListener("keydown",c.d),this.updateComplete.then((()=>{this.codemirror.destroy(),delete this.codemirror}))}},{kind:"method",key:"scheduleUpdate",value:async function(){var e;null!==(e=this._loadedCodeMirror)&&void 0!==e||(this._loadedCodeMirror=await Promise.all([i.e(9076),i.e(8791)]).then(i.bind(i,78791))),(0,o.A)((0,r.A)(a.prototype),"scheduleUpdate",this).call(this)}},{kind:"method",key:"update",value:function(e){if((0,o.A)((0,r.A)(a.prototype),"update",this).call(this,e),!this.codemirror)return void this._createCodeMirror();const t=[];e.has("mode")&&t.push({effects:this._loadedCodeMirror.langCompartment.reconfigure(this._mode)}),e.has("readOnly")&&t.push({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("linewrap")&&t.push({effects:this._loadedCodeMirror.linewrapCompartment.reconfigure(this.linewrap?this._loadedCodeMirror.EditorView.lineWrapping:[])}),e.has("_value")&&this._value!==this.value&&t.push({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),t.length>0&&this.codemirror.dispatch(...t),e.has("error")&&this.classList.toggle("error-state",this.error)}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_createCodeMirror",value:function(){if(!this._loadedCodeMirror)throw new Error("Cannot create editor before CodeMirror is loaded");const e=[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.history(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.crosshairCursor(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.keymap.of([...this._loadedCodeMirror.defaultKeymap,...this._loadedCodeMirror.searchKeymap,...this._loadedCodeMirror.historyKeymap,...this._loadedCodeMirror.tabKeyBindings,u]),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.haTheme,this._loadedCodeMirror.haSyntaxHighlighting,this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.linewrapCompartment.of(this.linewrap?this._loadedCodeMirror.EditorView.lineWrapping:[]),this._loadedCodeMirror.EditorView.updateListener.of(this._onUpdate)];if(!this.readOnly){const t=[];this.autocompleteEntities&&this.hass&&t.push(this._entityCompletions.bind(this)),this.autocompleteIcons&&t.push(this._mdiCompletions.bind(this)),t.length>0&&e.push(this._loadedCodeMirror.autocompletion({override:t,maxRenderedOptions:10}))}this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:e}),parent:this.renderRoot})}},{kind:"field",key:"_getStates",value(){return(0,l.A)((e=>{if(!e)return[];return Object.keys(e).map((t=>({type:"variable",label:t,detail:e[t].attributes.friendly_name,info:`State: ${e[t].state}`})))}))}},{kind:"method",key:"_entityCompletions",value:function(e){const t=e.matchBefore(/[a-z_]{3,}\.\w*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=this._getStates(this.hass.states);return i&&i.length?{from:Number(t.from),options:i,validFor:/^[a-z_]{3,}\.\w*$/}:null}},{kind:"field",key:"_getIconItems",value(){return async()=>{if(!this._iconList){let e;e=(await i.e(3174).then(i.t.bind(i,83174,19))).default,this._iconList=e.map((e=>({type:"variable",label:`mdi:${e.name}`,detail:e.keywords.join(", "),info:h})))}return this._iconList}}},{kind:"method",key:"_mdiCompletions",value:async function(e){const t=e.matchBefore(/mdi:\S*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=await this._getIconItems();return{from:Number(t.from),options:i,validFor:/^mdi:\S*$/}}},{kind:"field",key:"_onUpdate",value(){return e=>{e.docChanged&&(this._value=e.state.doc.toString(),(0,d.r)(this,"value-changed",{value:this._value}))}}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      :host(.error-state) .cm-gutters {
        border-color: var(--error-state-color, red);
      }
    `}}]}}),n.mN)},68797:(e,t,i)=>{var a=i(62659),o=(i(23981),i(98597)),r=i(196),n=i(33167);const s=e=>e.replace(/^_*(.)|_+(.)/g,((e,t,i)=>t?t.toUpperCase():" "+i.toUpperCase()));i(66442);const l=[],d=e=>o.qy`
  <mwc-list-item graphic="icon" .twoline=${!!e.title}>
    <ha-icon .icon=${e.icon} slot="graphic"></ha-icon>
    <span>${e.title||e.path}</span>
    <span slot="secondary">${e.path}</span>
  </mwc-list-item>
`,c=(e,t,i)=>{var a,o,r;return{path:`/${e}/${null!==(a=t.path)&&void 0!==a?a:i}`,icon:null!==(o=t.icon)&&void 0!==o?o:"mdi:view-compact",title:null!==(r=t.title)&&void 0!==r?r:t.path?s(t.path):`${i}`}},u=(e,t)=>{var i;return{path:`/${t.url_path}`,icon:null!==(i=t.icon)&&void 0!==i?i:"mdi:view-dashboard",title:t.url_path===e.defaultPanel?e.localize("panel.states"):e.localize(`panel.${t.title}`)||t.title||(t.url_path?s(t.url_path):"")}};(0,a.A)([(0,r.EM)("ha-navigation-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_opened",value(){return!1}},{kind:"field",key:"navigationItemsLoaded",value(){return!1}},{kind:"field",key:"navigationItems",value(){return l}},{kind:"field",decorators:[(0,r.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-combo-box
        .hass=${this.hass}
        item-value-path="path"
        item-label-path="path"
        .value=${this._value}
        allow-custom-value
        .filteredItems=${this.navigationItems}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .renderer=${d}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
        @filter-changed=${this._filterChanged}
      >
      </ha-combo-box>
    `}},{kind:"method",key:"_openedChanged",value:async function(e){this._opened=e.detail.value,this._opened&&!this.navigationItemsLoaded&&this._loadNavigationItems()}},{kind:"method",key:"_loadNavigationItems",value:async function(){this.navigationItemsLoaded=!0;const e=Object.entries(this.hass.panels).map((([e,t])=>({id:e,...t}))),t=e.filter((e=>"lovelace"===e.component_name)),i=await Promise.all(t.map((e=>{return(t=this.hass.connection,i="lovelace"===e.url_path?null:e.url_path,a=!0,t.sendMessagePromise({type:"lovelace/config",url_path:i,force:a})).then((t=>[e.id,t])).catch((t=>[e.id,void 0]));var t,i,a}))),a=new Map(i);this.navigationItems=[];for(const o of e){this.navigationItems.push(u(this.hass,o));const e=a.get(o.id);e&&"views"in e&&e.views.forEach(((e,t)=>this.navigationItems.push(c(o.url_path,e,t))))}this.comboBox.filteredItems=this.navigationItems}},{kind:"method",key:"shouldUpdate",value:function(e){return!this._opened||e.has("_opened")}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this._setValue(e.detail.value)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,(0,n.r)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.detail.value.toLowerCase();if(t.length>=2){const e=[];this.navigationItems.forEach((i=>{(i.path.toLowerCase().includes(t)||i.title.toLowerCase().includes(t))&&e.push(i)})),e.length>0?this.comboBox.filteredItems=e:this.comboBox.filteredItems=[]}else this.comboBox.filteredItems=this.navigationItems}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-icon,
      ha-svg-icon {
        color: var(--primary-text-color);
        position: relative;
        bottom: 0px;
      }
      *[slot="prefix"] {
        margin-right: 8px;
        margin-inline-end: 8px;
        margin-inline-start: initial;
      }
    `}}]}}),o.WF)},43368:(e,t,i)=>{i.r(t),i.d(t,{HaSelectorUiAction:()=>p});var a=i(62659),o=i(98597),r=i(196),n=i(33167),s=i(76504),l=i(80792),d=i(45081),c=i(24517);i(54625),i(87777),i(29222);(0,a.A)([(0,r.EM)("ha-help-tooltip")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"position",value(){return"top"}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-svg-icon .path=${"M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z"}></ha-svg-icon>
      <simple-tooltip
        offset="4"
        .position=${this.position}
        .fitToVisibleBounds=${!0}
        >${this.label}</simple-tooltip
      >
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-svg-icon {
        --mdc-icon-size: var(--ha-help-tooltip-size, 14px);
        color: var(--ha-help-tooltip-color, var(--disabled-text-color));
      }
    `}}]}}),o.WF);i(68797),i(10263);const u=["more-info","toggle","navigate","url","call-service","assist","none"],h=[{name:"navigation_path",selector:{navigation:{}}}],v=[{type:"grid",name:"",schema:[{name:"pipeline_id",selector:{assist_pipeline:{include_last_used:!0}}},{name:"start_listening",selector:{boolean:{}}}]}];(0,a.A)([(0,r.EM)("hui-action-editor")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"config",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"actions",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"defaultAction",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"tooltipText",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.P)("ha-select")],key:"_select",value:void 0},{kind:"get",key:"_navigation_path",value:function(){const e=this.config;return(null==e?void 0:e.navigation_path)||""}},{kind:"get",key:"_url_path",value:function(){const e=this.config;return(null==e?void 0:e.url_path)||""}},{kind:"get",key:"_service",value:function(){const e=this.config;return(null==e?void 0:e.service)||""}},{kind:"field",key:"_serviceAction",value(){return(0,d.A)((e=>{var t;return{service:this._service,...e.data||e.service_data?{data:null!==(t=e.data)&&void 0!==t?t:e.service_data}:null,target:e.target}}))}},{kind:"method",key:"updated",value:function(e){(0,s.A)((0,l.A)(i.prototype),"updated",this).call(this,e),e.has("defaultAction")&&e.get("defaultAction")!==this.defaultAction&&this._select.layoutOptions()}},{kind:"method",key:"render",value:function(){var e,t,i,a,r,n,s,l;if(!this.hass)return o.s6;const d=null!==(e=this.actions)&&void 0!==e?e:u;return o.qy`
      <div class="dropdown">
        <ha-select
          .label=${this.label}
          .configValue=${"action"}
          @selected=${this._actionPicked}
          .value=${null!==(t=null===(i=this.config)||void 0===i?void 0:i.action)&&void 0!==t?t:"default"}
          @closed=${c.d}
          fixedMenuPosition
          naturalMenuWidt
        >
          <mwc-list-item value="default">
            ${this.hass.localize("ui.panel.lovelace.editor.action-editor.actions.default_action")}
            ${this.defaultAction?` (${this.hass.localize(`ui.panel.lovelace.editor.action-editor.actions.${this.defaultAction}`).toLowerCase()})`:o.s6}
          </mwc-list-item>
          ${d.map((e=>o.qy`
              <mwc-list-item .value=${e}>
                ${this.hass.localize(`ui.panel.lovelace.editor.action-editor.actions.${e}`)}
              </mwc-list-item>
            `))}
        </ha-select>
        ${this.tooltipText?o.qy`
              <ha-help-tooltip .label=${this.tooltipText}></ha-help-tooltip>
            `:o.s6}
      </div>
      ${"navigate"===(null===(a=this.config)||void 0===a?void 0:a.action)?o.qy`
            <ha-form
              .hass=${this.hass}
              .schema=${h}
              .data=${this.config}
              .computeLabel=${this._computeFormLabel}
              @value-changed=${this._formValueChanged}
            >
            </ha-form>
          `:o.s6}
      ${"url"===(null===(r=this.config)||void 0===r?void 0:r.action)?o.qy`
            <ha-textfield
              .label=${this.hass.localize("ui.panel.lovelace.editor.action-editor.url_path")}
              .value=${this._url_path}
              .configValue=${"url_path"}
              @input=${this._valueChanged}
            ></ha-textfield>
          `:o.s6}
      ${"call-service"===(null===(n=this.config)||void 0===n?void 0:n.action)?o.qy`
            <ha-service-control
              .hass=${this.hass}
              .value=${this._serviceAction(this.config)}
              .showAdvanced=${null===(s=this.hass.userData)||void 0===s?void 0:s.showAdvanced}
              narrow
              @value-changed=${this._serviceValueChanged}
            ></ha-service-control>
          `:o.s6}
      ${"assist"===(null===(l=this.config)||void 0===l?void 0:l.action)?o.qy`
            <ha-form
              .hass=${this.hass}
              .schema=${v}
              .data=${this.config}
              .computeLabel=${this._computeFormLabel}
              @value-changed=${this._formValueChanged}
            >
            </ha-form>
          `:o.s6}
    `}},{kind:"method",key:"_actionPicked",value:function(e){var t;if(e.stopPropagation(),!this.hass)return;const i=e.target.value;if((null===(t=this.config)||void 0===t?void 0:t.action)===i)return;if("default"===i)return void(0,n.r)(this,"value-changed",{value:void 0});let a;switch(i){case"url":a={url_path:this._url_path};break;case"call-service":a={service:this._service};break;case"navigate":a={navigation_path:this._navigation_path}}(0,n.r)(this,"value-changed",{value:{action:i,...a}})}},{kind:"method",key:"_valueChanged",value:function(e){var t;if(e.stopPropagation(),!this.hass)return;const i=e.target,a=null!==(t=e.target.value)&&void 0!==t?t:e.target.checked;this[`_${i.configValue}`]!==a&&i.configValue&&(0,n.r)(this,"value-changed",{value:{...this.config,[i.configValue]:a}})}},{kind:"method",key:"_formValueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,n.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_computeFormLabel",value:function(e){var t;return null===(t=this.hass)||void 0===t?void 0:t.localize(`ui.panel.lovelace.editor.action-editor.${e.name}`)}},{kind:"method",key:"_serviceValueChanged",value:function(e){e.stopPropagation();const t={...this.config,service:e.detail.value.service||"",data:e.detail.value.data,target:e.detail.value.target||{}};e.detail.value.data||delete t.data,"service_data"in t&&delete t.service_data,(0,n.r)(this,"value-changed",{value:t})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      .dropdown {
        position: relative;
      }
      ha-help-tooltip {
        position: absolute;
        right: 40px;
        top: 16px;
        inset-inline-start: initial;
        inset-inline-end: 40px;
        direction: var(--direction);
      }
      ha-select,
      ha-textfield {
        width: 100%;
      }
      ha-service-control,
      ha-navigation-picker,
      ha-form {
        display: block;
      }
      ha-textfield,
      ha-service-control,
      ha-navigation-picker,
      ha-form {
        margin-top: 8px;
      }
      ha-service-control {
        --service-control-padding: 0;
      }
      ha-formfield {
        display: flex;
        height: 56px;
        align-items: center;
        --mdc-typography-body2-font-size: 1em;
      }
    `}}]}}),o.WF);let p=(0,a.A)([(0,r.EM)("ha-selector-ui_action")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"method",key:"render",value:function(){var e,t;return o.qy`
      <hui-action-editor
        .label=${this.label}
        .hass=${this.hass}
        .config=${this.value}
        .actions=${null===(e=this.selector.ui_action)||void 0===e?void 0:e.actions}
        .defaultAction=${null===(t=this.selector.ui_action)||void 0===t?void 0:t.default_action}
        .tooltipText=${this.helper}
        @value-changed=${this._valueChanged}
      ></hui-action-editor>
    `}},{kind:"method",key:"_valueChanged",value:function(e){(0,n.r)(this,"value-changed",{value:e.detail.value})}}]}}),o.WF)},42459:(e,t,i)=>{var a=i(62659),o=i(76504),r=i(80792),n=i(47420),s=i(98597),l=i(196),d=i(33167),c=i(43799),u=(i(51029),i(34947)),h=i(57162);(0,a.A)([(0,l.EM)("ha-yaml-editor")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"yamlSchema",value(){return n.my}},{kind:"field",decorators:[(0,l.MZ)()],key:"defaultValue",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"isValid",value(){return!0}},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"autoUpdate",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"readOnly",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"copyClipboard",value(){return!1}},{kind:"field",decorators:[(0,l.wk)()],key:"_yaml",value(){return""}},{kind:"method",key:"setValue",value:function(e){try{this._yaml=e&&!(e=>{if("object"!=typeof e)return!1;for(const t in e)if(Object.prototype.hasOwnProperty.call(e,t))return!1;return!0})(e)?(0,n.Bh)(e,{schema:this.yamlSchema,quotingType:'"',noRefs:!0}):""}catch(t){console.error(t,e),alert(`There was an error converting to YAML: ${t}`)}}},{kind:"method",key:"firstUpdated",value:function(){this.defaultValue&&this.setValue(this.defaultValue)}},{kind:"method",key:"willUpdate",value:function(e){(0,o.A)((0,r.A)(i.prototype),"willUpdate",this).call(this,e),this.autoUpdate&&e.has("value")&&this.setValue(this.value)}},{kind:"method",key:"render",value:function(){return void 0===this._yaml?s.s6:s.qy`
      ${this.label?s.qy`<p>${this.label}${this.required?" *":""}</p>`:""}
      <ha-code-editor
        .hass=${this.hass}
        .value=${this._yaml}
        .readOnly=${this.readOnly}
        mode="yaml"
        autocomplete-entities
        autocomplete-icons
        .error=${!1===this.isValid}
        @value-changed=${this._onChange}
        dir="ltr"
      ></ha-code-editor>
      ${this.copyClipboard?s.qy`<div class="card-actions">
            <mwc-button @click=${this._copyYaml}>
              ${this.hass.localize("ui.components.yaml-editor.copy_to_clipboard")}
            </mwc-button>
          </div>`:s.s6}
    `}},{kind:"method",key:"_onChange",value:function(e){let t;e.stopPropagation(),this._yaml=e.detail.value;let i=!0;if(this._yaml)try{t=(0,n.Hh)(this._yaml,{schema:this.yamlSchema})}catch(a){i=!1}else t={};this.value=t,this.isValid=i,(0,d.r)(this,"value-changed",{value:t,isValid:i})}},{kind:"get",key:"yaml",value:function(){return this._yaml}},{kind:"method",key:"_copyYaml",value:async function(){this.yaml&&(await(0,h.l)(this.yaml),(0,u.P)(this,{message:this.hass.localize("ui.common.copied_clipboard")}))}},{kind:"get",static:!0,key:"styles",value:function(){return[c.RF,s.AH`
        .card-actions {
          border-radius: var(
            --actions-border-radius,
            0px 0px var(--ha-card-border-radius, 12px)
              var(--ha-card-border-radius, 12px)
          );
          border: 1px solid var(--divider-color);
          padding: 5px 16px;
        }
        ha-code-editor {
          flex-grow: 1;
        }
      `]}}]}}),s.WF)},74538:(e,t,i)=>{i.d(t,{_4:()=>b,fq:()=>k,Yd:()=>y,f$:()=>_});var a=i(19263),o=i(59782),r=i(80085),n=i(2503);const s={10:"mdi:battery-10",20:"mdi:battery-20",30:"mdi:battery-30",40:"mdi:battery-40",50:"mdi:battery-50",60:"mdi:battery-60",70:"mdi:battery-70",80:"mdi:battery-80",90:"mdi:battery-90",100:"mdi:battery"},l={10:"mdi:battery-charging-10",20:"mdi:battery-charging-20",30:"mdi:battery-charging-30",40:"mdi:battery-charging-40",50:"mdi:battery-charging-50",60:"mdi:battery-charging-60",70:"mdi:battery-charging-70",80:"mdi:battery-charging-80",90:"mdi:battery-charging-90",100:"mdi:battery-charging"},d=(e,t)=>{const i=Number(e);if(isNaN(i))return"off"===e?"mdi:battery":"on"===e?"mdi:battery-alert":"mdi:battery-unknown";const a=10*Math.round(i/10);return t&&i>=10?l[a]:t?"mdi:battery-charging-outline":i<=5?"mdi:battery-alert-variant-outline":s[a]},c=(e,t)=>{const i=(0,r.t)(e),a=null!=t?t:e.state,o=e.attributes.device_class;switch(i){case"update":return((e,t)=>"on"===(null!=t?t:e.state)?(0,n.Jy)(e)?"mdi:package-down":"mdi:package-up":"mdi:package")(e,a);case"sensor":if("battery"===o)return((e,t)=>{const i=null!=t?t:e.state;return d(i)})(e,a);break;case"device_tracker":return((e,t)=>{const i=null!=t?t:e.state;return"router"===(null==e?void 0:e.attributes.source_type)?"home"===i?"mdi:lan-connect":"mdi:lan-disconnect":["bluetooth","bluetooth_le"].includes(null==e?void 0:e.attributes.source_type)?"home"===i?"mdi:bluetooth-connect":"mdi:bluetooth":"not_home"===i?"mdi:account-arrow-right":"mdi:account"})(e,a);case"sun":return"above_horizon"===a?"mdi:white-balance-sunny":"mdi:weather-night";case"input_datetime":if(!e.attributes.has_date)return"mdi:clock";if(!e.attributes.has_time)return"mdi:calendar"}};var u=i(32872),h=i(14656);const v={entity:{},entity_component:{},services:{domains:{}}},p=async(e,t,i)=>e.callWS({type:"frontend/get_icons",category:t,integration:i}),m=async(e,t,i=!1)=>{if(!i&&t in v.entity)return v.entity[t];if(!(0,u.x)(e,t)||!(0,h.v)(e.connection.haVersion,2024,2))return;const a=p(e,"entity",t).then((e=>null==e?void 0:e.resources[t]));return v.entity[t]=a,v.entity[t]},f=async(e,t,i=!1)=>{var a;return!i&&v.entity_component.resources&&null!==(a=v.entity_component.domains)&&void 0!==a&&a.includes(t)?v.entity_component.resources.then((e=>e[t])):(0,u.x)(e,t)?(v.entity_component.domains=[...e.config.components],v.entity_component.resources=p(e,"entity_component").then((e=>e.resources)),v.entity_component.resources.then((e=>e[t]))):void 0},y=async(e,t,i=!1)=>{if(!t)return!i&&v.services.all||(v.services.all=p(e,"services",t).then((e=>(v.services.domains=e.resources,null==e?void 0:e.resources)))),v.services.all;if(!i&&t in v.services.domains)return v.services.domains[t];if(v.services.all&&!i&&(await v.services.all,t in v.services.domains))return v.services.domains[t];if(!(0,u.x)(e,t))return;const a=p(e,"services",t);return v.services.domains[t]=a.then((e=>null==e?void 0:e.resources[t])),v.services.domains[t]},k=async(e,t,i)=>{var a;const o=null===(a=e.entities)||void 0===a?void 0:a[t.entity_id];if(null!=o&&o.icon)return o.icon;const n=(0,r.t)(t);return g(e,n,t,i,o)},g=async(e,t,i,a,o)=>{const r=null==o?void 0:o.platform,n=null==o?void 0:o.translation_key,s=null==i?void 0:i.attributes.device_class,l=null!=a?a:null==i?void 0:i.state;let d;if(n&&r){const i=await m(e,r);if(i){var u,h;const e=null===(u=i[t])||void 0===u?void 0:u[n];d=l&&(null==e||null===(h=e.state)||void 0===h?void 0:h[l])||(null==e?void 0:e.default)}}if(!d&&i&&(d=c(i,l)),!d){const i=await f(e,t);if(i){var v;const e=s&&i[s]||i._;d=l&&(null==e||null===(v=e.state)||void 0===v?void 0:v[l])||(null==e?void 0:e.default)}}return d},_=async(e,t)=>{let i;const r=(0,a.m)(t),n=(0,o.Y)(t),s=await y(e,r);return s&&(i=s[n]),i||(i=await b(e,r)),i},b=async(e,t,i)=>{const a=await f(e,t);if(a){const e=i&&a[i]||a._;return null==e?void 0:e.default}}},31238:(e,t,i)=>{i.d(t,{QC:()=>r,fK:()=>o,p$:()=>a});const a=(e,t,i)=>e(`component.${t}.title`)||(null==i?void 0:i.name)||t,o=(e,t)=>{const i={type:"manifest/list"};return t&&(i.integrations=t),e.callWS(i)},r=(e,t)=>e.callWS({type:"manifest/get",integration:t})},2503:(e,t,i)=>{i.d(t,{A_:()=>n,Jy:()=>r});i(93758);var a=i(60222);i(66412);let o=function(e){return e[e.INSTALL=1]="INSTALL",e[e.SPECIFIC_VERSION=2]="SPECIFIC_VERSION",e[e.PROGRESS=4]="PROGRESS",e[e.BACKUP=8]="BACKUP",e[e.RELEASE_NOTES=16]="RELEASE_NOTES",e}({});const r=e=>(e=>(0,a.$)(e,o.PROGRESS)&&"number"==typeof e.attributes.in_progress)(e)||!!e.attributes.in_progress,n=(e,t)=>{const i=e.state,n=e.attributes;if("off"===i){return n.latest_version&&n.skipped_version===n.latest_version?n.latest_version:t.formatEntityState(e)}if("on"===i&&r(e)){return(0,a.$)(e,o.PROGRESS)&&"number"==typeof n.in_progress?t.localize("ui.card.update.installing_with_progress",{progress:n.in_progress}):t.localize("ui.card.update.installing")}return t.formatEntityState(e)}},34947:(e,t,i)=>{i.d(t,{P:()=>o});var a=i(33167);const o=(e,t)=>(0,a.r)(e,"hass-notification",t)}};
//# sourceMappingURL=RE0qUeNK.js.map