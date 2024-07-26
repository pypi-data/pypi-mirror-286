/*! For license information please see AUnvhNGy.js.LICENSE.txt */
export const id=3101;export const ids=[3101,3920];export const modules={80920:(e,t,i)=>{var n=i(62659),r=i(76504),o=i(80792),a=(i(27350),i(98597)),s=i(196),l=i(10),d=i(22994);(0,n.A)([(0,s.EM)("ha-button-menu")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:d.Xr,value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"corner",value(){return"BOTTOM_START"}},{kind:"field",decorators:[(0,s.MZ)()],key:"menuCorner",value(){return"START"}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"x",value(){return null}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"y",value(){return null}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"multi",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"activatable",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"fixed",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean,attribute:"no-anchor"})],key:"noAnchor",value(){return!1}},{kind:"field",decorators:[(0,s.P)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"focus",value:function(){var e,t;null!==(e=this._menu)&&void 0!==e&&e.open?this._menu.focusItemAtIndex(0):null===(t=this._triggerButton)||void 0===t||t.focus()}},{kind:"method",key:"render",value:function(){return a.qy`
      <div @click=${this._handleClick}>
        <slot name="trigger" @slotchange=${this._setTriggerAria}></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .menuCorner=${this.menuCorner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
        .y=${this.y}
        .x=${this.x}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,r.A)((0,o.A)(i.prototype),"firstUpdated",this).call(this,e),"rtl"===l.G.document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),a.WF)},33920:(e,t,i)=>{i.r(t),i.d(t,{HaIconOverflowMenu:()=>l});var n=i(62659),r=(i(87777),i(98597)),o=i(196),a=i(69760),s=i(43799);i(80920),i(89874),i(9484),i(29222);let l=(0,n.A)([(0,o.EM)("ha-icon-overflow-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Array})],key:"items",value(){return[]}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"method",key:"render",value:function(){return r.qy`
      ${this.narrow?r.qy` <!-- Collapsed representation for small screens -->
            <ha-button-menu
              @click=${this._handleIconOverflowMenuOpened}
              @closed=${this._handleIconOverflowMenuClosed}
              class="ha-icon-overflow-menu-overflow"
              absolute
            >
              <ha-icon-button
                .label=${this.hass.localize("ui.common.overflow_menu")}
                .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
                slot="trigger"
              ></ha-icon-button>

              ${this.items.map((e=>e.divider?r.qy`<li divider role="separator"></li>`:r.qy`<ha-list-item
                      graphic="icon"
                      ?disabled=${e.disabled}
                      @click=${e.action}
                      class=${(0,a.H)({warning:Boolean(e.warning)})}
                    >
                      <div slot="graphic">
                        <ha-svg-icon
                          class=${(0,a.H)({warning:Boolean(e.warning)})}
                          .path=${e.path}
                        ></ha-svg-icon>
                      </div>
                      ${e.label}
                    </ha-list-item> `))}
            </ha-button-menu>`:r.qy`
            <!-- Icon representation for big screens -->
            ${this.items.map((e=>e.narrowOnly?"":e.divider?r.qy`<div role="separator"></div>`:r.qy`<div>
                      ${e.tooltip?r.qy`<simple-tooltip
                            animation-delay="0"
                            position="left"
                          >
                            ${e.tooltip}
                          </simple-tooltip>`:""}
                      <ha-icon-button
                        @click=${e.action}
                        .label=${e.label}
                        .path=${e.path}
                        ?disabled=${e.disabled}
                      ></ha-icon-button>
                    </div> `))}
          `}
    `}},{kind:"method",key:"_handleIconOverflowMenuOpened",value:function(e){e.stopPropagation();const t=this.closest(".mdc-data-table__row");t&&(t.style.zIndex="1")}},{kind:"method",key:"_handleIconOverflowMenuClosed",value:function(){const e=this.closest(".mdc-data-table__row");e&&(e.style.zIndex="")}},{kind:"get",static:!0,key:"styles",value:function(){return[s.RF,r.AH`
        :host {
          display: flex;
          justify-content: flex-end;
        }
        li[role="separator"] {
          border-bottom-color: var(--divider-color);
        }
        div[role="separator"] {
          border-right: 1px solid var(--divider-color);
          width: 1px;
        }
        ha-list-item[disabled] ha-svg-icon {
          color: var(--disabled-text-color);
        }
      `]}}]}}),r.WF)},92518:(e,t,i)=>{function n(e){if(!e||"object"!=typeof e)return e;if("[object Date]"==Object.prototype.toString.call(e))return new Date(e.getTime());if(Array.isArray(e))return e.map(n);var t={};return Object.keys(e).forEach((function(i){t[i]=n(e[i])})),t}i.d(t,{A:()=>n})},60309:(e,t,i)=>{var n=i(62659),r=i(76504),o=i(80792),a=i(98597),s=i(196),l=i(69760),d=i(33167);const c=new(i(61328).Q)("knx-project-tree-view");(0,n.A)([(0,s.EM)("knx-project-tree-view")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"multiselect",value(){return!1}},{kind:"field",decorators:[(0,s.wk)()],key:"_selectableRanges",value(){return{}}},{kind:"method",key:"connectedCallback",value:function(){(0,r.A)((0,o.A)(i.prototype),"connectedCallback",this).call(this);const e=t=>{Object.entries(t).forEach((([t,i])=>{i.group_addresses.length>0&&(this._selectableRanges[t]={selected:!1,groupAddresses:i.group_addresses}),e(i.group_ranges)}))};e(this.data.group_ranges),c.debug("ranges",this._selectableRanges)}},{kind:"method",key:"render",value:function(){return a.qy`<div class="ha-tree-view">${this._recurseData(this.data.group_ranges)}</div>`}},{kind:"method",key:"_recurseData",value:function(e,t=0){const i=Object.entries(e).map((([e,i])=>{const n=Object.keys(i.group_ranges).length>0;if(!(n||i.group_addresses.length>0))return a.s6;const r=e in this._selectableRanges,o=!!r&&this._selectableRanges[e].selected,s={"range-item":!0,"root-range":0===t,"sub-range":t>0,selectable:r,"selected-range":o,"non-selected-range":r&&!o},d=a.qy`<div
        class=${(0,l.H)(s)}
        toggle-range=${r?e:a.s6}
        @click=${r?this.multiselect?this._selectionChangedMulti:this._selectionChangedSingle:a.s6}
      >
        <span class="range-key">${e}</span>
        <span class="range-text">${i.name}</span>
      </div>`;if(n){const e={"root-group":0===t,"sub-group":0!==t};return a.qy`<div class=${(0,l.H)(e)}>
          ${d} ${this._recurseData(i.group_ranges,t+1)}
        </div>`}return a.qy`${d}`}));return a.qy`${i}`}},{kind:"method",key:"_selectionChangedMulti",value:function(e){const t=e.target.getAttribute("toggle-range");this._selectableRanges[t].selected=!this._selectableRanges[t].selected,this._selectionUpdate(),this.requestUpdate()}},{kind:"method",key:"_selectionChangedSingle",value:function(e){const t=e.target.getAttribute("toggle-range"),i=this._selectableRanges[t].selected;Object.values(this._selectableRanges).forEach((e=>{e.selected=!1})),this._selectableRanges[t].selected=!i,this._selectionUpdate(),this.requestUpdate()}},{kind:"method",key:"_selectionUpdate",value:function(){const e=Object.values(this._selectableRanges).reduce(((e,t)=>t.selected?e.concat(t.groupAddresses):e),[]);c.debug("selection changed",e),(0,d.r)(this,"knx-group-range-selection-changed",{groupAddresses:e})}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host {
        margin: 0;
        height: 100%;
        overflow-y: scroll;
        overflow-x: hidden;
        background-color: var(--card-background-color);
      }

      .ha-tree-view {
        cursor: default;
      }

      .root-group {
        margin-bottom: 8px;
      }

      .root-group > * {
        padding-top: 5px;
        padding-bottom: 5px;
      }

      .range-item {
        display: block;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        font-size: 0.875rem;
      }

      .range-item > * {
        vertical-align: middle;
        pointer-events: none;
      }

      .range-key {
        color: var(--text-primary-color);
        font-size: 0.75rem;
        font-weight: 700;
        background-color: var(--label-badge-grey);
        border-radius: 4px;
        padding: 1px 4px;
        margin-right: 2px;
      }

      .root-range {
        padding-left: 8px;
        font-weight: 500;
        background-color: var(--secondary-background-color);

        & .range-key {
          color: var(--primary-text-color);
          background-color: var(--card-background-color);
        }
      }

      .sub-range {
        padding-left: 13px;
      }

      .selectable {
        cursor: pointer;
      }

      .selectable:hover {
        background-color: rgba(var(--rgb-primary-text-color), 0.04);
      }

      .selected-range {
        background-color: rgba(var(--rgb-primary-color), 0.12);

        & .range-key {
          background-color: var(--primary-color);
        }
      }

      .selected-range:hover {
        background-color: rgba(var(--rgb-primary-color), 0.07);
      }

      .non-selected-range {
        background-color: var(--card-background-color);
      }
    `}}]}}),a.WF)},7248:(e,t,i)=>{i.r(t),i.d(t,{KNXEntitiesView:()=>y});var n=i(62659),r=i(98597),o=i(196),a=i(79278),s=i(45081),l=(i(61424),i(7341),i(94392),i(97661),i(89874),i(33920),i(45063),i(29222),i(65206),i(13314)),d=i(10),c=i(33167),u=i(31447),h=(i(60309),i(39987)),v=i(61328);const g=new v.Q("knx-entities-view");let y=(0,n.A)([(0,o.EM)("knx-entities-view")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"knx_entities",value(){return[]}},{kind:"field",decorators:[(0,o.wk)()],key:"filterDevice",value(){return null}},{kind:"method",key:"firstUpdated",value:function(){this._fetchEntities()}},{kind:"method",key:"willUpdate",value:function(){const e=new URLSearchParams(d.G.location.search);this.filterDevice=e.get("device_id")}},{kind:"method",key:"_fetchEntities",value:async function(){const e=await(0,h.ek)(this.hass);g.debug(`Fetched ${e.length} entity entries.`),this.knx_entities=e.map((e=>{var t;const i=this.hass.states[e.entity_id],n=e.device_id?this.hass.devices[e.device_id]:void 0,r=null!==(t=e.area_id)&&void 0!==t?t:null==n?void 0:n.area_id,o=r?this.hass.areas[r]:void 0;return{...e,entityState:i,area:o}}))}},{kind:"field",key:"_columns",value(){return(0,s.A)(((e,t)=>{const i="56px",n="176px",o=`calc((100% - ${i} - ${n}) / 4)`;return{icon:{title:"",width:i,type:"icon",template:e=>{var t;return r.qy`
          <ha-state-icon
            title=${(0,a.J)(null===(t=e.entityState)||void 0===t?void 0:t.state)}
            slot="item-icon"
            .state=${e.entityState}
          ></ha-state-icon>
        `}},friendly_name:{filterable:!0,sortable:!0,title:"Friendly Name",width:o,template:e=>{var t,i;return null!==(t=null===(i=e.entityState)||void 0===i?void 0:i.attributes.friendly_name)&&void 0!==t?t:""}},entity_id:{filterable:!0,sortable:!0,title:"Entity ID",width:o},device:{filterable:!0,sortable:!0,title:"Device",width:o,template:e=>{var t;return e.device_id&&null!==(t=this.hass.devices[e.device_id].name)&&void 0!==t?t:""}},device_id:{hidden:!0,title:"Device ID",filterable:!0,template:e=>{var t;return null!==(t=e.device_id)&&void 0!==t?t:""}},area:{title:"Area",sortable:!0,filterable:!0,width:o,template:e=>{var t,i;return null!==(t=null===(i=e.area)||void 0===i?void 0:i.name)&&void 0!==t?t:""}},actions:{title:"",width:n,type:"icon-button",template:e=>r.qy`
          <ha-icon-button
            .label=${"More info"}
            .path=${"M11 7V9H13V7H11M14 17V15H13V11H10V13H11V15H10V17H14M22 12C22 17.5 17.5 22 12 22C6.5 22 2 17.5 2 12C2 6.5 6.5 2 12 2C17.5 2 22 6.5 22 12M20 12C20 7.58 16.42 4 12 4C7.58 4 4 7.58 4 12C4 16.42 7.58 20 12 20C16.42 20 20 16.42 20 12Z"}
            .entityEntry=${e}
            @click=${this._entityMoreInfo}
          ></ha-icon-button>
          <ha-icon-button
            .label=${this.hass.localize("ui.common.edit")}
            .path=${"M14.06,9L15,9.94L5.92,19H5V18.08L14.06,9M17.66,3C17.41,3 17.15,3.1 16.96,3.29L15.13,5.12L18.88,8.87L20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18.17,3.09 17.92,3 17.66,3M14.06,6.19L3,17.25V21H6.75L17.81,9.94L14.06,6.19Z"}
            .entityEntry=${e}
            @click=${this._entityEdit}
          ></ha-icon-button>
          <ha-icon-button
            .label=${this.hass.localize("ui.common.delete")}
            .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
            .entityEntry=${e}
            @click=${this._entityDelete}
          ></ha-icon-button>
        `}}}))}},{kind:"field",key:"_entityEdit",value(){return e=>{e.stopPropagation();const t=e.target.entityEntry;(0,l.o)("/knx/entities/edit/"+t.entity_id)}}},{kind:"field",key:"_entityMoreInfo",value(){return e=>{e.stopPropagation();const t=e.target.entityEntry;(0,c.r)(d.G.document.querySelector("home-assistant"),"hass-more-info",{entityId:t.entity_id})}}},{kind:"field",key:"_entityDelete",value(){return e=>{e.stopPropagation();const t=e.target.entityEntry;(0,u.dk)(this,{text:`${this.hass.localize("ui.common.delete")} ${t.entity_id}?`}).then((e=>{e&&(0,h.$b)(this.hass,t.entity_id).then((()=>{g.debug("entity deleted",t.entity_id),this._fetchEntities()})).catch((e=>{(0,u.K$)(this,{title:"Deletion failed",text:e})}))}))}}},{kind:"method",key:"render",value:function(){return this.hass&&this.knx_entities?r.qy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${this.tabs}
        .localizeFunc=${this.knx.localize}
      >
        <div class="sections">
          <ha-data-table
            class="entity-table"
            .hass=${this.hass}
            .columns=${this._columns(this.narrow,this.hass.language)}
            .data=${this.knx_entities}
            .hasFab=${!0}
            .searchLabel=${this.hass.localize("ui.components.data-table.search")}
            .clickable=${!1}
            .filter=${this.filterDevice}
          ></ha-data-table>
        </div>
        <ha-fab
          slot="fab"
          .label=${this.hass.localize("ui.common.add")}
          extended
          @click=${this._entityCreate}
        >
          <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage>
    `:r.qy` <hass-loading-screen></hass-loading-screen> `}},{kind:"method",key:"_entityCreate",value:function(){(0,l.o)("/knx/entities/create")}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`
      hass-loading-screen {
        --app-header-background-color: var(--sidebar-background-color);
        --app-header-text-color: var(--sidebar-text-color);
      }
      .sections {
        display: flex;
        flex-direction: row;
        height: 100%;
      }

      .entity-table {
        flex: 1;
      }
    `}}]}}),r.WF)},86625:(e,t,i)=>{i.d(t,{T:()=>h});var n=i(34078),r=i(3982),o=i(3267);class a{constructor(e){this.G=e}disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}}class s{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var e;null!==(e=this.Y)&&void 0!==e||(this.Y=new Promise((e=>this.Z=e)))}resume(){var e;null===(e=this.Z)||void 0===e||e.call(this),this.Y=this.Z=void 0}}var l=i(2154);const d=e=>!(0,r.sO)(e)&&"function"==typeof e.then,c=1073741823;class u extends o.Kq{constructor(){super(...arguments),this._$C_t=c,this._$Cwt=[],this._$Cq=new a(this),this._$CK=new s}render(...e){var t;return null!==(t=e.find((e=>!d(e))))&&void 0!==t?t:n.c0}update(e,t){const i=this._$Cwt;let r=i.length;this._$Cwt=t;const o=this._$Cq,a=this._$CK;this.isConnected||this.disconnected();for(let n=0;n<t.length&&!(n>this._$C_t);n++){const e=t[n];if(!d(e))return this._$C_t=n,e;n<r&&e===i[n]||(this._$C_t=c,r=0,Promise.resolve(e).then((async t=>{for(;a.get();)await a.get();const i=o.deref();if(void 0!==i){const n=i._$Cwt.indexOf(e);n>-1&&n<i._$C_t&&(i._$C_t=n,i.setValue(t))}})))}return n.c0}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const h=(0,l.u$)(u)}};
//# sourceMappingURL=AUnvhNGy.js.map