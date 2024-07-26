export const id=6048;export const ids=[6048];export const modules={66048:(e,a,t)=>{t.r(a),t.d(a,{HaFormExpendable:()=>s});var i=t(62659),o=t(98597),d=t(196);t(93259);let s=(0,i.A)([(0,d.EM)("ha-form-expandable")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"method",key:"render",value:function(){var e,a;return o.qy`
      <ha-expansion-panel outlined .expanded=${Boolean(this.schema.expanded)}>
        <div
          slot="header"
          role="heading"
          aria-level=${null!==(e=null===(a=this.schema.headingLevel)||void 0===a?void 0:a.toString())&&void 0!==e?e:"3"}
        >
          ${this.schema.icon?o.qy` <ha-icon .icon=${this.schema.icon}></ha-icon> `:this.schema.iconPath?o.qy`
                  <ha-svg-icon .path=${this.schema.iconPath}></ha-svg-icon>
                `:o.s6}
          ${this.schema.title}
        </div>
        <div class="content">
          <ha-form
            .hass=${this.hass}
            .data=${this.data}
            .schema=${this.schema.schema}
            .disabled=${this.disabled}
            .computeLabel=${this.computeLabel}
            .computeHelper=${this.computeHelper}
          ></ha-form>
        </div>
      </ha-expansion-panel>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        display: flex !important;
        flex-direction: column;
      }
      :host ha-form {
        display: block;
      }
      .content {
        padding: 12px;
      }
      ha-expansion-panel {
        display: block;
        --expansion-panel-content-padding: 0;
        border-radius: 6px;
        --ha-card-border-radius: 6px;
      }
      ha-svg-icon,
      ha-icon {
        color: var(--secondary-text-color);
      }
    `}}]}}),o.WF)}};
//# sourceMappingURL=ythPjOrC.js.map