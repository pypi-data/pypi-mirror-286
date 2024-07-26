export const id=8590;export const ids=[8590];export const modules={22560:(e,i,t)=>{var a=t(62659),d=(t(23981),t(98597)),s=t(196),n=t(79278),l=t(33167),r=t(24517);t(96334),t(43689);(0,a.A)([(0,s.EM)("ha-base-time-input")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"autoValidate",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"format",value(){return 12}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"days",value(){return 0}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"hours",value(){return 0}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"minutes",value(){return 0}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"seconds",value(){return 0}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"milliseconds",value(){return 0}},{kind:"field",decorators:[(0,s.MZ)()],key:"dayLabel",value(){return""}},{kind:"field",decorators:[(0,s.MZ)()],key:"hourLabel",value(){return""}},{kind:"field",decorators:[(0,s.MZ)()],key:"minLabel",value(){return""}},{kind:"field",decorators:[(0,s.MZ)()],key:"secLabel",value(){return""}},{kind:"field",decorators:[(0,s.MZ)()],key:"millisecLabel",value(){return""}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"enableSecond",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"enableMillisecond",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"enableDay",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"noHoursLimit",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)()],key:"amPm",value(){return"AM"}},{kind:"method",key:"render",value:function(){return d.qy`
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
          max=${(0,n.J)(this._hourMax)}
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
              @closed=${r.d}
            >
              <mwc-list-item value="AM">AM</mwc-list-item>
              <mwc-list-item value="PM">PM</mwc-list-item>
            </ha-select>`}
      </div>
      ${this.helper?d.qy`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
    `}},{kind:"method",key:"_valueChanged",value:function(e){const i=e.currentTarget;this[i.name]="amPm"===i.name?i.value:Number(i.value);const t={hours:this.hours,minutes:this.minutes,seconds:this.seconds,milliseconds:this.milliseconds};this.enableDay&&(t.days=this.days),12===this.format&&(t.amPm=this.amPm),(0,l.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_onFocus",value:function(e){e.currentTarget.select()}},{kind:"method",key:"_formatValue",value:function(e,i=2){return e.toString().padStart(i,"0")}},{kind:"get",key:"_hourMax",value:function(){if(!this.noHoursLimit)return 12===this.format?12:23}},{kind:"field",static:!0,key:"styles",value(){return d.AH`
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
  `}}]}}),d.WF)},6759:(e,i,t)=>{var a=t(62659),d=t(98597),s=t(196),n=t(33167);t(22560);(0,a.A)([(0,s.EM)("ha-duration-input")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"enableMillisecond",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"enableDay",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.P)("paper-time-input",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return d.qy`
      <ha-base-time-input
        .label=${this.label}
        .helper=${this.helper}
        .required=${this.required}
        .autoValidate=${this.required}
        .disabled=${this.disabled}
        errorMessage="Required"
        enableSecond
        .enableMillisecond=${this.enableMillisecond}
        .enableDay=${this.enableDay}
        format="24"
        .days=${this._days}
        .hours=${this._hours}
        .minutes=${this._minutes}
        .seconds=${this._seconds}
        .milliseconds=${this._milliseconds}
        @value-changed=${this._durationChanged}
        noHoursLimit
        dayLabel="dd"
        hourLabel="hh"
        minLabel="mm"
        secLabel="ss"
        millisecLabel="ms"
      ></ha-base-time-input>
    `}},{kind:"get",key:"_days",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.days?Number(this.data.days):0}},{kind:"get",key:"_hours",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.hours?Number(this.data.hours):0}},{kind:"get",key:"_minutes",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.minutes?Number(this.data.minutes):0}},{kind:"get",key:"_seconds",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.seconds?Number(this.data.seconds):0}},{kind:"get",key:"_milliseconds",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.milliseconds?Number(this.data.milliseconds):0}},{kind:"method",key:"_durationChanged",value:function(e){e.stopPropagation();const i={...e.detail.value};var t;(this.enableMillisecond||i.milliseconds?i.milliseconds>999&&(i.seconds+=Math.floor(i.milliseconds/1e3),i.milliseconds%=1e3):delete i.milliseconds,i.seconds>59&&(i.minutes+=Math.floor(i.seconds/60),i.seconds%=60),i.minutes>59&&(i.hours+=Math.floor(i.minutes/60),i.minutes%=60),this.enableDay&&i.hours>24)&&(i.days=(null!==(t=i.days)&&void 0!==t?t:0)+Math.floor(i.hours/24),i.hours%=24);(0,n.r)(this,"value-changed",{value:i})}}]}}),d.WF)},38590:(e,i,t)=>{t.r(i),t.d(i,{HaFormTimePeriod:()=>n});var a=t(62659),d=t(98597),s=t(196);t(6759);let n=(0,a.A)([(0,s.EM)("ha-form-positive_time_period_dict")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.P)("ha-time-input",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return d.qy`
      <ha-duration-input
        .label=${this.label}
        ?required=${this.schema.required}
        .data=${this.data}
        .disabled=${this.disabled}
      ></ha-duration-input>
    `}}]}}),d.WF)}};
//# sourceMappingURL=MyBSfUOd.js.map