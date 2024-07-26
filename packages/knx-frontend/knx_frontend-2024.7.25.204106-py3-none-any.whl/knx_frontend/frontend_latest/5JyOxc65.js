export const id=3399;export const ids=[3399];export const modules={43399:(e,i,a)=>{a.r(i),a.d(i,{HaImageSelector:()=>n});var l=a(62659),t=a(76504),o=a(80792),d=a(98597),r=a(196),s=a(33167),h=(a(89874),a(77984),a(59373),a(47385),a(32283),a(10377));let n=(0,l.A)([(0,r.EM)("ha-selector-image")],(function(e,i){class a extends i{constructor(...i){super(...i),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"name",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,r.wk)()],key:"showUpload",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(e){(0,t.A)((0,o.A)(a.prototype),"firstUpdated",this).call(this,e),this.value&&!this.value.startsWith(h.fO)||(this.showUpload=!0)}},{kind:"method",key:"render",value:function(){var e,i,a;return d.qy`
      <div>
        <label>
          ${this.hass.localize("ui.components.selectors.image.select_image")}
          <ha-formfield
            .label=${this.hass.localize("ui.components.selectors.image.upload")}
          >
            <ha-radio
              name="mode"
              value="upload"
              .checked=${this.showUpload}
              @change=${this._radioGroupPicked}
            ></ha-radio>
          </ha-formfield>
          <ha-formfield
            .label=${this.hass.localize("ui.components.selectors.image.url")}
          >
            <ha-radio
              name="mode"
              value="url"
              .checked=${!this.showUpload}
              @change=${this._radioGroupPicked}
            ></ha-radio>
          </ha-formfield>
        </label>
        ${this.showUpload?d.qy`
              <ha-picture-upload
                .hass=${this.hass}
                .value=${null!==(e=this.value)&&void 0!==e&&e.startsWith(h.fO)?this.value:null}
                .original=${null===(i=this.selector.image)||void 0===i?void 0:i.original}
                .cropOptions=${null===(a=this.selector.image)||void 0===a?void 0:a.crop}
                @change=${this._pictureChanged}
              ></ha-picture-upload>
            `:d.qy`
              <ha-textfield
                .name=${this.name}
                .value=${this.value||""}
                .placeholder=${this.placeholder||""}
                .helper=${this.helper}
                helperPersistent
                .disabled=${this.disabled}
                @input=${this._handleChange}
                .label=${this.label||""}
                .required=${this.required}
              ></ha-textfield>
            `}
      </div>
    `}},{kind:"method",key:"_radioGroupPicked",value:function(e){this.showUpload="upload"===e.target.value}},{kind:"method",key:"_pictureChanged",value:function(e){const i=e.target.value;(0,s.r)(this,"value-changed",{value:null!=i?i:void 0})}},{kind:"method",key:"_handleChange",value:function(e){let i=e.target.value;this.value!==i&&(""!==i||this.required||(i=void 0),(0,s.r)(this,"value-changed",{value:i}))}},{kind:"get",static:!0,key:"styles",value:function(){return d.AH`
      :host {
        display: block;
        position: relative;
      }
      div {
        display: flex;
        flex-direction: column;
      }
      label {
        display: flex;
        flex-direction: column;
      }
      ha-textarea,
      ha-textfield {
        width: 100%;
      }
    `}}]}}),d.WF)}};
//# sourceMappingURL=5JyOxc65.js.map