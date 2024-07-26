var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc2) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc2 = __getOwnPropDesc(from, key)) || desc2.enumerable });
  }
  return to;
};
var __reExport = (target, mod, secondTarget) => (__copyProps(target, mod, "default"), secondTarget && __copyProps(secondTarget, mod, "default"));

// lib/widget.ts
import * as mc from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import { Query as Query5 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
import * as arrow3 from "https://esm.sh/apache-arrow@16.1.0";
import * as uuid from "https://esm.sh/@lukeed/uuid@2.0.1";
import { effect as effect4 } from "https://esm.sh/@preact/signals-core@1.6.1";

// lib/clients/DataTable.ts
import * as arrow2 from "https://esm.sh/apache-arrow@16.1.0";
import {
  MosaicClient as MosaicClient4,
  Selection as Selection2
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import { desc, Query as Query4 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
import * as signals from "https://esm.sh/@preact/signals-core@1.6.1";
import { html } from "https://esm.sh/htl@0.3.1";

// lib/utils/assert.ts
var AssertionError = class extends Error {
  /** @param message The error message. */
  constructor(message) {
    super(message);
    this.name = "AssertionError";
  }
};
function assert(expr, msg = "") {
  if (!expr) {
    throw new AssertionError(msg);
  }
}

// lib/utils/AsyncBatchReader.ts
var AsyncBatchReader = class {
  /** the iterable batches to read */
  #batches = [];
  /** the index of the current row */
  #index = 0;
  /** resolves a promise for when the next batch is available */
  #resolve = null;
  /** the current batch */
  #current = null;
  /** A function to request more data. */
  #requestNextBatch;
  /**
   * @param requestNextBatch - a function to request more data. When
   * this function completes, it should enqueue the next batch, otherwise the
   * reader will be stuck.
   */
  constructor(requestNextBatch) {
    this.#requestNextBatch = requestNextBatch;
  }
  /**
   * Enqueue a batch of data
   *
   * The last batch should have `last: true` set,
   * so the reader can terminate when it has
   * exhausted all the data.
   *
   * @param batch - the batch of data to enqueue
   * @param options
   * @param options.last - whether this is the last batch
   */
  enqueueBatch(batch, { last }) {
    this.#batches.push({ data: batch, last });
    if (this.#resolve) {
      this.#resolve();
      this.#resolve = null;
    }
  }
  async next() {
    if (!this.#current) {
      if (this.#batches.length === 0) {
        let promise = new Promise((resolve) => {
          this.#resolve = resolve;
        });
        this.#requestNextBatch();
        await promise;
      }
      let next = this.#batches.shift();
      assert(next, "No next batch");
      this.#current = next;
    }
    let result = this.#current.data.next();
    if (result.done) {
      if (this.#current.last) {
        return { done: true, value: void 0 };
      }
      this.#current = null;
      return this.next();
    }
    return {
      done: false,
      value: { row: result.value, index: this.#index++ }
    };
  }
};

// lib/utils/formatting.ts
import { Temporal } from "https://esm.sh/@js-temporal/polyfill@0.4.4";
import * as arrow from "https://esm.sh/apache-arrow@16.1.0";
function fmt(_arrowDataTypeValue, format2, log = false) {
  return (value) => {
    if (log)
      console.log(value);
    if (value === void 0 || value === null) {
      return stringify(value);
    }
    return format2(value);
  };
}
function stringify(x) {
  return `${x}`;
}
function formatDataType(type) {
  if (arrow.DataType.isLargeBinary(type))
    return "large binary";
  if (arrow.DataType.isLargeUtf8(type))
    return "large utf8";
  return type.toString().toLowerCase().replace("<second>", "[s]").replace("<millisecond>", "[ms]").replace("<microsecond>", "[\xB5s]").replace("<nanosecond>", "[ns]").replace("<day>", "[day]").replace("dictionary<", "dict<");
}
function formatterForValue(type) {
  if (arrow.DataType.isNull(type)) {
    return fmt(type.TValue, stringify);
  }
  if (arrow.DataType.isInt(type) || arrow.DataType.isFloat(type)) {
    return fmt(type.TValue, (value) => {
      if (Number.isNaN(value))
        return "NaN";
      return value === 0 ? "0" : value.toLocaleString("en");
    });
  }
  if (arrow.DataType.isBinary(type) || arrow.DataType.isFixedSizeBinary(type) || arrow.DataType.isLargeBinary(type)) {
    return fmt(type.TValue, (bytes) => {
      let maxlen = 32;
      let result = "b'";
      for (let i = 0; i < Math.min(bytes.length, maxlen); i++) {
        const byte = bytes[i];
        if (byte >= 32 && byte <= 126) {
          result += String.fromCharCode(byte);
        } else {
          result += "\\x" + ("00" + byte.toString(16)).slice(-2);
        }
      }
      if (bytes.length > maxlen)
        result += "...";
      result += "'";
      return result;
    });
  }
  if (arrow.DataType.isUtf8(type) || arrow.DataType.isLargeUtf8(type)) {
    return fmt(type.TValue, (text) => text);
  }
  if (arrow.DataType.isBool(type)) {
    return fmt(type.TValue, stringify);
  }
  if (arrow.DataType.isDecimal(type)) {
    return fmt(type.TValue, () => "TODO");
  }
  if (arrow.DataType.isDate(type)) {
    return fmt(type.TValue, (ms) => {
      return Temporal.Instant.fromEpochMilliseconds(ms).toZonedDateTimeISO("UTC").toPlainDate().toString();
    });
  }
  if (arrow.DataType.isTime(type)) {
    return fmt(type.TValue, (ms) => {
      return instantFromTimeUnit(ms, type.unit).toZonedDateTimeISO("UTC").toPlainTime().toString();
    });
  }
  if (arrow.DataType.isTimestamp(type)) {
    return fmt(type.TValue, (ms) => {
      return Temporal.Instant.fromEpochMilliseconds(ms).toZonedDateTimeISO("UTC").toPlainDateTime().toString();
    });
  }
  if (arrow.DataType.isInterval(type)) {
    return fmt(type.TValue, (_value) => {
      return "TODO";
    });
  }
  if (arrow.DataType.isDuration(type)) {
    return fmt(type.TValue, (bigintValue) => {
      return durationFromTimeUnit(bigintValue, type.unit).toString();
    });
  }
  if (arrow.DataType.isList(type)) {
    return fmt(type.TValue, (value) => {
      return value.toString();
    });
  }
  if (arrow.DataType.isStruct(type)) {
    return fmt(type.TValue, (value) => {
      return value.toString();
    });
  }
  if (arrow.DataType.isUnion(type)) {
    return fmt(type.TValue, (_value) => {
      return "TODO";
    });
  }
  if (arrow.DataType.isMap(type)) {
    return fmt(type.TValue, (_value) => {
      return "TODO";
    });
  }
  if (arrow.DataType.isDictionary(type)) {
    let formatter = formatterForValue(type.dictionary);
    return fmt(type.TValue, formatter);
  }
  return () => `Unsupported type: ${type}`;
}
function instantFromTimeUnit(value, unit) {
  if (unit === arrow.TimeUnit.SECOND) {
    if (typeof value === "bigint")
      value = Number(value);
    return Temporal.Instant.fromEpochSeconds(value);
  }
  if (unit === arrow.TimeUnit.MILLISECOND) {
    if (typeof value === "bigint")
      value = Number(value);
    return Temporal.Instant.fromEpochMilliseconds(value);
  }
  if (unit === arrow.TimeUnit.MICROSECOND) {
    if (typeof value === "number")
      value = BigInt(value);
    return Temporal.Instant.fromEpochMicroseconds(value);
  }
  if (unit === arrow.TimeUnit.NANOSECOND) {
    if (typeof value === "number")
      value = BigInt(value);
    return Temporal.Instant.fromEpochNanoseconds(value);
  }
  throw new Error("Invalid TimeUnit");
}
function durationFromTimeUnit(value, unit) {
  value = Number(value);
  if (unit === arrow.TimeUnit.SECOND) {
    return Temporal.Duration.from({ seconds: value });
  }
  if (unit === arrow.TimeUnit.MILLISECOND) {
    return Temporal.Duration.from({ milliseconds: value });
  }
  if (unit === arrow.TimeUnit.MICROSECOND) {
    return Temporal.Duration.from({ microseconds: value });
  }
  if (unit === arrow.TimeUnit.NANOSECOND) {
    return Temporal.Duration.from({ nanoseconds: value });
  }
  throw new Error("Invalid TimeUnit");
}

// lib/clients/Histogram.ts
import {
  MosaicClient
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import { count, Query } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
import * as mplot from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-plot@0.10.0/+esm";

// lib/deps/d3.ts
var d3_exports = {};
__reExport(d3_exports, d3_selection_star);
__reExport(d3_exports, d3_scale_star);
__reExport(d3_exports, d3_axis_star);
__reExport(d3_exports, d3_format_star);
__reExport(d3_exports, d3_time_format_star);
import * as d3_selection_star from "https://esm.sh/d3-selection@3.0.0";
import * as d3_scale_star from "https://esm.sh/d3-scale@4.0.2";
import * as d3_axis_star from "https://esm.sh/d3-axis@3.0.0";
import * as d3_format_star from "https://esm.sh/d3-format@3.1.0";
import * as d3_time_format_star from "https://esm.sh/d3-time-format@4.1.0";

// lib/utils/tick-formatter-for-bins.ts
var YEAR = "year";
var MONTH = "month";
var DAY = "day";
var HOUR = "hour";
var MINUTE = "minute";
var SECOND = "second";
var MILLISECOND = "millisecond";
var durationSecond = 1e3;
var durationMinute = durationSecond * 60;
var durationHour = durationMinute * 60;
var durationDay = durationHour * 24;
var durationWeek = durationDay * 7;
var durationMonth = durationDay * 30;
var durationYear = durationDay * 365;
var intervals = [
  [SECOND, 1, durationSecond],
  [SECOND, 5, 5 * durationSecond],
  [SECOND, 15, 15 * durationSecond],
  [SECOND, 30, 30 * durationSecond],
  [MINUTE, 1, durationMinute],
  [MINUTE, 5, 5 * durationMinute],
  [MINUTE, 15, 15 * durationMinute],
  [MINUTE, 30, 30 * durationMinute],
  [HOUR, 1, durationHour],
  [HOUR, 3, 3 * durationHour],
  [HOUR, 6, 6 * durationHour],
  [HOUR, 12, 12 * durationHour],
  [DAY, 1, durationDay],
  [DAY, 7, durationWeek],
  [MONTH, 1, durationMonth],
  [MONTH, 3, 3 * durationMonth],
  [YEAR, 1, durationYear]
];
var formatMap = {
  [MILLISECOND]: d3_exports.timeFormat("%L"),
  [SECOND]: d3_exports.timeFormat("%S s"),
  [MINUTE]: d3_exports.timeFormat("%H:%M"),
  [HOUR]: d3_exports.timeFormat("%H:%M"),
  [DAY]: d3_exports.timeFormat("%b %d"),
  [MONTH]: d3_exports.timeFormat("%b %Y"),
  [YEAR]: d3_exports.timeFormat("%Y")
};
function tickFormatterForBins(type, bins) {
  if (type === "number") {
    return d3_exports.format("~s");
  }
  let interval = timeInterval(
    bins[0].x0,
    bins[bins.length - 1].x1,
    bins.length
  );
  return formatMap[interval.interval];
}
function timeInterval(min, max, steps) {
  const span = max - min;
  const target = span / steps;
  let i = 0;
  while (i < intervals.length && intervals[i][2] < target) {
    i++;
  }
  if (i === intervals.length) {
    return { interval: YEAR, step: binStep(span, steps) };
  }
  if (i > 0) {
    let interval = intervals[target / intervals[i - 1][2] < intervals[i][2] / target ? i - 1 : i];
    return { interval: interval[0], step: interval[1] };
  }
  return { interval: MILLISECOND, step: binStep(span, steps, 1) };
}
function binStep(span, steps, minstep = 0, logb = Math.LN10) {
  let v;
  const level = Math.ceil(Math.log(steps) / logb);
  let step = Math.max(
    minstep,
    Math.pow(10, Math.round(Math.log(span) / logb) - level)
  );
  while (Math.ceil(span / step) > steps)
    step *= 10;
  const div = [5, 2];
  for (let i = 0, n = div.length; i < n; ++i) {
    v = step / div[i];
    if (v >= minstep && span / v <= steps)
      step = v;
  }
  return step;
}

// lib/utils/CrossfilterHistogramPlot.ts
function CrossfilterHistogramPlot(bins, {
  type = "number",
  width = 125,
  height = 40,
  marginTop = 0,
  marginRight = 2,
  marginBottom = 12,
  marginLeft = 2,
  nullCount = 0,
  fillColor = "var(--primary)",
  nullFillColor = "var(--secondary)",
  backgroundBarColor = "var(--moon-gray)"
}) {
  let nullBinWidth = nullCount === 0 ? 0 : 5;
  let spacing = nullBinWidth ? 4 : 0;
  let extent = (
    /** @type {const} */
    [
      Math.min(...bins.map((d) => d.x0)),
      Math.max(...bins.map((d) => d.x1))
    ]
  );
  let x = type === "date" ? d3_exports.scaleUtc() : d3_exports.scaleLinear();
  x.domain(extent).range([marginLeft + nullBinWidth + spacing, width - marginRight]).nice();
  let y = d3_exports.scaleLinear().domain([0, Math.max(nullCount, ...bins.map((d) => d.length))]).range([height - marginBottom, marginTop]);
  let svg = d3_exports.create("svg").attr("width", width).attr("height", height).attr("viewBox", [0, 0, width, height]).attr("style", "max-width: 100%; height: auto; overflow: visible;");
  {
    svg.append("g").attr("fill", backgroundBarColor).selectAll("rect").data(bins).join("rect").attr("x", (d) => x(d.x0) + 1.5).attr("width", (d) => x(d.x1) - x(d.x0) - 1.5).attr("y", (d) => y(d.length)).attr("height", (d) => y(0) - y(d.length));
  }
  let foregroundBarGroup = svg.append("g").attr("fill", fillColor);
  svg.append("g").attr("transform", `translate(0,${height - marginBottom})`).call(
    d3_exports.axisBottom(x).tickValues(x.domain()).tickFormat(tickFormatterForBins(type, bins)).tickSize(2.5)
  ).call((g) => {
    g.select(".domain").remove();
    g.attr("class", "gray");
    g.selectAll(".tick text").attr("text-anchor", (_, i) => i === 0 ? "start" : "end").attr("dx", (_, i) => i === 0 ? "-0.25em" : "0.25em");
  });
  let foregroundNullGroup = void 0;
  if (nullCount > 0) {
    let xnull = d3_exports.scaleLinear().range([marginLeft, marginLeft + nullBinWidth]);
    svg.append("g").attr("fill", backgroundBarColor).append("rect").attr("x", xnull(0)).attr("width", xnull(1) - xnull(0)).attr("y", y(nullCount)).attr("height", y(0) - y(nullCount));
    foregroundNullGroup = svg.append("g").attr("fill", nullFillColor).attr("color", nullFillColor);
    foregroundNullGroup.append("rect").attr("x", xnull(0)).attr("width", xnull(1) - xnull(0));
    let axisGroup = foregroundNullGroup.append("g").attr("transform", `translate(0,${height - marginBottom})`).append("g").attr("transform", `translate(${xnull(0.5)}, 0)`).attr("class", "tick");
    axisGroup.append("line").attr("stroke", "currentColor").attr("y2", 2.5);
    axisGroup.append("text").attr("fill", "currentColor").attr("y", 4.5).attr("dy", "0.71em").attr("text-anchor", "middle").text("\u2205").attr("font-size", "0.9em").attr("font-family", "var(--sans-serif)").attr("font-weight", "normal");
  }
  svg.selectAll(".tick").attr("font-family", "var(--sans-serif)").attr("font-weight", "normal");
  function render(bins2, nullCount2) {
    foregroundBarGroup.selectAll("rect").data(bins2).join("rect").attr("x", (d) => x(d.x0) + 1.5).attr("width", (d) => x(d.x1) - x(d.x0) - 1.5).attr("y", (d) => y(d.length)).attr("height", (d) => y(0) - y(d.length));
    foregroundNullGroup?.select("rect").attr("y", y(nullCount2)).attr("height", y(0) - y(nullCount2));
  }
  let scales = {
    x: Object.assign(x, {
      type: "linear",
      domain: x.domain(),
      range: x.range()
    }),
    y: Object.assign(y, {
      type: "linear",
      domain: y.domain(),
      range: y.range()
    })
  };
  let node = svg.node();
  assert(node, "Infallable");
  render(bins, nullCount);
  return Object.assign(node, {
    /** @param {string} type */
    scale(type2) {
      let scale = scales[type2];
      assert(scale, "Invalid scale type");
      return scale;
    },
    /**
     * @param {Array<Bin>} bins
     * @param {{ nullCount: number }} opts
     */
    update(bins2, { nullCount: nullCount2 }) {
      render(bins2, nullCount2);
    },
    reset() {
      render(bins, nullCount);
    }
  });
}

// lib/clients/Histogram.ts
var Histogram = class extends MosaicClient {
  #source;
  #el = document.createElement("div");
  #select;
  #interval = void 0;
  #initialized = false;
  #fieldInfo;
  svg;
  constructor(options) {
    super(options.filterBy);
    this.#source = options;
    let bin2 = mplot.bin(options.column)(this, "x");
    this.#select = { x1: bin2.x1, x2: bin2.x2, y: count() };
    this.#interval = new mplot.Interval1D(this, {
      channel: "x",
      selection: this.filterBy,
      field: this.#source.column,
      brush: void 0
    });
  }
  fields() {
    return [
      {
        table: this.#source.table,
        column: this.#source.column,
        stats: ["min", "max"]
      }
    ];
  }
  fieldInfo(info) {
    this.#fieldInfo = info[0];
    return this;
  }
  /**
   * Return a query specifying the data needed by this Mark client.
   * @param filter The filtering criteria to apply in the query.
   * @returns The client query
   */
  query(filter = []) {
    return Query.from({ source: this.#source.table }).select(this.#select).groupby(["x1", "x2"]).where(filter);
  }
  /**
   * Provide query result data to the mark.
   */
  queryResult(data) {
    let bins = Array.from(data, (d) => ({
      x0: d.x1,
      x1: d.x2,
      length: d.y
    }));
    let nullCount = 0;
    let nullBinIndex = bins.findIndex((b) => b.x0 == null);
    if (nullBinIndex >= 0) {
      nullCount = bins[nullBinIndex].length;
      bins.splice(nullBinIndex, 1);
    }
    if (!this.#initialized) {
      this.svg = CrossfilterHistogramPlot(bins, {
        nullCount,
        type: this.#source.type
      });
      this.#interval?.init(this.svg, null);
      this.#el.appendChild(this.svg);
      this.#initialized = true;
    } else {
      this.svg?.update(bins, { nullCount });
    }
    return this;
  }
  /* Required by the Mark interface */
  type = "rectY";
  /** Required by `mplot.bin` to get the field info. */
  channelField(channel) {
    assert(channel === "x");
    assert(this.#fieldInfo, "No field info yet");
    return this.#fieldInfo;
  }
  get plot() {
    return {
      node: () => this.#el,
      getAttribute(_name) {
        return void 0;
      }
    };
  }
};

// lib/clients/ValueCounts.ts
import { clausePoint, MosaicClient as MosaicClient2 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import {
  column,
  count as count2,
  Query as Query2,
  sql,
  sum
} from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
import { effect as effect2 } from "https://esm.sh/@preact/signals-core@1.6.1";

// lib/utils/ValueCountsPlot.ts
import { effect, signal } from "https://esm.sh/@preact/signals-core@1.6.1";
function ValueCountsPlot(data, {
  width = 125,
  height = 30,
  marginBottom = 12,
  marginRight = 2,
  marginLeft = 2,
  fillColor = "var(--primary)",
  nullFillColor = "var(--secondary)",
  backgroundBarColor = "rgb(226, 226, 226)"
} = {}) {
  let root = document.createElement("div");
  root.style.position = "relative";
  let container = document.createElement("div");
  Object.assign(container.style, {
    width: `${width}px`,
    height: `${height}px`,
    display: "flex",
    borderRadius: "5px",
    overflow: "hidden"
  });
  let bars = createBars(data, {
    width,
    height,
    marginRight,
    marginLeft,
    fillColor,
    nullFillColor,
    backgroundBarColor
  });
  for (let bar of bars.elements) {
    container.appendChild(bar);
  }
  let text = createTextOutput();
  let hovering = signal(void 0);
  let selected = signal(void 0);
  let counts = signal(data);
  let hitArea = document.createElement("div");
  Object.assign(hitArea.style, {
    position: "absolute",
    top: "0",
    left: "-5px",
    width: `${width + 10}px`,
    height: `${height + marginBottom}px`,
    backgroundColor: "rgba(255, 255, 255, 0.01)",
    cursor: "pointer"
  });
  hitArea.addEventListener("mousemove", (event) => {
    hovering.value = bars.nearestX(event);
  });
  hitArea.addEventListener("mouseout", () => {
    hovering.value = void 0;
  });
  hitArea.addEventListener("mousedown", (event) => {
    let next = bars.nearestX(event);
    selected.value = selected.value === next ? void 0 : next;
  });
  effect(() => {
    text.textContent = bars.textFor(hovering.value ?? selected.value);
    bars.render(counts.value, hovering.value, selected.value);
  });
  root.appendChild(container);
  root.appendChild(text);
  root.appendChild(hitArea);
  return Object.assign(root, { selected, data: counts });
}
function createBar(opts) {
  let { title, fillColor, textColor, width, height } = opts;
  let bar = document.createElement("div");
  bar.title = title;
  Object.assign(bar.style, {
    background: createSplitBarFill({
      color: fillColor,
      bgColor: "var(--moon-gray)",
      frac: 50
    }),
    width: `${width}px`,
    height: `${height}px`,
    borderColor: "white",
    borderWidth: "0px 1px 0px 0px",
    borderStyle: "solid",
    opacity: 1,
    textAlign: "center",
    position: "relative",
    display: "flex",
    overflow: "hidden",
    alignItems: "center",
    fontWeight: 400,
    fontFamily: "var(--sans-serif)",
    boxSizing: "border-box"
  });
  let span = document.createElement("span");
  Object.assign(span.style, {
    overflow: "hidden",
    width: `calc(100% - 4px)`,
    left: "0px",
    position: "absolute",
    padding: "0px 2px",
    color: textColor
  });
  if (width > 10) {
    span.textContent = title;
  }
  bar.appendChild(span);
  return bar;
}
function prepareData(data) {
  let arr = data.toArray().toSorted((a, b) => b.total - a.total);
  let total = arr.reduce((acc, d) => acc + d.total, 0);
  return {
    bins: arr.filter(
      (d) => d.key !== "__quak_null__" && d.key !== "__quak_unique__"
    ),
    nullCount: arr.find((d) => d.key === "__quak_null__")?.total ?? 0,
    uniqueCount: arr.find((d) => d.key === "__quak_unique__")?.total ?? 0,
    total
  };
}
function createBars(data, opts) {
  let source = prepareData(data);
  let x = d3_exports.scaleLinear().domain([0, source.total]).range([opts.marginLeft, opts.width - opts.marginRight]);
  let thresh = 20;
  let bars = [];
  for (let d of source.bins.slice(0, thresh)) {
    let bar = createBar({
      title: d.key,
      fillColor: opts.fillColor,
      textColor: "white",
      width: x(d.total),
      height: opts.height
    });
    bars.push(Object.assign(bar, { data: d }));
  }
  let hoverBar = createVirtualSelectionBar(opts);
  let selectBar = createVirtualSelectionBar(opts);
  let virtualBar;
  if (source.bins.length > thresh) {
    let total = source.bins.slice(thresh).reduce(
      (acc, d) => acc + d.total,
      0
    );
    virtualBar = Object.assign(document.createElement("div"), {
      title: "__quak_virtual__"
    });
    Object.assign(virtualBar.style, {
      width: `${x(total)}px`,
      height: "100%",
      borderColor: "white",
      borderWidth: "0px 1px 0px 0px",
      borderStyle: "solid",
      opacity: 1
    });
    let vbars = document.createElement("div");
    Object.assign(vbars.style, {
      width: "100%",
      height: "100%",
      background: `repeating-linear-gradient(to right, ${opts.fillColor} 0px, ${opts.fillColor} 1px, white 1px, white 2px)`
    });
    virtualBar.appendChild(vbars);
    virtualBar.appendChild(hoverBar);
    virtualBar.appendChild(selectBar);
    Object.defineProperty(virtualBar, "data", {
      value: source.bins.slice(thresh)
    });
    bars.push(virtualBar);
  }
  if (source.uniqueCount) {
    let bar = createBar({
      title: "unique",
      fillColor: opts.backgroundBarColor,
      textColor: "var(--mid-gray)",
      width: x(source.uniqueCount),
      height: opts.height
    });
    bar.title = "__quak_unique__";
    bars.push(Object.assign(bar, {
      data: {
        key: "__quak_unique__",
        total: source.uniqueCount
      }
    }));
  }
  if (source.nullCount) {
    let bar = createBar({
      title: "null",
      fillColor: opts.nullFillColor,
      textColor: "white",
      width: x(source.nullCount),
      height: opts.height
    });
    bar.title = "__quak_null__";
    bars.push(Object.assign(bar, {
      data: {
        key: "__quak_null__",
        total: source.uniqueCount
      }
    }));
  }
  let first = bars[0];
  let last = bars[bars.length - 1];
  if (first === last) {
    first.style.borderRadius = "5px";
  } else {
    first.style.borderRadius = "5px 0px 0px 5px";
    last.style.borderRadius = "0px 5px 5px 0px";
  }
  function virtualBin(key) {
    assert(virtualBar);
    let voffset = bars.slice(0, thresh).map((b) => b.getBoundingClientRect().width).reduce((a, b) => a + b, 0);
    let vbins = virtualBar.data;
    let rect = virtualBar.getBoundingClientRect();
    let dx = rect.width / vbins.length;
    let idx = vbins.findIndex((d) => d.key === key);
    assert(idx !== -1, `key ${key} not found in virtual bins`);
    return {
      ...vbins[idx],
      x: dx * idx + voffset
    };
  }
  function reset(opactiy) {
    bars.forEach((bar) => {
      if (bar.title === "__quak_virtual__") {
        let vbars = bar.firstChild;
        vbars.style.opacity = opactiy.toString();
        vbars.style.background = createVirtualBarRepeatingBackground({
          color: opts.fillColor
        });
      } else {
        bar.style.opacity = opactiy.toString();
        bar.style.background = createSplitBarFill({
          color: bar.title === "__quak_unique__" ? opts.backgroundBarColor : bar.title === "__quak_null__" ? opts.nullFillColor : opts.fillColor,
          bgColor: opts.backgroundBarColor,
          frac: 1
        });
      }
      bar.style.borderColor = "white";
      bar.style.borderWidth = "0px 1px 0px 0px";
      bar.style.removeProperty("box-shadow");
    });
    bars[bars.length - 1].style.borderWidth = "0px";
    hoverBar.style.visibility = "hidden";
    selectBar.style.visibility = "hidden";
  }
  function hover(key, selected) {
    let bar = bars.find((b) => b.data.key === key);
    if (bar !== void 0) {
      bar.style.opacity = "1";
      return;
    }
    let vbin = virtualBin(key);
    hoverBar.title = vbin.key;
    hoverBar.data = vbin;
    hoverBar.style.opacity = selected ? "0.25" : "1";
    hoverBar.style.left = `${vbin.x}px`;
    hoverBar.style.visibility = "visible";
  }
  function select(key) {
    let bar = bars.find((b) => b.data.key === key);
    if (bar !== void 0) {
      bar.style.opacity = "1";
      bar.style.boxShadow = "inset 0 0 0 1.2px black";
      return;
    }
    let vbin = virtualBin(key);
    selectBar.style.opacity = "1";
    selectBar.title = vbin.key;
    selectBar.data = vbin;
    selectBar.style.left = `${vbin.x}px`;
    selectBar.style.visibility = "visible";
  }
  let counts = Object.fromEntries(
    Array.from(data.toArray(), (d) => [d.key, d.total])
  );
  return {
    elements: bars,
    nearestX(event) {
      let bar = nearestX(event, bars);
      if (!bar)
        return;
      if (bar.title !== "__quak_virtual__") {
        return bar.data.key;
      }
      let rect = bar.getBoundingClientRect();
      let mouseX = event.clientX - rect.left;
      let data2 = bar.data;
      let idx = Math.floor(mouseX / rect.width * data2.length);
      return data2[idx].key;
    },
    render(data2, hovering, selected) {
      reset(hovering || selected ? 0.4 : 1);
      let update = Object.fromEntries(
        Array.from(data2.toArray(), (d) => [d.key, d.total])
      );
      let total = Object.values(update).reduce((a, b) => a + b, 0);
      for (let bar of bars) {
        if (bar.title === "__quak_virtual__") {
          let vbars = bar.firstChild;
          vbars.style.background = createVirtualBarRepeatingBackground({
            color: total < source.total || selected ? opts.backgroundBarColor : opts.fillColor
          });
        } else {
          let key = bar.data.key;
          let frac = (update[key] ?? 0) / counts[key];
          if (selected)
            frac = key === selected ? frac : 0;
          bar.style.background = createSplitBarFill({
            color: bar.title === "__quak_unique__" ? opts.backgroundBarColor : bar.title === "__quak_null__" ? opts.nullFillColor : opts.fillColor,
            bgColor: opts.backgroundBarColor,
            frac: isNaN(frac) ? 0 : frac
          });
        }
      }
      if (hovering !== void 0) {
        hover(hovering, selected);
      }
      if (selected !== void 0) {
        select(selected);
      }
    },
    textFor(key) {
      if (key === void 0) {
        let ncats = data.numRows;
        return `${ncats.toLocaleString()} categor${ncats === 1 ? "y" : "ies"}`;
      }
      if (key === "__quak_unique__") {
        return `${source.uniqueCount.toLocaleString()} unique value${source.uniqueCount === 1 ? "" : "s"}`;
      }
      if (key === "__quak_null__") {
        return "null";
      }
      return key.toString();
    }
  };
}
function createTextOutput() {
  let node = document.createElement("div");
  Object.assign(node.style, {
    pointerEvents: "none",
    height: "15px",
    maxWidth: "100%",
    overflow: "hidden",
    textOverflow: "ellipsis",
    position: "absolute",
    fontWeight: 400,
    marginTop: "1.5px",
    color: "var(--mid-gray)"
  });
  return node;
}
function createVirtualSelectionBar(opts) {
  let node = document.createElement("div");
  Object.assign(node.style, {
    position: "absolute",
    top: "0",
    width: "1.5px",
    height: "100%",
    backgroundColor: opts.fillColor,
    pointerEvents: "none",
    visibility: "hidden"
  });
  return Object.assign(node, {
    data: { key: "", total: 0 }
  });
}
function nearestX({ clientX }, bars) {
  for (let bar of bars) {
    let rect = bar.getBoundingClientRect();
    if (clientX >= rect.left && clientX <= rect.right) {
      return bar;
    }
  }
}
function createSplitBarFill(options) {
  let { color, bgColor, frac } = options;
  let p = frac * 100;
  return `linear-gradient(to top, ${color} ${p}%, ${bgColor} ${p}%, ${bgColor} ${100 - p}%)`;
}
function createVirtualBarRepeatingBackground({ color }) {
  return `repeating-linear-gradient(to right, ${color} 0px, ${color} 1px, white 1px, white 2px)`;
}

// lib/clients/ValueCounts.ts
var ValueCounts = class extends MosaicClient2 {
  #table;
  #column;
  #el = document.createElement("div");
  #plot;
  constructor(options) {
    super(options.filterBy);
    this.#table = options.table;
    this.#column = options.column;
    options.filterBy.addEventListener("value", async () => {
      let filters = options.filterBy.predicate();
      let query = this.query(filters);
      if (this.#plot) {
        let data = await this.coordinator.query(query);
        this.#plot.data.value = data;
      }
    });
  }
  query(filter = []) {
    let counts = Query2.from({ source: this.#table }).select({
      value: sql`CASE
					WHEN ${column(this.#column)} IS NULL THEN '__quak_null__'
					ELSE ${column(this.#column)}
				END`,
      count: count2()
    }).groupby("value").where(filter);
    return Query2.with({ counts }).select(
      {
        key: sql`CASE
						WHEN "count" = 1 AND "value" != '__quak_null__' THEN '__quak_unique__'
						ELSE "value"
					END`,
        total: sum("count")
      }
    ).from("counts").groupby("key");
  }
  queryResult(data) {
    if (!this.#plot) {
      let plot = this.#plot = ValueCountsPlot(data);
      this.#el.appendChild(plot);
      effect2(() => {
        let clause = this.clause(plot.selected.value);
        this.filterBy.update(clause);
      });
    } else {
      this.#plot.data.value = data;
    }
    return this;
  }
  clause(value) {
    let update = value === "__quak_null__" ? null : value;
    return clausePoint(this.#column, update, {
      source: this
    });
  }
  reset() {
    assert(this.#plot, "ValueCounts plot not initialized");
    this.#plot.selected.value = void 0;
  }
  get plot() {
    return {
      node: () => this.#el
    };
  }
};

// lib/clients/DataTable.ts
import { signal as signal3 } from "https://esm.sh/@preact/signals-core@1.6.1";

// lib/clients/styles.css?raw
var styles_default = ':host {\n	all: initial;\n	--sans-serif: -apple-system, BlinkMacSystemFont, "avenir next", avenir, helvetica, "helvetica neue", ubuntu, roboto, noto, "segoe ui", arial, sans-serif;\n	--light-silver: #efefef;\n	--spacing-none: 0;\n	--white: #fff;\n	--gray: #929292;\n	--dark-gray: #333;\n	--moon-gray: #c4c4c4;\n	--mid-gray: #6e6e6e;\n\n	--stone-blue: #64748b;\n	--yellow-gold: #ca8a04;\n\n	--teal: #027982;\n	--dark-pink: #D35A5F;\n\n	--light-blue: #7E93CF;\n	--dark-yellow-gold: #A98447;\n\n	--purple: #987fd3;\n\n	--primary: var(--stone-blue);\n	--secondary: var(--yellow-gold);\n}\n\n.highlight {\n	background-color: var(--light-silver);\n}\n\n.highlight-cell {\n	border: 1px solid var(--moon-gray);\n}\n\n.quak {\n  border-radius: 0.2rem;\n  border: 1px solid var(--light-silver);\n  overflow-y: auto;\n}\n\ntable {\n  border-collapse: separate;\n  border-spacing: 0;\n  white-space: nowrap;\n  box-sizing: border-box;\n\n  margin: var(--spacing-none);\n  color: var(--dark-gray);\n  font: 13px / 1.2 var(--sans-serif);\n\n  width: 100%;\n}\n\nthead {\n  position: sticky;\n  vertical-align: top;\n  text-align: left;\n  top: 0;\n}\n\ntd {\n  border: 1px solid var(--light-silver);\n  border-bottom: solid 1px transparent;\n  border-right: solid 1px transparent;\n  overflow: hidden;\n  -o-text-overflow: ellipsis;\n  text-overflow: ellipsis;\n  padding: 4px 6px;\n}\n\ntr:first-child td {\n  border-top: solid 1px transparent;\n}\n\nth {\n  display: table-cell;\n  vertical-align: inherit;\n  font-weight: bold;\n  text-align: -internal-center;\n  unicode-bidi: isolate;\n\n  position: relative;\n  background: var(--white);\n  border-bottom: solid 1px var(--light-silver);\n  border-left: solid 1px var(--light-silver);\n  padding: 5px 6px;\n  user-select: none;\n}\n\n.number, .date {\n  font-variant-numeric: tabular-nums;\n}\n\n.gray {\n  color: var(--gray);\n}\n\n.number {\n  text-align: right;\n}\n\ntd:nth-child(1), th:nth-child(1) {\n  font-variant-numeric: tabular-nums;\n  text-align: center;\n  color: var(--moon-gray);\n  padding: 0 4px;\n}\n\ntd:first-child, th:first-child {\n  border-left: none;\n}\n\nth:first-child {\n  border-left: none;\n  vertical-align: top;\n  width: 20px;\n  padding: 7px;\n}\n\ntd:nth-last-child(2), th:nth-last-child(2) {\n  border-right: 1px solid var(--light-silver);\n}\n\ntr:first-child td {\n	border-top: solid 1px transparent;\n}\n\n.resize-handle {\n	width: 5px;\n	height: 100%;\n	background-color: transparent;\n	position: absolute;\n	right: -2.5px;\n	top: 0;\n	cursor: ew-resize;\n	z-index: 1;\n}\n\n.quak .sort-button {\n	cursor: pointer;\n	background-color: var(--white);\n	user-select: none;\n}\n\n.status-bar {\n	display: flex;\n	justify-content: flex-end;\n	font-family: var(--sans-serif);\n	margin-right: 10px;\n	margin-top: 5px;\n}\n\n.status-bar button {\n	border: none;\n	background-color: var(--white);\n	color: var(--primary);\n	font-weight: 600;\n	font-size: 0.875rem;\n	cursor: pointer;\n	margin-right: 5px;\n}\n\n.status-bar span {\n	color: var(--gray);\n	font-weight: 400;\n	font-size: 0.75rem;\n	font-variant-numeric: tabular-nums;\n}\n';

// lib/clients/StatusBar.ts
import { MosaicClient as MosaicClient3 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.10.0/+esm";
import { count as count3, Query as Query3 } from "https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.10.0/+esm";
var StatusBar = class extends MosaicClient3 {
  #table;
  #el = document.createElement("div");
  #button;
  #span;
  #totalRows = void 0;
  constructor(options) {
    super(options.filterBy);
    this.#table = options.table;
    this.#button = document.createElement("button");
    this.#button.innerText = "Reset";
    this.#span = document.createElement("span");
    let div = document.createElement("div");
    div.appendChild(this.#button);
    div.appendChild(this.#span);
    this.#el.appendChild(div);
    this.#el.classList.add("status-bar");
    this.#button.addEventListener("mousedown", () => {
      if (!this.filterBy)
        return;
      for (let { source } of this.filterBy.clauses) {
        if (!isInteractor(source)) {
          console.warn("Skipping non-interactor source", source);
          continue;
        }
        source.reset();
        this.filterBy.update(source.clause());
      }
    });
    this.#button.style.visibility = "hidden";
    this.filterBy?.addEventListener("value", () => {
      if (this.filterBy?.clauses.length === 0) {
        this.#button.style.visibility = "hidden";
      } else {
        this.#button.style.visibility = "visible";
      }
    });
  }
  query(filter = []) {
    let query = Query3.from(this.#table).select({ count: count3() }).where(filter);
    return query;
  }
  queryResult(table) {
    let count4 = Number(table.get(0)?.count ?? 0);
    if (!this.#totalRows) {
      this.#totalRows = count4;
    }
    let countStr = count4.toLocaleString();
    if (count4 == this.#totalRows) {
      this.#span.innerText = `${countStr} rows`;
    } else {
      let totalStr = this.#totalRows.toLocaleString();
      this.#span.innerText = `${countStr} of ${totalStr} rows`;
    }
    return this;
  }
  node() {
    return this.#el;
  }
};
function isObject(x) {
  return typeof x === "object" && x !== null && !Array.isArray(x);
}
function isInteractor(x) {
  return isObject(x) && "clause" in x && "reset" in x;
}

// lib/clients/DataTable.ts
var DataTable = class extends MosaicClient4 {
  /** source of the data */
  #meta;
  /** for the component */
  #root = document.createElement("div");
  /** shadow root for the component */
  #shadowRoot = this.#root.attachShadow({ mode: "open" });
  /** header of the table */
  #thead = document.createElement("thead");
  /** body of the table */
  #tbody = document.createElement("tbody");
  /** The SQL order by */
  #orderby = [];
  /** template row for data */
  #templateRow = void 0;
  /** div containing the table */
  #tableRoot;
  /** offset into the data */
  #offset = 0;
  /** number of rows to fetch */
  #limit = 100;
  /** whether an internal request is pending */
  #pendingInternalRequest = false;
  /** number of rows to display */
  #rows = 11.5;
  /** height of a row */
  #rowHeight = 22;
  /** width of a column */
  #columnWidth = 125;
  /** height of the header */
  #headerHeight = "94px";
  /** the formatter for the data table entries */
  #format;
  /** @type {AsyncBatchReader<arrow.StructRowProxy> | null} */
  #reader = null;
  #sql = signal3(void 0);
  constructor(source) {
    super(Selection2.crossfilter());
    this.#format = formatof(source.schema);
    this.#pendingInternalRequest = false;
    this.#meta = source;
    let maxHeight = `${(this.#rows + 1) * this.#rowHeight - 1}px`;
    if (source.height) {
      this.#rows = Math.floor(source.height / this.#rowHeight);
      maxHeight = `${source.height}px`;
    }
    let root = html`<div class="quak" style=${{
      maxHeight
    }}>`;
    root.appendChild(
      html.fragment`<table style=${{ tableLayout: "fixed" }}>${this.#thead}${this.#tbody}</table>`
    );
    this.#shadowRoot.appendChild(html`<style>${styles_default}</style>`);
    this.#shadowRoot.appendChild(root);
    this.#tableRoot = root;
    this.#tableRoot.addEventListener("scroll", async () => {
      let isAtBottom = this.#tableRoot.scrollHeight - this.#tableRoot.scrollTop < this.#rows * this.#rowHeight * 1.5;
      if (isAtBottom) {
        await this.#appendRows(this.#rows);
      }
    });
  }
  get sql() {
    return this.#sql.value;
  }
  fields() {
    return this.#columns.map((column2) => ({
      table: this.#meta.table,
      column: column2,
      stats: []
    }));
  }
  node() {
    return this.#root;
  }
  get #columns() {
    return this.#meta.schema.fields.map((field) => field.name);
  }
  /**
   * @param {Array<unknown>} filter
   */
  query(filter = []) {
    let query = Query4.from(this.#meta.table).select(this.#columns).where(filter).orderby(
      this.#orderby.filter((o) => o.order !== "unset").map((o) => o.order === "asc" ? asc(o.field) : desc(o.field))
    );
    this.#sql.value = query.clone().toString();
    return query.limit(this.#limit).offset(this.#offset);
  }
  /**
   * A mosiac lifecycle function that is called with the results from `query`.
   * Must be synchronous, and return `this`.
   */
  queryResult(table) {
    if (!this.#pendingInternalRequest) {
      this.#reader = new AsyncBatchReader(() => {
        this.#pendingInternalRequest = true;
        this.requestData(this.#offset + this.#limit);
      });
      this.#tbody.replaceChildren();
      this.#tableRoot.scrollTop = 0;
      this.#offset = 0;
    }
    let batch = table[Symbol.iterator]();
    this.#reader?.enqueueBatch(batch, {
      last: table.numRows < this.#limit
    });
    return this;
  }
  update() {
    if (!this.#pendingInternalRequest) {
      this.#appendRows(this.#rows * 2);
    }
    this.#pendingInternalRequest = false;
    return this;
  }
  requestData(offset = 0) {
    this.#offset = offset;
    let query = this.query(this.filterBy?.predicate(this));
    this.requestQuery(query);
    this.coordinator.prefetch(query.clone().offset(offset + this.#limit));
  }
  fieldInfo(infos) {
    let classes = classof(this.#meta.schema);
    {
      let statusBar = new StatusBar({
        table: this.#meta.table,
        filterBy: this.filterBy
      });
      this.coordinator.connect(statusBar);
      this.#shadowRoot.appendChild(statusBar.node());
    }
    this.#templateRow = html`<tr><td></td>${infos.map((info) => html.fragment`<td class=${classes[info.column]}></td>`)}
			<td style=${{ width: "99%", borderLeft: "none", borderRight: "none" }}></td>
		</tr>`;
    let observer = new IntersectionObserver((entries) => {
      for (let entry of entries) {
        if (!isTableColumnHeaderWithSvg(entry.target))
          continue;
        let vis = entry.target.vis;
        if (!vis)
          continue;
        if (entry.isIntersecting) {
          this.coordinator.connect(vis);
        } else {
          this.coordinator?.disconnect(vis);
        }
      }
    }, {
      root: this.#tableRoot
    });
    let cols = this.#meta.schema.fields.map((field) => {
      let info = infos.find((c) => c.column === field.name);
      assert(info, `No info for column ${field.name}`);
      let vis = void 0;
      if (info.type === "number" || info.type === "date") {
        vis = new Histogram({
          table: this.#meta.table,
          column: field.name,
          type: info.type,
          filterBy: this.filterBy
        });
      } else {
        vis = new ValueCounts({
          table: this.#meta.table,
          column: field.name,
          filterBy: this.filterBy
        });
      }
      let th = thcol(field, this.#columnWidth, vis);
      observer.observe(th);
      return th;
    });
    signals.effect(() => {
      this.#orderby = cols.map((col, i) => ({
        field: this.#columns[i],
        order: col.sortState.value
      }));
      this.requestData();
    });
    this.#thead.appendChild(
      html`<tr style=${{ height: this.#headerHeight }}>
				<th></th>
				${cols}
				<th style=${{ width: "99%", borderLeft: "none", borderRight: "none" }}></th>
			</tr>`
    );
    {
      this.#tableRoot.addEventListener("mouseover", (event) => {
        if (isTableCellElement(event.target) && isTableRowElement(event.target.parentNode)) {
          const cell = event.target;
          const row = event.target.parentNode;
          highlight(cell, row);
        }
      });
      this.#tableRoot.addEventListener("mouseout", (event) => {
        if (isTableCellElement(event.target) && isTableRowElement(event.target.parentNode)) {
          const cell = event.target;
          const row = event.target.parentNode;
          removeHighlight(cell, row);
        }
      });
    }
    return this;
  }
  /** Number of rows to append */
  async #appendRows(nrows) {
    nrows = Math.trunc(nrows);
    while (nrows >= 0) {
      let result = await this.#reader?.next();
      if (!result || result?.done) {
        break;
      }
      this.#appendRow(result.value.row, result.value.index);
      nrows--;
      continue;
    }
  }
  #appendRow(d, i) {
    let itr = this.#templateRow?.cloneNode(true);
    assert(itr, "Must have a data row");
    let td = itr.childNodes[0];
    td.appendChild(document.createTextNode(String(i)));
    for (let j = 0; j < this.#columns.length; ++j) {
      td = itr.childNodes[j + 1];
      td.classList.remove("gray");
      let col = this.#columns[j];
      let stringified = this.#format[col](d[col]);
      if (shouldGrayoutValue(stringified)) {
        td.classList.add("gray");
      }
      let value = document.createTextNode(stringified);
      td.appendChild(value);
    }
    this.#tbody.append(itr);
  }
};
var TRUNCATE = (
  /** @type {const} */
  {
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis"
  }
);
function thcol(field, minWidth, vis) {
  let buttonVisible = signals.signal(false);
  let width = signals.signal(minWidth);
  let sortState = signals.signal(
    "unset"
  );
  function nextSortState() {
    sortState.value = {
      "unset": "asc",
      "asc": "desc",
      "desc": "unset"
    }[sortState.value];
  }
  let svg = html`<svg style=${{ width: "1.5em" }} fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
		<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 9L12 5.25L15.75 9" />
		<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15L12 18.75L15.75 15" />
	</svg>`;
  let uparrow = svg.children[0];
  let downarrow = svg.children[1];
  let verticalResizeHandle = html`<div class="resize-handle"></div>`;
  let sortButton = html`<span aria-role="button" class="sort-button" onmousedown=${nextSortState}>${svg}</span>`;
  let th = html`<th style=${{ overflow: "hidden" }}>
		<div style=${{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
			<span style=${{ marginBottom: "5px", maxWidth: "250px", ...TRUNCATE }}>${field.name}</span>
			${sortButton}
		</div>
		${verticalResizeHandle}
		<span class="gray" style=${{ fontWeight: 400, fontSize: "12px", userSelect: "none" }}>${formatDataType(field.type)}</span>
		${vis?.plot?.node()}
	</th>`;
  signals.effect(() => {
    uparrow.setAttribute("stroke", "var(--moon-gray)");
    downarrow.setAttribute("stroke", "var(--moon-gray)");
    let element = { "asc": uparrow, "desc": downarrow, "unset": null }[sortState.value];
    element?.setAttribute("stroke", "var(--dark-gray)");
  });
  signals.effect(() => {
    sortButton.style.visibility = buttonVisible.value ? "visible" : "hidden";
  });
  signals.effect(() => {
    th.style.width = `${width.value}px`;
  });
  th.addEventListener("mouseover", () => {
    if (sortState.value === "unset")
      buttonVisible.value = true;
  });
  th.addEventListener("mouseleave", () => {
    if (sortState.value === "unset")
      buttonVisible.value = false;
  });
  th.addEventListener("dblclick", (event) => {
    if (event.offsetX < sortButton.offsetWidth && event.offsetY < sortButton.offsetHeight) {
      return;
    }
    width.value = minWidth;
  });
  verticalResizeHandle.addEventListener("mousedown", (event) => {
    event.preventDefault();
    let startX = event.clientX;
    let startWidth = th.offsetWidth - parseFloat(getComputedStyle(th).paddingLeft) - parseFloat(getComputedStyle(th).paddingRight);
    function onMouseMove(event2) {
      let dx = event2.clientX - startX;
      width.value = Math.max(minWidth, startWidth + dx);
      verticalResizeHandle.style.backgroundColor = "var(--light-silver)";
    }
    function onMouseUp() {
      verticalResizeHandle.style.backgroundColor = "transparent";
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
    }
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  });
  verticalResizeHandle.addEventListener("mouseover", () => {
    verticalResizeHandle.style.backgroundColor = "var(--light-silver)";
  });
  verticalResizeHandle.addEventListener("mouseleave", () => {
    verticalResizeHandle.style.backgroundColor = "transparent";
  });
  return Object.assign(th, { vis, sortState });
}
function formatof(schema) {
  const format2 = /* @__PURE__ */ Object.create(
    null
  );
  for (const field of schema.fields) {
    format2[field.name] = formatterForValue(field.type);
  }
  return format2;
}
function classof(schema) {
  const classes = /* @__PURE__ */ Object.create(null);
  for (const field of schema.fields) {
    if (arrow2.DataType.isInt(field.type) || arrow2.DataType.isFloat(field.type)) {
      classes[field.name] = "number";
    }
    if (arrow2.DataType.isDate(field.type) || arrow2.DataType.isTimestamp(field.type)) {
      classes[field.name] = "date";
    }
  }
  return classes;
}
function highlight(cell, row) {
  if (row.firstChild !== cell && cell !== row.lastElementChild) {
    cell.style.border = "1px solid var(--moon-gray)";
  }
  row.style.backgroundColor = "var(--light-silver)";
}
function removeHighlight(cell, row) {
  cell.style.removeProperty("border");
  row.style.removeProperty("background-color");
}
function isTableCellElement(node) {
  return node?.tagName === "TD";
}
function isTableRowElement(node) {
  return node instanceof HTMLTableRowElement;
}
function shouldGrayoutValue(value) {
  return value === "null" || value === "undefined" || value === "NaN" || value === "TODO";
}
function isTableColumnHeaderWithSvg(node) {
  return node instanceof HTMLTableCellElement && "vis" in node;
}
function asc(field) {
  let expr = desc(field);
  expr._expr[0] = expr._expr[0].replace("DESC", "ASC");
  return expr;
}

// lib/utils/defer.ts
function defer() {
  let resolve;
  let reject;
  let promise = new Promise((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

// lib/widget.ts
var widget_default = () => {
  let coordinator = new mc.Coordinator();
  let schema;
  return {
    async initialize({ model }) {
      let logger = coordinator.logger(_voidLogger());
      let openQueries = /* @__PURE__ */ new Map();
      function send(query, resolve, reject) {
        let id = uuid.v4();
        openQueries.set(id, {
          query,
          startTime: performance.now(),
          resolve,
          reject
        });
        model.send({ ...query, uuid: id });
      }
      model.on("msg:custom", (msg, buffers) => {
        logger.group(`query ${msg.uuid}`);
        logger.log("received message", msg, buffers);
        let query = openQueries.get(msg.uuid);
        openQueries.delete(msg.uuid);
        assert(query, `No query found for ${msg.uuid}`);
        logger.log(
          query.query.toString(),
          (performance.now() - query.startTime).toFixed(1)
        );
        if (msg.error) {
          query.reject(msg.error);
          logger.error(msg.error);
          return;
        } else {
          switch (msg.type) {
            case "arrow": {
              let table = arrow3.tableFromIPC(buffers[0].buffer);
              logger.log("table", table);
              query.resolve(table);
              break;
            }
            case "json": {
              logger.log("json", msg.result);
              query.resolve(msg.result);
              break;
            }
            default: {
              query.resolve({});
              break;
            }
          }
        }
        logger.groupEnd("query");
      });
      coordinator.databaseConnector({
        query(query) {
          let { promise, resolve, reject } = defer();
          send(query, resolve, reject);
          return promise;
        }
      });
      let empty = await coordinator.query(
        Query5.from(model.get("_table_name")).select(...model.get("_columns")).limit(0).toString()
      );
      schema = empty.schema;
      return () => {
        coordinator.clear();
      };
    },
    render({ model, el }) {
      let table = new DataTable({
        table: model.get("_table_name"),
        schema
      });
      coordinator.connect(table);
      effect4(() => {
        model.set("sql", table.sql ?? "");
        model.save_changes();
      });
      el.appendChild(table.node());
    }
  };
};
function _voidLogger() {
  return Object.fromEntries(
    Object.keys(console).map((key) => [key, () => {
    }])
  );
}
export {
  widget_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsiLi4vLi4vbGliL3dpZGdldC50cyIsICIuLi8uLi9saWIvY2xpZW50cy9EYXRhVGFibGUudHMiLCAiLi4vLi4vbGliL3V0aWxzL2Fzc2VydC50cyIsICIuLi8uLi9saWIvdXRpbHMvQXN5bmNCYXRjaFJlYWRlci50cyIsICIuLi8uLi9saWIvdXRpbHMvZm9ybWF0dGluZy50cyIsICIuLi8uLi9saWIvY2xpZW50cy9IaXN0b2dyYW0udHMiLCAiLi4vLi4vbGliL2RlcHMvZDMudHMiLCAiLi4vLi4vbGliL3V0aWxzL3RpY2stZm9ybWF0dGVyLWZvci1iaW5zLnRzIiwgIi4uLy4uL2xpYi91dGlscy9Dcm9zc2ZpbHRlckhpc3RvZ3JhbVBsb3QudHMiLCAiLi4vLi4vbGliL2NsaWVudHMvVmFsdWVDb3VudHMudHMiLCAiLi4vLi4vbGliL3V0aWxzL1ZhbHVlQ291bnRzUGxvdC50cyIsICIuLi8uLi9saWIvY2xpZW50cy9zdHlsZXMuY3NzIiwgIi4uLy4uL2xpYi9jbGllbnRzL1N0YXR1c0Jhci50cyIsICIuLi8uLi9saWIvdXRpbHMvZGVmZXIudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbIi8vIEBkZW5vLXR5cGVzPVwiLi9kZXBzL21vc2FpYy1jb3JlLmQudHNcIjtcbmltcG9ydCAqIGFzIG1jIGZyb20gXCJAdXdkYXRhL21vc2FpYy1jb3JlXCI7XG4vLyBAZGVuby10eXBlcz1cIi4vZGVwcy9tb3NhaWMtc3FsLmQudHNcIjtcbmltcG9ydCB7IFF1ZXJ5IH0gZnJvbSBcIkB1d2RhdGEvbW9zYWljLXNxbFwiO1xuaW1wb3J0ICogYXMgYXJyb3cgZnJvbSBcImFwYWNoZS1hcnJvd1wiO1xuaW1wb3J0ICogYXMgdXVpZCBmcm9tIFwiQGx1a2VlZC91dWlkXCI7XG5pbXBvcnQgdHlwZSAqIGFzIGF3IGZyb20gXCJAYW55d2lkZ2V0L3R5cGVzXCI7XG5pbXBvcnQgeyBlZmZlY3QgfSBmcm9tIFwiQHByZWFjdC9zaWduYWxzLWNvcmVcIjtcblxuaW1wb3J0IHsgRGF0YVRhYmxlIH0gZnJvbSBcIi4vY2xpZW50cy9EYXRhVGFibGUudHNcIjtcbmltcG9ydCB7IGFzc2VydCB9IGZyb20gXCIuL3V0aWxzL2Fzc2VydC50c1wiO1xuaW1wb3J0IHsgZGVmZXIgfSBmcm9tIFwiLi91dGlscy9kZWZlci50c1wiO1xuXG50eXBlIE1vZGVsID0ge1xuXHRfdGFibGVfbmFtZTogc3RyaW5nO1xuXHRfY29sdW1uczogQXJyYXk8c3RyaW5nPjtcblx0dGVtcF9pbmRleGVzOiBib29sZWFuO1xuXHRzcWw6IHN0cmluZztcbn07XG5cbmludGVyZmFjZSBPcGVuUXVlcnkge1xuXHRxdWVyeTogbWMuQ29ubmVjdG9yUXVlcnk7XG5cdHN0YXJ0VGltZTogbnVtYmVyO1xuXHRyZXNvbHZlOiAoeDogYXJyb3cuVGFibGUgfCBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPikgPT4gdm9pZDtcblx0cmVqZWN0OiAoZXJyPzogc3RyaW5nKSA9PiB2b2lkO1xufVxuXG5leHBvcnQgZGVmYXVsdCAoKSA9PiB7XG5cdGxldCBjb29yZGluYXRvciA9IG5ldyBtYy5Db29yZGluYXRvcigpO1xuXHRsZXQgc2NoZW1hOiBhcnJvdy5TY2hlbWE7XG5cblx0cmV0dXJuIHtcblx0XHRhc3luYyBpbml0aWFsaXplKHsgbW9kZWwgfTogYXcuSW5pdGlhbGl6ZVByb3BzPE1vZGVsPikge1xuXHRcdFx0bGV0IGxvZ2dlciA9IGNvb3JkaW5hdG9yLmxvZ2dlcihfdm9pZExvZ2dlcigpKTtcblx0XHRcdGxldCBvcGVuUXVlcmllcyA9IG5ldyBNYXA8c3RyaW5nLCBPcGVuUXVlcnk+KCk7XG5cblx0XHRcdC8qKlxuXHRcdFx0ICogQHBhcmFtIHF1ZXJ5IC0gdGhlIHF1ZXJ5IHRvIHNlbmRcblx0XHRcdCAqIEBwYXJhbSByZXNvbHZlIC0gdGhlIHByb21pc2UgcmVzb2x2ZSBjYWxsYmFja1xuXHRcdFx0ICogQHBhcmFtIHJlamVjdCAtIHRoZSBwcm9taXNlIHJlamVjdCBjYWxsYmFja1xuXHRcdFx0ICovXG5cdFx0XHRmdW5jdGlvbiBzZW5kKFxuXHRcdFx0XHRxdWVyeTogbWMuQ29ubmVjdG9yUXVlcnksXG5cdFx0XHRcdHJlc29sdmU6ICh2YWx1ZTogYXJyb3cuVGFibGUgfCBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPikgPT4gdm9pZCxcblx0XHRcdFx0cmVqZWN0OiAocmVhc29uPzogc3RyaW5nKSA9PiB2b2lkLFxuXHRcdFx0KSB7XG5cdFx0XHRcdGxldCBpZCA9IHV1aWQudjQoKTtcblx0XHRcdFx0b3BlblF1ZXJpZXMuc2V0KGlkLCB7XG5cdFx0XHRcdFx0cXVlcnksXG5cdFx0XHRcdFx0c3RhcnRUaW1lOiBwZXJmb3JtYW5jZS5ub3coKSxcblx0XHRcdFx0XHRyZXNvbHZlLFxuXHRcdFx0XHRcdHJlamVjdCxcblx0XHRcdFx0fSk7XG5cdFx0XHRcdG1vZGVsLnNlbmQoeyAuLi5xdWVyeSwgdXVpZDogaWQgfSk7XG5cdFx0XHR9XG5cblx0XHRcdG1vZGVsLm9uKFwibXNnOmN1c3RvbVwiLCAobXNnLCBidWZmZXJzKSA9PiB7XG5cdFx0XHRcdGxvZ2dlci5ncm91cChgcXVlcnkgJHttc2cudXVpZH1gKTtcblx0XHRcdFx0bG9nZ2VyLmxvZyhcInJlY2VpdmVkIG1lc3NhZ2VcIiwgbXNnLCBidWZmZXJzKTtcblx0XHRcdFx0bGV0IHF1ZXJ5ID0gb3BlblF1ZXJpZXMuZ2V0KG1zZy51dWlkKTtcblx0XHRcdFx0b3BlblF1ZXJpZXMuZGVsZXRlKG1zZy51dWlkKTtcblx0XHRcdFx0YXNzZXJ0KHF1ZXJ5LCBgTm8gcXVlcnkgZm91bmQgZm9yICR7bXNnLnV1aWR9YCk7XG5cdFx0XHRcdGxvZ2dlci5sb2coXG5cdFx0XHRcdFx0cXVlcnkucXVlcnkudG9TdHJpbmcoKSxcblx0XHRcdFx0XHQocGVyZm9ybWFuY2Uubm93KCkgLSBxdWVyeS5zdGFydFRpbWUpLnRvRml4ZWQoMSksXG5cdFx0XHRcdCk7XG5cdFx0XHRcdGlmIChtc2cuZXJyb3IpIHtcblx0XHRcdFx0XHRxdWVyeS5yZWplY3QobXNnLmVycm9yKTtcblx0XHRcdFx0XHRsb2dnZXIuZXJyb3IobXNnLmVycm9yKTtcblx0XHRcdFx0XHRyZXR1cm47XG5cdFx0XHRcdH0gZWxzZSB7XG5cdFx0XHRcdFx0c3dpdGNoIChtc2cudHlwZSkge1xuXHRcdFx0XHRcdFx0Y2FzZSBcImFycm93XCI6IHtcblx0XHRcdFx0XHRcdFx0bGV0IHRhYmxlID0gYXJyb3cudGFibGVGcm9tSVBDKGJ1ZmZlcnNbMF0uYnVmZmVyKTtcblx0XHRcdFx0XHRcdFx0bG9nZ2VyLmxvZyhcInRhYmxlXCIsIHRhYmxlKTtcblx0XHRcdFx0XHRcdFx0cXVlcnkucmVzb2x2ZSh0YWJsZSk7XG5cdFx0XHRcdFx0XHRcdGJyZWFrO1xuXHRcdFx0XHRcdFx0fVxuXHRcdFx0XHRcdFx0Y2FzZSBcImpzb25cIjoge1xuXHRcdFx0XHRcdFx0XHRsb2dnZXIubG9nKFwianNvblwiLCBtc2cucmVzdWx0KTtcblx0XHRcdFx0XHRcdFx0cXVlcnkucmVzb2x2ZShtc2cucmVzdWx0KTtcblx0XHRcdFx0XHRcdFx0YnJlYWs7XG5cdFx0XHRcdFx0XHR9XG5cdFx0XHRcdFx0XHRkZWZhdWx0OiB7XG5cdFx0XHRcdFx0XHRcdHF1ZXJ5LnJlc29sdmUoe30pO1xuXHRcdFx0XHRcdFx0XHRicmVhaztcblx0XHRcdFx0XHRcdH1cblx0XHRcdFx0XHR9XG5cdFx0XHRcdH1cblx0XHRcdFx0bG9nZ2VyLmdyb3VwRW5kKFwicXVlcnlcIik7XG5cdFx0XHR9KTtcblxuXHRcdFx0Y29vcmRpbmF0b3IuZGF0YWJhc2VDb25uZWN0b3Ioe1xuXHRcdFx0XHRxdWVyeShxdWVyeSkge1xuXHRcdFx0XHRcdGxldCB7IHByb21pc2UsIHJlc29sdmUsIHJlamVjdCB9ID0gZGVmZXI8XG5cdFx0XHRcdFx0XHRhcnJvdy5UYWJsZSB8IFJlY29yZDxzdHJpbmcsIHVua25vd24+LFxuXHRcdFx0XHRcdFx0c3RyaW5nXG5cdFx0XHRcdFx0PigpO1xuXHRcdFx0XHRcdHNlbmQocXVlcnksIHJlc29sdmUsIHJlamVjdCk7XG5cdFx0XHRcdFx0cmV0dXJuIHByb21pc2U7XG5cdFx0XHRcdH0sXG5cdFx0XHR9KTtcblxuXHRcdFx0Ly8gZ2V0IHNvbWUgaW5pdGlhbCBkYXRhIHRvIGdldCB0aGUgc2NoZW1hXG5cdFx0XHRsZXQgZW1wdHkgPSBhd2FpdCBjb29yZGluYXRvci5xdWVyeShcblx0XHRcdFx0UXVlcnlcblx0XHRcdFx0XHQuZnJvbShtb2RlbC5nZXQoXCJfdGFibGVfbmFtZVwiKSlcblx0XHRcdFx0XHQuc2VsZWN0KC4uLm1vZGVsLmdldChcIl9jb2x1bW5zXCIpKVxuXHRcdFx0XHRcdC5saW1pdCgwKVxuXHRcdFx0XHRcdC50b1N0cmluZygpLFxuXHRcdFx0KTtcblx0XHRcdHNjaGVtYSA9IGVtcHR5LnNjaGVtYTtcblxuXHRcdFx0cmV0dXJuICgpID0+IHtcblx0XHRcdFx0Y29vcmRpbmF0b3IuY2xlYXIoKTtcblx0XHRcdH07XG5cdFx0fSxcblx0XHRyZW5kZXIoeyBtb2RlbCwgZWwgfTogYXcuUmVuZGVyUHJvcHM8TW9kZWw+KSB7XG5cdFx0XHRsZXQgdGFibGUgPSBuZXcgRGF0YVRhYmxlKHtcblx0XHRcdFx0dGFibGU6IG1vZGVsLmdldChcIl90YWJsZV9uYW1lXCIpLFxuXHRcdFx0XHRzY2hlbWE6IHNjaGVtYSxcblx0XHRcdH0pO1xuXHRcdFx0Y29vcmRpbmF0b3IuY29ubmVjdCh0YWJsZSk7XG5cdFx0XHRlZmZlY3QoKCkgPT4ge1xuXHRcdFx0XHRtb2RlbC5zZXQoXCJzcWxcIiwgdGFibGUuc3FsID8/IFwiXCIpO1xuXHRcdFx0XHRtb2RlbC5zYXZlX2NoYW5nZXMoKTtcblx0XHRcdH0pO1xuXHRcdFx0ZWwuYXBwZW5kQ2hpbGQodGFibGUubm9kZSgpKTtcblx0XHR9LFxuXHR9O1xufTtcblxuZnVuY3Rpb24gX3ZvaWRMb2dnZXIoKSB7XG5cdHJldHVybiBPYmplY3QuZnJvbUVudHJpZXMoXG5cdFx0T2JqZWN0LmtleXMoY29uc29sZSkubWFwKChrZXkpID0+IFtrZXksICgpID0+IHt9XSksXG5cdCk7XG59XG4iLCAiaW1wb3J0ICogYXMgYXJyb3cgZnJvbSBcImFwYWNoZS1hcnJvd1wiO1xuLy8gQGRlbm8tdHlwZXM9XCIuLi9kZXBzL21vc2FpYy1jb3JlLmQudHNcIlxuaW1wb3J0IHtcblx0dHlwZSBGaWVsZEluZm8sXG5cdHR5cGUgRmllbGRSZXF1ZXN0LFxuXHRNb3NhaWNDbGllbnQsXG5cdFNlbGVjdGlvbixcbn0gZnJvbSBcIkB1d2RhdGEvbW9zYWljLWNvcmVcIjtcbi8vIEBkZW5vLXR5cGVzPVwiLi4vZGVwcy9tb3NhaWMtc3FsLmQudHNcIlxuaW1wb3J0IHsgZGVzYywgUXVlcnksIFNRTEV4cHJlc3Npb24gfSBmcm9tIFwiQHV3ZGF0YS9tb3NhaWMtc3FsXCI7XG5pbXBvcnQgKiBhcyBzaWduYWxzIGZyb20gXCJAcHJlYWN0L3NpZ25hbHMtY29yZVwiO1xuaW1wb3J0IHsgaHRtbCB9IGZyb20gXCJodGxcIjtcblxuaW1wb3J0IHsgQXN5bmNCYXRjaFJlYWRlciB9IGZyb20gXCIuLi91dGlscy9Bc3luY0JhdGNoUmVhZGVyLnRzXCI7XG5pbXBvcnQgeyBhc3NlcnQgfSBmcm9tIFwiLi4vdXRpbHMvYXNzZXJ0LnRzXCI7XG5pbXBvcnQgeyBmb3JtYXREYXRhVHlwZSwgZm9ybWF0dGVyRm9yVmFsdWUgfSBmcm9tIFwiLi4vdXRpbHMvZm9ybWF0dGluZy50c1wiO1xuaW1wb3J0IHsgSGlzdG9ncmFtIH0gZnJvbSBcIi4vSGlzdG9ncmFtLnRzXCI7XG5pbXBvcnQgeyBWYWx1ZUNvdW50cyB9IGZyb20gXCIuL1ZhbHVlQ291bnRzLnRzXCI7XG5pbXBvcnQgeyBzaWduYWwgfSBmcm9tIFwiQHByZWFjdC9zaWduYWxzLWNvcmVcIjtcblxuaW1wb3J0IHN0eWxlc1N0cmluZyBmcm9tIFwiLi9zdHlsZXMuY3NzP3Jhd1wiO1xuaW1wb3J0IHsgU3RhdHVzQmFyIH0gZnJvbSBcIi4vU3RhdHVzQmFyLnRzXCI7XG5cbmludGVyZmFjZSBEYXRhVGFibGVPcHRpb25zIHtcblx0dGFibGU6IHN0cmluZztcblx0c2NoZW1hOiBhcnJvdy5TY2hlbWE7XG5cdGhlaWdodD86IG51bWJlcjtcbn1cblxuLy8gVE9ETzogbW9yZVxudHlwZSBDb2x1bW5TdW1tYXJ5Q2xpZW50ID0gSGlzdG9ncmFtIHwgVmFsdWVDb3VudHM7XG5cbmV4cG9ydCBjbGFzcyBEYXRhVGFibGUgZXh0ZW5kcyBNb3NhaWNDbGllbnQge1xuXHQvKiogc291cmNlIG9mIHRoZSBkYXRhICovXG5cdCNtZXRhOiB7IHRhYmxlOiBzdHJpbmc7IHNjaGVtYTogYXJyb3cuU2NoZW1hIH07XG5cdC8qKiBmb3IgdGhlIGNvbXBvbmVudCAqL1xuXHQjcm9vdDogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuXHQvKiogc2hhZG93IHJvb3QgZm9yIHRoZSBjb21wb25lbnQgKi9cblx0I3NoYWRvd1Jvb3Q6IFNoYWRvd1Jvb3QgPSB0aGlzLiNyb290LmF0dGFjaFNoYWRvdyh7IG1vZGU6IFwib3BlblwiIH0pO1xuXHQvKiogaGVhZGVyIG9mIHRoZSB0YWJsZSAqL1xuXHQjdGhlYWQ6IEhUTUxUYWJsZVNlY3Rpb25FbGVtZW50ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcInRoZWFkXCIpO1xuXHQvKiogYm9keSBvZiB0aGUgdGFibGUgKi9cblx0I3Rib2R5OiBIVE1MVGFibGVTZWN0aW9uRWxlbWVudCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJ0Ym9keVwiKTtcblx0LyoqIFRoZSBTUUwgb3JkZXIgYnkgKi9cblx0I29yZGVyYnk6IEFycmF5PHsgZmllbGQ6IHN0cmluZzsgb3JkZXI6IFwiYXNjXCIgfCBcImRlc2NcIiB8IFwidW5zZXRcIiB9PiA9IFtdO1xuXHQvKiogdGVtcGxhdGUgcm93IGZvciBkYXRhICovXG5cdCN0ZW1wbGF0ZVJvdzogSFRNTFRhYmxlUm93RWxlbWVudCB8IHVuZGVmaW5lZCA9IHVuZGVmaW5lZDtcblx0LyoqIGRpdiBjb250YWluaW5nIHRoZSB0YWJsZSAqL1xuXHQjdGFibGVSb290OiBIVE1MRGl2RWxlbWVudDtcblx0LyoqIG9mZnNldCBpbnRvIHRoZSBkYXRhICovXG5cdCNvZmZzZXQ6IG51bWJlciA9IDA7XG5cdC8qKiBudW1iZXIgb2Ygcm93cyB0byBmZXRjaCAqL1xuXHQjbGltaXQ6IG51bWJlciA9IDEwMDtcblx0LyoqIHdoZXRoZXIgYW4gaW50ZXJuYWwgcmVxdWVzdCBpcyBwZW5kaW5nICovXG5cdCNwZW5kaW5nSW50ZXJuYWxSZXF1ZXN0OiBib29sZWFuID0gZmFsc2U7XG5cdC8qKiBudW1iZXIgb2Ygcm93cyB0byBkaXNwbGF5ICovXG5cdCNyb3dzOiBudW1iZXIgPSAxMS41O1xuXHQvKiogaGVpZ2h0IG9mIGEgcm93ICovXG5cdCNyb3dIZWlnaHQ6IG51bWJlciA9IDIyO1xuXHQvKiogd2lkdGggb2YgYSBjb2x1bW4gKi9cblx0I2NvbHVtbldpZHRoOiBudW1iZXIgPSAxMjU7XG5cdC8qKiBoZWlnaHQgb2YgdGhlIGhlYWRlciAqL1xuXHQjaGVhZGVySGVpZ2h0OiBzdHJpbmcgPSBcIjk0cHhcIjtcblx0LyoqIHRoZSBmb3JtYXR0ZXIgZm9yIHRoZSBkYXRhIHRhYmxlIGVudHJpZXMgKi9cblx0I2Zvcm1hdDogUmVjb3JkPHN0cmluZywgKHZhbHVlOiB1bmtub3duKSA9PiBzdHJpbmc+O1xuXG5cdC8qKiBAdHlwZSB7QXN5bmNCYXRjaFJlYWRlcjxhcnJvdy5TdHJ1Y3RSb3dQcm94eT4gfCBudWxsfSAqL1xuXHQjcmVhZGVyOiBBc3luY0JhdGNoUmVhZGVyPGFycm93LlN0cnVjdFJvd1Byb3h5PiB8IG51bGwgPSBudWxsO1xuXG5cdCNzcWwgPSBzaWduYWwodW5kZWZpbmVkIGFzIHN0cmluZyB8IHVuZGVmaW5lZCk7XG5cblx0Y29uc3RydWN0b3Ioc291cmNlOiBEYXRhVGFibGVPcHRpb25zKSB7XG5cdFx0c3VwZXIoU2VsZWN0aW9uLmNyb3NzZmlsdGVyKCkpO1xuXHRcdHRoaXMuI2Zvcm1hdCA9IGZvcm1hdG9mKHNvdXJjZS5zY2hlbWEpO1xuXHRcdHRoaXMuI3BlbmRpbmdJbnRlcm5hbFJlcXVlc3QgPSBmYWxzZTtcblx0XHR0aGlzLiNtZXRhID0gc291cmNlO1xuXG5cdFx0bGV0IG1heEhlaWdodCA9IGAkeyh0aGlzLiNyb3dzICsgMSkgKiB0aGlzLiNyb3dIZWlnaHQgLSAxfXB4YDtcblx0XHQvLyBpZiBtYXhIZWlnaHQgaXMgc2V0LCBjYWxjdWxhdGUgdGhlIG51bWJlciBvZiByb3dzIHRvIGRpc3BsYXlcblx0XHRpZiAoc291cmNlLmhlaWdodCkge1xuXHRcdFx0dGhpcy4jcm93cyA9IE1hdGguZmxvb3Ioc291cmNlLmhlaWdodCAvIHRoaXMuI3Jvd0hlaWdodCk7XG5cdFx0XHRtYXhIZWlnaHQgPSBgJHtzb3VyY2UuaGVpZ2h0fXB4YDtcblx0XHR9XG5cblx0XHRsZXQgcm9vdDogSFRNTERpdkVsZW1lbnQgPSBodG1sYDxkaXYgY2xhc3M9XCJxdWFrXCIgc3R5bGU9JHt7XG5cdFx0XHRtYXhIZWlnaHQsXG5cdFx0fX0+YDtcblx0XHQvLyBAZGVuby1mbXQtaWdub3JlXG5cdFx0cm9vdC5hcHBlbmRDaGlsZChcblx0XHRcdGh0bWwuZnJhZ21lbnRgPHRhYmxlIHN0eWxlPSR7eyB0YWJsZUxheW91dDogXCJmaXhlZFwiIH19PiR7dGhpcy4jdGhlYWR9JHt0aGlzLiN0Ym9keX08L3RhYmxlPmBcblx0XHQpO1xuXHRcdHRoaXMuI3NoYWRvd1Jvb3QuYXBwZW5kQ2hpbGQoaHRtbGA8c3R5bGU+JHtzdHlsZXNTdHJpbmd9PC9zdHlsZT5gKTtcblx0XHR0aGlzLiNzaGFkb3dSb290LmFwcGVuZENoaWxkKHJvb3QpO1xuXHRcdHRoaXMuI3RhYmxlUm9vdCA9IHJvb3Q7XG5cblx0XHQvLyBzY3JvbGwgZXZlbnQgbGlzdGVuZXJcblx0XHR0aGlzLiN0YWJsZVJvb3QuYWRkRXZlbnRMaXN0ZW5lcihcInNjcm9sbFwiLCBhc3luYyAoKSA9PiB7XG5cdFx0XHRsZXQgaXNBdEJvdHRvbSA9XG5cdFx0XHRcdHRoaXMuI3RhYmxlUm9vdC5zY3JvbGxIZWlnaHQgLSB0aGlzLiN0YWJsZVJvb3Quc2Nyb2xsVG9wIDxcblx0XHRcdFx0XHR0aGlzLiNyb3dzICogdGhpcy4jcm93SGVpZ2h0ICogMS41O1xuXHRcdFx0aWYgKGlzQXRCb3R0b20pIHtcblx0XHRcdFx0YXdhaXQgdGhpcy4jYXBwZW5kUm93cyh0aGlzLiNyb3dzKTtcblx0XHRcdH1cblx0XHR9KTtcblx0fVxuXG5cdGdldCBzcWwoKSB7XG5cdFx0cmV0dXJuIHRoaXMuI3NxbC52YWx1ZTtcblx0fVxuXG5cdGZpZWxkcygpOiBBcnJheTxGaWVsZFJlcXVlc3Q+IHtcblx0XHRyZXR1cm4gdGhpcy4jY29sdW1ucy5tYXAoKGNvbHVtbikgPT4gKHtcblx0XHRcdHRhYmxlOiB0aGlzLiNtZXRhLnRhYmxlLFxuXHRcdFx0Y29sdW1uLFxuXHRcdFx0c3RhdHM6IFtdLFxuXHRcdH0pKTtcblx0fVxuXG5cdG5vZGUoKSB7XG5cdFx0cmV0dXJuIHRoaXMuI3Jvb3Q7XG5cdH1cblxuXHRnZXQgI2NvbHVtbnMoKSB7XG5cdFx0cmV0dXJuIHRoaXMuI21ldGEuc2NoZW1hLmZpZWxkcy5tYXAoKGZpZWxkKSA9PiBmaWVsZC5uYW1lKTtcblx0fVxuXG5cdC8qKlxuXHQgKiBAcGFyYW0ge0FycmF5PHVua25vd24+fSBmaWx0ZXJcblx0ICovXG5cdHF1ZXJ5KGZpbHRlcjogQXJyYXk8dW5rbm93bj4gPSBbXSkge1xuXHRcdGxldCBxdWVyeSA9IFF1ZXJ5LmZyb20odGhpcy4jbWV0YS50YWJsZSlcblx0XHRcdC5zZWxlY3QodGhpcy4jY29sdW1ucylcblx0XHRcdC53aGVyZShmaWx0ZXIpXG5cdFx0XHQub3JkZXJieShcblx0XHRcdFx0dGhpcy4jb3JkZXJieVxuXHRcdFx0XHRcdC5maWx0ZXIoKG8pID0+IG8ub3JkZXIgIT09IFwidW5zZXRcIilcblx0XHRcdFx0XHQubWFwKChvKSA9PiBvLm9yZGVyID09PSBcImFzY1wiID8gYXNjKG8uZmllbGQpIDogZGVzYyhvLmZpZWxkKSksXG5cdFx0XHQpO1xuXHRcdHRoaXMuI3NxbC52YWx1ZSA9IHF1ZXJ5LmNsb25lKCkudG9TdHJpbmcoKTtcblx0XHRyZXR1cm4gcXVlcnlcblx0XHRcdC5saW1pdCh0aGlzLiNsaW1pdClcblx0XHRcdC5vZmZzZXQodGhpcy4jb2Zmc2V0KTtcblx0fVxuXG5cdC8qKlxuXHQgKiBBIG1vc2lhYyBsaWZlY3ljbGUgZnVuY3Rpb24gdGhhdCBpcyBjYWxsZWQgd2l0aCB0aGUgcmVzdWx0cyBmcm9tIGBxdWVyeWAuXG5cdCAqIE11c3QgYmUgc3luY2hyb25vdXMsIGFuZCByZXR1cm4gYHRoaXNgLlxuXHQgKi9cblx0cXVlcnlSZXN1bHQodGFibGU6IGFycm93LlRhYmxlKSB7XG5cdFx0aWYgKCF0aGlzLiNwZW5kaW5nSW50ZXJuYWxSZXF1ZXN0KSB7XG5cdFx0XHQvLyBkYXRhIGlzIG5vdCBmcm9tIGFuIGludGVybmFsIHJlcXVlc3QsIHNvIHJlc2V0IHRhYmxlXG5cdFx0XHR0aGlzLiNyZWFkZXIgPSBuZXcgQXN5bmNCYXRjaFJlYWRlcigoKSA9PiB7XG5cdFx0XHRcdHRoaXMuI3BlbmRpbmdJbnRlcm5hbFJlcXVlc3QgPSB0cnVlO1xuXHRcdFx0XHR0aGlzLnJlcXVlc3REYXRhKHRoaXMuI29mZnNldCArIHRoaXMuI2xpbWl0KTtcblx0XHRcdH0pO1xuXHRcdFx0dGhpcy4jdGJvZHkucmVwbGFjZUNoaWxkcmVuKCk7XG5cdFx0XHR0aGlzLiN0YWJsZVJvb3Quc2Nyb2xsVG9wID0gMDtcblx0XHRcdHRoaXMuI29mZnNldCA9IDA7XG5cdFx0fVxuXHRcdGxldCBiYXRjaCA9IHRhYmxlW1N5bWJvbC5pdGVyYXRvcl0oKTtcblx0XHR0aGlzLiNyZWFkZXI/LmVucXVldWVCYXRjaChiYXRjaCwge1xuXHRcdFx0bGFzdDogdGFibGUubnVtUm93cyA8IHRoaXMuI2xpbWl0LFxuXHRcdH0pO1xuXHRcdHJldHVybiB0aGlzO1xuXHR9XG5cblx0dXBkYXRlKCkge1xuXHRcdGlmICghdGhpcy4jcGVuZGluZ0ludGVybmFsUmVxdWVzdCkge1xuXHRcdFx0Ly8gb24gdGhlIGZpcnN0IHVwZGF0ZSwgcG9wdWxhdGUgdGhlIHRhYmxlIHdpdGggaW5pdGlhbCBkYXRhXG5cdFx0XHR0aGlzLiNhcHBlbmRSb3dzKHRoaXMuI3Jvd3MgKiAyKTtcblx0XHR9XG5cdFx0dGhpcy4jcGVuZGluZ0ludGVybmFsUmVxdWVzdCA9IGZhbHNlO1xuXHRcdHJldHVybiB0aGlzO1xuXHR9XG5cblx0cmVxdWVzdERhdGEob2Zmc2V0ID0gMCkge1xuXHRcdHRoaXMuI29mZnNldCA9IG9mZnNldDtcblxuXHRcdC8vIHJlcXVlc3QgbmV4dCBkYXRhIGJhdGNoXG5cdFx0bGV0IHF1ZXJ5ID0gdGhpcy5xdWVyeSh0aGlzLmZpbHRlckJ5Py5wcmVkaWNhdGUodGhpcykpO1xuXHRcdHRoaXMucmVxdWVzdFF1ZXJ5KHF1ZXJ5KTtcblxuXHRcdC8vIHByZWZldGNoIHN1YnNlcXVlbnQgZGF0YSBiYXRjaFxuXHRcdHRoaXMuY29vcmRpbmF0b3IucHJlZmV0Y2gocXVlcnkuY2xvbmUoKS5vZmZzZXQob2Zmc2V0ICsgdGhpcy4jbGltaXQpKTtcblx0fVxuXG5cdGZpZWxkSW5mbyhpbmZvczogQXJyYXk8RmllbGRJbmZvPikge1xuXHRcdGxldCBjbGFzc2VzID0gY2xhc3NvZih0aGlzLiNtZXRhLnNjaGVtYSk7XG5cblx0XHR7XG5cdFx0XHRsZXQgc3RhdHVzQmFyID0gbmV3IFN0YXR1c0Jhcih7XG5cdFx0XHRcdHRhYmxlOiB0aGlzLiNtZXRhLnRhYmxlLFxuXHRcdFx0XHRmaWx0ZXJCeTogdGhpcy5maWx0ZXJCeSxcblx0XHRcdH0pO1xuXHRcdFx0dGhpcy5jb29yZGluYXRvci5jb25uZWN0KHN0YXR1c0Jhcik7XG5cdFx0XHR0aGlzLiNzaGFkb3dSb290LmFwcGVuZENoaWxkKHN0YXR1c0Jhci5ub2RlKCkpO1xuXHRcdH1cblxuXHRcdC8vIEBkZW5vLWZtdC1pZ25vcmVcblx0XHR0aGlzLiN0ZW1wbGF0ZVJvdyA9IGh0bWxgPHRyPjx0ZD48L3RkPiR7XG5cdFx0XHRpbmZvcy5tYXAoKGluZm8pID0+IGh0bWwuZnJhZ21lbnRgPHRkIGNsYXNzPSR7Y2xhc3Nlc1tpbmZvLmNvbHVtbl19PjwvdGQ+YClcblx0XHR9XG5cdFx0XHQ8dGQgc3R5bGU9JHt7IHdpZHRoOiBcIjk5JVwiLCBib3JkZXJMZWZ0OiBcIm5vbmVcIiwgYm9yZGVyUmlnaHQ6IFwibm9uZVwiIH19PjwvdGQ+XG5cdFx0PC90cj5gO1xuXG5cdFx0bGV0IG9ic2VydmVyID0gbmV3IEludGVyc2VjdGlvbk9ic2VydmVyKChlbnRyaWVzKSA9PiB7XG5cdFx0XHRmb3IgKGxldCBlbnRyeSBvZiBlbnRyaWVzKSB7XG5cdFx0XHRcdGlmICghaXNUYWJsZUNvbHVtbkhlYWRlcldpdGhTdmcoZW50cnkudGFyZ2V0KSkgY29udGludWU7XG5cdFx0XHRcdGxldCB2aXMgPSBlbnRyeS50YXJnZXQudmlzO1xuXHRcdFx0XHRpZiAoIXZpcykgY29udGludWU7XG5cdFx0XHRcdGlmIChlbnRyeS5pc0ludGVyc2VjdGluZykge1xuXHRcdFx0XHRcdHRoaXMuY29vcmRpbmF0b3IuY29ubmVjdCh2aXMpO1xuXHRcdFx0XHR9IGVsc2Uge1xuXHRcdFx0XHRcdHRoaXMuY29vcmRpbmF0b3I/LmRpc2Nvbm5lY3QodmlzKTtcblx0XHRcdFx0fVxuXHRcdFx0fVxuXHRcdH0sIHtcblx0XHRcdHJvb3Q6IHRoaXMuI3RhYmxlUm9vdCxcblx0XHR9KTtcblxuXHRcdGxldCBjb2xzID0gdGhpcy4jbWV0YS5zY2hlbWEuZmllbGRzLm1hcCgoZmllbGQpID0+IHtcblx0XHRcdGxldCBpbmZvID0gaW5mb3MuZmluZCgoYykgPT4gYy5jb2x1bW4gPT09IGZpZWxkLm5hbWUpO1xuXHRcdFx0YXNzZXJ0KGluZm8sIGBObyBpbmZvIGZvciBjb2x1bW4gJHtmaWVsZC5uYW1lfWApO1xuXHRcdFx0bGV0IHZpczogQ29sdW1uU3VtbWFyeUNsaWVudCB8IHVuZGVmaW5lZCA9IHVuZGVmaW5lZDtcblx0XHRcdGlmIChpbmZvLnR5cGUgPT09IFwibnVtYmVyXCIgfHwgaW5mby50eXBlID09PSBcImRhdGVcIikge1xuXHRcdFx0XHR2aXMgPSBuZXcgSGlzdG9ncmFtKHtcblx0XHRcdFx0XHR0YWJsZTogdGhpcy4jbWV0YS50YWJsZSxcblx0XHRcdFx0XHRjb2x1bW46IGZpZWxkLm5hbWUsXG5cdFx0XHRcdFx0dHlwZTogaW5mby50eXBlLFxuXHRcdFx0XHRcdGZpbHRlckJ5OiB0aGlzLmZpbHRlckJ5ISxcblx0XHRcdFx0fSk7XG5cdFx0XHR9IGVsc2Uge1xuXHRcdFx0XHR2aXMgPSBuZXcgVmFsdWVDb3VudHMoe1xuXHRcdFx0XHRcdHRhYmxlOiB0aGlzLiNtZXRhLnRhYmxlLFxuXHRcdFx0XHRcdGNvbHVtbjogZmllbGQubmFtZSxcblx0XHRcdFx0XHRmaWx0ZXJCeTogdGhpcy5maWx0ZXJCeSEsXG5cdFx0XHRcdH0pO1xuXHRcdFx0fVxuXHRcdFx0bGV0IHRoID0gdGhjb2woZmllbGQsIHRoaXMuI2NvbHVtbldpZHRoLCB2aXMpO1xuXHRcdFx0b2JzZXJ2ZXIub2JzZXJ2ZSh0aCk7XG5cdFx0XHRyZXR1cm4gdGg7XG5cdFx0fSk7XG5cblx0XHRzaWduYWxzLmVmZmVjdCgoKSA9PiB7XG5cdFx0XHR0aGlzLiNvcmRlcmJ5ID0gY29scy5tYXAoKGNvbCwgaSkgPT4gKHtcblx0XHRcdFx0ZmllbGQ6IHRoaXMuI2NvbHVtbnNbaV0sXG5cdFx0XHRcdG9yZGVyOiBjb2wuc29ydFN0YXRlLnZhbHVlLFxuXHRcdFx0fSkpO1xuXHRcdFx0dGhpcy5yZXF1ZXN0RGF0YSgpO1xuXHRcdH0pO1xuXG5cdFx0Ly8gQGRlbm8tZm10LWlnbm9yZVxuXHRcdHRoaXMuI3RoZWFkLmFwcGVuZENoaWxkKFxuXHRcdFx0aHRtbGA8dHIgc3R5bGU9JHt7IGhlaWdodDogdGhpcy4jaGVhZGVySGVpZ2h0IH19PlxuXHRcdFx0XHQ8dGg+PC90aD5cblx0XHRcdFx0JHtjb2xzfVxuXHRcdFx0XHQ8dGggc3R5bGU9JHt7IHdpZHRoOiBcIjk5JVwiLCBib3JkZXJMZWZ0OiBcIm5vbmVcIiwgYm9yZGVyUmlnaHQ6IFwibm9uZVwiIH19PjwvdGg+XG5cdFx0XHQ8L3RyPmAsXG5cdFx0KTtcblxuXHRcdC8vIGhpZ2hsaWdodCBvbiBob3ZlclxuXHRcdHtcblx0XHRcdHRoaXMuI3RhYmxlUm9vdC5hZGRFdmVudExpc3RlbmVyKFwibW91c2VvdmVyXCIsIChldmVudCkgPT4ge1xuXHRcdFx0XHRpZiAoXG5cdFx0XHRcdFx0aXNUYWJsZUNlbGxFbGVtZW50KGV2ZW50LnRhcmdldCkgJiZcblx0XHRcdFx0XHRpc1RhYmxlUm93RWxlbWVudChldmVudC50YXJnZXQucGFyZW50Tm9kZSlcblx0XHRcdFx0KSB7XG5cdFx0XHRcdFx0Y29uc3QgY2VsbCA9IGV2ZW50LnRhcmdldDtcblx0XHRcdFx0XHRjb25zdCByb3cgPSBldmVudC50YXJnZXQucGFyZW50Tm9kZTtcblx0XHRcdFx0XHRoaWdobGlnaHQoY2VsbCwgcm93KTtcblx0XHRcdFx0fVxuXHRcdFx0fSk7XG5cdFx0XHR0aGlzLiN0YWJsZVJvb3QuYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNlb3V0XCIsIChldmVudCkgPT4ge1xuXHRcdFx0XHRpZiAoXG5cdFx0XHRcdFx0aXNUYWJsZUNlbGxFbGVtZW50KGV2ZW50LnRhcmdldCkgJiZcblx0XHRcdFx0XHRpc1RhYmxlUm93RWxlbWVudChldmVudC50YXJnZXQucGFyZW50Tm9kZSlcblx0XHRcdFx0KSB7XG5cdFx0XHRcdFx0Y29uc3QgY2VsbCA9IGV2ZW50LnRhcmdldDtcblx0XHRcdFx0XHRjb25zdCByb3cgPSBldmVudC50YXJnZXQucGFyZW50Tm9kZTtcblx0XHRcdFx0XHRyZW1vdmVIaWdobGlnaHQoY2VsbCwgcm93KTtcblx0XHRcdFx0fVxuXHRcdFx0fSk7XG5cdFx0fVxuXG5cdFx0cmV0dXJuIHRoaXM7XG5cdH1cblxuXHQvKiogTnVtYmVyIG9mIHJvd3MgdG8gYXBwZW5kICovXG5cdGFzeW5jICNhcHBlbmRSb3dzKG5yb3dzOiBudW1iZXIpIHtcblx0XHRucm93cyA9IE1hdGgudHJ1bmMobnJvd3MpO1xuXHRcdHdoaWxlIChucm93cyA+PSAwKSB7XG5cdFx0XHRsZXQgcmVzdWx0ID0gYXdhaXQgdGhpcy4jcmVhZGVyPy5uZXh0KCk7XG5cdFx0XHRpZiAoIXJlc3VsdCB8fCByZXN1bHQ/LmRvbmUpIHtcblx0XHRcdFx0Ly8gd2UndmUgZXhoYXVzdGVkIGFsbCByb3dzXG5cdFx0XHRcdGJyZWFrO1xuXHRcdFx0fVxuXHRcdFx0dGhpcy4jYXBwZW5kUm93KHJlc3VsdC52YWx1ZS5yb3csIHJlc3VsdC52YWx1ZS5pbmRleCk7XG5cdFx0XHRucm93cy0tO1xuXHRcdFx0Y29udGludWU7XG5cdFx0fVxuXHR9XG5cblx0I2FwcGVuZFJvdyhkOiBhcnJvdy5TdHJ1Y3RSb3dQcm94eSwgaTogbnVtYmVyKSB7XG5cdFx0bGV0IGl0ciA9IHRoaXMuI3RlbXBsYXRlUm93Py5jbG9uZU5vZGUodHJ1ZSk7XG5cdFx0YXNzZXJ0KGl0ciwgXCJNdXN0IGhhdmUgYSBkYXRhIHJvd1wiKTtcblx0XHRsZXQgdGQgPSBpdHIuY2hpbGROb2Rlc1swXSBhcyBIVE1MVGFibGVDZWxsRWxlbWVudDtcblx0XHR0ZC5hcHBlbmRDaGlsZChkb2N1bWVudC5jcmVhdGVUZXh0Tm9kZShTdHJpbmcoaSkpKTtcblx0XHRmb3IgKGxldCBqID0gMDsgaiA8IHRoaXMuI2NvbHVtbnMubGVuZ3RoOyArK2opIHtcblx0XHRcdHRkID0gaXRyLmNoaWxkTm9kZXNbaiArIDFdIGFzIEhUTUxUYWJsZUNlbGxFbGVtZW50O1xuXHRcdFx0dGQuY2xhc3NMaXN0LnJlbW92ZShcImdyYXlcIik7XG5cdFx0XHRsZXQgY29sID0gdGhpcy4jY29sdW1uc1tqXTtcblx0XHRcdGxldCBzdHJpbmdpZmllZCA9IHRoaXMuI2Zvcm1hdFtjb2xdKGRbY29sXSk7XG5cdFx0XHRpZiAoc2hvdWxkR3JheW91dFZhbHVlKHN0cmluZ2lmaWVkKSkge1xuXHRcdFx0XHR0ZC5jbGFzc0xpc3QuYWRkKFwiZ3JheVwiKTtcblx0XHRcdH1cblx0XHRcdGxldCB2YWx1ZSA9IGRvY3VtZW50LmNyZWF0ZVRleHROb2RlKHN0cmluZ2lmaWVkKTtcblx0XHRcdHRkLmFwcGVuZENoaWxkKHZhbHVlKTtcblx0XHR9XG5cdFx0dGhpcy4jdGJvZHkuYXBwZW5kKGl0cik7XG5cdH1cbn1cblxuY29uc3QgVFJVTkNBVEUgPSAvKiogQHR5cGUge2NvbnN0fSAqLyAoe1xuXHR3aGl0ZVNwYWNlOiBcIm5vd3JhcFwiLFxuXHRvdmVyZmxvdzogXCJoaWRkZW5cIixcblx0dGV4dE92ZXJmbG93OiBcImVsbGlwc2lzXCIsXG59KTtcblxuZnVuY3Rpb24gdGhjb2woXG5cdGZpZWxkOiBhcnJvdy5GaWVsZCxcblx0bWluV2lkdGg6IG51bWJlcixcblx0dmlzPzogQ29sdW1uU3VtbWFyeUNsaWVudCxcbikge1xuXHRsZXQgYnV0dG9uVmlzaWJsZSA9IHNpZ25hbHMuc2lnbmFsKGZhbHNlKTtcblx0bGV0IHdpZHRoID0gc2lnbmFscy5zaWduYWwobWluV2lkdGgpO1xuXHRsZXQgc29ydFN0YXRlOiBzaWduYWxzLlNpZ25hbDxcInVuc2V0XCIgfCBcImFzY1wiIHwgXCJkZXNjXCI+ID0gc2lnbmFscy5zaWduYWwoXG5cdFx0XCJ1bnNldFwiLFxuXHQpO1xuXG5cdGZ1bmN0aW9uIG5leHRTb3J0U3RhdGUoKSB7XG5cdFx0Ly8gc2ltcGxlIHN0YXRlIG1hY2hpbmVcblx0XHQvLyB1bnNldCAtPiBhc2MgLT4gZGVzYyAtPiB1bnNldFxuXHRcdHNvcnRTdGF0ZS52YWx1ZSA9ICh7XG5cdFx0XHRcInVuc2V0XCI6IFwiYXNjXCIsXG5cdFx0XHRcImFzY1wiOiBcImRlc2NcIixcblx0XHRcdFwiZGVzY1wiOiBcInVuc2V0XCIsXG5cdFx0fSBhcyBjb25zdClbc29ydFN0YXRlLnZhbHVlXTtcblx0fVxuXG5cdC8vIEBkZW5vLWZtdC1pZ25vcmVcblx0bGV0IHN2ZyA9IGh0bWxgPHN2ZyBzdHlsZT0ke3sgd2lkdGg6IFwiMS41ZW1cIiB9fSBmaWxsPVwibm9uZVwiIHZpZXdCb3g9XCIwIDAgMjQgMjRcIiBzdHJva2Utd2lkdGg9XCIxLjVcIiBzdHJva2U9XCJjdXJyZW50Q29sb3JcIj5cblx0XHQ8cGF0aCBzdHJva2UtbGluZWNhcD1cInJvdW5kXCIgc3Ryb2tlLWxpbmVqb2luPVwicm91bmRcIiBkPVwiTTguMjUgOUwxMiA1LjI1TDE1Ljc1IDlcIiAvPlxuXHRcdDxwYXRoIHN0cm9rZS1saW5lY2FwPVwicm91bmRcIiBzdHJva2UtbGluZWpvaW49XCJyb3VuZFwiIGQ9XCJNOC4yNSAxNUwxMiAxOC43NUwxNS43NSAxNVwiIC8+XG5cdDwvc3ZnPmA7XG5cdGxldCB1cGFycm93OiBTVkdQYXRoRWxlbWVudCA9IHN2Zy5jaGlsZHJlblswXTtcblx0bGV0IGRvd25hcnJvdzogU1ZHUGF0aEVsZW1lbnQgPSBzdmcuY2hpbGRyZW5bMV07XG5cdGxldCB2ZXJ0aWNhbFJlc2l6ZUhhbmRsZTogSFRNTERpdkVsZW1lbnQgPVxuXHRcdGh0bWxgPGRpdiBjbGFzcz1cInJlc2l6ZS1oYW5kbGVcIj48L2Rpdj5gO1xuXHQvLyBAZGVuby1mbXQtaWdub3JlXG5cdGxldCBzb3J0QnV0dG9uID0gaHRtbGA8c3BhbiBhcmlhLXJvbGU9XCJidXR0b25cIiBjbGFzcz1cInNvcnQtYnV0dG9uXCIgb25tb3VzZWRvd249JHtuZXh0U29ydFN0YXRlfT4ke3N2Z308L3NwYW4+YDtcblx0Ly8gQGRlbm8tZm10LWlnbm9yZVxuXHRsZXQgdGg6IEhUTUxUYWJsZUNlbGxFbGVtZW50ID0gaHRtbGA8dGggc3R5bGU9JHt7IG92ZXJmbG93OiBcImhpZGRlblwiIH19PlxuXHRcdDxkaXYgc3R5bGU9JHt7IGRpc3BsYXk6IFwiZmxleFwiLCBqdXN0aWZ5Q29udGVudDogXCJzcGFjZS1iZXR3ZWVuXCIsIGFsaWduSXRlbXM6IFwiY2VudGVyXCIgfX0+XG5cdFx0XHQ8c3BhbiBzdHlsZT0ke3sgbWFyZ2luQm90dG9tOiBcIjVweFwiLCBtYXhXaWR0aDogXCIyNTBweFwiLCAuLi5UUlVOQ0FURSB9fT4ke2ZpZWxkLm5hbWV9PC9zcGFuPlxuXHRcdFx0JHtzb3J0QnV0dG9ufVxuXHRcdDwvZGl2PlxuXHRcdCR7dmVydGljYWxSZXNpemVIYW5kbGV9XG5cdFx0PHNwYW4gY2xhc3M9XCJncmF5XCIgc3R5bGU9JHt7IGZvbnRXZWlnaHQ6IDQwMCwgZm9udFNpemU6IFwiMTJweFwiLCB1c2VyU2VsZWN0OiBcIm5vbmVcIiB9fT4ke2Zvcm1hdERhdGFUeXBlKGZpZWxkLnR5cGUpfTwvc3Bhbj5cblx0XHQke3Zpcz8ucGxvdD8ubm9kZSgpfVxuXHQ8L3RoPmA7XG5cblx0c2lnbmFscy5lZmZlY3QoKCkgPT4ge1xuXHRcdHVwYXJyb3cuc2V0QXR0cmlidXRlKFwic3Ryb2tlXCIsIFwidmFyKC0tbW9vbi1ncmF5KVwiKTtcblx0XHRkb3duYXJyb3cuc2V0QXR0cmlidXRlKFwic3Ryb2tlXCIsIFwidmFyKC0tbW9vbi1ncmF5KVwiKTtcblx0XHQvLyBAZGVuby1mbXQtaWdub3JlXG5cdFx0bGV0IGVsZW1lbnQgPSB7IFwiYXNjXCI6IHVwYXJyb3csIFwiZGVzY1wiOiBkb3duYXJyb3csIFwidW5zZXRcIjogbnVsbCB9W3NvcnRTdGF0ZS52YWx1ZV07XG5cdFx0ZWxlbWVudD8uc2V0QXR0cmlidXRlKFwic3Ryb2tlXCIsIFwidmFyKC0tZGFyay1ncmF5KVwiKTtcblx0fSk7XG5cblx0c2lnbmFscy5lZmZlY3QoKCkgPT4ge1xuXHRcdHNvcnRCdXR0b24uc3R5bGUudmlzaWJpbGl0eSA9IGJ1dHRvblZpc2libGUudmFsdWUgPyBcInZpc2libGVcIiA6IFwiaGlkZGVuXCI7XG5cdH0pO1xuXG5cdHNpZ25hbHMuZWZmZWN0KCgpID0+IHtcblx0XHR0aC5zdHlsZS53aWR0aCA9IGAke3dpZHRoLnZhbHVlfXB4YDtcblx0fSk7XG5cblx0dGguYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNlb3ZlclwiLCAoKSA9PiB7XG5cdFx0aWYgKHNvcnRTdGF0ZS52YWx1ZSA9PT0gXCJ1bnNldFwiKSBidXR0b25WaXNpYmxlLnZhbHVlID0gdHJ1ZTtcblx0fSk7XG5cblx0dGguYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNlbGVhdmVcIiwgKCkgPT4ge1xuXHRcdGlmIChzb3J0U3RhdGUudmFsdWUgPT09IFwidW5zZXRcIikgYnV0dG9uVmlzaWJsZS52YWx1ZSA9IGZhbHNlO1xuXHR9KTtcblxuXHR0aC5hZGRFdmVudExpc3RlbmVyKFwiZGJsY2xpY2tcIiwgKGV2ZW50KSA9PiB7XG5cdFx0Ly8gcmVzZXQgY29sdW1uIHdpZHRoIGJ1dCB3ZSBkb24ndCB3YW50IHRvIGludGVyZmVyZSB3aXRoIHNvbWVvbmVcblx0XHQvLyBkb3VibGUtY2xpY2tpbmcgdGhlIHNvcnQgYnV0dG9uXG5cdFx0Ly8gaWYgdGhlIG1vdXNlIGlzIHdpdGhpbiB0aGUgc29ydCBidXR0b24sIGRvbid0IHJlc2V0IHRoZSB3aWR0aFxuXHRcdGlmIChcblx0XHRcdGV2ZW50Lm9mZnNldFggPCBzb3J0QnV0dG9uLm9mZnNldFdpZHRoICYmXG5cdFx0XHRldmVudC5vZmZzZXRZIDwgc29ydEJ1dHRvbi5vZmZzZXRIZWlnaHRcblx0XHQpIHtcblx0XHRcdHJldHVybjtcblx0XHR9XG5cdFx0d2lkdGgudmFsdWUgPSBtaW5XaWR0aDtcblx0fSk7XG5cblx0dmVydGljYWxSZXNpemVIYW5kbGUuYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNlZG93blwiLCAoZXZlbnQpID0+IHtcblx0XHRldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuXHRcdGxldCBzdGFydFggPSBldmVudC5jbGllbnRYO1xuXHRcdGxldCBzdGFydFdpZHRoID0gdGgub2Zmc2V0V2lkdGggLVxuXHRcdFx0cGFyc2VGbG9hdChnZXRDb21wdXRlZFN0eWxlKHRoKS5wYWRkaW5nTGVmdCkgLVxuXHRcdFx0cGFyc2VGbG9hdChnZXRDb21wdXRlZFN0eWxlKHRoKS5wYWRkaW5nUmlnaHQpO1xuXHRcdGZ1bmN0aW9uIG9uTW91c2VNb3ZlKC8qKiBAdHlwZSB7TW91c2VFdmVudH0gKi8gZXZlbnQ6IE1vdXNlRXZlbnQpIHtcblx0XHRcdGxldCBkeCA9IGV2ZW50LmNsaWVudFggLSBzdGFydFg7XG5cdFx0XHR3aWR0aC52YWx1ZSA9IE1hdGgubWF4KG1pbldpZHRoLCBzdGFydFdpZHRoICsgZHgpO1xuXHRcdFx0dmVydGljYWxSZXNpemVIYW5kbGUuc3R5bGUuYmFja2dyb3VuZENvbG9yID0gXCJ2YXIoLS1saWdodC1zaWx2ZXIpXCI7XG5cdFx0fVxuXHRcdGZ1bmN0aW9uIG9uTW91c2VVcCgpIHtcblx0XHRcdHZlcnRpY2FsUmVzaXplSGFuZGxlLnN0eWxlLmJhY2tncm91bmRDb2xvciA9IFwidHJhbnNwYXJlbnRcIjtcblx0XHRcdGRvY3VtZW50LnJlbW92ZUV2ZW50TGlzdGVuZXIoXCJtb3VzZW1vdmVcIiwgb25Nb3VzZU1vdmUpO1xuXHRcdFx0ZG9jdW1lbnQucmVtb3ZlRXZlbnRMaXN0ZW5lcihcIm1vdXNldXBcIiwgb25Nb3VzZVVwKTtcblx0XHR9XG5cdFx0ZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNlbW92ZVwiLCBvbk1vdXNlTW92ZSk7XG5cdFx0ZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNldXBcIiwgb25Nb3VzZVVwKTtcblx0fSk7XG5cblx0dmVydGljYWxSZXNpemVIYW5kbGUuYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNlb3ZlclwiLCAoKSA9PiB7XG5cdFx0dmVydGljYWxSZXNpemVIYW5kbGUuc3R5bGUuYmFja2dyb3VuZENvbG9yID0gXCJ2YXIoLS1saWdodC1zaWx2ZXIpXCI7XG5cdH0pO1xuXG5cdHZlcnRpY2FsUmVzaXplSGFuZGxlLmFkZEV2ZW50TGlzdGVuZXIoXCJtb3VzZWxlYXZlXCIsICgpID0+IHtcblx0XHR2ZXJ0aWNhbFJlc2l6ZUhhbmRsZS5zdHlsZS5iYWNrZ3JvdW5kQ29sb3IgPSBcInRyYW5zcGFyZW50XCI7XG5cdH0pO1xuXG5cdHJldHVybiBPYmplY3QuYXNzaWduKHRoLCB7IHZpcywgc29ydFN0YXRlIH0pO1xufVxuXG4vKipcbiAqIFJldHVybiBhIGZvcm1hdHRlciBmb3IgZWFjaCBmaWVsZCBpbiB0aGUgc2NoZW1hXG4gKi9cbmZ1bmN0aW9uIGZvcm1hdG9mKHNjaGVtYTogYXJyb3cuU2NoZW1hKSB7XG5cdGNvbnN0IGZvcm1hdDogUmVjb3JkPHN0cmluZywgKHZhbHVlOiB1bmtub3duKSA9PiBzdHJpbmc+ID0gT2JqZWN0LmNyZWF0ZShcblx0XHRudWxsLFxuXHQpO1xuXHRmb3IgKGNvbnN0IGZpZWxkIG9mIHNjaGVtYS5maWVsZHMpIHtcblx0XHRmb3JtYXRbZmllbGQubmFtZV0gPSBmb3JtYXR0ZXJGb3JWYWx1ZShmaWVsZC50eXBlKTtcblx0fVxuXHRyZXR1cm4gZm9ybWF0O1xufVxuXG4vKipcbiAqIFJldHVybiBhIGNsYXNzIHR5cGUgb2YgZWFjaCBmaWVsZCBpbiB0aGUgc2NoZW1hLlxuICovXG5mdW5jdGlvbiBjbGFzc29mKHNjaGVtYTogYXJyb3cuU2NoZW1hKTogUmVjb3JkPHN0cmluZywgXCJudW1iZXJcIiB8IFwiZGF0ZVwiPiB7XG5cdGNvbnN0IGNsYXNzZXM6IFJlY29yZDxzdHJpbmcsIFwibnVtYmVyXCIgfCBcImRhdGVcIj4gPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuXHRmb3IgKGNvbnN0IGZpZWxkIG9mIHNjaGVtYS5maWVsZHMpIHtcblx0XHRpZiAoXG5cdFx0XHRhcnJvdy5EYXRhVHlwZS5pc0ludChmaWVsZC50eXBlKSB8fFxuXHRcdFx0YXJyb3cuRGF0YVR5cGUuaXNGbG9hdChmaWVsZC50eXBlKVxuXHRcdCkge1xuXHRcdFx0Y2xhc3Nlc1tmaWVsZC5uYW1lXSA9IFwibnVtYmVyXCI7XG5cdFx0fVxuXHRcdGlmIChcblx0XHRcdGFycm93LkRhdGFUeXBlLmlzRGF0ZShmaWVsZC50eXBlKSB8fFxuXHRcdFx0YXJyb3cuRGF0YVR5cGUuaXNUaW1lc3RhbXAoZmllbGQudHlwZSlcblx0XHQpIHtcblx0XHRcdGNsYXNzZXNbZmllbGQubmFtZV0gPSBcImRhdGVcIjtcblx0XHR9XG5cdH1cblx0cmV0dXJuIGNsYXNzZXM7XG59XG5cbmZ1bmN0aW9uIGhpZ2hsaWdodChjZWxsOiBIVE1MVGFibGVDZWxsRWxlbWVudCwgcm93OiBIVE1MVGFibGVSb3dFbGVtZW50KSB7XG5cdGlmIChyb3cuZmlyc3RDaGlsZCAhPT0gY2VsbCAmJiBjZWxsICE9PSByb3cubGFzdEVsZW1lbnRDaGlsZCkge1xuXHRcdGNlbGwuc3R5bGUuYm9yZGVyID0gXCIxcHggc29saWQgdmFyKC0tbW9vbi1ncmF5KVwiO1xuXHR9XG5cdHJvdy5zdHlsZS5iYWNrZ3JvdW5kQ29sb3IgPSBcInZhcigtLWxpZ2h0LXNpbHZlcilcIjtcbn1cblxuZnVuY3Rpb24gcmVtb3ZlSGlnaGxpZ2h0KGNlbGw6IEhUTUxUYWJsZUNlbGxFbGVtZW50LCByb3c6IEhUTUxUYWJsZVJvd0VsZW1lbnQpIHtcblx0Y2VsbC5zdHlsZS5yZW1vdmVQcm9wZXJ0eShcImJvcmRlclwiKTtcblx0cm93LnN0eWxlLnJlbW92ZVByb3BlcnR5KFwiYmFja2dyb3VuZC1jb2xvclwiKTtcbn1cblxuZnVuY3Rpb24gaXNUYWJsZUNlbGxFbGVtZW50KG5vZGU6IHVua25vd24pOiBub2RlIGlzIEhUTUxUYWJsZURhdGFDZWxsRWxlbWVudCB7XG5cdC8vIEB0cy1leHBlY3QtZXJyb3IgLSB0YWdOYW1lIGlzIG5vdCBkZWZpbmVkIG9uIHVua25vd25cblx0cmV0dXJuIG5vZGU/LnRhZ05hbWUgPT09IFwiVERcIjtcbn1cblxuZnVuY3Rpb24gaXNUYWJsZVJvd0VsZW1lbnQobm9kZTogdW5rbm93bik6IG5vZGUgaXMgSFRNTFRhYmxlUm93RWxlbWVudCB7XG5cdHJldHVybiBub2RlIGluc3RhbmNlb2YgSFRNTFRhYmxlUm93RWxlbWVudDtcbn1cblxuLyoqIEBwYXJhbSB7c3RyaW5nfSB2YWx1ZSAqL1xuZnVuY3Rpb24gc2hvdWxkR3JheW91dFZhbHVlKHZhbHVlOiBzdHJpbmcpIHtcblx0cmV0dXJuIChcblx0XHR2YWx1ZSA9PT0gXCJudWxsXCIgfHxcblx0XHR2YWx1ZSA9PT0gXCJ1bmRlZmluZWRcIiB8fFxuXHRcdHZhbHVlID09PSBcIk5hTlwiIHx8XG5cdFx0dmFsdWUgPT09IFwiVE9ET1wiXG5cdCk7XG59XG5cbmZ1bmN0aW9uIGlzVGFibGVDb2x1bW5IZWFkZXJXaXRoU3ZnKFxuXHRub2RlOiB1bmtub3duLFxuKTogbm9kZSBpcyBSZXR1cm5UeXBlPHR5cGVvZiB0aGNvbD4ge1xuXHRyZXR1cm4gbm9kZSBpbnN0YW5jZW9mIEhUTUxUYWJsZUNlbGxFbGVtZW50ICYmIFwidmlzXCIgaW4gbm9kZTtcbn1cblxuLyoqXG4gKiBBIG1vc2FpYyBTUUwgZXhwcmVzc2lvbiBmb3IgYXNjZW5kaW5nIG9yZGVyXG4gKlxuICogVGhlIG5vcm1hbCBiZWhhdmlvciBpbiBTUUwgaXMgdG8gc29ydCBudWxscyBmaXJzdCB3aGVuIHNvcnRpbmcgaW4gYXNjZW5kaW5nIG9yZGVyLlxuICogVGhpcyBmdW5jdGlvbiByZXR1cm5zIGFuIGV4cHJlc3Npb24gdGhhdCBzb3J0cyBudWxscyBsYXN0IChpLmUuLCBgTlVMTFMgTEFTVGApLFxuICogbGlrZSB0aGUgYGRlc2NgIGZ1bmN0aW9uLlxuICpcbiAqIEBwYXJhbSBmaWVsZFxuICovXG5mdW5jdGlvbiBhc2MoZmllbGQ6IHN0cmluZyk6IFNRTEV4cHJlc3Npb24ge1xuXHQvLyBkb2Vzbid0IHNvcnQgbnVsbHMgZm9yIGFzY1xuXHRsZXQgZXhwciA9IGRlc2MoZmllbGQpO1xuXHQvLyBAdHMtZXhwZWN0LWVycm9yIC0gcHJpdmF0ZSBmaWVsZFxuXHRleHByLl9leHByWzBdID0gZXhwci5fZXhwclswXS5yZXBsYWNlKFwiREVTQ1wiLCBcIkFTQ1wiKTtcblx0cmV0dXJuIGV4cHI7XG59XG4iLCAiLyoqXG4gKiBFcnJvciB0aHJvd24gd2hlbiBhbiBhc3NlcnRpb24gZmFpbHMuXG4gKi9cbmV4cG9ydCBjbGFzcyBBc3NlcnRpb25FcnJvciBleHRlbmRzIEVycm9yIHtcblx0LyoqIEBwYXJhbSBtZXNzYWdlIFRoZSBlcnJvciBtZXNzYWdlLiAqL1xuXHRjb25zdHJ1Y3RvcihtZXNzYWdlOiBzdHJpbmcpIHtcblx0XHRzdXBlcihtZXNzYWdlKTtcblx0XHR0aGlzLm5hbWUgPSBcIkFzc2VydGlvbkVycm9yXCI7XG5cdH1cbn1cblxuLyoqXG4gKiBNYWtlIGFuIGFzc2VydGlvbi4gQW4gZXJyb3IgaXMgdGhyb3duIGlmIGBleHByYCBkb2VzIG5vdCBoYXZlIHRydXRoeSB2YWx1ZS5cbiAqXG4gKiBAcGFyYW0gZXhwciBUaGUgZXhwcmVzc2lvbiB0byB0ZXN0LlxuICogQHBhcmFtIG1zZyBUaGUgbWVzc2FnZSB0byBkaXNwbGF5IGlmIHRoZSBhc3NlcnRpb24gZmFpbHMuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBhc3NlcnQoZXhwcjogdW5rbm93biwgbXNnID0gXCJcIik6IGFzc2VydHMgZXhwciB7XG5cdGlmICghZXhwcikge1xuXHRcdHRocm93IG5ldyBBc3NlcnRpb25FcnJvcihtc2cpO1xuXHR9XG59XG4iLCAiaW1wb3J0IHsgYXNzZXJ0IH0gZnJvbSBcIi4vYXNzZXJ0LnRzXCI7XG5cbi8qKlxuICogQW4gYXN5bmMgaXRlcmF0b3IgdGhhdCByZWFkcyBkYXRhIGluIGJhdGNoZXMgZnJvbSBhbiBhc3luYyBzb3VyY2UuXG4gKlxuICogQGV4YW1wbGVcbiAqIGBgYHRzXG4gKiBsZXQgaSA9IDA7XG4gKiBsZXQgYmF0Y2hlcyA9IFtbMSwgMiwgM10sIFs0LCA1LCA2XV07XG4gKiBsZXQgcmVxdWVzdE5leHRCYXRjaCA9IGFzeW5jICgpID0+IHtcbiAqICAgLy8gc2ltdWxhdGUgZmV0Y2hpbmcgYSBiYXRjaFxuICogICBhd2FpdCBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4gc2V0VGltZW91dChyZXNvbHZlLCAxMDAwKSk7XG4gKiAgIGxldCBiYXRjaCA9IGJhdGNoZXMuc2hpZnQoKTtcbiAqICAgcmVhZGVyLmVucXVldWVCYXRjaChiYXRjaCwgeyBsYXN0OiBiYXRjaGVzLmxlbmd0aCA9PT0gMCB9KTtcbiAqIH07XG4gKiBsZXQgcmVhZGVyID0gbmV3IEFzeW5jQmF0Y2hSZWFkZXIocmVxdWVzdE5leHRCYXRjaCk7XG4gKlxuICogZm9yIGF3YWl0IChsZXQgeyByb3csIGluZGV4IH0gb2YgcmVhZGVyKSB7XG4gKiAgIGNvbnNvbGUubG9nKHJvdywgaW5kZXgpO1xuICogfVxuICogYGBgXG4gKi9cbmV4cG9ydCBjbGFzcyBBc3luY0JhdGNoUmVhZGVyPFQ+IHtcblx0LyoqIHRoZSBpdGVyYWJsZSBiYXRjaGVzIHRvIHJlYWQgKi9cblx0I2JhdGNoZXM6IEFycmF5PHsgZGF0YTogSXRlcmF0b3I8VD47IGxhc3Q6IGJvb2xlYW4gfT4gPSBbXTtcblx0LyoqIHRoZSBpbmRleCBvZiB0aGUgY3VycmVudCByb3cgKi9cblx0I2luZGV4OiBudW1iZXIgPSAwO1xuXHQvKiogcmVzb2x2ZXMgYSBwcm9taXNlIGZvciB3aGVuIHRoZSBuZXh0IGJhdGNoIGlzIGF2YWlsYWJsZSAqL1xuXHQjcmVzb2x2ZTogKCgpID0+IHZvaWQpIHwgbnVsbCA9IG51bGw7XG5cdC8qKiB0aGUgY3VycmVudCBiYXRjaCAqL1xuXHQjY3VycmVudDogeyBkYXRhOiBJdGVyYXRvcjxUPjsgbGFzdDogYm9vbGVhbiB9IHwgbnVsbCA9IG51bGw7XG5cdC8qKiBBIGZ1bmN0aW9uIHRvIHJlcXVlc3QgbW9yZSBkYXRhLiAqL1xuXHQjcmVxdWVzdE5leHRCYXRjaDogKCkgPT4gdm9pZDtcblx0LyoqXG5cdCAqIEBwYXJhbSByZXF1ZXN0TmV4dEJhdGNoIC0gYSBmdW5jdGlvbiB0byByZXF1ZXN0IG1vcmUgZGF0YS4gV2hlblxuXHQgKiB0aGlzIGZ1bmN0aW9uIGNvbXBsZXRlcywgaXQgc2hvdWxkIGVucXVldWUgdGhlIG5leHQgYmF0Y2gsIG90aGVyd2lzZSB0aGVcblx0ICogcmVhZGVyIHdpbGwgYmUgc3R1Y2suXG5cdCAqL1xuXHRjb25zdHJ1Y3RvcihyZXF1ZXN0TmV4dEJhdGNoOiAoKSA9PiB2b2lkKSB7XG5cdFx0dGhpcy4jcmVxdWVzdE5leHRCYXRjaCA9IHJlcXVlc3ROZXh0QmF0Y2g7XG5cdH1cblx0LyoqXG5cdCAqIEVucXVldWUgYSBiYXRjaCBvZiBkYXRhXG5cdCAqXG5cdCAqIFRoZSBsYXN0IGJhdGNoIHNob3VsZCBoYXZlIGBsYXN0OiB0cnVlYCBzZXQsXG5cdCAqIHNvIHRoZSByZWFkZXIgY2FuIHRlcm1pbmF0ZSB3aGVuIGl0IGhhc1xuXHQgKiBleGhhdXN0ZWQgYWxsIHRoZSBkYXRhLlxuXHQgKlxuXHQgKiBAcGFyYW0gYmF0Y2ggLSB0aGUgYmF0Y2ggb2YgZGF0YSB0byBlbnF1ZXVlXG5cdCAqIEBwYXJhbSBvcHRpb25zXG5cdCAqIEBwYXJhbSBvcHRpb25zLmxhc3QgLSB3aGV0aGVyIHRoaXMgaXMgdGhlIGxhc3QgYmF0Y2hcblx0ICovXG5cdGVucXVldWVCYXRjaChiYXRjaDogSXRlcmF0b3I8VD4sIHsgbGFzdCB9OiB7IGxhc3Q6IGJvb2xlYW4gfSkge1xuXHRcdHRoaXMuI2JhdGNoZXMucHVzaCh7IGRhdGE6IGJhdGNoLCBsYXN0IH0pO1xuXHRcdGlmICh0aGlzLiNyZXNvbHZlKSB7XG5cdFx0XHR0aGlzLiNyZXNvbHZlKCk7XG5cdFx0XHR0aGlzLiNyZXNvbHZlID0gbnVsbDtcblx0XHR9XG5cdH1cblx0YXN5bmMgbmV4dCgpOiBQcm9taXNlPEl0ZXJhdG9yUmVzdWx0PHsgcm93OiBUOyBpbmRleDogbnVtYmVyIH0+PiB7XG5cdFx0aWYgKCF0aGlzLiNjdXJyZW50KSB7XG5cdFx0XHRpZiAodGhpcy4jYmF0Y2hlcy5sZW5ndGggPT09IDApIHtcblx0XHRcdFx0LyoqIEB0eXBlIHtQcm9taXNlPHZvaWQ+fSAqL1xuXHRcdFx0XHRsZXQgcHJvbWlzZTogUHJvbWlzZTx2b2lkPiA9IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiB7XG5cdFx0XHRcdFx0dGhpcy4jcmVzb2x2ZSA9IHJlc29sdmU7XG5cdFx0XHRcdH0pO1xuXHRcdFx0XHR0aGlzLiNyZXF1ZXN0TmV4dEJhdGNoKCk7XG5cdFx0XHRcdGF3YWl0IHByb21pc2U7XG5cdFx0XHR9XG5cdFx0XHRsZXQgbmV4dCA9IHRoaXMuI2JhdGNoZXMuc2hpZnQoKTtcblx0XHRcdGFzc2VydChuZXh0LCBcIk5vIG5leHQgYmF0Y2hcIik7XG5cdFx0XHR0aGlzLiNjdXJyZW50ID0gbmV4dDtcblx0XHR9XG5cdFx0bGV0IHJlc3VsdCA9IHRoaXMuI2N1cnJlbnQuZGF0YS5uZXh0KCk7XG5cdFx0aWYgKHJlc3VsdC5kb25lKSB7XG5cdFx0XHRpZiAodGhpcy4jY3VycmVudC5sYXN0KSB7XG5cdFx0XHRcdHJldHVybiB7IGRvbmU6IHRydWUsIHZhbHVlOiB1bmRlZmluZWQgfTtcblx0XHRcdH1cblx0XHRcdHRoaXMuI2N1cnJlbnQgPSBudWxsO1xuXHRcdFx0cmV0dXJuIHRoaXMubmV4dCgpO1xuXHRcdH1cblx0XHRyZXR1cm4ge1xuXHRcdFx0ZG9uZTogZmFsc2UsXG5cdFx0XHR2YWx1ZTogeyByb3c6IHJlc3VsdC52YWx1ZSwgaW5kZXg6IHRoaXMuI2luZGV4KysgfSxcblx0XHR9O1xuXHR9XG59XG4iLCAiaW1wb3J0IHsgVGVtcG9yYWwgfSBmcm9tIFwiQGpzLXRlbXBvcmFsL3BvbHlmaWxsXCI7XG5pbXBvcnQgKiBhcyBhcnJvdyBmcm9tIFwiYXBhY2hlLWFycm93XCI7XG5cbi8qKlxuICogQSB1dGlsaXR5IGZ1bmN0aW9uIHRvIGNyZWF0ZSBhIGZvcm1hdHRlciBmb3IgYSBnaXZlbiBkYXRhIHR5cGUuXG4gKlxuICogVGhlIGRhdGF0eXBlIGlzIG9ubHkgdXNlZCBmb3IgdHlwZSBpbmZlcmVuY2UgdG8gZW5zdXJlIHRoYXQgdGhlIGZvcm1hdHRlciBpc1xuICogY29ycmVjdGx5IHR5cGVkLlxuICovXG5mdW5jdGlvbiBmbXQ8VFZhbHVlPihcblx0X2Fycm93RGF0YVR5cGVWYWx1ZTogVFZhbHVlLFxuXHRmb3JtYXQ6ICh2YWx1ZTogVFZhbHVlKSA9PiBzdHJpbmcsXG5cdGxvZyA9IGZhbHNlLFxuKTogKHZhbHVlOiBUVmFsdWUgfCBudWxsIHwgdW5kZWZpbmVkKSA9PiBzdHJpbmcge1xuXHRyZXR1cm4gKHZhbHVlKSA9PiB7XG5cdFx0aWYgKGxvZykgY29uc29sZS5sb2codmFsdWUpO1xuXHRcdGlmICh2YWx1ZSA9PT0gdW5kZWZpbmVkIHx8IHZhbHVlID09PSBudWxsKSB7XG5cdFx0XHRyZXR1cm4gc3RyaW5naWZ5KHZhbHVlKTtcblx0XHR9XG5cdFx0cmV0dXJuIGZvcm1hdCh2YWx1ZSk7XG5cdH07XG59XG5cbmZ1bmN0aW9uIHN0cmluZ2lmeSh4OiB1bmtub3duKTogc3RyaW5nIHtcblx0cmV0dXJuIGAke3h9YDtcbn1cblxuLyoqIEBwYXJhbSB7YXJyb3cuRGF0YVR5cGV9IHR5cGUgKi9cbmV4cG9ydCBmdW5jdGlvbiBmb3JtYXREYXRhVHlwZSh0eXBlOiBhcnJvdy5EYXRhVHlwZSkge1xuXHQvLyBzcGVjaWFsIGNhc2Ugc29tZSB0eXBlc1xuXHRpZiAoYXJyb3cuRGF0YVR5cGUuaXNMYXJnZUJpbmFyeSh0eXBlKSkgcmV0dXJuIFwibGFyZ2UgYmluYXJ5XCI7XG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc0xhcmdlVXRmOCh0eXBlKSkgcmV0dXJuIFwibGFyZ2UgdXRmOFwiO1xuXHQvLyBvdGhlcndpc2UsIGp1c3Qgc3RyaW5naWZ5IGFuZCBsb3dlcmNhc2Vcblx0cmV0dXJuIHR5cGVcblx0XHQudG9TdHJpbmcoKVxuXHRcdC50b0xvd2VyQ2FzZSgpXG5cdFx0LnJlcGxhY2UoXCI8c2Vjb25kPlwiLCBcIltzXVwiKVxuXHRcdC5yZXBsYWNlKFwiPG1pbGxpc2Vjb25kPlwiLCBcIlttc11cIilcblx0XHQucmVwbGFjZShcIjxtaWNyb3NlY29uZD5cIiwgXCJbXHUwMEI1c11cIilcblx0XHQucmVwbGFjZShcIjxuYW5vc2Vjb25kPlwiLCBcIltuc11cIilcblx0XHQucmVwbGFjZShcIjxkYXk+XCIsIFwiW2RheV1cIilcblx0XHQucmVwbGFjZShcImRpY3Rpb25hcnk8XCIsIFwiZGljdDxcIik7XG59XG5cbi8qKlxuICogQHBhcmFtIHthcnJvdy5EYXRhVHlwZX0gdHlwZVxuICogQHJldHVybnMgeyh2YWx1ZTogYW55KSA9PiBzdHJpbmd9XG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBmb3JtYXR0ZXJGb3JWYWx1ZShcblx0dHlwZTogYXJyb3cuRGF0YVR5cGUsXG5cdC8vIGRlbm8tbGludC1pZ25vcmUgbm8tZXhwbGljaXQtYW55XG4pOiAodmFsdWU6IGFueSkgPT4gc3RyaW5nIHtcblx0aWYgKGFycm93LkRhdGFUeXBlLmlzTnVsbCh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsIHN0cmluZ2lmeSk7XG5cdH1cblxuXHRpZiAoXG5cdFx0YXJyb3cuRGF0YVR5cGUuaXNJbnQodHlwZSkgfHxcblx0XHRhcnJvdy5EYXRhVHlwZS5pc0Zsb2F0KHR5cGUpXG5cdCkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsICh2YWx1ZSkgPT4ge1xuXHRcdFx0aWYgKE51bWJlci5pc05hTih2YWx1ZSkpIHJldHVybiBcIk5hTlwiO1xuXHRcdFx0cmV0dXJuIHZhbHVlID09PSAwID8gXCIwXCIgOiB2YWx1ZS50b0xvY2FsZVN0cmluZyhcImVuXCIpOyAvLyBoYW5kbGUgbmVnYXRpdmUgemVyb1xuXHRcdH0pO1xuXHR9XG5cblx0aWYgKFxuXHRcdGFycm93LkRhdGFUeXBlLmlzQmluYXJ5KHR5cGUpIHx8XG5cdFx0YXJyb3cuRGF0YVR5cGUuaXNGaXhlZFNpemVCaW5hcnkodHlwZSkgfHxcblx0XHRhcnJvdy5EYXRhVHlwZS5pc0xhcmdlQmluYXJ5KHR5cGUpXG5cdCkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsIChieXRlcykgPT4ge1xuXHRcdFx0bGV0IG1heGxlbiA9IDMyO1xuXHRcdFx0bGV0IHJlc3VsdCA9IFwiYidcIjtcblx0XHRcdGZvciAobGV0IGkgPSAwOyBpIDwgTWF0aC5taW4oYnl0ZXMubGVuZ3RoLCBtYXhsZW4pOyBpKyspIHtcblx0XHRcdFx0Y29uc3QgYnl0ZSA9IGJ5dGVzW2ldO1xuXHRcdFx0XHRpZiAoYnl0ZSA+PSAzMiAmJiBieXRlIDw9IDEyNikge1xuXHRcdFx0XHRcdC8vIEFTQ0lJIHByaW50YWJsZSBjaGFyYWN0ZXJzIHJhbmdlIGZyb20gMzIgKHNwYWNlKSB0byAxMjYgKH4pXG5cdFx0XHRcdFx0cmVzdWx0ICs9IFN0cmluZy5mcm9tQ2hhckNvZGUoYnl0ZSk7XG5cdFx0XHRcdH0gZWxzZSB7XG5cdFx0XHRcdFx0cmVzdWx0ICs9IFwiXFxcXHhcIiArIChcIjAwXCIgKyBieXRlLnRvU3RyaW5nKDE2KSkuc2xpY2UoLTIpO1xuXHRcdFx0XHR9XG5cdFx0XHR9XG5cdFx0XHRpZiAoYnl0ZXMubGVuZ3RoID4gbWF4bGVuKSByZXN1bHQgKz0gXCIuLi5cIjtcblx0XHRcdHJlc3VsdCArPSBcIidcIjtcblx0XHRcdHJldHVybiByZXN1bHQ7XG5cdFx0fSk7XG5cdH1cblxuXHRpZiAoYXJyb3cuRGF0YVR5cGUuaXNVdGY4KHR5cGUpIHx8IGFycm93LkRhdGFUeXBlLmlzTGFyZ2VVdGY4KHR5cGUpKSB7XG5cdFx0cmV0dXJuIGZtdCh0eXBlLlRWYWx1ZSwgKHRleHQpID0+IHRleHQpO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzQm9vbCh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsIHN0cmluZ2lmeSk7XG5cdH1cblxuXHRpZiAoYXJyb3cuRGF0YVR5cGUuaXNEZWNpbWFsKHR5cGUpKSB7XG5cdFx0cmV0dXJuIGZtdCh0eXBlLlRWYWx1ZSwgKCkgPT4gXCJUT0RPXCIpO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzRGF0ZSh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsIChtcykgPT4ge1xuXHRcdFx0Ly8gQWx3YXlzIHJldHVybnMgdmFsdWUgaW4gbWlsbGlzZWNvbmRzXG5cdFx0XHQvLyBodHRwczovL2dpdGh1Yi5jb20vYXBhY2hlL2Fycm93L2Jsb2IvODlkNjM1NDA2OGMxMWE2NmZjZWMyZjM0ZDA0MTRkYWNhMzI3ZTJlMC9qcy9zcmMvdmlzaXRvci9nZXQudHMjTDE2Ny1MMTcxXG5cdFx0XHRyZXR1cm4gVGVtcG9yYWwuSW5zdGFudFxuXHRcdFx0XHQuZnJvbUVwb2NoTWlsbGlzZWNvbmRzKG1zKVxuXHRcdFx0XHQudG9ab25lZERhdGVUaW1lSVNPKFwiVVRDXCIpXG5cdFx0XHRcdC50b1BsYWluRGF0ZSgpXG5cdFx0XHRcdC50b1N0cmluZygpO1xuXHRcdH0pO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzVGltZSh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsIChtcykgPT4ge1xuXHRcdFx0cmV0dXJuIGluc3RhbnRGcm9tVGltZVVuaXQobXMsIHR5cGUudW5pdClcblx0XHRcdFx0LnRvWm9uZWREYXRlVGltZUlTTyhcIlVUQ1wiKVxuXHRcdFx0XHQudG9QbGFpblRpbWUoKVxuXHRcdFx0XHQudG9TdHJpbmcoKTtcblx0XHR9KTtcblx0fVxuXG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc1RpbWVzdGFtcCh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsIChtcykgPT4ge1xuXHRcdFx0Ly8gQWx3YXlzIHJldHVybnMgdmFsdWUgaW4gbWlsbGlzZWNvbmRzXG5cdFx0XHQvLyBodHRwczovL2dpdGh1Yi5jb20vYXBhY2hlL2Fycm93L2Jsb2IvODlkNjM1NDA2OGMxMWE2NmZjZWMyZjM0ZDA0MTRkYWNhMzI3ZTJlMC9qcy9zcmMvdmlzaXRvci9nZXQudHMjTDE3My1MMTkwXG5cdFx0XHRyZXR1cm4gVGVtcG9yYWwuSW5zdGFudFxuXHRcdFx0XHQuZnJvbUVwb2NoTWlsbGlzZWNvbmRzKG1zKVxuXHRcdFx0XHQudG9ab25lZERhdGVUaW1lSVNPKFwiVVRDXCIpXG5cdFx0XHRcdC50b1BsYWluRGF0ZVRpbWUoKVxuXHRcdFx0XHQudG9TdHJpbmcoKTtcblx0XHR9KTtcblx0fVxuXG5cdGlmIChhcnJvdy5EYXRhVHlwZS5pc0ludGVydmFsKHR5cGUpKSB7XG5cdFx0cmV0dXJuIGZtdCh0eXBlLlRWYWx1ZSwgKF92YWx1ZSkgPT4ge1xuXHRcdFx0cmV0dXJuIFwiVE9ET1wiO1xuXHRcdH0pO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzRHVyYXRpb24odHlwZSkpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCAoYmlnaW50VmFsdWUpID0+IHtcblx0XHRcdC8vIGh0dHBzOi8vdGMzOS5lcy9wcm9wb3NhbC10ZW1wb3JhbC9kb2NzL2R1cmF0aW9uLmh0bWwjdG9TdHJpbmdcblx0XHRcdHJldHVybiBkdXJhdGlvbkZyb21UaW1lVW5pdChiaWdpbnRWYWx1ZSwgdHlwZS51bml0KS50b1N0cmluZygpO1xuXHRcdH0pO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzTGlzdCh0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsICh2YWx1ZSkgPT4ge1xuXHRcdFx0Ly8gVE9ETzogU29tZSByZWN1cnNpdmUgZm9ybWF0dGluZz9cblx0XHRcdHJldHVybiB2YWx1ZS50b1N0cmluZygpO1xuXHRcdH0pO1xuXHR9XG5cblx0aWYgKGFycm93LkRhdGFUeXBlLmlzU3RydWN0KHR5cGUpKSB7XG5cdFx0cmV0dXJuIGZtdCh0eXBlLlRWYWx1ZSwgKHZhbHVlKSA9PiB7XG5cdFx0XHQvLyBUT0RPOiBTb21lIHJlY3Vyc2l2ZSBmb3JtYXR0aW5nP1xuXHRcdFx0cmV0dXJuIHZhbHVlLnRvU3RyaW5nKCk7XG5cdFx0fSk7XG5cdH1cblxuXHRpZiAoYXJyb3cuRGF0YVR5cGUuaXNVbmlvbih0eXBlKSkge1xuXHRcdHJldHVybiBmbXQodHlwZS5UVmFsdWUsIChfdmFsdWUpID0+IHtcblx0XHRcdHJldHVybiBcIlRPRE9cIjtcblx0XHR9KTtcblx0fVxuXHRpZiAoYXJyb3cuRGF0YVR5cGUuaXNNYXAodHlwZSkpIHtcblx0XHRyZXR1cm4gZm10KHR5cGUuVFZhbHVlLCAoX3ZhbHVlKSA9PiB7XG5cdFx0XHRyZXR1cm4gXCJUT0RPXCI7XG5cdFx0fSk7XG5cdH1cblxuXHRpZiAoYXJyb3cuRGF0YVR5cGUuaXNEaWN0aW9uYXJ5KHR5cGUpKSB7XG5cdFx0bGV0IGZvcm1hdHRlciA9IGZvcm1hdHRlckZvclZhbHVlKHR5cGUuZGljdGlvbmFyeSk7XG5cdFx0cmV0dXJuIGZtdCh0eXBlLlRWYWx1ZSwgZm9ybWF0dGVyKTtcblx0fVxuXG5cdHJldHVybiAoKSA9PiBgVW5zdXBwb3J0ZWQgdHlwZTogJHt0eXBlfWA7XG59XG5cbi8qKlxuICogQHBhcmFtIHtudW1iZXIgfCBiaWdpbnR9IHZhbHVlXG4gKiBAcGFyYW0ge2Fycm93LlRpbWVVbml0fSB1bml0XG4gKi9cbmZ1bmN0aW9uIGluc3RhbnRGcm9tVGltZVVuaXQodmFsdWU6IG51bWJlciB8IGJpZ2ludCwgdW5pdDogYXJyb3cuVGltZVVuaXQpIHtcblx0aWYgKHVuaXQgPT09IGFycm93LlRpbWVVbml0LlNFQ09ORCkge1xuXHRcdGlmICh0eXBlb2YgdmFsdWUgPT09IFwiYmlnaW50XCIpIHZhbHVlID0gTnVtYmVyKHZhbHVlKTtcblx0XHRyZXR1cm4gVGVtcG9yYWwuSW5zdGFudC5mcm9tRXBvY2hTZWNvbmRzKHZhbHVlKTtcblx0fVxuXHRpZiAodW5pdCA9PT0gYXJyb3cuVGltZVVuaXQuTUlMTElTRUNPTkQpIHtcblx0XHRpZiAodHlwZW9mIHZhbHVlID09PSBcImJpZ2ludFwiKSB2YWx1ZSA9IE51bWJlcih2YWx1ZSk7XG5cdFx0cmV0dXJuIFRlbXBvcmFsLkluc3RhbnQuZnJvbUVwb2NoTWlsbGlzZWNvbmRzKHZhbHVlKTtcblx0fVxuXHRpZiAodW5pdCA9PT0gYXJyb3cuVGltZVVuaXQuTUlDUk9TRUNPTkQpIHtcblx0XHRpZiAodHlwZW9mIHZhbHVlID09PSBcIm51bWJlclwiKSB2YWx1ZSA9IEJpZ0ludCh2YWx1ZSk7XG5cdFx0cmV0dXJuIFRlbXBvcmFsLkluc3RhbnQuZnJvbUVwb2NoTWljcm9zZWNvbmRzKHZhbHVlKTtcblx0fVxuXHRpZiAodW5pdCA9PT0gYXJyb3cuVGltZVVuaXQuTkFOT1NFQ09ORCkge1xuXHRcdGlmICh0eXBlb2YgdmFsdWUgPT09IFwibnVtYmVyXCIpIHZhbHVlID0gQmlnSW50KHZhbHVlKTtcblx0XHRyZXR1cm4gVGVtcG9yYWwuSW5zdGFudC5mcm9tRXBvY2hOYW5vc2Vjb25kcyh2YWx1ZSk7XG5cdH1cblx0dGhyb3cgbmV3IEVycm9yKFwiSW52YWxpZCBUaW1lVW5pdFwiKTtcbn1cblxuLyoqXG4gKiBAcGFyYW0ge251bWJlciB8IGJpZ2ludH0gdmFsdWVcbiAqIEBwYXJhbSB7YXJyb3cuVGltZVVuaXR9IHVuaXRcbiAqL1xuZnVuY3Rpb24gZHVyYXRpb25Gcm9tVGltZVVuaXQodmFsdWU6IG51bWJlciB8IGJpZ2ludCwgdW5pdDogYXJyb3cuVGltZVVuaXQpIHtcblx0Ly8gVE9ETzogVGVtcG9yYWwuRHVyYXRpb24gcG9seWZpbGwgb25seSBzdXBwb3J0cyBudW1iZXIgbm90IGJpZ2ludFxuXHR2YWx1ZSA9IE51bWJlcih2YWx1ZSk7XG5cdGlmICh1bml0ID09PSBhcnJvdy5UaW1lVW5pdC5TRUNPTkQpIHtcblx0XHRyZXR1cm4gVGVtcG9yYWwuRHVyYXRpb24uZnJvbSh7IHNlY29uZHM6IHZhbHVlIH0pO1xuXHR9XG5cdGlmICh1bml0ID09PSBhcnJvdy5UaW1lVW5pdC5NSUxMSVNFQ09ORCkge1xuXHRcdHJldHVybiBUZW1wb3JhbC5EdXJhdGlvbi5mcm9tKHsgbWlsbGlzZWNvbmRzOiB2YWx1ZSB9KTtcblx0fVxuXHRpZiAodW5pdCA9PT0gYXJyb3cuVGltZVVuaXQuTUlDUk9TRUNPTkQpIHtcblx0XHRyZXR1cm4gVGVtcG9yYWwuRHVyYXRpb24uZnJvbSh7IG1pY3Jvc2Vjb25kczogdmFsdWUgfSk7XG5cdH1cblx0aWYgKHVuaXQgPT09IGFycm93LlRpbWVVbml0Lk5BTk9TRUNPTkQpIHtcblx0XHRyZXR1cm4gVGVtcG9yYWwuRHVyYXRpb24uZnJvbSh7IG5hbm9zZWNvbmRzOiB2YWx1ZSB9KTtcblx0fVxuXHR0aHJvdyBuZXcgRXJyb3IoXCJJbnZhbGlkIFRpbWVVbml0XCIpO1xufVxuIiwgIi8vIEBkZW5vLXR5cGVzPVwiLi4vZGVwcy9tb3NhaWMtY29yZS5kLnRzXCI7XG5pbXBvcnQge1xuXHR0eXBlIENvbHVtbkZpZWxkLFxuXHR0eXBlIEZpZWxkSW5mbyxcblx0dHlwZSBGaWVsZFJlcXVlc3QsXG5cdE1vc2FpY0NsaWVudCxcblx0dHlwZSBTZWxlY3Rpb24sXG59IGZyb20gXCJAdXdkYXRhL21vc2FpYy1jb3JlXCI7XG4vLyBAZGVuby10eXBlcz1cIi4uL2RlcHMvbW9zYWljLXNxbC5kLnRzXCI7XG5pbXBvcnQgeyBjb3VudCwgUXVlcnksIFNRTEV4cHJlc3Npb24gfSBmcm9tIFwiQHV3ZGF0YS9tb3NhaWMtc3FsXCI7XG5pbXBvcnQgKiBhcyBtcGxvdCBmcm9tIFwiQHV3ZGF0YS9tb3NhaWMtcGxvdFwiO1xuaW1wb3J0IHR5cGUgKiBhcyBhcnJvdyBmcm9tIFwiYXBhY2hlLWFycm93XCI7XG5cbmltcG9ydCB7IENyb3NzZmlsdGVySGlzdG9ncmFtUGxvdCB9IGZyb20gXCIuLi91dGlscy9Dcm9zc2ZpbHRlckhpc3RvZ3JhbVBsb3QudHNcIjtcblxuaW1wb3J0IHR5cGUgeyBNYXJrIH0gZnJvbSBcIi4uL3R5cGVzLnRzXCI7XG5pbXBvcnQgeyBhc3NlcnQgfSBmcm9tIFwiLi4vdXRpbHMvYXNzZXJ0LnRzXCI7XG5cbi8qKiBBbiBvcHRpb25zIGJhZyBmb3IgdGhlIEhpc3RvZ3JhbSBNb3NpYWMgY2xpZW50LiAqL1xuaW50ZXJmYWNlIEhpc3RvZ3JhbU9wdGlvbnMge1xuXHQvKiogVGhlIHRhYmxlIHRvIHF1ZXJ5LiAqL1xuXHR0YWJsZTogc3RyaW5nO1xuXHQvKiogVGhlIGNvbHVtbiB0byB1c2UgZm9yIHRoZSBoaXN0b2dyYW0uICovXG5cdGNvbHVtbjogc3RyaW5nO1xuXHQvKiogVGhlIHR5cGUgb2YgdGhlIGNvbHVtbi4gTXVzdCBiZSBcIm51bWJlclwiIG9yIFwiZGF0ZVwiLiAqL1xuXHR0eXBlOiBcIm51bWJlclwiIHwgXCJkYXRlXCI7XG5cdC8qKiBBIG1vc2FpYyBzZWxlY3Rpb24gdG8gZmlsdGVyIHRoZSBkYXRhLiAqL1xuXHRmaWx0ZXJCeTogU2VsZWN0aW9uO1xufVxuXG50eXBlIEJpblRhYmxlID0gYXJyb3cuVGFibGU8eyB4MTogYXJyb3cuSW50OyB4MjogYXJyb3cuSW50OyB5OiBhcnJvdy5JbnQgfT47XG5cbi8qKiBSZXByZXNlbnRzIGEgQ3Jvc3MtZmlsdGVyZWQgSGlzdG9ncmFtICovXG5leHBvcnQgY2xhc3MgSGlzdG9ncmFtIGV4dGVuZHMgTW9zYWljQ2xpZW50IGltcGxlbWVudHMgTWFyayB7XG5cdCNzb3VyY2U6IHsgdGFibGU6IHN0cmluZzsgY29sdW1uOiBzdHJpbmc7IHR5cGU6IFwibnVtYmVyXCIgfCBcImRhdGVcIiB9O1xuXHQjZWw6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcblx0I3NlbGVjdDoge1xuXHRcdHgxOiBDb2x1bW5GaWVsZDtcblx0XHR4MjogQ29sdW1uRmllbGQ7XG5cdFx0eTogU1FMRXhwcmVzc2lvbjtcblx0fTtcblx0I2ludGVydmFsOiBtcGxvdC5JbnRlcnZhbDFEIHwgdW5kZWZpbmVkID0gdW5kZWZpbmVkO1xuXHQjaW5pdGlhbGl6ZWQ6IGJvb2xlYW4gPSBmYWxzZTtcblx0I2ZpZWxkSW5mbzogRmllbGRJbmZvIHwgdW5kZWZpbmVkO1xuXG5cdHN2ZzogUmV0dXJuVHlwZTx0eXBlb2YgQ3Jvc3NmaWx0ZXJIaXN0b2dyYW1QbG90PiB8IHVuZGVmaW5lZDtcblxuXHRjb25zdHJ1Y3RvcihvcHRpb25zOiBIaXN0b2dyYW1PcHRpb25zKSB7XG5cdFx0c3VwZXIob3B0aW9ucy5maWx0ZXJCeSk7XG5cdFx0dGhpcy4jc291cmNlID0gb3B0aW9ucztcblx0XHQvLyBjYWxscyB0aGlzLmNoYW5uZWxGaWVsZCBpbnRlcm5hbGx5XG5cdFx0bGV0IGJpbiA9IG1wbG90LmJpbihvcHRpb25zLmNvbHVtbikodGhpcywgXCJ4XCIpO1xuXHRcdHRoaXMuI3NlbGVjdCA9IHsgeDE6IGJpbi54MSwgeDI6IGJpbi54MiwgeTogY291bnQoKSB9O1xuXHRcdHRoaXMuI2ludGVydmFsID0gbmV3IG1wbG90LkludGVydmFsMUQodGhpcywge1xuXHRcdFx0Y2hhbm5lbDogXCJ4XCIsXG5cdFx0XHRzZWxlY3Rpb246IHRoaXMuZmlsdGVyQnksXG5cdFx0XHRmaWVsZDogdGhpcy4jc291cmNlLmNvbHVtbixcblx0XHRcdGJydXNoOiB1bmRlZmluZWQsXG5cdFx0fSk7XG5cdH1cblxuXHRmaWVsZHMoKTogQXJyYXk8RmllbGRSZXF1ZXN0PiB7XG5cdFx0cmV0dXJuIFtcblx0XHRcdHtcblx0XHRcdFx0dGFibGU6IHRoaXMuI3NvdXJjZS50YWJsZSxcblx0XHRcdFx0Y29sdW1uOiB0aGlzLiNzb3VyY2UuY29sdW1uLFxuXHRcdFx0XHRzdGF0czogW1wibWluXCIsIFwibWF4XCJdLFxuXHRcdFx0fSxcblx0XHRdO1xuXHR9XG5cblx0ZmllbGRJbmZvKGluZm86IEFycmF5PEZpZWxkSW5mbz4pIHtcblx0XHR0aGlzLiNmaWVsZEluZm8gPSBpbmZvWzBdO1xuXHRcdHJldHVybiB0aGlzO1xuXHR9XG5cdC8qKlxuXHQgKiBSZXR1cm4gYSBxdWVyeSBzcGVjaWZ5aW5nIHRoZSBkYXRhIG5lZWRlZCBieSB0aGlzIE1hcmsgY2xpZW50LlxuXHQgKiBAcGFyYW0gZmlsdGVyIFRoZSBmaWx0ZXJpbmcgY3JpdGVyaWEgdG8gYXBwbHkgaW4gdGhlIHF1ZXJ5LlxuXHQgKiBAcmV0dXJucyBUaGUgY2xpZW50IHF1ZXJ5XG5cdCAqL1xuXHRxdWVyeShmaWx0ZXI6IEFycmF5PFNRTEV4cHJlc3Npb24+ID0gW10pOiBRdWVyeSB7XG5cdFx0cmV0dXJuIFF1ZXJ5XG5cdFx0XHQuZnJvbSh7IHNvdXJjZTogdGhpcy4jc291cmNlLnRhYmxlIH0pXG5cdFx0XHQuc2VsZWN0KHRoaXMuI3NlbGVjdClcblx0XHRcdC5ncm91cGJ5KFtcIngxXCIsIFwieDJcIl0pXG5cdFx0XHQud2hlcmUoZmlsdGVyKTtcblx0fVxuXG5cdC8qKlxuXHQgKiBQcm92aWRlIHF1ZXJ5IHJlc3VsdCBkYXRhIHRvIHRoZSBtYXJrLlxuXHQgKi9cblx0cXVlcnlSZXN1bHQoZGF0YTogQmluVGFibGUpIHtcblx0XHRsZXQgYmlucyA9IEFycmF5LmZyb20oZGF0YSwgKGQpID0+ICh7XG5cdFx0XHR4MDogZC54MSxcblx0XHRcdHgxOiBkLngyLFxuXHRcdFx0bGVuZ3RoOiBkLnksXG5cdFx0fSkpO1xuXHRcdGxldCBudWxsQ291bnQgPSAwO1xuXHRcdGxldCBudWxsQmluSW5kZXggPSBiaW5zLmZpbmRJbmRleCgoYikgPT4gYi54MCA9PSBudWxsKTtcblx0XHRpZiAobnVsbEJpbkluZGV4ID49IDApIHtcblx0XHRcdG51bGxDb3VudCA9IGJpbnNbbnVsbEJpbkluZGV4XS5sZW5ndGg7XG5cdFx0XHRiaW5zLnNwbGljZShudWxsQmluSW5kZXgsIDEpO1xuXHRcdH1cblx0XHRpZiAoIXRoaXMuI2luaXRpYWxpemVkKSB7XG5cdFx0XHR0aGlzLnN2ZyA9IENyb3NzZmlsdGVySGlzdG9ncmFtUGxvdChiaW5zLCB7XG5cdFx0XHRcdG51bGxDb3VudCxcblx0XHRcdFx0dHlwZTogdGhpcy4jc291cmNlLnR5cGUsXG5cdFx0XHR9KTtcblx0XHRcdHRoaXMuI2ludGVydmFsPy5pbml0KHRoaXMuc3ZnLCBudWxsKTtcblx0XHRcdHRoaXMuI2VsLmFwcGVuZENoaWxkKHRoaXMuc3ZnKTtcblx0XHRcdHRoaXMuI2luaXRpYWxpemVkID0gdHJ1ZTtcblx0XHR9IGVsc2Uge1xuXHRcdFx0dGhpcy5zdmc/LnVwZGF0ZShiaW5zLCB7IG51bGxDb3VudCB9KTtcblx0XHR9XG5cdFx0cmV0dXJuIHRoaXM7XG5cdH1cblxuXHQvKiBSZXF1aXJlZCBieSB0aGUgTWFyayBpbnRlcmZhY2UgKi9cblx0dHlwZSA9IFwicmVjdFlcIjtcblx0LyoqIFJlcXVpcmVkIGJ5IGBtcGxvdC5iaW5gIHRvIGdldCB0aGUgZmllbGQgaW5mby4gKi9cblx0Y2hhbm5lbEZpZWxkKGNoYW5uZWw6IHN0cmluZyk6IEZpZWxkSW5mbyB7XG5cdFx0YXNzZXJ0KGNoYW5uZWwgPT09IFwieFwiKTtcblx0XHRhc3NlcnQodGhpcy4jZmllbGRJbmZvLCBcIk5vIGZpZWxkIGluZm8geWV0XCIpO1xuXHRcdHJldHVybiB0aGlzLiNmaWVsZEluZm87XG5cdH1cblx0Z2V0IHBsb3QoKSB7XG5cdFx0cmV0dXJuIHtcblx0XHRcdG5vZGU6ICgpID0+IHRoaXMuI2VsLFxuXHRcdFx0Z2V0QXR0cmlidXRlKF9uYW1lOiBzdHJpbmcpIHtcblx0XHRcdFx0cmV0dXJuIHVuZGVmaW5lZDtcblx0XHRcdH0sXG5cdFx0fTtcblx0fVxufVxuIiwgIi8vIFRoZSB0eXBlcyBmb3IgZDMgYXJlIHJlYWxseSBhbm5veWluZy5cblxuLy8gQGRlbm8tdHlwZXM9XCJucG06QHR5cGVzL2QzLXNlbGVjdGlvbkAzXCJcbmV4cG9ydCAqIGZyb20gXCJkMy1zZWxlY3Rpb25cIjtcbi8vIEBkZW5vLXR5cGVzPVwibnBtOkB0eXBlcy9kMy1zY2FsZUA0XCJcbmV4cG9ydCAqIGZyb20gXCJkMy1zY2FsZVwiO1xuLy8gQGRlbm8tdHlwZXM9XCJucG06QHR5cGVzL2QzLWF4aXNAM1wiXG5leHBvcnQgKiBmcm9tIFwiZDMtYXhpc1wiO1xuLy8gQGRlbm8tdHlwZXM9XCJucG06QHR5cGVzL2QzLWZvcm1hdEAzXCJcbmV4cG9ydCAqIGZyb20gXCJkMy1mb3JtYXRcIjtcbi8vIEBkZW5vLXR5cGVzPVwibnBtOkB0eXBlcy9kMy10aW1lLWZvcm1hdEA0XCJcbmV4cG9ydCAqIGZyb20gXCJkMy10aW1lLWZvcm1hdFwiO1xuIiwgImltcG9ydCAqIGFzIGQzIGZyb20gXCIuLi9kZXBzL2QzLnRzXCI7XG5pbXBvcnQgdHlwZSB7IEJpbiB9IGZyb20gXCIuLi90eXBlcy50c1wiO1xuXG5sZXQgWUVBUiA9IFwieWVhclwiO1xubGV0IE1PTlRIID0gXCJtb250aFwiO1xubGV0IERBWSA9IFwiZGF5XCI7XG5sZXQgSE9VUiA9IFwiaG91clwiO1xubGV0IE1JTlVURSA9IFwibWludXRlXCI7XG5sZXQgU0VDT05EID0gXCJzZWNvbmRcIjtcbmxldCBNSUxMSVNFQ09ORCA9IFwibWlsbGlzZWNvbmRcIjtcblxubGV0IGR1cmF0aW9uU2Vjb25kID0gMTAwMDtcbmxldCBkdXJhdGlvbk1pbnV0ZSA9IGR1cmF0aW9uU2Vjb25kICogNjA7XG5sZXQgZHVyYXRpb25Ib3VyID0gZHVyYXRpb25NaW51dGUgKiA2MDtcbmxldCBkdXJhdGlvbkRheSA9IGR1cmF0aW9uSG91ciAqIDI0O1xubGV0IGR1cmF0aW9uV2VlayA9IGR1cmF0aW9uRGF5ICogNztcbmxldCBkdXJhdGlvbk1vbnRoID0gZHVyYXRpb25EYXkgKiAzMDtcbmxldCBkdXJhdGlvblllYXIgPSBkdXJhdGlvbkRheSAqIDM2NTtcblxubGV0IGludGVydmFscyA9IFtcblx0W1NFQ09ORCwgMSwgZHVyYXRpb25TZWNvbmRdLFxuXHRbU0VDT05ELCA1LCA1ICogZHVyYXRpb25TZWNvbmRdLFxuXHRbU0VDT05ELCAxNSwgMTUgKiBkdXJhdGlvblNlY29uZF0sXG5cdFtTRUNPTkQsIDMwLCAzMCAqIGR1cmF0aW9uU2Vjb25kXSxcblx0W01JTlVURSwgMSwgZHVyYXRpb25NaW51dGVdLFxuXHRbTUlOVVRFLCA1LCA1ICogZHVyYXRpb25NaW51dGVdLFxuXHRbTUlOVVRFLCAxNSwgMTUgKiBkdXJhdGlvbk1pbnV0ZV0sXG5cdFtNSU5VVEUsIDMwLCAzMCAqIGR1cmF0aW9uTWludXRlXSxcblx0W0hPVVIsIDEsIGR1cmF0aW9uSG91cl0sXG5cdFtIT1VSLCAzLCAzICogZHVyYXRpb25Ib3VyXSxcblx0W0hPVVIsIDYsIDYgKiBkdXJhdGlvbkhvdXJdLFxuXHRbSE9VUiwgMTIsIDEyICogZHVyYXRpb25Ib3VyXSxcblx0W0RBWSwgMSwgZHVyYXRpb25EYXldLFxuXHRbREFZLCA3LCBkdXJhdGlvbldlZWtdLFxuXHRbTU9OVEgsIDEsIGR1cmF0aW9uTW9udGhdLFxuXHRbTU9OVEgsIDMsIDMgKiBkdXJhdGlvbk1vbnRoXSxcblx0W1lFQVIsIDEsIGR1cmF0aW9uWWVhcl0sXG5dIGFzIGNvbnN0O1xuXG5sZXQgZm9ybWF0TWFwID0ge1xuXHRbTUlMTElTRUNPTkRdOiBkMy50aW1lRm9ybWF0KFwiJUxcIiksXG5cdFtTRUNPTkRdOiBkMy50aW1lRm9ybWF0KFwiJVMgc1wiKSxcblx0W01JTlVURV06IGQzLnRpbWVGb3JtYXQoXCIlSDolTVwiKSxcblx0W0hPVVJdOiBkMy50aW1lRm9ybWF0KFwiJUg6JU1cIiksXG5cdFtEQVldOiBkMy50aW1lRm9ybWF0KFwiJWIgJWRcIiksXG5cdFtNT05USF06IGQzLnRpbWVGb3JtYXQoXCIlYiAlWVwiKSxcblx0W1lFQVJdOiBkMy50aW1lRm9ybWF0KFwiJVlcIiksXG59O1xuXG4vKipcbiAqIEBwYXJhbSB0eXBlIC0gdGhlIHR5cGUgb2YgZGF0YSBhcyBhIEphdmFTY3JpcHQgcHJpbWl0aXZlXG4gKiBAcGFyYW0gYmlucyAtIHRoZSBiaW4gZGF0YSB0aGF0IG5lZWRzIHRvIGJlIGZvcm1hdHRlZFxuICovXG5leHBvcnQgZnVuY3Rpb24gdGlja0Zvcm1hdHRlckZvckJpbnMoXG5cdHR5cGU6IFwiZGF0ZVwiIHwgXCJudW1iZXJcIixcblx0YmluczogQXJyYXk8QmluPixcbik6IChkOiBkMy5OdW1iZXJWYWx1ZSkgPT4gc3RyaW5nIHtcblx0aWYgKHR5cGUgPT09IFwibnVtYmVyXCIpIHtcblx0XHRyZXR1cm4gZDMuZm9ybWF0KFwifnNcIik7XG5cdH1cblx0bGV0IGludGVydmFsID0gdGltZUludGVydmFsKFxuXHRcdGJpbnNbMF0ueDAsXG5cdFx0Ymluc1tiaW5zLmxlbmd0aCAtIDFdLngxLFxuXHRcdGJpbnMubGVuZ3RoLFxuXHQpO1xuXHQvLyBAdHMtZXhwZWN0LWVycm9yIC0gZDMgb2sgd2l0aCBkYXRlIC0+IHN0cmluZyBhcyBsb25nIGFzIGl0J3MgdXRjXG5cdHJldHVybiBmb3JtYXRNYXBbaW50ZXJ2YWwuaW50ZXJ2YWxdO1xufVxuXG4vLy8gYmluIHN0dWZmIGZyb20gdmdwbG90XG5cbi8qKlxuICogQHBhcmFtIG1pblxuICogQHBhcmFtIG1heFxuICogQHBhcmFtIHN0ZXBzXG4gKi9cbmZ1bmN0aW9uIHRpbWVJbnRlcnZhbChcblx0bWluOiBudW1iZXIsXG5cdG1heDogbnVtYmVyLFxuXHRzdGVwczogbnVtYmVyLFxuKToge1xuXHRpbnRlcnZhbDogdHlwZW9mIGludGVydmFsc1tudW1iZXJdWzBdIHwgdHlwZW9mIE1JTExJU0VDT05EO1xuXHRzdGVwOiBudW1iZXI7XG59IHtcblx0Y29uc3Qgc3BhbiA9IG1heCAtIG1pbjtcblx0Y29uc3QgdGFyZ2V0ID0gc3BhbiAvIHN0ZXBzO1xuXG5cdGxldCBpID0gMDtcblx0d2hpbGUgKGkgPCBpbnRlcnZhbHMubGVuZ3RoICYmIGludGVydmFsc1tpXVsyXSA8IHRhcmdldCkge1xuXHRcdGkrKztcblx0fVxuXG5cdGlmIChpID09PSBpbnRlcnZhbHMubGVuZ3RoKSB7XG5cdFx0cmV0dXJuIHsgaW50ZXJ2YWw6IFlFQVIsIHN0ZXA6IGJpblN0ZXAoc3Bhbiwgc3RlcHMpIH07XG5cdH1cblxuXHRpZiAoaSA+IDApIHtcblx0XHRsZXQgaW50ZXJ2YWwgPSBpbnRlcnZhbHNbXG5cdFx0XHR0YXJnZXQgLyBpbnRlcnZhbHNbaSAtIDFdWzJdIDwgaW50ZXJ2YWxzW2ldWzJdIC8gdGFyZ2V0ID8gaSAtIDEgOiBpXG5cdFx0XTtcblx0XHRyZXR1cm4geyBpbnRlcnZhbDogaW50ZXJ2YWxbMF0sIHN0ZXA6IGludGVydmFsWzFdIH07XG5cdH1cblxuXHRyZXR1cm4geyBpbnRlcnZhbDogTUlMTElTRUNPTkQsIHN0ZXA6IGJpblN0ZXAoc3Bhbiwgc3RlcHMsIDEpIH07XG59XG5cbi8qKlxuICogQHBhcmFtIHtudW1iZXJ9IHNwYW5cbiAqIEBwYXJhbSB7bnVtYmVyfSBzdGVwc1xuICogQHBhcmFtIHtudW1iZXJ9IFttaW5zdGVwXVxuICogQHBhcmFtIHtudW1iZXJ9IFtsb2diXVxuICovXG5mdW5jdGlvbiBiaW5TdGVwKFxuXHRzcGFuOiBudW1iZXIsXG5cdHN0ZXBzOiBudW1iZXIsXG5cdG1pbnN0ZXA6IG51bWJlciA9IDAsXG5cdGxvZ2I6IG51bWJlciA9IE1hdGguTE4xMCxcbikge1xuXHRsZXQgdjtcblxuXHRjb25zdCBsZXZlbCA9IE1hdGguY2VpbChNYXRoLmxvZyhzdGVwcykgLyBsb2diKTtcblx0bGV0IHN0ZXAgPSBNYXRoLm1heChcblx0XHRtaW5zdGVwLFxuXHRcdE1hdGgucG93KDEwLCBNYXRoLnJvdW5kKE1hdGgubG9nKHNwYW4pIC8gbG9nYikgLSBsZXZlbCksXG5cdCk7XG5cblx0Ly8gaW5jcmVhc2Ugc3RlcCBzaXplIGlmIHRvbyBtYW55IGJpbnNcblx0d2hpbGUgKE1hdGguY2VpbChzcGFuIC8gc3RlcCkgPiBzdGVwcykgc3RlcCAqPSAxMDtcblxuXHQvLyBkZWNyZWFzZSBzdGVwIHNpemUgaWYgYWxsb3dlZFxuXHRjb25zdCBkaXYgPSBbNSwgMl07XG5cdGZvciAobGV0IGkgPSAwLCBuID0gZGl2Lmxlbmd0aDsgaSA8IG47ICsraSkge1xuXHRcdHYgPSBzdGVwIC8gZGl2W2ldO1xuXHRcdGlmICh2ID49IG1pbnN0ZXAgJiYgc3BhbiAvIHYgPD0gc3RlcHMpIHN0ZXAgPSB2O1xuXHR9XG5cblx0cmV0dXJuIHN0ZXA7XG59XG4iLCAiaW1wb3J0ICogYXMgZDMgZnJvbSBcIi4uL2RlcHMvZDMudHNcIjtcbmltcG9ydCB7IGFzc2VydCB9IGZyb20gXCIuLi91dGlscy9hc3NlcnQudHNcIjtcbmltcG9ydCB7IHRpY2tGb3JtYXR0ZXJGb3JCaW5zIH0gZnJvbSBcIi4vdGljay1mb3JtYXR0ZXItZm9yLWJpbnMudHNcIjtcbmltcG9ydCB0eXBlIHsgQmluLCBTY2FsZSB9IGZyb20gXCIuLi90eXBlcy50c1wiO1xuXG5pbnRlcmZhY2UgSGlzdG9ncmFtT3B0aW9ucyB7XG5cdHR5cGU6IFwibnVtYmVyXCIgfCBcImRhdGVcIjtcblx0d2lkdGg/OiBudW1iZXI7XG5cdGhlaWdodD86IG51bWJlcjtcblx0bWFyZ2luVG9wPzogbnVtYmVyO1xuXHRtYXJnaW5SaWdodD86IG51bWJlcjtcblx0bWFyZ2luQm90dG9tPzogbnVtYmVyO1xuXHRtYXJnaW5MZWZ0PzogbnVtYmVyO1xuXHRudWxsQ291bnQ/OiBudW1iZXI7XG5cdGZpbGxDb2xvcj86IHN0cmluZztcblx0bnVsbEZpbGxDb2xvcj86IHN0cmluZztcblx0YmFja2dyb3VuZEJhckNvbG9yPzogc3RyaW5nO1xufVxuXG4vKipcbiAqIFJldHVybnMgYW4gU1ZHIGVsZW1lbnQuXG4gKlxuICogQHBhcmFtIGJpbnMgLSB0aGUgXCJjb21wbGV0ZVwiLCBvciB0b3RhbCBiaW5zIGZvciB0aGUgY3Jvc3NmaWx0ZXIgaGlzdG9ncmFtLlxuICogQHBhcmFtIG9wdGlvbnMgLSBBIGJhZyBvZiBvcHRpb25zIHRvIGNvbmZpZ3VyZSB0aGUgaGlzdG9ncmFtXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBDcm9zc2ZpbHRlckhpc3RvZ3JhbVBsb3QoXG5cdGJpbnM6IEFycmF5PEJpbj4sXG5cdHtcblx0XHR0eXBlID0gXCJudW1iZXJcIixcblx0XHR3aWR0aCA9IDEyNSxcblx0XHRoZWlnaHQgPSA0MCxcblx0XHRtYXJnaW5Ub3AgPSAwLFxuXHRcdG1hcmdpblJpZ2h0ID0gMixcblx0XHRtYXJnaW5Cb3R0b20gPSAxMixcblx0XHRtYXJnaW5MZWZ0ID0gMixcblx0XHRudWxsQ291bnQgPSAwLFxuXHRcdGZpbGxDb2xvciA9IFwidmFyKC0tcHJpbWFyeSlcIixcblx0XHRudWxsRmlsbENvbG9yID0gXCJ2YXIoLS1zZWNvbmRhcnkpXCIsXG5cdFx0YmFja2dyb3VuZEJhckNvbG9yID0gXCJ2YXIoLS1tb29uLWdyYXkpXCIsXG5cdH06IEhpc3RvZ3JhbU9wdGlvbnMsXG4pOiBTVkdTVkdFbGVtZW50ICYge1xuXHRzY2FsZTogKHR5cGU6IHN0cmluZykgPT4gU2NhbGU8bnVtYmVyLCBudW1iZXI+O1xuXHR1cGRhdGUoYmluczogQXJyYXk8QmluPiwgb3B0czogeyBudWxsQ291bnQ6IG51bWJlciB9KTogdm9pZDtcbn0ge1xuXHRsZXQgbnVsbEJpbldpZHRoID0gbnVsbENvdW50ID09PSAwID8gMCA6IDU7XG5cdGxldCBzcGFjaW5nID0gbnVsbEJpbldpZHRoID8gNCA6IDA7XG5cdGxldCBleHRlbnQgPSAvKiogQHR5cGUge2NvbnN0fSAqLyAoW1xuXHRcdE1hdGgubWluKC4uLmJpbnMubWFwKChkKSA9PiBkLngwKSksXG5cdFx0TWF0aC5tYXgoLi4uYmlucy5tYXAoKGQpID0+IGQueDEpKSxcblx0XSk7XG5cdGxldCB4ID0gdHlwZSA9PT0gXCJkYXRlXCIgPyBkMy5zY2FsZVV0YygpIDogZDMuc2NhbGVMaW5lYXIoKTtcblx0eFxuXHRcdC5kb21haW4oZXh0ZW50KVxuXHRcdC8vIEB0cy1leHBlY3QtZXJyb3IgLSByYW5nZSBpcyBvayB3aXRoIG51bWJlciBmb3IgYm90aCBudW1iZXIgYW5kIHRpbWVcblx0XHQucmFuZ2UoW21hcmdpbkxlZnQgKyBudWxsQmluV2lkdGggKyBzcGFjaW5nLCB3aWR0aCAtIG1hcmdpblJpZ2h0XSlcblx0XHQubmljZSgpO1xuXG5cdGxldCB5ID0gZDMuc2NhbGVMaW5lYXIoKVxuXHRcdC5kb21haW4oWzAsIE1hdGgubWF4KG51bGxDb3VudCwgLi4uYmlucy5tYXAoKGQpID0+IGQubGVuZ3RoKSldKVxuXHRcdC5yYW5nZShbaGVpZ2h0IC0gbWFyZ2luQm90dG9tLCBtYXJnaW5Ub3BdKTtcblxuXHRsZXQgc3ZnID0gZDMuY3JlYXRlKFwic3ZnXCIpXG5cdFx0LmF0dHIoXCJ3aWR0aFwiLCB3aWR0aClcblx0XHQuYXR0cihcImhlaWdodFwiLCBoZWlnaHQpXG5cdFx0LmF0dHIoXCJ2aWV3Qm94XCIsIFswLCAwLCB3aWR0aCwgaGVpZ2h0XSlcblx0XHQuYXR0cihcInN0eWxlXCIsIFwibWF4LXdpZHRoOiAxMDAlOyBoZWlnaHQ6IGF1dG87IG92ZXJmbG93OiB2aXNpYmxlO1wiKTtcblxuXHR7XG5cdFx0Ly8gYmFja2dyb3VuZCBiYXJzIHdpdGggdGhlIFwidG90YWxcIiBiaW5zXG5cdFx0c3ZnLmFwcGVuZChcImdcIilcblx0XHRcdC5hdHRyKFwiZmlsbFwiLCBiYWNrZ3JvdW5kQmFyQ29sb3IpXG5cdFx0XHQuc2VsZWN0QWxsKFwicmVjdFwiKVxuXHRcdFx0LmRhdGEoYmlucylcblx0XHRcdC5qb2luKFwicmVjdFwiKVxuXHRcdFx0LmF0dHIoXCJ4XCIsIChkKSA9PiB4KGQueDApICsgMS41KVxuXHRcdFx0LmF0dHIoXCJ3aWR0aFwiLCAoZCkgPT4geChkLngxKSAtIHgoZC54MCkgLSAxLjUpXG5cdFx0XHQuYXR0cihcInlcIiwgKGQpID0+IHkoZC5sZW5ndGgpKVxuXHRcdFx0LmF0dHIoXCJoZWlnaHRcIiwgKGQpID0+IHkoMCkgLSB5KGQubGVuZ3RoKSk7XG5cdH1cblxuXHQvLyBGb3JlZ3JvdW5kIGJhcnMgZm9yIHRoZSBjdXJyZW50IHN1YnNldFxuXHRsZXQgZm9yZWdyb3VuZEJhckdyb3VwID0gc3ZnXG5cdFx0LmFwcGVuZChcImdcIilcblx0XHQuYXR0cihcImZpbGxcIiwgZmlsbENvbG9yKTtcblxuXHRzdmdcblx0XHQuYXBwZW5kKFwiZ1wiKVxuXHRcdC5hdHRyKFwidHJhbnNmb3JtXCIsIGB0cmFuc2xhdGUoMCwke2hlaWdodCAtIG1hcmdpbkJvdHRvbX0pYClcblx0XHQuY2FsbChcblx0XHRcdGQzXG5cdFx0XHRcdC5heGlzQm90dG9tKHgpXG5cdFx0XHRcdC50aWNrVmFsdWVzKHguZG9tYWluKCkpXG5cdFx0XHRcdC50aWNrRm9ybWF0KHRpY2tGb3JtYXR0ZXJGb3JCaW5zKHR5cGUsIGJpbnMpKVxuXHRcdFx0XHQudGlja1NpemUoMi41KSxcblx0XHQpXG5cdFx0LmNhbGwoKGcpID0+IHtcblx0XHRcdGcuc2VsZWN0KFwiLmRvbWFpblwiKS5yZW1vdmUoKTtcblx0XHRcdGcuYXR0cihcImNsYXNzXCIsIFwiZ3JheVwiKTtcblx0XHRcdGcuc2VsZWN0QWxsKFwiLnRpY2sgdGV4dFwiKVxuXHRcdFx0XHQuYXR0cihcInRleHQtYW5jaG9yXCIsIChfLCBpKSA9PiBpID09PSAwID8gXCJzdGFydFwiIDogXCJlbmRcIilcblx0XHRcdFx0LmF0dHIoXCJkeFwiLCAoXywgaSkgPT4gaSA9PT0gMCA/IFwiLTAuMjVlbVwiIDogXCIwLjI1ZW1cIik7XG5cdFx0fSk7XG5cblx0LyoqIEB0eXBlIHt0eXBlb2YgZm9yZWdyb3VuZEJhckdyb3VwIHwgdW5kZWZpbmVkfSAqL1xuXHRsZXQgZm9yZWdyb3VuZE51bGxHcm91cDogdHlwZW9mIGZvcmVncm91bmRCYXJHcm91cCB8IHVuZGVmaW5lZCA9IHVuZGVmaW5lZDtcblx0aWYgKG51bGxDb3VudCA+IDApIHtcblx0XHRsZXQgeG51bGwgPSBkMy5zY2FsZUxpbmVhcigpXG5cdFx0XHQucmFuZ2UoW21hcmdpbkxlZnQsIG1hcmdpbkxlZnQgKyBudWxsQmluV2lkdGhdKTtcblxuXHRcdC8vIGJhY2tncm91bmQgYmFyIGZvciB0aGUgbnVsbCBiaW5cblx0XHRzdmcuYXBwZW5kKFwiZ1wiKVxuXHRcdFx0LmF0dHIoXCJmaWxsXCIsIGJhY2tncm91bmRCYXJDb2xvcilcblx0XHRcdC5hcHBlbmQoXCJyZWN0XCIpXG5cdFx0XHQuYXR0cihcInhcIiwgeG51bGwoMCkpXG5cdFx0XHQuYXR0cihcIndpZHRoXCIsIHhudWxsKDEpIC0geG51bGwoMCkpXG5cdFx0XHQuYXR0cihcInlcIiwgeShudWxsQ291bnQpKVxuXHRcdFx0LmF0dHIoXCJoZWlnaHRcIiwgeSgwKSAtIHkobnVsbENvdW50KSk7XG5cblx0XHRmb3JlZ3JvdW5kTnVsbEdyb3VwID0gc3ZnXG5cdFx0XHQuYXBwZW5kKFwiZ1wiKVxuXHRcdFx0LmF0dHIoXCJmaWxsXCIsIG51bGxGaWxsQ29sb3IpXG5cdFx0XHQuYXR0cihcImNvbG9yXCIsIG51bGxGaWxsQ29sb3IpO1xuXG5cdFx0Zm9yZWdyb3VuZE51bGxHcm91cC5hcHBlbmQoXCJyZWN0XCIpXG5cdFx0XHQuYXR0cihcInhcIiwgeG51bGwoMCkpXG5cdFx0XHQuYXR0cihcIndpZHRoXCIsIHhudWxsKDEpIC0geG51bGwoMCkpO1xuXG5cdFx0Ly8gQXBwZW5kIHRoZSB4LWF4aXMgYW5kIGFkZCBhIG51bGwgdGlja1xuXHRcdGxldCBheGlzR3JvdXAgPSBmb3JlZ3JvdW5kTnVsbEdyb3VwLmFwcGVuZChcImdcIilcblx0XHRcdC5hdHRyKFwidHJhbnNmb3JtXCIsIGB0cmFuc2xhdGUoMCwke2hlaWdodCAtIG1hcmdpbkJvdHRvbX0pYClcblx0XHRcdC5hcHBlbmQoXCJnXCIpXG5cdFx0XHQuYXR0cihcInRyYW5zZm9ybVwiLCBgdHJhbnNsYXRlKCR7eG51bGwoMC41KX0sIDApYClcblx0XHRcdC5hdHRyKFwiY2xhc3NcIiwgXCJ0aWNrXCIpO1xuXG5cdFx0YXhpc0dyb3VwXG5cdFx0XHQuYXBwZW5kKFwibGluZVwiKVxuXHRcdFx0LmF0dHIoXCJzdHJva2VcIiwgXCJjdXJyZW50Q29sb3JcIilcblx0XHRcdC5hdHRyKFwieTJcIiwgMi41KTtcblxuXHRcdGF4aXNHcm91cFxuXHRcdFx0LmFwcGVuZChcInRleHRcIilcblx0XHRcdC5hdHRyKFwiZmlsbFwiLCBcImN1cnJlbnRDb2xvclwiKVxuXHRcdFx0LmF0dHIoXCJ5XCIsIDQuNSlcblx0XHRcdC5hdHRyKFwiZHlcIiwgXCIwLjcxZW1cIilcblx0XHRcdC5hdHRyKFwidGV4dC1hbmNob3JcIiwgXCJtaWRkbGVcIilcblx0XHRcdC50ZXh0KFwiXHUyMjA1XCIpXG5cdFx0XHQuYXR0cihcImZvbnQtc2l6ZVwiLCBcIjAuOWVtXCIpXG5cdFx0XHQuYXR0cihcImZvbnQtZmFtaWx5XCIsIFwidmFyKC0tc2Fucy1zZXJpZilcIilcblx0XHRcdC5hdHRyKFwiZm9udC13ZWlnaHRcIiwgXCJub3JtYWxcIik7XG5cdH1cblxuXHQvLyBBcHBseSBzdHlsZXMgZm9yIGFsbCBheGlzIHRpY2tzXG5cdHN2Zy5zZWxlY3RBbGwoXCIudGlja1wiKVxuXHRcdC5hdHRyKFwiZm9udC1mYW1pbHlcIiwgXCJ2YXIoLS1zYW5zLXNlcmlmKVwiKVxuXHRcdC5hdHRyKFwiZm9udC13ZWlnaHRcIiwgXCJub3JtYWxcIik7XG5cblx0LyoqXG5cdCAqIEBwYXJhbSB7QXJyYXk8QmluPn0gYmluc1xuXHQgKiBAcGFyYW0ge251bWJlcn0gbnVsbENvdW50XG5cdCAqL1xuXHRmdW5jdGlvbiByZW5kZXIoYmluczogQXJyYXk8QmluPiwgbnVsbENvdW50OiBudW1iZXIpIHtcblx0XHRmb3JlZ3JvdW5kQmFyR3JvdXBcblx0XHRcdC5zZWxlY3RBbGwoXCJyZWN0XCIpXG5cdFx0XHQuZGF0YShiaW5zKVxuXHRcdFx0LmpvaW4oXCJyZWN0XCIpXG5cdFx0XHQuYXR0cihcInhcIiwgKGQpID0+IHgoZC54MCkgKyAxLjUpXG5cdFx0XHQuYXR0cihcIndpZHRoXCIsIChkKSA9PiB4KGQueDEpIC0geChkLngwKSAtIDEuNSlcblx0XHRcdC5hdHRyKFwieVwiLCAoZCkgPT4geShkLmxlbmd0aCkpXG5cdFx0XHQuYXR0cihcImhlaWdodFwiLCAoZCkgPT4geSgwKSAtIHkoZC5sZW5ndGgpKTtcblx0XHRmb3JlZ3JvdW5kTnVsbEdyb3VwXG5cdFx0XHQ/LnNlbGVjdChcInJlY3RcIilcblx0XHRcdC5hdHRyKFwieVwiLCB5KG51bGxDb3VudCkpXG5cdFx0XHQuYXR0cihcImhlaWdodFwiLCB5KDApIC0geShudWxsQ291bnQpKTtcblx0fVxuXG5cdGxldCBzY2FsZXMgPSB7XG5cdFx0eDogT2JqZWN0LmFzc2lnbih4LCB7XG5cdFx0XHR0eXBlOiBcImxpbmVhclwiLFxuXHRcdFx0ZG9tYWluOiB4LmRvbWFpbigpLFxuXHRcdFx0cmFuZ2U6IHgucmFuZ2UoKSxcblx0XHR9KSxcblx0XHR5OiBPYmplY3QuYXNzaWduKHksIHtcblx0XHRcdHR5cGU6IFwibGluZWFyXCIsXG5cdFx0XHRkb21haW46IHkuZG9tYWluKCksXG5cdFx0XHRyYW5nZTogeS5yYW5nZSgpLFxuXHRcdH0pLFxuXHR9O1xuXHRsZXQgbm9kZSA9IHN2Zy5ub2RlKCk7XG5cdGFzc2VydChub2RlLCBcIkluZmFsbGFibGVcIik7XG5cblx0cmVuZGVyKGJpbnMsIG51bGxDb3VudCk7XG5cdHJldHVybiBPYmplY3QuYXNzaWduKG5vZGUsIHtcblx0XHQvKiogQHBhcmFtIHtzdHJpbmd9IHR5cGUgKi9cblx0XHRzY2FsZSh0eXBlOiBzdHJpbmcpIHtcblx0XHRcdC8vIEB0cy1leHBlY3QtZXJyb3IgLSBzY2FsZXMgaXMgbm90IGRlZmluZWRcblx0XHRcdGxldCBzY2FsZSA9IHNjYWxlc1t0eXBlXTtcblx0XHRcdGFzc2VydChzY2FsZSwgXCJJbnZhbGlkIHNjYWxlIHR5cGVcIik7XG5cdFx0XHRyZXR1cm4gc2NhbGU7XG5cdFx0fSxcblx0XHQvKipcblx0XHQgKiBAcGFyYW0ge0FycmF5PEJpbj59IGJpbnNcblx0XHQgKiBAcGFyYW0ge3sgbnVsbENvdW50OiBudW1iZXIgfX0gb3B0c1xuXHRcdCAqL1xuXHRcdHVwZGF0ZShiaW5zOiBBcnJheTxCaW4+LCB7IG51bGxDb3VudCB9OiB7IG51bGxDb3VudDogbnVtYmVyIH0pIHtcblx0XHRcdHJlbmRlcihiaW5zLCBudWxsQ291bnQpO1xuXHRcdH0sXG5cdFx0cmVzZXQoKSB7XG5cdFx0XHRyZW5kZXIoYmlucywgbnVsbENvdW50KTtcblx0XHR9LFxuXHR9KTtcbn1cbiIsICIvLyBAZGVuby10eXBlcz1cIi4uL2RlcHMvbW9zYWljLWNvcmUuZC50c1wiO1xuaW1wb3J0IHsgY2xhdXNlUG9pbnQsIE1vc2FpY0NsaWVudCwgdHlwZSBTZWxlY3Rpb24gfSBmcm9tIFwiQHV3ZGF0YS9tb3NhaWMtY29yZVwiO1xuLy8gQGRlbm8tdHlwZXM9XCIuLi9kZXBzL21vc2FpYy1zcWwuZC50c1wiO1xuaW1wb3J0IHtcblx0Y29sdW1uLFxuXHRjb3VudCxcblx0UXVlcnksXG5cdHNxbCxcblx0U1FMRXhwcmVzc2lvbixcblx0c3VtLFxufSBmcm9tIFwiQHV3ZGF0YS9tb3NhaWMtc3FsXCI7XG5pbXBvcnQgdHlwZSAqIGFzIGFycm93IGZyb20gXCJhcGFjaGUtYXJyb3dcIjtcbmltcG9ydCB7IGVmZmVjdCB9IGZyb20gXCJAcHJlYWN0L3NpZ25hbHMtY29yZVwiO1xuXG5pbXBvcnQgeyBWYWx1ZUNvdW50c1Bsb3QgfSBmcm9tIFwiLi4vdXRpbHMvVmFsdWVDb3VudHNQbG90LnRzXCI7XG5pbXBvcnQgeyBhc3NlcnQgfSBmcm9tIFwiLi4vdXRpbHMvYXNzZXJ0LnRzXCI7XG5cbmludGVyZmFjZSBVbmlxdWVWYWx1ZXNPcHRpb25zIHtcblx0LyoqIFRoZSB0YWJsZSB0byBxdWVyeS4gKi9cblx0dGFibGU6IHN0cmluZztcblx0LyoqIFRoZSBjb2x1bW4gdG8gdXNlIGZvciB0aGUgaGlzdG9ncmFtLiAqL1xuXHRjb2x1bW46IHN0cmluZztcblx0LyoqIEEgbW9zYWljIHNlbGVjdGlvbiB0byBmaWx0ZXIgdGhlIGRhdGEuICovXG5cdGZpbHRlckJ5OiBTZWxlY3Rpb247XG59XG5cbnR5cGUgQ291bnRUYWJsZSA9IGFycm93LlRhYmxlPHsga2V5OiBhcnJvdy5VdGY4OyB0b3RhbDogYXJyb3cuSW50IH0+O1xuXG5leHBvcnQgY2xhc3MgVmFsdWVDb3VudHMgZXh0ZW5kcyBNb3NhaWNDbGllbnQge1xuXHQjdGFibGU6IHN0cmluZztcblx0I2NvbHVtbjogc3RyaW5nO1xuXHQjZWw6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcblx0I3Bsb3Q6IFJldHVyblR5cGU8dHlwZW9mIFZhbHVlQ291bnRzUGxvdD4gfCB1bmRlZmluZWQ7XG5cblx0Y29uc3RydWN0b3Iob3B0aW9uczogVW5pcXVlVmFsdWVzT3B0aW9ucykge1xuXHRcdHN1cGVyKG9wdGlvbnMuZmlsdGVyQnkpO1xuXHRcdHRoaXMuI3RhYmxlID0gb3B0aW9ucy50YWJsZTtcblx0XHR0aGlzLiNjb2x1bW4gPSBvcHRpb25zLmNvbHVtbjtcblxuXHRcdC8vIEZJWE1FOiBUaGVyZSBpcyBzb21lIGlzc3VlIHdpdGggdGhlIG1vc2FpYyBjbGllbnQgb3IgdGhlIHF1ZXJ5IHdlXG5cdFx0Ly8gYXJlIHVzaW5nIGhlcmUuIFVwZGF0ZXMgdG8gdGhlIFNlbGVjdGlvbiAoYGZpbHRlckJ5YCkgc2VlbSB0byBiZVxuXHRcdC8vIG1pc3NlZCBieSB0aGUgY29vcmRpbmF0b3IsIGFuZCBxdWVyeS9xdWVyeVJlc3VsdCBhcmUgbm90IGNhbGxlZFxuXHRcdC8vIGJ5IHRoZSBjb29yZGluYXRvciB3aGVuIHRoZSBmaWx0ZXJCeSBpcyB1cGRhdGVkLlxuXHRcdC8vXG5cdFx0Ly8gSGVyZSB3ZSBtYW51YWxseSBsaXN0ZW4gZm9yIHRoZSBjaGFuZ2VzIHRvIGZpbHRlckJ5IGFuZCB1cGRhdGUgdGhpc1xuXHRcdC8vIGNsaWVudCBpbnRlcm5hbGx5LiBJdCBfc2hvdWxkXyBnbyB0aHJvdWdoIHRoZSBjb29yZGluYXRvci5cblx0XHRvcHRpb25zLmZpbHRlckJ5LmFkZEV2ZW50TGlzdGVuZXIoXCJ2YWx1ZVwiLCBhc3luYyAoKSA9PiB7XG5cdFx0XHRsZXQgZmlsdGVycyA9IG9wdGlvbnMuZmlsdGVyQnkucHJlZGljYXRlKCk7XG5cdFx0XHRsZXQgcXVlcnkgPSB0aGlzLnF1ZXJ5KGZpbHRlcnMpO1xuXHRcdFx0aWYgKHRoaXMuI3Bsb3QpIHtcblx0XHRcdFx0bGV0IGRhdGEgPSBhd2FpdCB0aGlzLmNvb3JkaW5hdG9yLnF1ZXJ5KHF1ZXJ5KTtcblx0XHRcdFx0dGhpcy4jcGxvdC5kYXRhLnZhbHVlID0gZGF0YTtcblx0XHRcdH1cblx0XHR9KTtcblx0fVxuXG5cdHF1ZXJ5KGZpbHRlcjogQXJyYXk8U1FMRXhwcmVzc2lvbj4gPSBbXSk6IFF1ZXJ5IHtcblx0XHRsZXQgY291bnRzID0gUXVlcnlcblx0XHRcdC5mcm9tKHsgc291cmNlOiB0aGlzLiN0YWJsZSB9KVxuXHRcdFx0LnNlbGVjdCh7XG5cdFx0XHRcdHZhbHVlOiBzcWxgQ0FTRVxuXHRcdFx0XHRcdFdIRU4gJHtjb2x1bW4odGhpcy4jY29sdW1uKX0gSVMgTlVMTCBUSEVOICdfX3F1YWtfbnVsbF9fJ1xuXHRcdFx0XHRcdEVMU0UgJHtjb2x1bW4odGhpcy4jY29sdW1uKX1cblx0XHRcdFx0RU5EYCxcblx0XHRcdFx0Y291bnQ6IGNvdW50KCksXG5cdFx0XHR9KVxuXHRcdFx0Lmdyb3VwYnkoXCJ2YWx1ZVwiKVxuXHRcdFx0LndoZXJlKGZpbHRlcik7XG5cdFx0cmV0dXJuIFF1ZXJ5XG5cdFx0XHQud2l0aCh7IGNvdW50cyB9KVxuXHRcdFx0LnNlbGVjdChcblx0XHRcdFx0e1xuXHRcdFx0XHRcdGtleTogc3FsYENBU0Vcblx0XHRcdFx0XHRcdFdIRU4gXCJjb3VudFwiID0gMSBBTkQgXCJ2YWx1ZVwiICE9ICdfX3F1YWtfbnVsbF9fJyBUSEVOICdfX3F1YWtfdW5pcXVlX18nXG5cdFx0XHRcdFx0XHRFTFNFIFwidmFsdWVcIlxuXHRcdFx0XHRcdEVORGAsXG5cdFx0XHRcdFx0dG90YWw6IHN1bShcImNvdW50XCIpLFxuXHRcdFx0XHR9LFxuXHRcdFx0KVxuXHRcdFx0LmZyb20oXCJjb3VudHNcIilcblx0XHRcdC5ncm91cGJ5KFwia2V5XCIpO1xuXHR9XG5cblx0cXVlcnlSZXN1bHQoZGF0YTogQ291bnRUYWJsZSk6IHRoaXMge1xuXHRcdGlmICghdGhpcy4jcGxvdCkge1xuXHRcdFx0bGV0IHBsb3QgPSB0aGlzLiNwbG90ID0gVmFsdWVDb3VudHNQbG90KGRhdGEpO1xuXHRcdFx0dGhpcy4jZWwuYXBwZW5kQ2hpbGQocGxvdCk7XG5cdFx0XHRlZmZlY3QoKCkgPT4ge1xuXHRcdFx0XHRsZXQgY2xhdXNlID0gdGhpcy5jbGF1c2UocGxvdC5zZWxlY3RlZC52YWx1ZSk7XG5cdFx0XHRcdHRoaXMuZmlsdGVyQnkhLnVwZGF0ZShjbGF1c2UpO1xuXHRcdFx0fSk7XG5cdFx0fSBlbHNlIHtcblx0XHRcdHRoaXMuI3Bsb3QuZGF0YS52YWx1ZSA9IGRhdGE7XG5cdFx0fVxuXHRcdHJldHVybiB0aGlzO1xuXHR9XG5cblx0Y2xhdXNlPFQ+KHZhbHVlPzogVCkge1xuXHRcdGxldCB1cGRhdGUgPSB2YWx1ZSA9PT0gXCJfX3F1YWtfbnVsbF9fXCIgPyBudWxsIDogdmFsdWU7XG5cdFx0cmV0dXJuIGNsYXVzZVBvaW50KHRoaXMuI2NvbHVtbiwgdXBkYXRlLCB7XG5cdFx0XHRzb3VyY2U6IHRoaXMsXG5cdFx0fSk7XG5cdH1cblxuXHRyZXNldCgpIHtcblx0XHRhc3NlcnQodGhpcy4jcGxvdCwgXCJWYWx1ZUNvdW50cyBwbG90IG5vdCBpbml0aWFsaXplZFwiKTtcblx0XHR0aGlzLiNwbG90LnNlbGVjdGVkLnZhbHVlID0gdW5kZWZpbmVkO1xuXHR9XG5cblx0Z2V0IHBsb3QoKSB7XG5cdFx0cmV0dXJuIHtcblx0XHRcdG5vZGU6ICgpID0+IHRoaXMuI2VsLFxuXHRcdH07XG5cdH1cbn1cbiIsICJpbXBvcnQgeyBlZmZlY3QsIHNpZ25hbCB9IGZyb20gXCJAcHJlYWN0L3NpZ25hbHMtY29yZVwiO1xuaW1wb3J0IHR5cGUgKiBhcyBhcnJvdyBmcm9tIFwiYXBhY2hlLWFycm93XCI7XG5pbXBvcnQgKiBhcyBkMyBmcm9tIFwiLi4vZGVwcy9kMy50c1wiO1xuaW1wb3J0IHsgYXNzZXJ0IH0gZnJvbSBcIi4vYXNzZXJ0LnRzXCI7XG5cbnR5cGUgQ291bnRUYWJsZURhdGEgPSBhcnJvdy5UYWJsZTx7XG5cdGtleTogYXJyb3cuVXRmODtcblx0dG90YWw6IGFycm93LkludDtcbn0+O1xuXG5pbnRlcmZhY2UgVmFsdWVDb3VudHNQbG90IHtcblx0d2lkdGg/OiBudW1iZXI7XG5cdGhlaWdodD86IG51bWJlcjtcblx0bWFyZ2luUmlnaHQ/OiBudW1iZXI7XG5cdG1hcmdpbkJvdHRvbT86IG51bWJlcjtcblx0bWFyZ2luTGVmdD86IG51bWJlcjtcblx0bnVsbENvdW50PzogbnVtYmVyO1xuXHRmaWxsQ29sb3I/OiBzdHJpbmc7XG5cdG51bGxGaWxsQ29sb3I/OiBzdHJpbmc7XG5cdGJhY2tncm91bmRCYXJDb2xvcj86IHN0cmluZztcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIFZhbHVlQ291bnRzUGxvdChcblx0ZGF0YTogQ291bnRUYWJsZURhdGEsXG5cdHtcblx0XHR3aWR0aCA9IDEyNSxcblx0XHRoZWlnaHQgPSAzMCxcblx0XHRtYXJnaW5Cb3R0b20gPSAxMixcblx0XHRtYXJnaW5SaWdodCA9IDIsXG5cdFx0bWFyZ2luTGVmdCA9IDIsXG5cdFx0ZmlsbENvbG9yID0gXCJ2YXIoLS1wcmltYXJ5KVwiLFxuXHRcdG51bGxGaWxsQ29sb3IgPSBcInZhcigtLXNlY29uZGFyeSlcIixcblx0XHRiYWNrZ3JvdW5kQmFyQ29sb3IgPSBcInJnYigyMjYsIDIyNiwgMjI2KVwiLFxuXHR9OiBWYWx1ZUNvdW50c1Bsb3QgPSB7fSxcbikge1xuXHRsZXQgcm9vdCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdHJvb3Quc3R5bGUucG9zaXRpb24gPSBcInJlbGF0aXZlXCI7XG5cblx0bGV0IGNvbnRhaW5lciA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdE9iamVjdC5hc3NpZ24oY29udGFpbmVyLnN0eWxlLCB7XG5cdFx0d2lkdGg6IGAke3dpZHRofXB4YCxcblx0XHRoZWlnaHQ6IGAke2hlaWdodH1weGAsXG5cdFx0ZGlzcGxheTogXCJmbGV4XCIsXG5cdFx0Ym9yZGVyUmFkaXVzOiBcIjVweFwiLFxuXHRcdG92ZXJmbG93OiBcImhpZGRlblwiLFxuXHR9KTtcblxuXHRsZXQgYmFycyA9IGNyZWF0ZUJhcnMoZGF0YSwge1xuXHRcdHdpZHRoLFxuXHRcdGhlaWdodCxcblx0XHRtYXJnaW5SaWdodCxcblx0XHRtYXJnaW5MZWZ0LFxuXHRcdGZpbGxDb2xvcixcblx0XHRudWxsRmlsbENvbG9yLFxuXHRcdGJhY2tncm91bmRCYXJDb2xvcixcblx0fSk7XG5cblx0Zm9yIChsZXQgYmFyIG9mIGJhcnMuZWxlbWVudHMpIHtcblx0XHRjb250YWluZXIuYXBwZW5kQ2hpbGQoYmFyKTtcblx0fVxuXG5cdGxldCB0ZXh0ID0gY3JlYXRlVGV4dE91dHB1dCgpO1xuXG5cdGxldCBob3ZlcmluZyA9IHNpZ25hbDxzdHJpbmcgfCB1bmRlZmluZWQ+KHVuZGVmaW5lZCk7XG5cdGxldCBzZWxlY3RlZCA9IHNpZ25hbDxzdHJpbmcgfCB1bmRlZmluZWQ+KHVuZGVmaW5lZCk7XG5cdGxldCBjb3VudHMgPSBzaWduYWw8Q291bnRUYWJsZURhdGE+KGRhdGEpO1xuXG5cdGxldCBoaXRBcmVhID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcblx0T2JqZWN0LmFzc2lnbihoaXRBcmVhLnN0eWxlLCB7XG5cdFx0cG9zaXRpb246IFwiYWJzb2x1dGVcIixcblx0XHR0b3A6IFwiMFwiLFxuXHRcdGxlZnQ6IFwiLTVweFwiLFxuXHRcdHdpZHRoOiBgJHt3aWR0aCArIDEwfXB4YCxcblx0XHRoZWlnaHQ6IGAke2hlaWdodCArIG1hcmdpbkJvdHRvbX1weGAsXG5cdFx0YmFja2dyb3VuZENvbG9yOiBcInJnYmEoMjU1LCAyNTUsIDI1NSwgMC4wMSlcIixcblx0XHRjdXJzb3I6IFwicG9pbnRlclwiLFxuXHR9KTtcblx0aGl0QXJlYS5hZGRFdmVudExpc3RlbmVyKFwibW91c2Vtb3ZlXCIsIChldmVudCkgPT4ge1xuXHRcdGhvdmVyaW5nLnZhbHVlID0gYmFycy5uZWFyZXN0WChldmVudCk7XG5cdH0pO1xuXHRoaXRBcmVhLmFkZEV2ZW50TGlzdGVuZXIoXCJtb3VzZW91dFwiLCAoKSA9PiB7XG5cdFx0aG92ZXJpbmcudmFsdWUgPSB1bmRlZmluZWQ7XG5cdH0pO1xuXHRoaXRBcmVhLmFkZEV2ZW50TGlzdGVuZXIoXCJtb3VzZWRvd25cIiwgKGV2ZW50KSA9PiB7XG5cdFx0bGV0IG5leHQgPSBiYXJzLm5lYXJlc3RYKGV2ZW50KTtcblx0XHRzZWxlY3RlZC52YWx1ZSA9IHNlbGVjdGVkLnZhbHVlID09PSBuZXh0ID8gdW5kZWZpbmVkIDogbmV4dDtcblx0fSk7XG5cblx0ZWZmZWN0KCgpID0+IHtcblx0XHR0ZXh0LnRleHRDb250ZW50ID0gYmFycy50ZXh0Rm9yKGhvdmVyaW5nLnZhbHVlID8/IHNlbGVjdGVkLnZhbHVlKTtcblx0XHRiYXJzLnJlbmRlcihjb3VudHMudmFsdWUsIGhvdmVyaW5nLnZhbHVlLCBzZWxlY3RlZC52YWx1ZSk7XG5cdH0pO1xuXG5cdHJvb3QuYXBwZW5kQ2hpbGQoY29udGFpbmVyKTtcblx0cm9vdC5hcHBlbmRDaGlsZCh0ZXh0KTtcblx0cm9vdC5hcHBlbmRDaGlsZChoaXRBcmVhKTtcblxuXHRyZXR1cm4gT2JqZWN0LmFzc2lnbihyb290LCB7IHNlbGVjdGVkLCBkYXRhOiBjb3VudHMgfSk7XG59XG5cbmZ1bmN0aW9uIGNyZWF0ZUJhcihvcHRzOiB7XG5cdHRpdGxlOiBzdHJpbmc7XG5cdGZpbGxDb2xvcjogc3RyaW5nO1xuXHR0ZXh0Q29sb3I6IHN0cmluZztcblx0aGVpZ2h0OiBudW1iZXI7XG5cdHdpZHRoOiBudW1iZXI7XG59KSB7XG5cdGxldCB7IHRpdGxlLCBmaWxsQ29sb3IsIHRleHRDb2xvciwgd2lkdGgsIGhlaWdodCB9ID0gb3B0cztcblx0bGV0IGJhciA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdGJhci50aXRsZSA9IHRpdGxlO1xuXHRPYmplY3QuYXNzaWduKGJhci5zdHlsZSwge1xuXHRcdGJhY2tncm91bmQ6IGNyZWF0ZVNwbGl0QmFyRmlsbCh7XG5cdFx0XHRjb2xvcjogZmlsbENvbG9yLFxuXHRcdFx0YmdDb2xvcjogXCJ2YXIoLS1tb29uLWdyYXkpXCIsXG5cdFx0XHRmcmFjOiA1MCxcblx0XHR9KSxcblx0XHR3aWR0aDogYCR7d2lkdGh9cHhgLFxuXHRcdGhlaWdodDogYCR7aGVpZ2h0fXB4YCxcblx0XHRib3JkZXJDb2xvcjogXCJ3aGl0ZVwiLFxuXHRcdGJvcmRlcldpZHRoOiBcIjBweCAxcHggMHB4IDBweFwiLFxuXHRcdGJvcmRlclN0eWxlOiBcInNvbGlkXCIsXG5cdFx0b3BhY2l0eTogMSxcblx0XHR0ZXh0QWxpZ246IFwiY2VudGVyXCIsXG5cdFx0cG9zaXRpb246IFwicmVsYXRpdmVcIixcblx0XHRkaXNwbGF5OiBcImZsZXhcIixcblx0XHRvdmVyZmxvdzogXCJoaWRkZW5cIixcblx0XHRhbGlnbkl0ZW1zOiBcImNlbnRlclwiLFxuXHRcdGZvbnRXZWlnaHQ6IDQwMCxcblx0XHRmb250RmFtaWx5OiBcInZhcigtLXNhbnMtc2VyaWYpXCIsXG5cdFx0Ym94U2l6aW5nOiBcImJvcmRlci1ib3hcIixcblx0fSk7XG5cdGxldCBzcGFuID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcInNwYW5cIik7XG5cdE9iamVjdC5hc3NpZ24oc3Bhbi5zdHlsZSwge1xuXHRcdG92ZXJmbG93OiBcImhpZGRlblwiLFxuXHRcdHdpZHRoOiBgY2FsYygxMDAlIC0gNHB4KWAsXG5cdFx0bGVmdDogXCIwcHhcIixcblx0XHRwb3NpdGlvbjogXCJhYnNvbHV0ZVwiLFxuXHRcdHBhZGRpbmc6IFwiMHB4IDJweFwiLFxuXHRcdGNvbG9yOiB0ZXh0Q29sb3IsXG5cdH0pO1xuXHRpZiAod2lkdGggPiAxMCkge1xuXHRcdHNwYW4udGV4dENvbnRlbnQgPSB0aXRsZTtcblx0fVxuXHRiYXIuYXBwZW5kQ2hpbGQoc3Bhbik7XG5cdHJldHVybiBiYXI7XG59XG5cbmZ1bmN0aW9uIHByZXBhcmVEYXRhKGRhdGE6IENvdW50VGFibGVEYXRhKSB7XG5cdGxldCBhcnI6IEFycmF5PHsga2V5OiBzdHJpbmc7IHRvdGFsOiBudW1iZXIgfT4gPSBkYXRhXG5cdFx0LnRvQXJyYXkoKVxuXHRcdC50b1NvcnRlZCgoYSwgYikgPT4gYi50b3RhbCAtIGEudG90YWwpO1xuXHRsZXQgdG90YWwgPSBhcnIucmVkdWNlKChhY2MsIGQpID0+IGFjYyArIGQudG90YWwsIDApO1xuXHRyZXR1cm4ge1xuXHRcdGJpbnM6IGFyci5maWx0ZXIoKGQpID0+XG5cdFx0XHRkLmtleSAhPT0gXCJfX3F1YWtfbnVsbF9fXCIgJiYgZC5rZXkgIT09IFwiX19xdWFrX3VuaXF1ZV9fXCJcblx0XHQpLFxuXHRcdG51bGxDb3VudDogYXJyLmZpbmQoKGQpID0+IGQua2V5ID09PSBcIl9fcXVha19udWxsX19cIik/LnRvdGFsID8/IDAsXG5cdFx0dW5pcXVlQ291bnQ6IGFyci5maW5kKChkKSA9PiBkLmtleSA9PT0gXCJfX3F1YWtfdW5pcXVlX19cIik/LnRvdGFsID8/IDAsXG5cdFx0dG90YWwsXG5cdH07XG59XG5cbnR5cGUgRW50cnkgPSB7IGtleTogc3RyaW5nOyB0b3RhbDogbnVtYmVyIH07XG5cbmZ1bmN0aW9uIGNyZWF0ZUJhcnMoZGF0YTogQ291bnRUYWJsZURhdGEsIG9wdHM6IHtcblx0d2lkdGg6IG51bWJlcjtcblx0aGVpZ2h0OiBudW1iZXI7XG5cdG1hcmdpblJpZ2h0OiBudW1iZXI7XG5cdG1hcmdpbkxlZnQ6IG51bWJlcjtcblx0ZmlsbENvbG9yOiBzdHJpbmc7XG5cdGJhY2tncm91bmRCYXJDb2xvcjogc3RyaW5nO1xuXHRudWxsRmlsbENvbG9yOiBzdHJpbmc7XG59KSB7XG5cdGxldCBzb3VyY2UgPSBwcmVwYXJlRGF0YShkYXRhKTtcblx0bGV0IHggPSBkMy5zY2FsZUxpbmVhcigpXG5cdFx0LmRvbWFpbihbMCwgc291cmNlLnRvdGFsXSlcblx0XHQucmFuZ2UoW29wdHMubWFyZ2luTGVmdCwgb3B0cy53aWR0aCAtIG9wdHMubWFyZ2luUmlnaHRdKTtcblxuXHQvLyBudW1iZXIgb2YgYmFycyB0byBzaG93IGJlZm9yZSB2aXJ0dWFsaXppbmdcblx0bGV0IHRocmVzaCA9IDIwO1xuXG5cdGxldCBiYXJzOiBBcnJheTxIVE1MRWxlbWVudCAmIHsgZGF0YTogRW50cnkgfT4gPSBbXTtcblx0Zm9yIChsZXQgZCBvZiBzb3VyY2UuYmlucy5zbGljZSgwLCB0aHJlc2gpKSB7XG5cdFx0bGV0IGJhciA9IGNyZWF0ZUJhcih7XG5cdFx0XHR0aXRsZTogZC5rZXksXG5cdFx0XHRmaWxsQ29sb3I6IG9wdHMuZmlsbENvbG9yLFxuXHRcdFx0dGV4dENvbG9yOiBcIndoaXRlXCIsXG5cdFx0XHR3aWR0aDogeChkLnRvdGFsKSxcblx0XHRcdGhlaWdodDogb3B0cy5oZWlnaHQsXG5cdFx0fSk7XG5cdFx0YmFycy5wdXNoKE9iamVjdC5hc3NpZ24oYmFyLCB7IGRhdGE6IGQgfSkpO1xuXHR9XG5cblx0Ly8gVE9ETzogY3JlYXRlIGEgZGl2IFwiaG92ZXJcIiBiYXIgZm9yIHRoaXMgXCJhcmVhXCIgb2YgdGhlIHZpc3VhbGl6YXRpb25cblx0bGV0IGhvdmVyQmFyID0gY3JlYXRlVmlydHVhbFNlbGVjdGlvbkJhcihvcHRzKTtcblx0bGV0IHNlbGVjdEJhciA9IGNyZWF0ZVZpcnR1YWxTZWxlY3Rpb25CYXIob3B0cyk7XG5cdGxldCB2aXJ0dWFsQmFyOiBIVE1MRWxlbWVudCB8IHVuZGVmaW5lZDtcblx0aWYgKHNvdXJjZS5iaW5zLmxlbmd0aCA+IHRocmVzaCkge1xuXHRcdGxldCB0b3RhbCA9IHNvdXJjZS5iaW5zLnNsaWNlKHRocmVzaCkucmVkdWNlKFxuXHRcdFx0KGFjYywgZCkgPT4gYWNjICsgZC50b3RhbCxcblx0XHRcdDAsXG5cdFx0KTtcblx0XHR2aXJ0dWFsQmFyID0gT2JqZWN0LmFzc2lnbihkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpLCB7XG5cdFx0XHR0aXRsZTogXCJfX3F1YWtfdmlydHVhbF9fXCIsXG5cdFx0fSk7XG5cdFx0T2JqZWN0LmFzc2lnbih2aXJ0dWFsQmFyLnN0eWxlLCB7XG5cdFx0XHR3aWR0aDogYCR7eCh0b3RhbCl9cHhgLFxuXHRcdFx0aGVpZ2h0OiBcIjEwMCVcIixcblx0XHRcdGJvcmRlckNvbG9yOiBcIndoaXRlXCIsXG5cdFx0XHRib3JkZXJXaWR0aDogXCIwcHggMXB4IDBweCAwcHhcIixcblx0XHRcdGJvcmRlclN0eWxlOiBcInNvbGlkXCIsXG5cdFx0XHRvcGFjaXR5OiAxLFxuXHRcdH0pO1xuXHRcdGxldCB2YmFycyA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdFx0T2JqZWN0LmFzc2lnbih2YmFycy5zdHlsZSwge1xuXHRcdFx0d2lkdGg6IFwiMTAwJVwiLFxuXHRcdFx0aGVpZ2h0OiBcIjEwMCVcIixcblx0XHRcdGJhY2tncm91bmQ6XG5cdFx0XHRcdGByZXBlYXRpbmctbGluZWFyLWdyYWRpZW50KHRvIHJpZ2h0LCAke29wdHMuZmlsbENvbG9yfSAwcHgsICR7b3B0cy5maWxsQ29sb3J9IDFweCwgd2hpdGUgMXB4LCB3aGl0ZSAycHgpYCxcblx0XHR9KTtcblx0XHR2aXJ0dWFsQmFyLmFwcGVuZENoaWxkKHZiYXJzKTtcblx0XHR2aXJ0dWFsQmFyLmFwcGVuZENoaWxkKGhvdmVyQmFyKTtcblx0XHR2aXJ0dWFsQmFyLmFwcGVuZENoaWxkKHNlbGVjdEJhcik7XG5cdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KHZpcnR1YWxCYXIsIFwiZGF0YVwiLCB7XG5cdFx0XHR2YWx1ZTogc291cmNlLmJpbnMuc2xpY2UodGhyZXNoKSxcblx0XHR9KTtcblx0XHQvLyBAdHMtZXhwZWN0LWVycm9yIC0gZGF0YSBpcyBkaWZmZXJlbnQgZm9yIHZpcnR1YWwgYmFyLi4uXG5cdFx0Ly8gVE9ETzogbmVlZCB0byByZXByZXNlbnQgZGlmZmVyZW5jZSBpbiB0eXBlc1xuXHRcdGJhcnMucHVzaCh2aXJ0dWFsQmFyKTtcblx0fVxuXG5cdGlmIChzb3VyY2UudW5pcXVlQ291bnQpIHtcblx0XHRsZXQgYmFyID0gY3JlYXRlQmFyKHtcblx0XHRcdHRpdGxlOiBcInVuaXF1ZVwiLFxuXHRcdFx0ZmlsbENvbG9yOiBvcHRzLmJhY2tncm91bmRCYXJDb2xvcixcblx0XHRcdHRleHRDb2xvcjogXCJ2YXIoLS1taWQtZ3JheSlcIixcblx0XHRcdHdpZHRoOiB4KHNvdXJjZS51bmlxdWVDb3VudCksXG5cdFx0XHRoZWlnaHQ6IG9wdHMuaGVpZ2h0LFxuXHRcdH0pO1xuXHRcdGJhci50aXRsZSA9IFwiX19xdWFrX3VuaXF1ZV9fXCI7XG5cdFx0YmFycy5wdXNoKE9iamVjdC5hc3NpZ24oYmFyLCB7XG5cdFx0XHRkYXRhOiB7XG5cdFx0XHRcdGtleTogXCJfX3F1YWtfdW5pcXVlX19cIixcblx0XHRcdFx0dG90YWw6IHNvdXJjZS51bmlxdWVDb3VudCxcblx0XHRcdH0sXG5cdFx0fSkpO1xuXHR9XG5cblx0aWYgKHNvdXJjZS5udWxsQ291bnQpIHtcblx0XHRsZXQgYmFyID0gY3JlYXRlQmFyKHtcblx0XHRcdHRpdGxlOiBcIm51bGxcIixcblx0XHRcdGZpbGxDb2xvcjogb3B0cy5udWxsRmlsbENvbG9yLFxuXHRcdFx0dGV4dENvbG9yOiBcIndoaXRlXCIsXG5cdFx0XHR3aWR0aDogeChzb3VyY2UubnVsbENvdW50KSxcblx0XHRcdGhlaWdodDogb3B0cy5oZWlnaHQsXG5cdFx0fSk7XG5cdFx0YmFyLnRpdGxlID0gXCJfX3F1YWtfbnVsbF9fXCI7XG5cdFx0YmFycy5wdXNoKE9iamVjdC5hc3NpZ24oYmFyLCB7XG5cdFx0XHRkYXRhOiB7XG5cdFx0XHRcdGtleTogXCJfX3F1YWtfbnVsbF9fXCIsXG5cdFx0XHRcdHRvdGFsOiBzb3VyY2UudW5pcXVlQ291bnQsXG5cdFx0XHR9LFxuXHRcdH0pKTtcblx0fVxuXG5cdGxldCBmaXJzdCA9IGJhcnNbMF07XG5cdGxldCBsYXN0ID0gYmFyc1tiYXJzLmxlbmd0aCAtIDFdO1xuXHRpZiAoZmlyc3QgPT09IGxhc3QpIHtcblx0XHRmaXJzdC5zdHlsZS5ib3JkZXJSYWRpdXMgPSBcIjVweFwiO1xuXHR9IGVsc2Uge1xuXHRcdGZpcnN0LnN0eWxlLmJvcmRlclJhZGl1cyA9IFwiNXB4IDBweCAwcHggNXB4XCI7XG5cdFx0bGFzdC5zdHlsZS5ib3JkZXJSYWRpdXMgPSBcIjBweCA1cHggNXB4IDBweFwiO1xuXHR9XG5cblx0ZnVuY3Rpb24gdmlydHVhbEJpbihrZXk6IHN0cmluZykge1xuXHRcdGFzc2VydCh2aXJ0dWFsQmFyKTtcblx0XHQvL1RPRE86IElzIHRoZXJlIGEgYmV0dGVyIHdheSB0byBkbyB0aGlzP1xuXHRcdGxldCB2b2Zmc2V0ID0gYmFyc1xuXHRcdFx0LnNsaWNlKDAsIHRocmVzaClcblx0XHRcdC5tYXAoKGIpID0+IGIuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCkud2lkdGgpXG5cdFx0XHQucmVkdWNlKChhLCBiKSA9PiBhICsgYiwgMCk7XG5cblx0XHQvLyBAdHMtZXhwZWN0LWVycm9yIC0gZGF0YSBpcyBhIHByb3BlcnR5IHdlIHNldCBvbiB0aGUgZWxlbWVudFxuXHRcdGxldCB2YmluczogQXJyYXk8eyBrZXk6IHN0cmluZzsgdG90YWw6IG51bWJlciB9PiA9IHZpcnR1YWxCYXIuZGF0YTtcblx0XHRsZXQgcmVjdCA9IHZpcnR1YWxCYXIuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCk7XG5cdFx0bGV0IGR4ID0gcmVjdC53aWR0aCAvIHZiaW5zLmxlbmd0aDtcblx0XHRsZXQgaWR4ID0gdmJpbnMuZmluZEluZGV4KChkKSA9PiBkLmtleSA9PT0ga2V5KTtcblx0XHRhc3NlcnQoaWR4ICE9PSAtMSwgYGtleSAke2tleX0gbm90IGZvdW5kIGluIHZpcnR1YWwgYmluc2ApO1xuXHRcdHJldHVybiB7XG5cdFx0XHQuLi52Ymluc1tpZHhdLFxuXHRcdFx0eDogZHggKiBpZHggKyB2b2Zmc2V0LFxuXHRcdH07XG5cdH1cblxuXHRmdW5jdGlvbiByZXNldChvcGFjdGl5OiBudW1iZXIpIHtcblx0XHRiYXJzLmZvckVhY2goKGJhcikgPT4ge1xuXHRcdFx0aWYgKGJhci50aXRsZSA9PT0gXCJfX3F1YWtfdmlydHVhbF9fXCIpIHtcblx0XHRcdFx0Ly8gQHRzLWV4cGVjdC1lcnJvciAtIHdlIHNldCB0aGlzIGFib3ZlXG5cdFx0XHRcdGxldCB2YmFyczogSFRNTERpdkVsZW1lbnQgPSBiYXIuZmlyc3RDaGlsZCE7XG5cdFx0XHRcdHZiYXJzLnN0eWxlLm9wYWNpdHkgPSBvcGFjdGl5LnRvU3RyaW5nKCk7XG5cdFx0XHRcdHZiYXJzLnN0eWxlLmJhY2tncm91bmQgPSBjcmVhdGVWaXJ0dWFsQmFyUmVwZWF0aW5nQmFja2dyb3VuZCh7XG5cdFx0XHRcdFx0Y29sb3I6IG9wdHMuZmlsbENvbG9yLFxuXHRcdFx0XHR9KTtcblx0XHRcdH0gZWxzZSB7XG5cdFx0XHRcdGJhci5zdHlsZS5vcGFjaXR5ID0gb3BhY3RpeS50b1N0cmluZygpO1xuXHRcdFx0XHRiYXIuc3R5bGUuYmFja2dyb3VuZCA9IGNyZWF0ZVNwbGl0QmFyRmlsbCh7XG5cdFx0XHRcdFx0Y29sb3I6IGJhci50aXRsZSA9PT0gXCJfX3F1YWtfdW5pcXVlX19cIlxuXHRcdFx0XHRcdFx0PyBvcHRzLmJhY2tncm91bmRCYXJDb2xvclxuXHRcdFx0XHRcdFx0OiBiYXIudGl0bGUgPT09IFwiX19xdWFrX251bGxfX1wiXG5cdFx0XHRcdFx0XHQ/IG9wdHMubnVsbEZpbGxDb2xvclxuXHRcdFx0XHRcdFx0OiBvcHRzLmZpbGxDb2xvcixcblx0XHRcdFx0XHRiZ0NvbG9yOiBvcHRzLmJhY2tncm91bmRCYXJDb2xvcixcblx0XHRcdFx0XHRmcmFjOiAxLFxuXHRcdFx0XHR9KTtcblx0XHRcdH1cblx0XHRcdGJhci5zdHlsZS5ib3JkZXJDb2xvciA9IFwid2hpdGVcIjtcblx0XHRcdGJhci5zdHlsZS5ib3JkZXJXaWR0aCA9IFwiMHB4IDFweCAwcHggMHB4XCI7XG5cdFx0XHRiYXIuc3R5bGUucmVtb3ZlUHJvcGVydHkoXCJib3gtc2hhZG93XCIpO1xuXHRcdH0pO1xuXHRcdGJhcnNbYmFycy5sZW5ndGggLSAxXS5zdHlsZS5ib3JkZXJXaWR0aCA9IFwiMHB4XCI7XG5cdFx0aG92ZXJCYXIuc3R5bGUudmlzaWJpbGl0eSA9IFwiaGlkZGVuXCI7XG5cdFx0c2VsZWN0QmFyLnN0eWxlLnZpc2liaWxpdHkgPSBcImhpZGRlblwiO1xuXHR9XG5cblx0ZnVuY3Rpb24gaG92ZXIoa2V5OiBzdHJpbmcsIHNlbGVjdGVkPzogc3RyaW5nKSB7XG5cdFx0bGV0IGJhciA9IGJhcnMuZmluZCgoYikgPT4gYi5kYXRhLmtleSA9PT0ga2V5KTtcblx0XHRpZiAoYmFyICE9PSB1bmRlZmluZWQpIHtcblx0XHRcdGJhci5zdHlsZS5vcGFjaXR5ID0gXCIxXCI7XG5cdFx0XHRyZXR1cm47XG5cdFx0fVxuXHRcdGxldCB2YmluID0gdmlydHVhbEJpbihrZXkpO1xuXHRcdGhvdmVyQmFyLnRpdGxlID0gdmJpbi5rZXk7XG5cdFx0aG92ZXJCYXIuZGF0YSA9IHZiaW47XG5cdFx0aG92ZXJCYXIuc3R5bGUub3BhY2l0eSA9IHNlbGVjdGVkID8gXCIwLjI1XCIgOiBcIjFcIjtcblx0XHRob3ZlckJhci5zdHlsZS5sZWZ0ID0gYCR7dmJpbi54fXB4YDtcblx0XHRob3ZlckJhci5zdHlsZS52aXNpYmlsaXR5ID0gXCJ2aXNpYmxlXCI7XG5cdH1cblxuXHRmdW5jdGlvbiBzZWxlY3Qoa2V5OiBzdHJpbmcpIHtcblx0XHRsZXQgYmFyID0gYmFycy5maW5kKChiKSA9PiBiLmRhdGEua2V5ID09PSBrZXkpO1xuXHRcdGlmIChiYXIgIT09IHVuZGVmaW5lZCkge1xuXHRcdFx0YmFyLnN0eWxlLm9wYWNpdHkgPSBcIjFcIjtcblx0XHRcdGJhci5zdHlsZS5ib3hTaGFkb3cgPSBcImluc2V0IDAgMCAwIDEuMnB4IGJsYWNrXCI7XG5cdFx0XHRyZXR1cm47XG5cdFx0fVxuXHRcdGxldCB2YmluID0gdmlydHVhbEJpbihrZXkpO1xuXHRcdHNlbGVjdEJhci5zdHlsZS5vcGFjaXR5ID0gXCIxXCI7XG5cdFx0c2VsZWN0QmFyLnRpdGxlID0gdmJpbi5rZXk7XG5cdFx0c2VsZWN0QmFyLmRhdGEgPSB2YmluO1xuXHRcdHNlbGVjdEJhci5zdHlsZS5sZWZ0ID0gYCR7dmJpbi54fXB4YDtcblx0XHRzZWxlY3RCYXIuc3R5bGUudmlzaWJpbGl0eSA9IFwidmlzaWJsZVwiO1xuXHR9XG5cblx0bGV0IGNvdW50czogUmVjb3JkPHN0cmluZywgbnVtYmVyPiA9IE9iamVjdC5mcm9tRW50cmllcyhcblx0XHRBcnJheS5mcm9tKGRhdGEudG9BcnJheSgpLCAoZCkgPT4gW2Qua2V5LCBkLnRvdGFsXSksXG5cdCk7XG5cblx0cmV0dXJuIHtcblx0XHRlbGVtZW50czogYmFycyxcblx0XHRuZWFyZXN0WChldmVudDogTW91c2VFdmVudCk6IHN0cmluZyB8IHVuZGVmaW5lZCB7XG5cdFx0XHRsZXQgYmFyID0gbmVhcmVzdFgoZXZlbnQsIGJhcnMpO1xuXHRcdFx0aWYgKCFiYXIpIHJldHVybjtcblx0XHRcdGlmIChiYXIudGl0bGUgIT09IFwiX19xdWFrX3ZpcnR1YWxfX1wiKSB7XG5cdFx0XHRcdC8vIEB0cy1leHBlY3QtZXJyb3IgLSBkYXRhIGlzIGEgcHJvcGVydHkgd2Ugc2V0IG9uIHRoZSBlbGVtZW50XG5cdFx0XHRcdHJldHVybiBiYXIuZGF0YS5rZXk7XG5cdFx0XHR9XG5cdFx0XHRsZXQgcmVjdCA9IGJhci5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKTtcblx0XHRcdGxldCBtb3VzZVggPSBldmVudC5jbGllbnRYIC0gcmVjdC5sZWZ0O1xuXHRcdFx0Ly8gQHRzLWV4cGVjdC1lcnJvciAtIGRhdGEgaXMgYSBwcm9wZXJ0eSB3ZSBzZXQgb24gdGhlIGVsZW1lbnRcblx0XHRcdGxldCBkYXRhOiBBcnJheTx7IGtleTogc3RyaW5nOyB0b3RhbDogbnVtYmVyIH0+ID0gYmFyLmRhdGE7XG5cdFx0XHRsZXQgaWR4ID0gTWF0aC5mbG9vcigobW91c2VYIC8gcmVjdC53aWR0aCkgKiBkYXRhLmxlbmd0aCk7XG5cdFx0XHRyZXR1cm4gZGF0YVtpZHhdLmtleTtcblx0XHR9LFxuXHRcdHJlbmRlcihkYXRhOiBDb3VudFRhYmxlRGF0YSwgaG92ZXJpbmc/OiBzdHJpbmcsIHNlbGVjdGVkPzogc3RyaW5nKSB7XG5cdFx0XHRyZXNldChob3ZlcmluZyB8fCBzZWxlY3RlZCA/IDAuNCA6IDEpO1xuXHRcdFx0bGV0IHVwZGF0ZTogUmVjb3JkPHN0cmluZywgbnVtYmVyPiA9IE9iamVjdC5mcm9tRW50cmllcyhcblx0XHRcdFx0QXJyYXkuZnJvbShkYXRhLnRvQXJyYXkoKSwgKGQpID0+IFtkLmtleSwgZC50b3RhbF0pLFxuXHRcdFx0KTtcblx0XHRcdGxldCB0b3RhbCA9IE9iamVjdC52YWx1ZXModXBkYXRlKS5yZWR1Y2UoKGEsIGIpID0+IGEgKyBiLCAwKTtcblx0XHRcdGZvciAobGV0IGJhciBvZiBiYXJzKSB7XG5cdFx0XHRcdGlmIChiYXIudGl0bGUgPT09IFwiX19xdWFrX3ZpcnR1YWxfX1wiKSB7XG5cdFx0XHRcdFx0bGV0IHZiYXJzID0gYmFyLmZpcnN0Q2hpbGQgYXMgSFRNTERpdkVsZW1lbnQ7XG5cdFx0XHRcdFx0dmJhcnMuc3R5bGUuYmFja2dyb3VuZCA9IGNyZWF0ZVZpcnR1YWxCYXJSZXBlYXRpbmdCYWNrZ3JvdW5kKHtcblx0XHRcdFx0XHRcdGNvbG9yOiAodG90YWwgPCBzb3VyY2UudG90YWwpIHx8IHNlbGVjdGVkXG5cdFx0XHRcdFx0XHRcdD8gb3B0cy5iYWNrZ3JvdW5kQmFyQ29sb3Jcblx0XHRcdFx0XHRcdFx0OiBvcHRzLmZpbGxDb2xvcixcblx0XHRcdFx0XHR9KTtcblx0XHRcdFx0fSBlbHNlIHtcblx0XHRcdFx0XHRsZXQga2V5OiBzdHJpbmcgPSBiYXIuZGF0YS5rZXk7XG5cdFx0XHRcdFx0bGV0IGZyYWMgPSAodXBkYXRlW2tleV0gPz8gMCkgLyBjb3VudHNba2V5XTtcblx0XHRcdFx0XHRpZiAoc2VsZWN0ZWQpIGZyYWMgPSBrZXkgPT09IHNlbGVjdGVkID8gZnJhYyA6IDA7XG5cdFx0XHRcdFx0YmFyLnN0eWxlLmJhY2tncm91bmQgPSBjcmVhdGVTcGxpdEJhckZpbGwoe1xuXHRcdFx0XHRcdFx0Y29sb3I6IGJhci50aXRsZSA9PT0gXCJfX3F1YWtfdW5pcXVlX19cIlxuXHRcdFx0XHRcdFx0XHQ/IG9wdHMuYmFja2dyb3VuZEJhckNvbG9yXG5cdFx0XHRcdFx0XHRcdDogYmFyLnRpdGxlID09PSBcIl9fcXVha19udWxsX19cIlxuXHRcdFx0XHRcdFx0XHQ/IG9wdHMubnVsbEZpbGxDb2xvclxuXHRcdFx0XHRcdFx0XHQ6IG9wdHMuZmlsbENvbG9yLFxuXHRcdFx0XHRcdFx0YmdDb2xvcjogb3B0cy5iYWNrZ3JvdW5kQmFyQ29sb3IsXG5cdFx0XHRcdFx0XHRmcmFjOiBpc05hTihmcmFjKSA/IDAgOiBmcmFjLFxuXHRcdFx0XHRcdH0pO1xuXHRcdFx0XHR9XG5cdFx0XHR9XG5cdFx0XHRpZiAoaG92ZXJpbmcgIT09IHVuZGVmaW5lZCkge1xuXHRcdFx0XHRob3Zlcihob3ZlcmluZywgc2VsZWN0ZWQpO1xuXHRcdFx0fVxuXHRcdFx0aWYgKHNlbGVjdGVkICE9PSB1bmRlZmluZWQpIHtcblx0XHRcdFx0c2VsZWN0KHNlbGVjdGVkKTtcblx0XHRcdH1cblx0XHR9LFxuXHRcdHRleHRGb3Ioa2V5Pzogc3RyaW5nKTogc3RyaW5nIHtcblx0XHRcdGlmIChrZXkgPT09IHVuZGVmaW5lZCkge1xuXHRcdFx0XHRsZXQgbmNhdHMgPSBkYXRhLm51bVJvd3M7XG5cdFx0XHRcdHJldHVybiBgJHtuY2F0cy50b0xvY2FsZVN0cmluZygpfSBjYXRlZ29yJHtuY2F0cyA9PT0gMSA/IFwieVwiIDogXCJpZXNcIn1gO1xuXHRcdFx0fVxuXHRcdFx0aWYgKGtleSA9PT0gXCJfX3F1YWtfdW5pcXVlX19cIikge1xuXHRcdFx0XHRyZXR1cm4gYCR7c291cmNlLnVuaXF1ZUNvdW50LnRvTG9jYWxlU3RyaW5nKCl9IHVuaXF1ZSB2YWx1ZSR7XG5cdFx0XHRcdFx0c291cmNlLnVuaXF1ZUNvdW50ID09PSAxID8gXCJcIiA6IFwic1wiXG5cdFx0XHRcdH1gO1xuXHRcdFx0fVxuXHRcdFx0aWYgKGtleSA9PT0gXCJfX3F1YWtfbnVsbF9fXCIpIHtcblx0XHRcdFx0cmV0dXJuIFwibnVsbFwiO1xuXHRcdFx0fVxuXHRcdFx0cmV0dXJuIGtleS50b1N0cmluZygpO1xuXHRcdH0sXG5cdH07XG59XG5cbmZ1bmN0aW9uIGNyZWF0ZVRleHRPdXRwdXQoKSB7XG5cdGxldCBub2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcblx0T2JqZWN0LmFzc2lnbihub2RlLnN0eWxlLCB7XG5cdFx0cG9pbnRlckV2ZW50czogXCJub25lXCIsXG5cdFx0aGVpZ2h0OiBcIjE1cHhcIixcblx0XHRtYXhXaWR0aDogXCIxMDAlXCIsXG5cdFx0b3ZlcmZsb3c6IFwiaGlkZGVuXCIsXG5cdFx0dGV4dE92ZXJmbG93OiBcImVsbGlwc2lzXCIsXG5cdFx0cG9zaXRpb246IFwiYWJzb2x1dGVcIixcblx0XHRmb250V2VpZ2h0OiA0MDAsXG5cdFx0bWFyZ2luVG9wOiBcIjEuNXB4XCIsXG5cdFx0Y29sb3I6IFwidmFyKC0tbWlkLWdyYXkpXCIsXG5cdH0pO1xuXHRyZXR1cm4gbm9kZTtcbn1cblxuZnVuY3Rpb24gY3JlYXRlVmlydHVhbFNlbGVjdGlvbkJhcihvcHRzOiB7IGZpbGxDb2xvcjogc3RyaW5nIH0pIHtcblx0bGV0IG5vZGUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuXHRPYmplY3QuYXNzaWduKG5vZGUuc3R5bGUsIHtcblx0XHRwb3NpdGlvbjogXCJhYnNvbHV0ZVwiLFxuXHRcdHRvcDogXCIwXCIsXG5cdFx0d2lkdGg6IFwiMS41cHhcIixcblx0XHRoZWlnaHQ6IFwiMTAwJVwiLFxuXHRcdGJhY2tncm91bmRDb2xvcjogb3B0cy5maWxsQ29sb3IsXG5cdFx0cG9pbnRlckV2ZW50czogXCJub25lXCIsXG5cdFx0dmlzaWJpbGl0eTogXCJoaWRkZW5cIixcblx0fSk7XG5cdHJldHVybiBPYmplY3QuYXNzaWduKG5vZGUsIHtcblx0XHRkYXRhOiB7IGtleTogXCJcIiwgdG90YWw6IDAgfSxcblx0fSk7XG59XG5cbmZ1bmN0aW9uIG5lYXJlc3RYKHsgY2xpZW50WCB9OiBNb3VzZUV2ZW50LCBiYXJzOiBBcnJheTxIVE1MRWxlbWVudD4pIHtcblx0Ly8gY291bGQgdXNlIGEgYmluYXJ5IHNlYXJjaCBoZXJlIGlmIG5lZWRlZFxuXHRmb3IgKGxldCBiYXIgb2YgYmFycykge1xuXHRcdGxldCByZWN0ID0gYmFyLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpO1xuXHRcdGlmIChjbGllbnRYID49IHJlY3QubGVmdCAmJiBjbGllbnRYIDw9IHJlY3QucmlnaHQpIHtcblx0XHRcdHJldHVybiBiYXI7XG5cdFx0fVxuXHR9XG59XG5cbi8qKlxuICogQ3JlYXRlcyBhIGZpbGwgZ3JhZGllbnQgdGhhdCBpcyBmaWxsZWQgeCUgd2l0aCBhIGNvbG9yIGFuZCB0aGUgcmVzdCB3aXRoIGEgYmFja2dyb3VuZCBjb2xvci5cbiAqL1xuZnVuY3Rpb24gY3JlYXRlU3BsaXRCYXJGaWxsKFxuXHRvcHRpb25zOiB7IGNvbG9yOiBzdHJpbmc7IGJnQ29sb3I6IHN0cmluZzsgZnJhYzogbnVtYmVyIH0sXG4pIHtcblx0bGV0IHsgY29sb3IsIGJnQ29sb3IsIGZyYWMgfSA9IG9wdGlvbnM7XG5cdGxldCBwID0gZnJhYyAqIDEwMDtcblx0Ly8gZGVuby1mbXQtaWdub3JlXG5cdHJldHVybiBgbGluZWFyLWdyYWRpZW50KHRvIHRvcCwgJHtjb2xvcn0gJHtwfSUsICR7YmdDb2xvcn0gJHtwfSUsICR7YmdDb2xvcn0gJHsxMDAgLSBwfSUpYDtcbn1cblxuZnVuY3Rpb24gY3JlYXRlVmlydHVhbEJhclJlcGVhdGluZ0JhY2tncm91bmQoeyBjb2xvciB9OiB7IGNvbG9yOiBzdHJpbmcgfSkge1xuXHRyZXR1cm4gYHJlcGVhdGluZy1saW5lYXItZ3JhZGllbnQodG8gcmlnaHQsICR7Y29sb3J9IDBweCwgJHtjb2xvcn0gMXB4LCB3aGl0ZSAxcHgsIHdoaXRlIDJweClgO1xufVxuIiwgIjpob3N0IHtcblx0YWxsOiBpbml0aWFsO1xuXHQtLXNhbnMtc2VyaWY6IC1hcHBsZS1zeXN0ZW0sIEJsaW5rTWFjU3lzdGVtRm9udCwgXCJhdmVuaXIgbmV4dFwiLCBhdmVuaXIsIGhlbHZldGljYSwgXCJoZWx2ZXRpY2EgbmV1ZVwiLCB1YnVudHUsIHJvYm90bywgbm90bywgXCJzZWdvZSB1aVwiLCBhcmlhbCwgc2Fucy1zZXJpZjtcblx0LS1saWdodC1zaWx2ZXI6ICNlZmVmZWY7XG5cdC0tc3BhY2luZy1ub25lOiAwO1xuXHQtLXdoaXRlOiAjZmZmO1xuXHQtLWdyYXk6ICM5MjkyOTI7XG5cdC0tZGFyay1ncmF5OiAjMzMzO1xuXHQtLW1vb24tZ3JheTogI2M0YzRjNDtcblx0LS1taWQtZ3JheTogIzZlNmU2ZTtcblxuXHQtLXN0b25lLWJsdWU6ICM2NDc0OGI7XG5cdC0teWVsbG93LWdvbGQ6ICNjYThhMDQ7XG5cblx0LS10ZWFsOiAjMDI3OTgyO1xuXHQtLWRhcmstcGluazogI0QzNUE1RjtcblxuXHQtLWxpZ2h0LWJsdWU6ICM3RTkzQ0Y7XG5cdC0tZGFyay15ZWxsb3ctZ29sZDogI0E5ODQ0NztcblxuXHQtLXB1cnBsZTogIzk4N2ZkMztcblxuXHQtLXByaW1hcnk6IHZhcigtLXN0b25lLWJsdWUpO1xuXHQtLXNlY29uZGFyeTogdmFyKC0teWVsbG93LWdvbGQpO1xufVxuXG4uaGlnaGxpZ2h0IHtcblx0YmFja2dyb3VuZC1jb2xvcjogdmFyKC0tbGlnaHQtc2lsdmVyKTtcbn1cblxuLmhpZ2hsaWdodC1jZWxsIHtcblx0Ym9yZGVyOiAxcHggc29saWQgdmFyKC0tbW9vbi1ncmF5KTtcbn1cblxuLnF1YWsge1xuICBib3JkZXItcmFkaXVzOiAwLjJyZW07XG4gIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLWxpZ2h0LXNpbHZlcik7XG4gIG92ZXJmbG93LXk6IGF1dG87XG59XG5cbnRhYmxlIHtcbiAgYm9yZGVyLWNvbGxhcHNlOiBzZXBhcmF0ZTtcbiAgYm9yZGVyLXNwYWNpbmc6IDA7XG4gIHdoaXRlLXNwYWNlOiBub3dyYXA7XG4gIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XG5cbiAgbWFyZ2luOiB2YXIoLS1zcGFjaW5nLW5vbmUpO1xuICBjb2xvcjogdmFyKC0tZGFyay1ncmF5KTtcbiAgZm9udDogMTNweCAvIDEuMiB2YXIoLS1zYW5zLXNlcmlmKTtcblxuICB3aWR0aDogMTAwJTtcbn1cblxudGhlYWQge1xuICBwb3NpdGlvbjogc3RpY2t5O1xuICB2ZXJ0aWNhbC1hbGlnbjogdG9wO1xuICB0ZXh0LWFsaWduOiBsZWZ0O1xuICB0b3A6IDA7XG59XG5cbnRkIHtcbiAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tbGlnaHQtc2lsdmVyKTtcbiAgYm9yZGVyLWJvdHRvbTogc29saWQgMXB4IHRyYW5zcGFyZW50O1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB0cmFuc3BhcmVudDtcbiAgb3ZlcmZsb3c6IGhpZGRlbjtcbiAgLW8tdGV4dC1vdmVyZmxvdzogZWxsaXBzaXM7XG4gIHRleHQtb3ZlcmZsb3c6IGVsbGlwc2lzO1xuICBwYWRkaW5nOiA0cHggNnB4O1xufVxuXG50cjpmaXJzdC1jaGlsZCB0ZCB7XG4gIGJvcmRlci10b3A6IHNvbGlkIDFweCB0cmFuc3BhcmVudDtcbn1cblxudGgge1xuICBkaXNwbGF5OiB0YWJsZS1jZWxsO1xuICB2ZXJ0aWNhbC1hbGlnbjogaW5oZXJpdDtcbiAgZm9udC13ZWlnaHQ6IGJvbGQ7XG4gIHRleHQtYWxpZ246IC1pbnRlcm5hbC1jZW50ZXI7XG4gIHVuaWNvZGUtYmlkaTogaXNvbGF0ZTtcblxuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIGJhY2tncm91bmQ6IHZhcigtLXdoaXRlKTtcbiAgYm9yZGVyLWJvdHRvbTogc29saWQgMXB4IHZhcigtLWxpZ2h0LXNpbHZlcik7XG4gIGJvcmRlci1sZWZ0OiBzb2xpZCAxcHggdmFyKC0tbGlnaHQtc2lsdmVyKTtcbiAgcGFkZGluZzogNXB4IDZweDtcbiAgdXNlci1zZWxlY3Q6IG5vbmU7XG59XG5cbi5udW1iZXIsIC5kYXRlIHtcbiAgZm9udC12YXJpYW50LW51bWVyaWM6IHRhYnVsYXItbnVtcztcbn1cblxuLmdyYXkge1xuICBjb2xvcjogdmFyKC0tZ3JheSk7XG59XG5cbi5udW1iZXIge1xuICB0ZXh0LWFsaWduOiByaWdodDtcbn1cblxudGQ6bnRoLWNoaWxkKDEpLCB0aDpudGgtY2hpbGQoMSkge1xuICBmb250LXZhcmlhbnQtbnVtZXJpYzogdGFidWxhci1udW1zO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGNvbG9yOiB2YXIoLS1tb29uLWdyYXkpO1xuICBwYWRkaW5nOiAwIDRweDtcbn1cblxudGQ6Zmlyc3QtY2hpbGQsIHRoOmZpcnN0LWNoaWxkIHtcbiAgYm9yZGVyLWxlZnQ6IG5vbmU7XG59XG5cbnRoOmZpcnN0LWNoaWxkIHtcbiAgYm9yZGVyLWxlZnQ6IG5vbmU7XG4gIHZlcnRpY2FsLWFsaWduOiB0b3A7XG4gIHdpZHRoOiAyMHB4O1xuICBwYWRkaW5nOiA3cHg7XG59XG5cbnRkOm50aC1sYXN0LWNoaWxkKDIpLCB0aDpudGgtbGFzdC1jaGlsZCgyKSB7XG4gIGJvcmRlci1yaWdodDogMXB4IHNvbGlkIHZhcigtLWxpZ2h0LXNpbHZlcik7XG59XG5cbnRyOmZpcnN0LWNoaWxkIHRkIHtcblx0Ym9yZGVyLXRvcDogc29saWQgMXB4IHRyYW5zcGFyZW50O1xufVxuXG4ucmVzaXplLWhhbmRsZSB7XG5cdHdpZHRoOiA1cHg7XG5cdGhlaWdodDogMTAwJTtcblx0YmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7XG5cdHBvc2l0aW9uOiBhYnNvbHV0ZTtcblx0cmlnaHQ6IC0yLjVweDtcblx0dG9wOiAwO1xuXHRjdXJzb3I6IGV3LXJlc2l6ZTtcblx0ei1pbmRleDogMTtcbn1cblxuLnF1YWsgLnNvcnQtYnV0dG9uIHtcblx0Y3Vyc29yOiBwb2ludGVyO1xuXHRiYWNrZ3JvdW5kLWNvbG9yOiB2YXIoLS13aGl0ZSk7XG5cdHVzZXItc2VsZWN0OiBub25lO1xufVxuXG4uc3RhdHVzLWJhciB7XG5cdGRpc3BsYXk6IGZsZXg7XG5cdGp1c3RpZnktY29udGVudDogZmxleC1lbmQ7XG5cdGZvbnQtZmFtaWx5OiB2YXIoLS1zYW5zLXNlcmlmKTtcblx0bWFyZ2luLXJpZ2h0OiAxMHB4O1xuXHRtYXJnaW4tdG9wOiA1cHg7XG59XG5cbi5zdGF0dXMtYmFyIGJ1dHRvbiB7XG5cdGJvcmRlcjogbm9uZTtcblx0YmFja2dyb3VuZC1jb2xvcjogdmFyKC0td2hpdGUpO1xuXHRjb2xvcjogdmFyKC0tcHJpbWFyeSk7XG5cdGZvbnQtd2VpZ2h0OiA2MDA7XG5cdGZvbnQtc2l6ZTogMC44NzVyZW07XG5cdGN1cnNvcjogcG9pbnRlcjtcblx0bWFyZ2luLXJpZ2h0OiA1cHg7XG59XG5cbi5zdGF0dXMtYmFyIHNwYW4ge1xuXHRjb2xvcjogdmFyKC0tZ3JheSk7XG5cdGZvbnQtd2VpZ2h0OiA0MDA7XG5cdGZvbnQtc2l6ZTogMC43NXJlbTtcblx0Zm9udC12YXJpYW50LW51bWVyaWM6IHRhYnVsYXItbnVtcztcbn1cbiIsICJpbXBvcnQgKiBhcyBhcnJvdyBmcm9tIFwiYXBhY2hlLWFycm93XCI7XG4vLyBAZGVuby10eXBlcz1cIi4uL2RlcHMvbW9zYWljLWNvcmUuZC50c1wiXG5pbXBvcnQgeyB0eXBlIEludGVyYWN0b3IsIE1vc2FpY0NsaWVudCwgU2VsZWN0aW9uIH0gZnJvbSBcIkB1d2RhdGEvbW9zYWljLWNvcmVcIjtcbi8vIEBkZW5vLXR5cGVzPVwiLi4vZGVwcy9tb3NhaWMtc3FsLmQudHNcIlxuaW1wb3J0IHsgY291bnQsIFF1ZXJ5IH0gZnJvbSBcIkB1d2RhdGEvbW9zYWljLXNxbFwiO1xuXG5pbnRlcmZhY2UgU3RhdHVzQmFyT3B0aW9ucyB7XG5cdHRhYmxlOiBzdHJpbmc7XG5cdGZpbHRlckJ5PzogU2VsZWN0aW9uO1xufVxuXG5leHBvcnQgY2xhc3MgU3RhdHVzQmFyIGV4dGVuZHMgTW9zYWljQ2xpZW50IHtcblx0I3RhYmxlOiBzdHJpbmc7XG5cdCNlbCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdCNidXR0b246IEhUTUxCdXR0b25FbGVtZW50O1xuXHQjc3BhbjogSFRNTFNwYW5FbGVtZW50O1xuXHQjdG90YWxSb3dzOiBudW1iZXIgfCB1bmRlZmluZWQgPSB1bmRlZmluZWQ7XG5cblx0Y29uc3RydWN0b3Iob3B0aW9uczogU3RhdHVzQmFyT3B0aW9ucykge1xuXHRcdHN1cGVyKG9wdGlvbnMuZmlsdGVyQnkpO1xuXHRcdHRoaXMuI3RhYmxlID0gb3B0aW9ucy50YWJsZTtcblx0XHR0aGlzLiNidXR0b24gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiYnV0dG9uXCIpO1xuXHRcdHRoaXMuI2J1dHRvbi5pbm5lclRleHQgPSBcIlJlc2V0XCI7XG5cdFx0dGhpcy4jc3BhbiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJzcGFuXCIpO1xuXG5cdFx0bGV0IGRpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG5cdFx0ZGl2LmFwcGVuZENoaWxkKHRoaXMuI2J1dHRvbik7XG5cdFx0ZGl2LmFwcGVuZENoaWxkKHRoaXMuI3NwYW4pO1xuXHRcdHRoaXMuI2VsLmFwcGVuZENoaWxkKGRpdik7XG5cdFx0dGhpcy4jZWwuY2xhc3NMaXN0LmFkZChcInN0YXR1cy1iYXJcIik7XG5cblx0XHR0aGlzLiNidXR0b24uYWRkRXZlbnRMaXN0ZW5lcihcIm1vdXNlZG93blwiLCAoKSA9PiB7XG5cdFx0XHRpZiAoIXRoaXMuZmlsdGVyQnkpIHJldHVybjtcblx0XHRcdC8vIFRPRE86IEEgYmV0dGVyIHdheSB0byBkbyB0aGlzP1xuXHRcdFx0Ly8gV2Ugd2FudCB0byBjbGVhciBhbGwgdGhlIGV4aXN0aW5nIHNlbGVjdGlvbnNcblx0XHRcdC8vIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3V3ZGF0YS9tb3NhaWMvYmxvYi84ZTYzMTQ5NzUzZTdkNmNhMzAyNzRjMDMyYTA0NzQ0ZTE0ZGYyZmQ2L3BhY2thZ2VzL2NvcmUvc3JjL1NlbGVjdGlvbi5qcyNMMjY1LUwyNzJcblx0XHRcdGZvciAobGV0IHsgc291cmNlIH0gb2YgdGhpcy5maWx0ZXJCeS5jbGF1c2VzKSB7XG5cdFx0XHRcdGlmICghaXNJbnRlcmFjdG9yKHNvdXJjZSkpIHtcblx0XHRcdFx0XHRjb25zb2xlLndhcm4oXCJTa2lwcGluZyBub24taW50ZXJhY3RvciBzb3VyY2VcIiwgc291cmNlKTtcblx0XHRcdFx0XHRjb250aW51ZTtcblx0XHRcdFx0fVxuXHRcdFx0XHRzb3VyY2UucmVzZXQoKTtcblx0XHRcdFx0dGhpcy5maWx0ZXJCeS51cGRhdGUoc291cmNlLmNsYXVzZSgpKTtcblx0XHRcdH1cblx0XHR9KTtcblxuXHRcdHRoaXMuI2J1dHRvbi5zdHlsZS52aXNpYmlsaXR5ID0gXCJoaWRkZW5cIjtcblx0XHR0aGlzLmZpbHRlckJ5Py5hZGRFdmVudExpc3RlbmVyKFwidmFsdWVcIiwgKCkgPT4ge1xuXHRcdFx0Ly8gZGVjaWRlIHdoZXRoZXIgdG8gZGlzcGxheSB0aGUgcmVzZXQgYnV0dG9uIGFueSB0aW1lIHRoZSBmaWx0ZXIgY2hhbmdlc1xuXHRcdFx0aWYgKHRoaXMuZmlsdGVyQnk/LmNsYXVzZXMubGVuZ3RoID09PSAwKSB7XG5cdFx0XHRcdHRoaXMuI2J1dHRvbi5zdHlsZS52aXNpYmlsaXR5ID0gXCJoaWRkZW5cIjtcblx0XHRcdH0gZWxzZSB7XG5cdFx0XHRcdHRoaXMuI2J1dHRvbi5zdHlsZS52aXNpYmlsaXR5ID0gXCJ2aXNpYmxlXCI7XG5cdFx0XHR9XG5cdFx0fSk7XG5cdH1cblxuXHRxdWVyeShmaWx0ZXIgPSBbXSkge1xuXHRcdGxldCBxdWVyeSA9IFF1ZXJ5LmZyb20odGhpcy4jdGFibGUpXG5cdFx0XHQuc2VsZWN0KHsgY291bnQ6IGNvdW50KCkgfSlcblx0XHRcdC53aGVyZShmaWx0ZXIpO1xuXHRcdHJldHVybiBxdWVyeTtcblx0fVxuXG5cdHF1ZXJ5UmVzdWx0KHRhYmxlOiBhcnJvdy5UYWJsZTx7IGNvdW50OiBhcnJvdy5JbnQgfT4pIHtcblx0XHRsZXQgY291bnQgPSBOdW1iZXIodGFibGUuZ2V0KDApPy5jb3VudCA/PyAwKTtcblx0XHRpZiAoIXRoaXMuI3RvdGFsUm93cykge1xuXHRcdFx0Ly8gd2UgbmVlZCB0byBrbm93IHRoZSB0b3RhbCBudW1iZXIgb2Ygcm93cyB0byBkaXNwbGF5XG5cdFx0XHR0aGlzLiN0b3RhbFJvd3MgPSBjb3VudDtcblx0XHR9XG5cdFx0bGV0IGNvdW50U3RyID0gY291bnQudG9Mb2NhbGVTdHJpbmcoKTtcblx0XHRpZiAoY291bnQgPT0gdGhpcy4jdG90YWxSb3dzKSB7XG5cdFx0XHR0aGlzLiNzcGFuLmlubmVyVGV4dCA9IGAke2NvdW50U3RyfSByb3dzYDtcblx0XHR9IGVsc2Uge1xuXHRcdFx0bGV0IHRvdGFsU3RyID0gdGhpcy4jdG90YWxSb3dzLnRvTG9jYWxlU3RyaW5nKCk7XG5cdFx0XHR0aGlzLiNzcGFuLmlubmVyVGV4dCA9IGAke2NvdW50U3RyfSBvZiAke3RvdGFsU3RyfSByb3dzYDtcblx0XHR9XG5cdFx0cmV0dXJuIHRoaXM7XG5cdH1cblxuXHRub2RlKCkge1xuXHRcdHJldHVybiB0aGlzLiNlbDtcblx0fVxufVxuXG5mdW5jdGlvbiBpc09iamVjdCh4OiB1bmtub3duKTogeCBpcyBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPiB7XG5cdHJldHVybiB0eXBlb2YgeCA9PT0gXCJvYmplY3RcIiAmJiB4ICE9PSBudWxsICYmICFBcnJheS5pc0FycmF5KHgpO1xufVxuXG5mdW5jdGlvbiBpc0ludGVyYWN0b3IoeDogdW5rbm93bik6IHggaXMgSW50ZXJhY3RvciB7XG5cdHJldHVybiBpc09iamVjdCh4KSAmJiBcImNsYXVzZVwiIGluIHggJiYgXCJyZXNldFwiIGluIHg7XG59XG4iLCAiLyoqXG4gKiBEZWZlciBhIHByb21pc2UuXG4gKlxuICogVE9ETzogU2hvdWxkIHVzZSBQcm9taXNlLndpdGhSZXNvbHZlcnMoKSB3aGVuIGF2YWlsYWJsZS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGRlZmVyPFN1Y2Nlc3MsIFJlamVjdD4oKToge1xuXHRwcm9taXNlOiBQcm9taXNlPFN1Y2Nlc3M+O1xuXHRyZXNvbHZlOiAodmFsdWU6IFN1Y2Nlc3MpID0+IHZvaWQ7XG5cdHJlamVjdDogKHJlYXNvbj86IFJlamVjdCkgPT4gdm9pZDtcbn0ge1xuXHRsZXQgcmVzb2x2ZTtcblx0bGV0IHJlamVjdDtcblx0bGV0IHByb21pc2UgPSBuZXcgUHJvbWlzZTxTdWNjZXNzPigocmVzLCByZWopID0+IHtcblx0XHRyZXNvbHZlID0gcmVzO1xuXHRcdHJlamVjdCA9IHJlajtcblx0fSk7XG5cdC8qKiBAdHMtZXhwZWN0LWVycm9yIC0gcmVzb2x2ZSBhbmQgcmVqZWN0IGFyZSBzZXQgKi9cblx0cmV0dXJuIHsgcHJvbWlzZSwgcmVzb2x2ZSwgcmVqZWN0IH07XG59XG4iXSwKICAibWFwcGluZ3MiOiAiOzs7Ozs7Ozs7Ozs7Ozs7QUFDQSxZQUFZLFFBQVE7QUFFcEIsU0FBUyxTQUFBQSxjQUFhO0FBQ3RCLFlBQVlDLFlBQVc7QUFDdkIsWUFBWSxVQUFVO0FBRXRCLFNBQVMsVUFBQUMsZUFBYzs7O0FDUHZCLFlBQVlDLFlBQVc7QUFFdkI7QUFBQSxFQUdDLGdCQUFBQztBQUFBLEVBQ0EsYUFBQUM7QUFBQSxPQUNNO0FBRVAsU0FBUyxNQUFNLFNBQUFDLGNBQTRCO0FBQzNDLFlBQVksYUFBYTtBQUN6QixT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QU8sTUFBTTtBQUNaLG9CQUFZLE1BQU07QUFBQSxNQUNuQjtBQUFBLElBQ0Q7QUFBQSxJQUNBLE9BQU8sRUFBRSxPQUFPLEdBQUcsR0FBMEI7QUFDNUMsVUFBSSxRQUFRLElBQUksVUFBVTtBQUFBLFFBQ3pCLE9BQU8sTUFBTSxJQUFJLGFBQWE7QUFBQSxRQUM5QjtBQUFBLE1BQ0QsQ0FBQztBQUNELGtCQUFZLFFBQVEsS0FBSztBQUN6QixNQUFBQyxRQUFPLE1BQU07QUFDWixjQUFNLElBQUksT0FBTyxNQUFNLE9BQU8sRUFBRTtBQUNoQyxjQUFNLGFBQWE7QUFBQSxNQUNwQixDQUFDO0FBQ0QsU0FBRyxZQUFZLE1BQU0sS0FBSyxDQUFDO0FBQUEsSUFDNUI7QUFBQSxFQUNEO0FBQ0Q7QUFFQSxTQUFTLGNBQWM7QUFDdEIsU0FBTyxPQUFPO0FBQUEsSUFDYixPQUFPLEtBQUssT0FBTyxFQUFFLElBQUksQ0FBQyxRQUFRLENBQUMsS0FBSyxNQUFNO0FBQUEsSUFBQyxDQUFDLENBQUM7QUFBQSxFQUNsRDtBQUNEOyIsCiAgIm5hbWVzIjogWyJRdWVyeSIsICJhcnJvdyIsICJlZmZlY3QiLCAiYXJyb3ciLCAiTW9zYWljQ2xpZW50IiwgIlNlbGVjdGlvbiIsICJRdWVyeSIsICJmb3JtYXQiLCAiYmlucyIsICJudWxsQ291bnQiLCAidHlwZSIsICJiaW4iLCAiTW9zYWljQ2xpZW50IiwgImNvdW50IiwgIlF1ZXJ5IiwgImVmZmVjdCIsICJkYXRhIiwgIk1vc2FpY0NsaWVudCIsICJRdWVyeSIsICJjb3VudCIsICJlZmZlY3QiLCAic2lnbmFsIiwgIk1vc2FpY0NsaWVudCIsICJjb3VudCIsICJRdWVyeSIsICJNb3NhaWNDbGllbnQiLCAic2lnbmFsIiwgIlNlbGVjdGlvbiIsICJjb2x1bW4iLCAiUXVlcnkiLCAiZXZlbnQiLCAiZm9ybWF0IiwgIlF1ZXJ5IiwgImVmZmVjdCJdCn0K
