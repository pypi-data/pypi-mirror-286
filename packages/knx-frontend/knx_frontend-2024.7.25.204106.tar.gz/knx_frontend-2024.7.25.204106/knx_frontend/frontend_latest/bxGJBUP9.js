export const id=5323;export const ids=[5323,3920];export const modules={32872:(e,t,r)=>{r.d(t,{x:()=>o});const o=(e,t)=>e&&e.config.components.includes(t)},80920:(e,t,r)=>{var o=r(62659),i=r(76504),a=r(80792),n=(r(27350),r(98597)),s=r(196),d=r(10),l=r(22994);(0,o.A)([(0,s.EM)("ha-button-menu")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",key:l.Xr,value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"corner",value(){return"BOTTOM_START"}},{kind:"field",decorators:[(0,s.MZ)()],key:"menuCorner",value(){return"START"}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"x",value(){return null}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"y",value(){return null}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"multi",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"activatable",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"fixed",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean,attribute:"no-anchor"})],key:"noAnchor",value(){return!1}},{kind:"field",decorators:[(0,s.P)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"focus",value:function(){var e,t;null!==(e=this._menu)&&void 0!==e&&e.open?this._menu.focusItemAtIndex(0):null===(t=this._triggerButton)||void 0===t||t.focus()}},{kind:"method",key:"render",value:function(){return n.qy`
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
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,i.A)((0,a.A)(r.prototype),"firstUpdated",this).call(this,e),"rtl"===d.G.document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),n.WF)},94392:(e,t,r)=>{var o=r(62659),i=r(98597),a=r(196);(0,o.A)([(0,a.EM)("ha-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)()],key:"header",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean,reflect:!0})],key:"raised",value(){return!1}},{kind:"get",static:!0,key:"styles",value:function(){return i.AH`
      :host {
        background: var(
          --ha-card-background,
          var(--card-background-color, white)
        );
        -webkit-backdrop-filter: var(--ha-card-backdrop-filter, none);
        backdrop-filter: var(--ha-card-backdrop-filter, none);
        box-shadow: var(--ha-card-box-shadow, none);
        box-sizing: border-box;
        border-radius: var(--ha-card-border-radius, 12px);
        border-width: var(--ha-card-border-width, 1px);
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      :host([raised]) {
        border: none;
        box-shadow: var(
          --ha-card-box-shadow,
          0px 2px 1px -1px rgba(0, 0, 0, 0.2),
          0px 1px 1px 0px rgba(0, 0, 0, 0.14),
          0px 1px 3px 0px rgba(0, 0, 0, 0.12)
        );
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 48px;
        padding: 12px 16px 16px;
        display: block;
        margin-block-start: 0px;
        margin-block-end: 0px;
        font-weight: normal;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid var(--divider-color, #e8e8e8);
        padding: 5px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return i.qy`
      ${this.header?i.qy`<h1 class="card-header">${this.header}</h1>`:i.s6}
      <slot></slot>
    `}}]}}),i.WF)},73279:(e,t,r)=>{var o=r(62659),i=r(76504),a=r(80792),n=r(57305),s=r(98597),d=r(196);(0,o.A)([(0,d.EM)("ha-circular-progress")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:"aria-label",type:String})],key:"ariaLabel",value(){return"Loading"}},{kind:"field",decorators:[(0,d.MZ)()],key:"size",value(){return"medium"}},{kind:"method",key:"updated",value:function(e){if((0,i.A)((0,a.A)(r.prototype),"updated",this).call(this,e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"field",static:!0,key:"styles",value(){return[...(0,i.A)((0,a.A)(r),"styles",this),s.AH`
      :host {
        --md-sys-color-primary: var(--primary-color);
        --md-circular-progress-size: 48px;
      }
    `]}}]}}),n.U)},33920:(e,t,r)=>{r.r(t),r.d(t,{HaIconOverflowMenu:()=>d});var o=r(62659),i=(r(87777),r(98597)),a=r(196),n=r(69760),s=r(43799);r(80920),r(89874),r(9484),r(29222);let d=(0,o.A)([(0,a.EM)("ha-icon-overflow-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array})],key:"items",value(){return[]}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"method",key:"render",value:function(){return i.qy`
      ${this.narrow?i.qy` <!-- Collapsed representation for small screens -->
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

              ${this.items.map((e=>e.divider?i.qy`<li divider role="separator"></li>`:i.qy`<ha-list-item
                      graphic="icon"
                      ?disabled=${e.disabled}
                      @click=${e.action}
                      class=${(0,n.H)({warning:Boolean(e.warning)})}
                    >
                      <div slot="graphic">
                        <ha-svg-icon
                          class=${(0,n.H)({warning:Boolean(e.warning)})}
                          .path=${e.path}
                        ></ha-svg-icon>
                      </div>
                      ${e.label}
                    </ha-list-item> `))}
            </ha-button-menu>`:i.qy`
            <!-- Icon representation for big screens -->
            ${this.items.map((e=>e.narrowOnly?"":e.divider?i.qy`<div role="separator"></div>`:i.qy`<div>
                      ${e.tooltip?i.qy`<simple-tooltip
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
    `}},{kind:"method",key:"_handleIconOverflowMenuOpened",value:function(e){e.stopPropagation();const t=this.closest(".mdc-data-table__row");t&&(t.style.zIndex="1")}},{kind:"method",key:"_handleIconOverflowMenuClosed",value:function(){const e=this.closest(".mdc-data-table__row");e&&(e.style.zIndex="")}},{kind:"get",static:!0,key:"styles",value:function(){return[s.RF,i.AH`
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
      `]}}]}}),i.WF)},9484:(e,t,r)=>{var o=r(62659),i=r(76504),a=r(80792),n=r(46175),s=r(45592),d=r(98597),l=r(196);(0,o.A)([(0,l.EM)("ha-list-item")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,i.A)((0,a.A)(r.prototype),"renderRipple",this).call(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[s.R,d.AH`
        :host {
          padding-left: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-start: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-right: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-end: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
        }
        :host([graphic="avatar"]:not([twoLine])),
        :host([graphic="icon"]:not([twoLine])) {
          height: 48px;
        }
        span.material-icons:first-of-type {
          margin-inline-start: 0px !important;
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            16px
          ) !important;
          direction: var(--direction) !important;
        }
        span.material-icons:last-of-type {
          margin-inline-start: auto !important;
          margin-inline-end: 0px !important;
          direction: var(--direction) !important;
        }
        .mdc-deprecated-list-item__meta {
          display: var(--mdc-list-item-meta-display);
          align-items: center;
          flex-shrink: 0;
        }
        :host([graphic="icon"]:not([twoline]))
          .mdc-deprecated-list-item__graphic {
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            20px
          ) !important;
        }
        :host([multiline-secondary]) {
          height: auto;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__text {
          padding: 8px 0;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text {
          text-overflow: initial;
          white-space: normal;
          overflow: auto;
          display: inline-block;
          margin-top: 10px;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__primary-text {
          margin-top: 10px;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__secondary-text::before {
          display: none;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__primary-text::before {
          display: none;
        }
        :host([disabled]) {
          color: var(--disabled-text-color);
        }
        :host([noninteractive]) {
          pointer-events: unset;
        }
      `,"rtl"===document.dir?d.AH`
            span.material-icons:first-of-type,
            span.material-icons:last-of-type {
              direction: rtl !important;
              --direction: rtl;
            }
          `:d.AH``]}}]}}),n.J)},61424:(e,t,r)=>{r.r(t);var o=r(62659),i=r(98597),a=r(196),n=(r(73279),r(92312),r(32010),r(43799));(0,o.A)([(0,a.EM)("hass-loading-screen")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean,attribute:"no-toolbar"})],key:"noToolbar",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"rootnav",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)()],key:"message",value:void 0},{kind:"method",key:"render",value:function(){var e;return i.qy`
      ${this.noToolbar?"":i.qy`<div class="toolbar">
            ${this.rootnav||null!==(e=history.state)&&void 0!==e&&e.root?i.qy`
                  <ha-menu-button
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                `:i.qy`
                  <ha-icon-button-arrow-prev
                    .hass=${this.hass}
                    @click=${this._handleBack}
                  ></ha-icon-button-arrow-prev>
                `}
          </div>`}
      <div class="content">
        <ha-circular-progress indeterminate></ha-circular-progress>
        ${this.message?i.qy`<div id="loading-text">${this.message}</div>`:i.s6}
      </div>
    `}},{kind:"method",key:"_handleBack",value:function(){history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[n.RF,i.AH`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }
        .toolbar {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: var(--header-height);
          padding: 8px 12px;
          pointer-events: none;
          background-color: var(--app-header-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar {
            padding: 4px;
          }
        }
        ha-menu-button,
        ha-icon-button-arrow-prev {
          pointer-events: auto;
        }
        .content {
          height: calc(100% - var(--header-height));
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        #loading-text {
          max-width: 350px;
          margin-top: 16px;
        }
      `]}}]}}),i.WF)},92518:(e,t,r)=>{function o(e){if(!e||"object"!=typeof e)return e;if("[object Date]"==Object.prototype.toString.call(e))return new Date(e.getTime());if(Array.isArray(e))return e.map(o);var t={};return Object.keys(e).forEach((function(r){t[r]=o(e[r])})),t}r.d(t,{A:()=>o})},60309:(e,t,r)=>{var o=r(62659),i=r(76504),a=r(80792),n=r(98597),s=r(196),d=r(69760),l=r(33167);const c=new(r(61328).Q)("knx-project-tree-view");(0,o.A)([(0,s.EM)("knx-project-tree-view")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"multiselect",value(){return!1}},{kind:"field",decorators:[(0,s.wk)()],key:"_selectableRanges",value(){return{}}},{kind:"method",key:"connectedCallback",value:function(){(0,i.A)((0,a.A)(r.prototype),"connectedCallback",this).call(this);const e=t=>{Object.entries(t).forEach((([t,r])=>{r.group_addresses.length>0&&(this._selectableRanges[t]={selected:!1,groupAddresses:r.group_addresses}),e(r.group_ranges)}))};e(this.data.group_ranges),c.debug("ranges",this._selectableRanges)}},{kind:"method",key:"render",value:function(){return n.qy`<div class="ha-tree-view">${this._recurseData(this.data.group_ranges)}</div>`}},{kind:"method",key:"_recurseData",value:function(e,t=0){const r=Object.entries(e).map((([e,r])=>{const o=Object.keys(r.group_ranges).length>0;if(!(o||r.group_addresses.length>0))return n.s6;const i=e in this._selectableRanges,a=!!i&&this._selectableRanges[e].selected,s={"range-item":!0,"root-range":0===t,"sub-range":t>0,selectable:i,"selected-range":a,"non-selected-range":i&&!a},l=n.qy`<div
        class=${(0,d.H)(s)}
        toggle-range=${i?e:n.s6}
        @click=${i?this.multiselect?this._selectionChangedMulti:this._selectionChangedSingle:n.s6}
      >
        <span class="range-key">${e}</span>
        <span class="range-text">${r.name}</span>
      </div>`;if(o){const e={"root-group":0===t,"sub-group":0!==t};return n.qy`<div class=${(0,d.H)(e)}>
          ${l} ${this._recurseData(r.group_ranges,t+1)}
        </div>`}return n.qy`${l}`}));return n.qy`${r}`}},{kind:"method",key:"_selectionChangedMulti",value:function(e){const t=e.target.getAttribute("toggle-range");this._selectableRanges[t].selected=!this._selectableRanges[t].selected,this._selectionUpdate(),this.requestUpdate()}},{kind:"method",key:"_selectionChangedSingle",value:function(e){const t=e.target.getAttribute("toggle-range"),r=this._selectableRanges[t].selected;Object.values(this._selectableRanges).forEach((e=>{e.selected=!1})),this._selectableRanges[t].selected=!r,this._selectionUpdate(),this.requestUpdate()}},{kind:"method",key:"_selectionUpdate",value:function(){const e=Object.values(this._selectableRanges).reduce(((e,t)=>t.selected?e.concat(t.groupAddresses):e),[]);c.debug("selection changed",e),(0,l.r)(this,"knx-group-range-selection-changed",{groupAddresses:e})}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
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
    `}}]}}),n.WF)},62685:(e,t,r)=>{r.r(t),r.d(t,{KNXProjectView:()=>f});var o=r(62659),i=r(98597),a=r(196),n=r(45081),s=r(13314);r(61424),r(7341),r(94392),r(89874),r(33920),r(65206),r(60309);const d=/^[v^~<>=]*?(\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+))?(?:-([\da-z\-]+(?:\.[\da-z\-]+)*))?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?)?)?$/i,l=e=>{if("string"!=typeof e)throw new TypeError("Invalid argument expected string");const t=e.match(d);if(!t)throw new Error(`Invalid argument not valid semver ('${e}' received)`);return t.shift(),t},c=e=>"*"===e||"x"===e||"X"===e,u=e=>{const t=parseInt(e,10);return isNaN(t)?e:t},p=(e,t)=>{if(c(e)||c(t))return 0;const[r,o]=((e,t)=>typeof e!=typeof t?[String(e),String(t)]:[e,t])(u(e),u(t));return r>o?1:r<o?-1:0},h=(e,t)=>{for(let r=0;r<Math.max(e.length,t.length);r++){const o=p(e[r]||"0",t[r]||"0");if(0!==o)return o}return 0},g=(e,t,r)=>{k(r);const o=((e,t)=>{const r=l(e),o=l(t),i=r.pop(),a=o.pop(),n=h(r,o);return 0!==n?n:i&&a?h(i.split("."),a.split(".")):i||a?i?-1:1:0})(e,t);return v[r].includes(o)},v={">":[1],">=":[0,1],"=":[0],"<=":[-1,0],"<":[-1],"!=":[-1,1]},m=Object.keys(v),k=e=>{if("string"!=typeof e)throw new TypeError("Invalid operator type, expected string but got "+typeof e);if(-1===m.indexOf(e))throw new Error(`Invalid operator, expected one of ${m.join("|")}`)};var b=r(61328);const y=new b.Q("knx-project-view");let f=(0,o.A)([(0,a.EM)("knx-project-view")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean,reflect:!0,attribute:"range-selector-hidden"})],key:"rangeSelectorHidden",value(){return!0}},{kind:"field",decorators:[(0,a.wk)()],key:"_visibleGroupAddresses",value(){return[]}},{kind:"field",decorators:[(0,a.wk)()],key:"_groupRangeAvailable",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){this.knx.project?this._isGroupRangeAvailable():this.knx.loadProject().then((()=>{this._isGroupRangeAvailable(),this.requestUpdate()}))}},{kind:"method",key:"_isGroupRangeAvailable",value:function(){var e,t;const r=null!==(e=null===(t=this.knx.project)||void 0===t?void 0:t.knxproject.info.xknxproject_version)&&void 0!==e?e:"0.0.0";y.debug("project version: "+r),this._groupRangeAvailable=g(r,"3.3.0",">=")}},{kind:"field",key:"_columns",value(){return(0,n.A)(((e,t)=>{const r="100px",o="82px",a="72px";return{address:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_address"),width:r},name:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_name"),width:`calc(100% - ${o} - ${r} - ${a})`},dpt:{sortable:!0,filterable:!0,title:this.knx.localize("project_view_table_dpt"),width:o,template:e=>e.dpt?i.qy`<span style="display:inline-block;width:24px;text-align:right;"
                  >${e.dpt.main}</span
                >${e.dpt.sub?"."+e.dpt.sub.toString().padStart(3,"0"):""} `:""},actions:{title:"",width:a,type:"overflow-menu",template:e=>this._groupAddressMenu(e)}}}))}},{kind:"method",key:"_groupAddressMenu",value:function(e){var t;const r=[];return 1===(null===(t=e.dpt)||void 0===t?void 0:t.main)&&r.push({path:"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",label:this.knx.localize("project_view_add_switch"),action:()=>{(0,s.o)("/knx/entities/create?ga="+e.address)}}),r.length?i.qy`
          <ha-icon-overflow-menu .hass=${this.hass} narrow .items=${r}> </ha-icon-overflow-menu>
        `:i.s6}},{kind:"method",key:"_getRows",value:function(e){return e.length?Object.entries(this.knx.project.knxproject.group_addresses).reduce(((t,[r,o])=>(e.includes(r)&&t.push(o),t)),[]):Object.values(this.knx.project.knxproject.group_addresses)}},{kind:"method",key:"_visibleAddressesChanged",value:function(e){this._visibleGroupAddresses=e.detail.groupAddresses}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.knx.project)return i.qy` <hass-loading-screen></hass-loading-screen> `;const e=this._getRows(this._visibleGroupAddresses);return i.qy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${this.tabs}
        .localizeFunc=${this.knx.localize}
      >
        ${this.knx.project.project_loaded?i.qy`${this.narrow&&this._groupRangeAvailable?i.qy`<ha-icon-button
                    slot="toolbar-icon"
                    .label=${this.hass.localize("ui.components.related-filter-menu.filter")}
                    .path=${"M6,13H18V11H6M3,6V8H21V6M10,18H14V16H10V18Z"}
                    @click=${this._toggleRangeSelector}
                  ></ha-icon-button>`:i.s6}
              <div class="sections">
                ${this._groupRangeAvailable?i.qy`
                      <knx-project-tree-view
                        .data=${this.knx.project.knxproject}
                        @knx-group-range-selection-changed=${this._visibleAddressesChanged}
                      ></knx-project-tree-view>
                    `:i.s6}
                <ha-data-table
                  class="ga-table"
                  .hass=${this.hass}
                  .columns=${this._columns(this.narrow,this.hass.language)}
                  .data=${e}
                  .hasFab=${!1}
                  .searchLabel=${this.hass.localize("ui.components.data-table.search")}
                  .clickable=${!1}
                ></ha-data-table>
              </div>`:i.qy` <ha-card .header=${this.knx.localize("attention")}>
              <div class="card-content">
                <p>${this.knx.localize("project_view_upload")}</p>
              </div>
            </ha-card>`}
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_toggleRangeSelector",value:function(){this.rangeSelectorHidden=!this.rangeSelectorHidden}},{kind:"get",static:!0,key:"styles",value:function(){return i.AH`
      hass-loading-screen {
        --app-header-background-color: var(--sidebar-background-color);
        --app-header-text-color: var(--sidebar-text-color);
      }
      .sections {
        display: flex;
        flex-direction: row;
        height: 100%;
      }

      :host([narrow]) knx-project-tree-view {
        position: absolute;
        max-width: calc(100% - 60px); /* 100% -> max 871px before not narrow */
        z-index: 1;
        right: 0;
        transition: 0.5s;
        border-left: 1px solid var(--divider-color);
      }

      :host([narrow][range-selector-hidden]) knx-project-tree-view {
        width: 0;
      }

      :host(:not([narrow])) knx-project-tree-view {
        max-width: 255px; /* min 616px - 816px for tree-view + ga-table (depending on side menu) */
      }

      .ga-table {
        flex: 1;
      }
    `}}]}}),i.WF)}};
//# sourceMappingURL=bxGJBUP9.js.map