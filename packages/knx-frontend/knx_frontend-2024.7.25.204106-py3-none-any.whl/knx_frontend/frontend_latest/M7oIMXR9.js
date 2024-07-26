export const id=6401;export const ids=[6401];export const modules={49655:(e,t,a)=>{a.d(t,{J:()=>r});var i=a(45081),d=a(76415);const r=(0,i.A)((e=>{if(e.time_format===d.Hg.language||e.time_format===d.Hg.system){const t=e.time_format===d.Hg.language?e.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(t).includes("10")}return e.time_format===d.Hg.am_pm}))},22560:(e,t,a)=>{var i=a(62659),d=(a(23981),a(98597)),r=a(196),l=a(79278),n=a(33167),s=a(24517);a(96334),a(43689);(0,i.A)([(0,r.EM)("ha-base-time-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"autoValidate",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Number})],key:"format",value(){return 12}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Number})],key:"days",value(){return 0}},{kind:"field",decorators:[(0,r.MZ)({type:Number})],key:"hours",value(){return 0}},{kind:"field",decorators:[(0,r.MZ)({type:Number})],key:"minutes",value(){return 0}},{kind:"field",decorators:[(0,r.MZ)({type:Number})],key:"seconds",value(){return 0}},{kind:"field",decorators:[(0,r.MZ)({type:Number})],key:"milliseconds",value(){return 0}},{kind:"field",decorators:[(0,r.MZ)()],key:"dayLabel",value(){return""}},{kind:"field",decorators:[(0,r.MZ)()],key:"hourLabel",value(){return""}},{kind:"field",decorators:[(0,r.MZ)()],key:"minLabel",value(){return""}},{kind:"field",decorators:[(0,r.MZ)()],key:"secLabel",value(){return""}},{kind:"field",decorators:[(0,r.MZ)()],key:"millisecLabel",value(){return""}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"enableSecond",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"enableMillisecond",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"enableDay",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"noHoursLimit",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)()],key:"amPm",value(){return"AM"}},{kind:"method",key:"render",value:function(){return d.qy`
      ${this.label?d.qy`<label>${this.label}${this.required?" *":""}</label>`:""}
      <div class="time-input-wrap">
        ${this.enableDay?d.qy`
              <ha-textfield
                id="day"
                type="number"
                inputmode="numeric"
                .value=${this.days.toFixed()}
                .label=${this.dayLabel}
                name="days"
                @change=${this._valueChanged}
                @focusin=${this._onFocus}
                no-spinner
                .required=${this.required}
                .autoValidate=${this.autoValidate}
                min="0"
                .disabled=${this.disabled}
                suffix=":"
                class="hasSuffix"
              >
              </ha-textfield>
            `:""}

        <ha-textfield
          id="hour"
          type="number"
          inputmode="numeric"
          .value=${this.hours.toFixed()}
          .label=${this.hourLabel}
          name="hours"
          @change=${this._valueChanged}
          @focusin=${this._onFocus}
          no-spinner
          .required=${this.required}
          .autoValidate=${this.autoValidate}
          maxlength="2"
          max=${(0,l.J)(this._hourMax)}
          min="0"
          .disabled=${this.disabled}
          suffix=":"
          class="hasSuffix"
        >
        </ha-textfield>
        <ha-textfield
          id="min"
          type="number"
          inputmode="numeric"
          .value=${this._formatValue(this.minutes)}
          .label=${this.minLabel}
          @change=${this._valueChanged}
          @focusin=${this._onFocus}
          name="minutes"
          no-spinner
          .required=${this.required}
          .autoValidate=${this.autoValidate}
          maxlength="2"
          max="59"
          min="0"
          .disabled=${this.disabled}
          .suffix=${this.enableSecond?":":""}
          class=${this.enableSecond?"has-suffix":""}
        >
        </ha-textfield>
        ${this.enableSecond?d.qy`<ha-textfield
              id="sec"
              type="number"
              inputmode="numeric"
              .value=${this._formatValue(this.seconds)}
              .label=${this.secLabel}
              @change=${this._valueChanged}
              @focusin=${this._onFocus}
              name="seconds"
              no-spinner
              .required=${this.required}
              .autoValidate=${this.autoValidate}
              maxlength="2"
              max="59"
              min="0"
              .disabled=${this.disabled}
              .suffix=${this.enableMillisecond?":":""}
              class=${this.enableMillisecond?"has-suffix":""}
            >
            </ha-textfield>`:""}
        ${this.enableMillisecond?d.qy`<ha-textfield
              id="millisec"
              type="number"
              .value=${this._formatValue(this.milliseconds,3)}
              .label=${this.millisecLabel}
              @change=${this._valueChanged}
              @focusin=${this._onFocus}
              name="milliseconds"
              no-spinner
              .required=${this.required}
              .autoValidate=${this.autoValidate}
              maxlength="3"
              max="999"
              min="0"
              .disabled=${this.disabled}
            >
            </ha-textfield>`:""}
        ${24===this.format?"":d.qy`<ha-select
              .required=${this.required}
              .value=${this.amPm}
              .disabled=${this.disabled}
              name="amPm"
              naturalMenuWidth
              fixedMenuPosition
              @selected=${this._valueChanged}
              @closed=${s.d}
            >
              <mwc-list-item value="AM">AM</mwc-list-item>
              <mwc-list-item value="PM">PM</mwc-list-item>
            </ha-select>`}
      </div>
      ${this.helper?d.qy`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
    `}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.currentTarget;this[t.name]="amPm"===t.name?t.value:Number(t.value);const a={hours:this.hours,minutes:this.minutes,seconds:this.seconds,milliseconds:this.milliseconds};this.enableDay&&(a.days=this.days),12===this.format&&(a.amPm=this.amPm),(0,n.r)(this,"value-changed",{value:a})}},{kind:"method",key:"_onFocus",value:function(e){e.currentTarget.select()}},{kind:"method",key:"_formatValue",value:function(e,t=2){return e.toString().padStart(t,"0")}},{kind:"get",key:"_hourMax",value:function(){if(!this.noHoursLimit)return 12===this.format?12:23}},{kind:"field",static:!0,key:"styles",value(){return d.AH`
    :host {
      display: block;
    }
    .time-input-wrap {
      display: flex;
      border-radius: var(--mdc-shape-small, 4px) var(--mdc-shape-small, 4px) 0 0;
      overflow: hidden;
      position: relative;
      direction: ltr;
    }
    ha-textfield {
      width: 40px;
      text-align: center;
      --mdc-shape-small: 0;
      --text-field-appearance: none;
      --text-field-padding: 0 4px;
      --text-field-suffix-padding-left: 2px;
      --text-field-suffix-padding-right: 0;
      --text-field-text-align: center;
    }
    ha-textfield.hasSuffix {
      --text-field-padding: 0 0 0 4px;
    }
    ha-textfield:first-child {
      --text-field-border-top-left-radius: var(--mdc-shape-medium);
    }
    ha-textfield:last-child {
      --text-field-border-top-right-radius: var(--mdc-shape-medium);
    }
    ha-select {
      --mdc-shape-small: 0;
      width: 85px;
    }
    label {
      -moz-osx-font-smoothing: grayscale;
      -webkit-font-smoothing: antialiased;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, Roboto, sans-serif)
      );
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      line-height: var(--mdc-typography-body2-line-height, 1.25rem);
      font-weight: var(--mdc-typography-body2-font-weight, 400);
      letter-spacing: var(
        --mdc-typography-body2-letter-spacing,
        0.0178571429em
      );
      text-decoration: var(--mdc-typography-body2-text-decoration, inherit);
      text-transform: var(--mdc-typography-body2-text-transform, inherit);
      color: var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));
      padding-left: 4px;
      padding-inline-start: 4px;
      padding-inline-end: initial;
    }
  `}}]}}),d.WF)},36401:(e,t,a)=>{a.r(t),a.d(t,{HaTimeSelector:()=>l});var i=a(62659),d=a(98597),r=a(196);a(94110);let l=(0,i.A)([(0,r.EM)("ha-selector-time")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"method",key:"render",value:function(){return d.qy`
      <ha-time-input
        .value=${"string"==typeof this.value?this.value:void 0}
        .locale=${this.hass.locale}
        .disabled=${this.disabled}
        .required=${this.required}
        .helper=${this.helper}
        .label=${this.label}
        enable-second
      ></ha-time-input>
    `}}]}}),d.WF)},94110:(e,t,a)=>{var i=a(62659),d=a(98597),r=a(196),l=a(49655),n=a(33167);a(22560);(0,i.A)([(0,r.EM)("ha-time-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"locale",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"enable-second"})],key:"enableSecond",value(){return!1}},{kind:"method",key:"render",value:function(){var e;const t=(0,l.J)(this.locale),a=(null===(e=this.value)||void 0===e?void 0:e.split(":"))||[];let i=a[0];const r=Number(a[0]);return r&&t&&r>12&&r<24&&(i=String(r-12).padStart(2,"0")),t&&0===r&&(i="12"),d.qy`
      <ha-base-time-input
        .label=${this.label}
        .hours=${Number(i)}
        .minutes=${Number(a[1])}
        .seconds=${Number(a[2])}
        .format=${t?12:24}
        .amPm=${t&&r>=12?"PM":"AM"}
        .disabled=${this.disabled}
        @value-changed=${this._timeChanged}
        .enableSecond=${this.enableSecond}
        .required=${this.required}
        .helper=${this.helper}
      ></ha-base-time-input>
    `}},{kind:"method",key:"_timeChanged",value:function(e){e.stopPropagation();const t=e.detail.value,a=(0,l.J)(this.locale);let i;if(!isNaN(t.hours)||!isNaN(t.minutes)||!isNaN(t.seconds)){let e=t.hours||0;t&&a&&("PM"===t.amPm&&e<12&&(e+=12),"AM"===t.amPm&&12===e&&(e=0)),i=`${e.toString().padStart(2,"0")}:${t.minutes?t.minutes.toString().padStart(2,"0"):"00"}:${t.seconds?t.seconds.toString().padStart(2,"0"):"00"}`}i!==this.value&&(this.value=i,(0,n.r)(this,"change"),(0,n.r)(this,"value-changed",{value:i}))}}]}}),d.WF)},76415:(e,t,a)=>{a.d(t,{Hg:()=>d,Wj:()=>r,jG:()=>i,ow:()=>l,zt:()=>n});let i=function(e){return e.language="language",e.system="system",e.comma_decimal="comma_decimal",e.decimal_comma="decimal_comma",e.space_comma="space_comma",e.none="none",e}({}),d=function(e){return e.language="language",e.system="system",e.am_pm="12",e.twenty_four="24",e}({}),r=function(e){return e.local="local",e.server="server",e}({}),l=function(e){return e.language="language",e.system="system",e.DMY="DMY",e.MDY="MDY",e.YMD="YMD",e}({}),n=function(e){return e.language="language",e.monday="monday",e.tuesday="tuesday",e.wednesday="wednesday",e.thursday="thursday",e.friday="friday",e.saturday="saturday",e.sunday="sunday",e}({})}};
//# sourceMappingURL=M7oIMXR9.js.map