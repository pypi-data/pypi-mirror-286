export const id=185;export const ids=[185];export const modules={86935:(t,e,i)=>{i.d(e,{mT:()=>u,Se:()=>l});var a=i(6601),o=i(19263);var r=i(94848);var s=i(68873);const n=new Set(["alarm_control_panel","alert","automation","binary_sensor","calendar","camera","climate","cover","device_tracker","fan","group","humidifier","input_boolean","lawn_mower","light","lock","media_player","person","plant","remote","schedule","script","siren","sun","switch","timer","update","vacuum","valve","water_heater"]),l=(t,e)=>{if((void 0!==e?e:null==t?void 0:t.state)===a.Hh)return"var(--state-unavailable-color)";const i=d(t,e);return i?(o=i,Array.isArray(o)?o.reverse().reduce(((t,e)=>`var(${e}${t?`, ${t}`:""})`),void 0):`var(${o})`):void 0;var o},c=(t,e,i)=>{const a=void 0!==i?i:e.state,o=(0,s.a)(e,i),n=[],l=(0,r.Y)(a,"_"),c=o?"active":"inactive",d=e.attributes.device_class;return d&&n.push(`--state-${t}-${d}-${l}-color`),n.push(`--state-${t}-${l}-color`,`--state-${t}-${c}-color`,`--state-${c}-color`),n},d=(t,e)=>{const i=void 0!==e?e:null==t?void 0:t.state,a=(0,o.m)(t.entity_id),r=t.attributes.device_class;if("sensor"===a&&"battery"===r){const t=(t=>{const e=Number(t);if(!isNaN(e))return e>=70?"--state-sensor-battery-high-color":e>=30?"--state-sensor-battery-medium-color":"--state-sensor-battery-low-color"})(i);if(t)return[t]}if("group"===a){const i=(t=>{const e=t.attributes.entity_id||[],i=[...new Set(e.map((t=>(0,o.m)(t))))];return 1===i.length?i[0]:void 0})(t);if(i&&n.has(i))return c(i,t,e)}if(n.has(a))return c(a,t,e)},u=t=>{if(t.attributes.brightness&&"plant"!==(0,o.m)(t.entity_id)){return`brightness(${(t.attributes.brightness+245)/5}%)`}return""}},94848:(t,e,i)=>{i.d(e,{Y:()=>a});const a=(t,e="_")=>{const i="àáâäæãåāăąçćčđďèéêëēėęěğǵḧîïíīįìıİłḿñńǹňôöòóœøōõőṕŕřßśšşșťțûüùúūǘůűųẃẍÿýžźż·",a=`aaaaaaaaaacccddeeeeeeeegghiiiiiiiilmnnnnoooooooooprrsssssttuuuuuuuuuwxyyzzz${e}`,o=new RegExp(i.split("").join("|"),"g");let r;return""===t?r="":(r=t.toString().toLowerCase().replace(o,(t=>a.charAt(i.indexOf(t)))).replace(/(\d),(?=\d)/g,"$1").replace(/[^a-z0-9]+/g,e).replace(new RegExp(`(${e})\\1+`,"g"),"$1").replace(new RegExp(`^${e}+`),"").replace(new RegExp(`${e}+$`),""),""===r&&(r="unknown")),r}},30185:(t,e,i)=>{var a=i(62659),o=i(76504),r=i(80792),s=i(98597),n=i(196),l=i(79278),c=i(12506),d=i(19263),u=i(80085),h=i(86935);const v=s.AH`
  ha-state-icon[data-domain="alarm_control_panel"][data-state="pending"],
  ha-state-icon[data-domain="alarm_control_panel"][data-state="arming"],
  ha-state-icon[data-domain="alarm_control_panel"][data-state="triggered"],
  ha-state-icon[data-domain="lock"][data-state="jammed"] {
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0% {
      opacity: 1;
    }
    50% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  /* Color the icon if unavailable */
  ha-state-icon[data-state="unavailable"] {
    color: var(--state-unavailable-color);
  }
`,b=(t,e,i)=>`${t}&width=${e}&height=${i}`;["auto","heat_cool","heat","cool","dry","fan_only","off"].reduce(((t,e,i)=>(t[e]=i,t)),{});const p={cooling:"cool",defrosting:"heat",drying:"dry",fan:"fan_only",heating:"heat",idle:"off",off:"off",preheating:"heat"};i(45063);let y=(0,a.A)(null,(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"overrideIcon",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"overrideImage",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"stateColor",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"color",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"icon",value(){return!0}},{kind:"field",decorators:[(0,n.wk)()],key:"_iconStyle",value(){return{}}},{kind:"method",key:"connectedCallback",value:function(){var t,e;(0,o.A)((0,r.A)(i.prototype),"connectedCallback",this).call(this),this.hasUpdated&&void 0===this.overrideImage&&(null!==(t=this.stateObj)&&void 0!==t&&t.attributes.entity_picture||null!==(e=this.stateObj)&&void 0!==e&&e.attributes.entity_picture_local)&&this.requestUpdate("stateObj")}},{kind:"method",key:"disconnectedCallback",value:function(){var t,e;(0,o.A)((0,r.A)(i.prototype),"disconnectedCallback",this).call(this),void 0===this.overrideImage&&(null!==(t=this.stateObj)&&void 0!==t&&t.attributes.entity_picture||null!==(e=this.stateObj)&&void 0!==e&&e.attributes.entity_picture_local)&&(this.style.backgroundImage="")}},{kind:"get",key:"_stateColor",value:function(){var t;const e=this.stateObj?(0,u.t)(this.stateObj):void 0;return null!==(t=this.stateColor)&&void 0!==t?t:"light"===e}},{kind:"method",key:"render",value:function(){const t=this.stateObj;if(!t&&!this.overrideIcon&&!this.overrideImage)return s.qy`<div class="missing">
        <ha-svg-icon .path=${"M13 14H11V9H13M13 18H11V16H13M1 21H23L12 2L1 21Z"}></ha-svg-icon>
      </div>`;if(!this.icon)return s.s6;const e=t?(0,u.t)(t):void 0;return s.qy`<ha-state-icon
      .hass=${this.hass}
      style=${(0,c.W)(this._iconStyle)}
      data-domain=${(0,l.J)(e)}
      data-state=${(0,l.J)(null==t?void 0:t.state)}
      .icon=${this.overrideIcon}
      .stateObj=${t}
    ></ha-state-icon>`}},{kind:"method",key:"willUpdate",value:function(t){if((0,o.A)((0,r.A)(i.prototype),"willUpdate",this).call(this,t),!(t.has("stateObj")||t.has("overrideImage")||t.has("overrideIcon")||t.has("stateColor")||t.has("color")))return;const e=this.stateObj,a={};let s="";if(this.icon=!0,e&&void 0===this.overrideImage)if(!e.attributes.entity_picture_local&&!e.attributes.entity_picture||this.overrideIcon){if(this.color)a.color=this.color;else if(this._stateColor){const t=(0,h.Se)(e);if(t&&(a.color=t),e.attributes.rgb_color&&(a.color=`rgb(${e.attributes.rgb_color.join(",")})`),e.attributes.brightness){const t=e.attributes.brightness;if("number"!=typeof t){const i=`Type error: state-badge expected number, but type of ${e.entity_id}.attributes.brightness is ${typeof t} (${t})`;console.warn(i)}a.filter=(0,h.mT)(e)}if(e.attributes.hvac_action){const t=e.attributes.hvac_action;t in p?a.color=(0,h.Se)(e,p[t]):delete a.color}}}else{let t=e.attributes.entity_picture_local||e.attributes.entity_picture;this.hass&&(t=this.hass.hassUrl(t));const i=(0,d.m)(e.entity_id);"camera"===i&&(t=b(t,80,80)),s=`url(${t})`,this.icon=!1,"update"===i?this.style.borderRadius="0":"media_player"===i&&(this.style.borderRadius="8%")}else if(this.overrideImage){let t=this.overrideImage;this.hass&&(t=this.hass.hassUrl(t)),s=`url(${t})`,this.icon=!1}this._iconStyle=a,this.style.backgroundImage=s}},{kind:"get",static:!0,key:"styles",value:function(){return[v,s.AH`
        :host {
          position: relative;
          display: inline-block;
          width: 40px;
          color: var(--paper-item-icon-color, #44739e);
          border-radius: 50%;
          height: 40px;
          text-align: center;
          background-size: cover;
          line-height: 40px;
          vertical-align: middle;
          box-sizing: border-box;
          --state-inactive-color: initial;
        }
        :host(:focus) {
          outline: none;
        }
        :host(:not([icon]):focus) {
          border: 2px solid var(--divider-color);
        }
        :host([icon]:focus) {
          background: var(--divider-color);
        }
        ha-state-icon {
          transition:
            color 0.3s ease-in-out,
            filter 0.3s ease-in-out;
        }
        .missing {
          color: #fce588;
        }
      `]}}]}}),s.WF);customElements.define("state-badge",y)}};
//# sourceMappingURL=q7w59gFK.js.map