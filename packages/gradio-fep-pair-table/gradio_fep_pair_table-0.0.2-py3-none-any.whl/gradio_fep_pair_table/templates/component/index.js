const {
  SvelteComponent: et,
  assign: tt,
  create_slot: it,
  detach: nt,
  element: rt,
  get_all_dirty_from_scope: at,
  get_slot_changes: st,
  get_spread_update: ot,
  init: lt,
  insert: ct,
  safe_not_equal: dt,
  set_dynamic_element_data: Ce,
  set_style: P,
  toggle_class: z,
  transition_in: Xe,
  transition_out: We,
  update_slot_base: ft
} = window.__gradio__svelte__internal;
function ut(i) {
  let e, t, n;
  const r = (
    /*#slots*/
    i[18].default
  ), a = it(
    r,
    i,
    /*$$scope*/
    i[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      i[7]
    ) },
    { id: (
      /*elem_id*/
      i[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      i[3].join(" ") + " svelte-nl1om8"
    }
  ], h = {};
  for (let o = 0; o < s.length; o += 1)
    h = tt(h, s[o]);
  return {
    c() {
      e = rt(
        /*tag*/
        i[14]
      ), a && a.c(), Ce(
        /*tag*/
        i[14]
      )(e, h), z(
        e,
        "hidden",
        /*visible*/
        i[10] === !1
      ), z(
        e,
        "padded",
        /*padding*/
        i[6]
      ), z(
        e,
        "border_focus",
        /*border_mode*/
        i[5] === "focus"
      ), z(
        e,
        "border_contrast",
        /*border_mode*/
        i[5] === "contrast"
      ), z(e, "hide-container", !/*explicit_call*/
      i[8] && !/*container*/
      i[9]), P(
        e,
        "height",
        /*get_dimension*/
        i[15](
          /*height*/
          i[0]
        )
      ), P(e, "width", typeof /*width*/
      i[1] == "number" ? `calc(min(${/*width*/
      i[1]}px, 100%))` : (
        /*get_dimension*/
        i[15](
          /*width*/
          i[1]
        )
      )), P(
        e,
        "border-style",
        /*variant*/
        i[4]
      ), P(
        e,
        "overflow",
        /*allow_overflow*/
        i[11] ? "visible" : "hidden"
      ), P(
        e,
        "flex-grow",
        /*scale*/
        i[12]
      ), P(e, "min-width", `calc(min(${/*min_width*/
      i[13]}px, 100%))`), P(e, "border-width", "var(--block-border-width)");
    },
    m(o, c) {
      ct(o, e, c), a && a.m(e, null), n = !0;
    },
    p(o, c) {
      a && a.p && (!n || c & /*$$scope*/
      131072) && ft(
        a,
        r,
        o,
        /*$$scope*/
        o[17],
        n ? st(
          r,
          /*$$scope*/
          o[17],
          c,
          null
        ) : at(
          /*$$scope*/
          o[17]
        ),
        null
      ), Ce(
        /*tag*/
        o[14]
      )(e, h = ot(s, [
        (!n || c & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!n || c & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!n || c & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), z(
        e,
        "hidden",
        /*visible*/
        o[10] === !1
      ), z(
        e,
        "padded",
        /*padding*/
        o[6]
      ), z(
        e,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), z(
        e,
        "border_contrast",
        /*border_mode*/
        o[5] === "contrast"
      ), z(e, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), c & /*height*/
      1 && P(
        e,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), c & /*width*/
      2 && P(e, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), c & /*variant*/
      16 && P(
        e,
        "border-style",
        /*variant*/
        o[4]
      ), c & /*allow_overflow*/
      2048 && P(
        e,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), c & /*scale*/
      4096 && P(
        e,
        "flex-grow",
        /*scale*/
        o[12]
      ), c & /*min_width*/
      8192 && P(e, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      n || (Xe(a, o), n = !0);
    },
    o(o) {
      We(a, o), n = !1;
    },
    d(o) {
      o && nt(e), a && a.d(o);
    }
  };
}
function ht(i) {
  let e, t = (
    /*tag*/
    i[14] && ut(i)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, r) {
      t && t.m(n, r), e = !0;
    },
    p(n, [r]) {
      /*tag*/
      n[14] && t.p(n, r);
    },
    i(n) {
      e || (Xe(t, n), e = !0);
    },
    o(n) {
      We(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function pt(i, e, t) {
  let { $$slots: n = {}, $$scope: r } = e, { height: a = void 0 } = e, { width: s = void 0 } = e, { elem_id: h = "" } = e, { elem_classes: o = [] } = e, { variant: c = "solid" } = e, { border_mode: v = "base" } = e, { padding: f = !0 } = e, { type: C = "normal" } = e, { test_id: u = void 0 } = e, { explicit_call: l = !1 } = e, { container: d = !0 } = e, { visible: _ = !0 } = e, { allow_overflow: w = !0 } = e, { scale: y = null } = e, { min_width: S = 0 } = e, k = C === "fieldset" ? "fieldset" : "div";
  const g = (p) => {
    if (p !== void 0) {
      if (typeof p == "number")
        return p + "px";
      if (typeof p == "string")
        return p;
    }
  };
  return i.$$set = (p) => {
    "height" in p && t(0, a = p.height), "width" in p && t(1, s = p.width), "elem_id" in p && t(2, h = p.elem_id), "elem_classes" in p && t(3, o = p.elem_classes), "variant" in p && t(4, c = p.variant), "border_mode" in p && t(5, v = p.border_mode), "padding" in p && t(6, f = p.padding), "type" in p && t(16, C = p.type), "test_id" in p && t(7, u = p.test_id), "explicit_call" in p && t(8, l = p.explicit_call), "container" in p && t(9, d = p.container), "visible" in p && t(10, _ = p.visible), "allow_overflow" in p && t(11, w = p.allow_overflow), "scale" in p && t(12, y = p.scale), "min_width" in p && t(13, S = p.min_width), "$$scope" in p && t(17, r = p.$$scope);
  }, [
    a,
    s,
    h,
    o,
    c,
    v,
    f,
    u,
    l,
    d,
    _,
    w,
    y,
    S,
    k,
    g,
    C,
    r,
    n
  ];
}
class vt extends et {
  constructor(e) {
    super(), lt(this, e, pt, ht, dt, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const mt = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Se = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
mt.reduce(
  (i, { color: e, primary: t, secondary: n }) => ({
    ...i,
    [e]: {
      primary: Se[e][t],
      secondary: Se[e][n]
    }
  }),
  {}
);
var ve = function(i, e) {
  return ve = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(t, n) {
    t.__proto__ = n;
  } || function(t, n) {
    for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r]);
  }, ve(i, e);
};
function ue(i, e) {
  if (typeof e != "function" && e !== null)
    throw new TypeError("Class extends value " + String(e) + " is not a constructor or null");
  ve(i, e);
  function t() {
    this.constructor = i;
  }
  i.prototype = e === null ? Object.create(e) : (t.prototype = e.prototype, new t());
}
var T = function() {
  return T = Object.assign || function(e) {
    for (var t, n = 1, r = arguments.length; n < r; n++) {
      t = arguments[n];
      for (var a in t) Object.prototype.hasOwnProperty.call(t, a) && (e[a] = t[a]);
    }
    return e;
  }, T.apply(this, arguments);
};
function V(i) {
  var e = typeof Symbol == "function" && Symbol.iterator, t = e && i[e], n = 0;
  if (t) return t.call(i);
  if (i && typeof i.length == "number") return {
    next: function() {
      return i && n >= i.length && (i = void 0), { value: i && i[n++], done: !i };
    }
  };
  throw new TypeError(e ? "Object is not iterable." : "Symbol.iterator is not defined.");
}
function gt(i, e) {
  var t = typeof Symbol == "function" && i[Symbol.iterator];
  if (!t) return i;
  var n = t.call(i), r, a = [], s;
  try {
    for (; (e === void 0 || e-- > 0) && !(r = n.next()).done; ) a.push(r.value);
  } catch (h) {
    s = { error: h };
  } finally {
    try {
      r && !r.done && (t = n.return) && t.call(n);
    } finally {
      if (s) throw s.error;
    }
  }
  return a;
}
function bt(i, e, t) {
  if (t || arguments.length === 2) for (var n = 0, r = e.length, a; n < r; n++)
    (a || !(n in e)) && (a || (a = Array.prototype.slice.call(e, 0, n)), a[n] = e[n]);
  return i.concat(a || Array.prototype.slice.call(e));
}
/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var Ve = (
  /** @class */
  function() {
    function i(e) {
      e === void 0 && (e = {}), this.adapter = e;
    }
    return Object.defineProperty(i, "cssClasses", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(i, "strings", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(i, "numbers", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(i, "defaultAdapter", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), i.prototype.init = function() {
    }, i.prototype.destroy = function() {
    }, i;
  }()
);
/**
 * @license
 * Copyright 2019 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function _t(i) {
  return i === void 0 && (i = window), yt(i) ? { passive: !0 } : !1;
}
function yt(i) {
  i === void 0 && (i = window);
  var e = !1;
  try {
    var t = {
      // This function will be called when the browser
      // attempts to access the passive property.
      get passive() {
        return e = !0, !1;
      }
    }, n = function() {
    };
    i.document.addEventListener("test", n, t), i.document.removeEventListener("test", n, t);
  } catch {
    e = !1;
  }
  return e;
}
const wt = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  applyPassive: _t
}, Symbol.toStringTag, { value: "Module" }));
/**
 * @license
 * Copyright 2018 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function Ct(i, e) {
  if (i.closest)
    return i.closest(e);
  for (var t = i; t; ) {
    if (xe(t, e))
      return t;
    t = t.parentElement;
  }
  return null;
}
function xe(i, e) {
  var t = i.matches || i.webkitMatchesSelector || i.msMatchesSelector;
  return t.call(i, e);
}
function St(i) {
  var e = i;
  if (e.offsetParent !== null)
    return e.scrollWidth;
  var t = e.cloneNode(!0);
  t.style.setProperty("position", "absolute"), t.style.setProperty("transform", "translate(-9999px, -9999px)"), document.documentElement.appendChild(t);
  var n = t.scrollWidth;
  return document.documentElement.removeChild(t), n;
}
const At = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  closest: Ct,
  estimateScrollWidth: St,
  matches: xe
}, Symbol.toStringTag, { value: "Module" }));
/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var kt = {
  // Ripple is a special case where the "root" component is really a "mixin" of sorts,
  // given that it's an 'upgrade' to an existing component. That being said it is the root
  // CSS class that all other CSS classes derive from.
  BG_FOCUSED: "mdc-ripple-upgraded--background-focused",
  FG_ACTIVATION: "mdc-ripple-upgraded--foreground-activation",
  FG_DEACTIVATION: "mdc-ripple-upgraded--foreground-deactivation",
  ROOT: "mdc-ripple-upgraded",
  UNBOUNDED: "mdc-ripple-upgraded--unbounded"
}, Dt = {
  VAR_FG_SCALE: "--mdc-ripple-fg-scale",
  VAR_FG_SIZE: "--mdc-ripple-fg-size",
  VAR_FG_TRANSLATE_END: "--mdc-ripple-fg-translate-end",
  VAR_FG_TRANSLATE_START: "--mdc-ripple-fg-translate-start",
  VAR_LEFT: "--mdc-ripple-left",
  VAR_TOP: "--mdc-ripple-top"
}, Ae = {
  DEACTIVATION_TIMEOUT_MS: 225,
  FG_DEACTIVATION_MS: 150,
  INITIAL_ORIGIN_SCALE: 0.6,
  PADDING: 10,
  TAP_DELAY_MS: 300
  // Delay between touch and simulated mouse events on touch devices
}, ee;
function Mt(i, e) {
  e === void 0 && (e = !1);
  var t = i.CSS, n = ee;
  if (typeof ee == "boolean" && !e)
    return ee;
  var r = t && typeof t.supports == "function";
  if (!r)
    return !1;
  var a = t.supports("--css-vars", "yes"), s = t.supports("(--css-vars: yes)") && t.supports("color", "#00000000");
  return n = a || s, e || (ee = n), n;
}
function Ot(i, e, t) {
  if (!i)
    return { x: 0, y: 0 };
  var n = e.x, r = e.y, a = n + t.left, s = r + t.top, h, o;
  if (i.type === "touchstart") {
    var c = i;
    h = c.changedTouches[0].pageX - a, o = c.changedTouches[0].pageY - s;
  } else {
    var v = i;
    h = v.pageX - a, o = v.pageY - s;
  }
  return { x: h, y: o };
}
/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var ke = [
  "touchstart",
  "pointerdown",
  "mousedown",
  "keydown"
], De = [
  "touchend",
  "pointerup",
  "mouseup",
  "contextmenu"
], te = [], Rt = (
  /** @class */
  function(i) {
    ue(e, i);
    function e(t) {
      var n = i.call(this, T(T({}, e.defaultAdapter), t)) || this;
      return n.activationAnimationHasEnded = !1, n.activationTimer = 0, n.fgDeactivationRemovalTimer = 0, n.fgScale = "0", n.frame = { width: 0, height: 0 }, n.initialSize = 0, n.layoutFrame = 0, n.maxRadius = 0, n.unboundedCoords = { left: 0, top: 0 }, n.activationState = n.defaultActivationState(), n.activationTimerCallback = function() {
        n.activationAnimationHasEnded = !0, n.runDeactivationUXLogicIfReady();
      }, n.activateHandler = function(r) {
        n.activateImpl(r);
      }, n.deactivateHandler = function() {
        n.deactivateImpl();
      }, n.focusHandler = function() {
        n.handleFocus();
      }, n.blurHandler = function() {
        n.handleBlur();
      }, n.resizeHandler = function() {
        n.layout();
      }, n;
    }
    return Object.defineProperty(e, "cssClasses", {
      get: function() {
        return kt;
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(e, "strings", {
      get: function() {
        return Dt;
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(e, "numbers", {
      get: function() {
        return Ae;
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(e, "defaultAdapter", {
      get: function() {
        return {
          addClass: function() {
          },
          browserSupportsCssVars: function() {
            return !0;
          },
          computeBoundingRect: function() {
            return { top: 0, right: 0, bottom: 0, left: 0, width: 0, height: 0 };
          },
          containsEventTarget: function() {
            return !0;
          },
          deregisterDocumentInteractionHandler: function() {
          },
          deregisterInteractionHandler: function() {
          },
          deregisterResizeHandler: function() {
          },
          getWindowPageOffset: function() {
            return { x: 0, y: 0 };
          },
          isSurfaceActive: function() {
            return !0;
          },
          isSurfaceDisabled: function() {
            return !0;
          },
          isUnbounded: function() {
            return !0;
          },
          registerDocumentInteractionHandler: function() {
          },
          registerInteractionHandler: function() {
          },
          registerResizeHandler: function() {
          },
          removeClass: function() {
          },
          updateCssVariable: function() {
          }
        };
      },
      enumerable: !1,
      configurable: !0
    }), e.prototype.init = function() {
      var t = this, n = this.supportsPressRipple();
      if (this.registerRootHandlers(n), n) {
        var r = e.cssClasses, a = r.ROOT, s = r.UNBOUNDED;
        requestAnimationFrame(function() {
          t.adapter.addClass(a), t.adapter.isUnbounded() && (t.adapter.addClass(s), t.layoutInternal());
        });
      }
    }, e.prototype.destroy = function() {
      var t = this;
      if (this.supportsPressRipple()) {
        this.activationTimer && (clearTimeout(this.activationTimer), this.activationTimer = 0, this.adapter.removeClass(e.cssClasses.FG_ACTIVATION)), this.fgDeactivationRemovalTimer && (clearTimeout(this.fgDeactivationRemovalTimer), this.fgDeactivationRemovalTimer = 0, this.adapter.removeClass(e.cssClasses.FG_DEACTIVATION));
        var n = e.cssClasses, r = n.ROOT, a = n.UNBOUNDED;
        requestAnimationFrame(function() {
          t.adapter.removeClass(r), t.adapter.removeClass(a), t.removeCssVars();
        });
      }
      this.deregisterRootHandlers(), this.deregisterDeactivationHandlers();
    }, e.prototype.activate = function(t) {
      this.activateImpl(t);
    }, e.prototype.deactivate = function() {
      this.deactivateImpl();
    }, e.prototype.layout = function() {
      var t = this;
      this.layoutFrame && cancelAnimationFrame(this.layoutFrame), this.layoutFrame = requestAnimationFrame(function() {
        t.layoutInternal(), t.layoutFrame = 0;
      });
    }, e.prototype.setUnbounded = function(t) {
      var n = e.cssClasses.UNBOUNDED;
      t ? this.adapter.addClass(n) : this.adapter.removeClass(n);
    }, e.prototype.handleFocus = function() {
      var t = this;
      requestAnimationFrame(function() {
        return t.adapter.addClass(e.cssClasses.BG_FOCUSED);
      });
    }, e.prototype.handleBlur = function() {
      var t = this;
      requestAnimationFrame(function() {
        return t.adapter.removeClass(e.cssClasses.BG_FOCUSED);
      });
    }, e.prototype.supportsPressRipple = function() {
      return this.adapter.browserSupportsCssVars();
    }, e.prototype.defaultActivationState = function() {
      return {
        activationEvent: void 0,
        hasDeactivationUXRun: !1,
        isActivated: !1,
        isProgrammatic: !1,
        wasActivatedByPointer: !1,
        wasElementMadeActive: !1
      };
    }, e.prototype.registerRootHandlers = function(t) {
      var n, r;
      if (t) {
        try {
          for (var a = V(ke), s = a.next(); !s.done; s = a.next()) {
            var h = s.value;
            this.adapter.registerInteractionHandler(h, this.activateHandler);
          }
        } catch (o) {
          n = { error: o };
        } finally {
          try {
            s && !s.done && (r = a.return) && r.call(a);
          } finally {
            if (n) throw n.error;
          }
        }
        this.adapter.isUnbounded() && this.adapter.registerResizeHandler(this.resizeHandler);
      }
      this.adapter.registerInteractionHandler("focus", this.focusHandler), this.adapter.registerInteractionHandler("blur", this.blurHandler);
    }, e.prototype.registerDeactivationHandlers = function(t) {
      var n, r;
      if (t.type === "keydown")
        this.adapter.registerInteractionHandler("keyup", this.deactivateHandler);
      else
        try {
          for (var a = V(De), s = a.next(); !s.done; s = a.next()) {
            var h = s.value;
            this.adapter.registerDocumentInteractionHandler(h, this.deactivateHandler);
          }
        } catch (o) {
          n = { error: o };
        } finally {
          try {
            s && !s.done && (r = a.return) && r.call(a);
          } finally {
            if (n) throw n.error;
          }
        }
    }, e.prototype.deregisterRootHandlers = function() {
      var t, n;
      try {
        for (var r = V(ke), a = r.next(); !a.done; a = r.next()) {
          var s = a.value;
          this.adapter.deregisterInteractionHandler(s, this.activateHandler);
        }
      } catch (h) {
        t = { error: h };
      } finally {
        try {
          a && !a.done && (n = r.return) && n.call(r);
        } finally {
          if (t) throw t.error;
        }
      }
      this.adapter.deregisterInteractionHandler("focus", this.focusHandler), this.adapter.deregisterInteractionHandler("blur", this.blurHandler), this.adapter.isUnbounded() && this.adapter.deregisterResizeHandler(this.resizeHandler);
    }, e.prototype.deregisterDeactivationHandlers = function() {
      var t, n;
      this.adapter.deregisterInteractionHandler("keyup", this.deactivateHandler);
      try {
        for (var r = V(De), a = r.next(); !a.done; a = r.next()) {
          var s = a.value;
          this.adapter.deregisterDocumentInteractionHandler(s, this.deactivateHandler);
        }
      } catch (h) {
        t = { error: h };
      } finally {
        try {
          a && !a.done && (n = r.return) && n.call(r);
        } finally {
          if (t) throw t.error;
        }
      }
    }, e.prototype.removeCssVars = function() {
      var t = this, n = e.strings, r = Object.keys(n);
      r.forEach(function(a) {
        a.indexOf("VAR_") === 0 && t.adapter.updateCssVariable(n[a], null);
      });
    }, e.prototype.activateImpl = function(t) {
      var n = this;
      if (!this.adapter.isSurfaceDisabled()) {
        var r = this.activationState;
        if (!r.isActivated) {
          var a = this.previousActivationEvent, s = a && t !== void 0 && a.type !== t.type;
          if (!s) {
            r.isActivated = !0, r.isProgrammatic = t === void 0, r.activationEvent = t, r.wasActivatedByPointer = r.isProgrammatic ? !1 : t !== void 0 && (t.type === "mousedown" || t.type === "touchstart" || t.type === "pointerdown");
            var h = t !== void 0 && te.length > 0 && te.some(function(o) {
              return n.adapter.containsEventTarget(o);
            });
            if (h) {
              this.resetActivationState();
              return;
            }
            t !== void 0 && (te.push(t.target), this.registerDeactivationHandlers(t)), r.wasElementMadeActive = this.checkElementMadeActive(t), r.wasElementMadeActive && this.animateActivation(), requestAnimationFrame(function() {
              te = [], !r.wasElementMadeActive && t !== void 0 && (t.key === " " || t.keyCode === 32) && (r.wasElementMadeActive = n.checkElementMadeActive(t), r.wasElementMadeActive && n.animateActivation()), r.wasElementMadeActive || (n.activationState = n.defaultActivationState());
            });
          }
        }
      }
    }, e.prototype.checkElementMadeActive = function(t) {
      return t !== void 0 && t.type === "keydown" ? this.adapter.isSurfaceActive() : !0;
    }, e.prototype.animateActivation = function() {
      var t = this, n = e.strings, r = n.VAR_FG_TRANSLATE_START, a = n.VAR_FG_TRANSLATE_END, s = e.cssClasses, h = s.FG_DEACTIVATION, o = s.FG_ACTIVATION, c = e.numbers.DEACTIVATION_TIMEOUT_MS;
      this.layoutInternal();
      var v = "", f = "";
      if (!this.adapter.isUnbounded()) {
        var C = this.getFgTranslationCoordinates(), u = C.startPoint, l = C.endPoint;
        v = u.x + "px, " + u.y + "px", f = l.x + "px, " + l.y + "px";
      }
      this.adapter.updateCssVariable(r, v), this.adapter.updateCssVariable(a, f), clearTimeout(this.activationTimer), clearTimeout(this.fgDeactivationRemovalTimer), this.rmBoundedActivationClasses(), this.adapter.removeClass(h), this.adapter.computeBoundingRect(), this.adapter.addClass(o), this.activationTimer = setTimeout(function() {
        t.activationTimerCallback();
      }, c);
    }, e.prototype.getFgTranslationCoordinates = function() {
      var t = this.activationState, n = t.activationEvent, r = t.wasActivatedByPointer, a;
      r ? a = Ot(n, this.adapter.getWindowPageOffset(), this.adapter.computeBoundingRect()) : a = {
        x: this.frame.width / 2,
        y: this.frame.height / 2
      }, a = {
        x: a.x - this.initialSize / 2,
        y: a.y - this.initialSize / 2
      };
      var s = {
        x: this.frame.width / 2 - this.initialSize / 2,
        y: this.frame.height / 2 - this.initialSize / 2
      };
      return { startPoint: a, endPoint: s };
    }, e.prototype.runDeactivationUXLogicIfReady = function() {
      var t = this, n = e.cssClasses.FG_DEACTIVATION, r = this.activationState, a = r.hasDeactivationUXRun, s = r.isActivated, h = a || !s;
      h && this.activationAnimationHasEnded && (this.rmBoundedActivationClasses(), this.adapter.addClass(n), this.fgDeactivationRemovalTimer = setTimeout(function() {
        t.adapter.removeClass(n);
      }, Ae.FG_DEACTIVATION_MS));
    }, e.prototype.rmBoundedActivationClasses = function() {
      var t = e.cssClasses.FG_ACTIVATION;
      this.adapter.removeClass(t), this.activationAnimationHasEnded = !1, this.adapter.computeBoundingRect();
    }, e.prototype.resetActivationState = function() {
      var t = this;
      this.previousActivationEvent = this.activationState.activationEvent, this.activationState = this.defaultActivationState(), setTimeout(function() {
        return t.previousActivationEvent = void 0;
      }, e.numbers.TAP_DELAY_MS);
    }, e.prototype.deactivateImpl = function() {
      var t = this, n = this.activationState;
      if (n.isActivated) {
        var r = T({}, n);
        n.isProgrammatic ? (requestAnimationFrame(function() {
          t.animateDeactivation(r);
        }), this.resetActivationState()) : (this.deregisterDeactivationHandlers(), requestAnimationFrame(function() {
          t.activationState.hasDeactivationUXRun = !0, t.animateDeactivation(r), t.resetActivationState();
        }));
      }
    }, e.prototype.animateDeactivation = function(t) {
      var n = t.wasActivatedByPointer, r = t.wasElementMadeActive;
      (n || r) && this.runDeactivationUXLogicIfReady();
    }, e.prototype.layoutInternal = function() {
      var t = this;
      this.frame = this.adapter.computeBoundingRect();
      var n = Math.max(this.frame.height, this.frame.width), r = function() {
        var s = Math.sqrt(Math.pow(t.frame.width, 2) + Math.pow(t.frame.height, 2));
        return s + e.numbers.PADDING;
      };
      this.maxRadius = this.adapter.isUnbounded() ? n : r();
      var a = Math.floor(n * e.numbers.INITIAL_ORIGIN_SCALE);
      this.adapter.isUnbounded() && a % 2 !== 0 ? this.initialSize = a - 1 : this.initialSize = a, this.fgScale = "" + this.maxRadius / this.initialSize, this.updateLayoutCssVars();
    }, e.prototype.updateLayoutCssVars = function() {
      var t = e.strings, n = t.VAR_FG_SIZE, r = t.VAR_LEFT, a = t.VAR_TOP, s = t.VAR_FG_SCALE;
      this.adapter.updateCssVariable(n, this.initialSize + "px"), this.adapter.updateCssVariable(s, this.fgScale), this.adapter.isUnbounded() && (this.unboundedCoords = {
        left: Math.round(this.frame.width / 2 - this.initialSize / 2),
        top: Math.round(this.frame.height / 2 - this.initialSize / 2)
      }, this.adapter.updateCssVariable(r, this.unboundedCoords.left + "px"), this.adapter.updateCssVariable(a, this.unboundedCoords.top + "px"));
    }, e;
  }(Ve)
);
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var Z;
(function(i) {
  i.PROCESSING = "mdc-switch--processing", i.SELECTED = "mdc-switch--selected", i.UNSELECTED = "mdc-switch--unselected";
})(Z || (Z = {}));
var Me;
(function(i) {
  i.RIPPLE = ".mdc-switch__ripple";
})(Me || (Me = {}));
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function Ft(i, e, t) {
  var n = Ht(i, e), r = n.getObservers(e);
  return r.push(t), function() {
    r.splice(r.indexOf(t), 1);
  };
}
var se = /* @__PURE__ */ new WeakMap();
function Ht(i, e) {
  var t = /* @__PURE__ */ new Map();
  se.has(i) || se.set(i, {
    isEnabled: !0,
    getObservers: function(c) {
      var v = t.get(c) || [];
      return t.has(c) || t.set(c, v), v;
    },
    installedProperties: /* @__PURE__ */ new Set()
  });
  var n = se.get(i);
  if (n.installedProperties.has(e))
    return n;
  var r = Lt(i, e) || {
    configurable: !0,
    enumerable: !0,
    value: i[e],
    writable: !0
  }, a = T({}, r), s = r.get, h = r.set;
  if ("value" in r) {
    delete a.value, delete a.writable;
    var o = r.value;
    s = function() {
      return o;
    }, r.writable && (h = function(c) {
      o = c;
    });
  }
  return s && (a.get = function() {
    return s.call(this);
  }), h && (a.set = function(c) {
    var v, f, C = s ? s.call(this) : c;
    if (h.call(this, c), n.isEnabled && (!s || c !== C))
      try {
        for (var u = V(n.getObservers(e)), l = u.next(); !l.done; l = u.next()) {
          var d = l.value;
          d(c, C);
        }
      } catch (_) {
        v = { error: _ };
      } finally {
        try {
          l && !l.done && (f = u.return) && f.call(u);
        } finally {
          if (v) throw v.error;
        }
      }
  }), n.installedProperties.add(e), Object.defineProperty(i, e, a), n;
}
function Lt(i, e) {
  for (var t = i, n; t && (n = Object.getOwnPropertyDescriptor(t, e), !n); )
    t = Object.getPrototypeOf(t);
  return n;
}
function Ut(i, e) {
  var t = se.get(i);
  t && (t.isEnabled = e);
}
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var It = (
  /** @class */
  function(i) {
    ue(e, i);
    function e(t) {
      var n = i.call(this, t) || this;
      return n.unobserves = /* @__PURE__ */ new Set(), n;
    }
    return e.prototype.destroy = function() {
      i.prototype.destroy.call(this), this.unobserve();
    }, e.prototype.observe = function(t, n) {
      var r, a, s = this, h = [];
      try {
        for (var o = V(Object.keys(n)), c = o.next(); !c.done; c = o.next()) {
          var v = c.value, f = n[v].bind(this);
          h.push(this.observeProperty(t, v, f));
        }
      } catch (u) {
        r = { error: u };
      } finally {
        try {
          c && !c.done && (a = o.return) && a.call(o);
        } finally {
          if (r) throw r.error;
        }
      }
      var C = function() {
        var u, l;
        try {
          for (var d = V(h), _ = d.next(); !_.done; _ = d.next()) {
            var w = _.value;
            w();
          }
        } catch (y) {
          u = { error: y };
        } finally {
          try {
            _ && !_.done && (l = d.return) && l.call(d);
          } finally {
            if (u) throw u.error;
          }
        }
        s.unobserves.delete(C);
      };
      return this.unobserves.add(C), C;
    }, e.prototype.observeProperty = function(t, n, r) {
      return Ft(t, n, r);
    }, e.prototype.setObserversEnabled = function(t, n) {
      Ut(t, n);
    }, e.prototype.unobserve = function() {
      var t, n;
      try {
        for (var r = V(bt([], gt(this.unobserves))), a = r.next(); !a.done; a = r.next()) {
          var s = a.value;
          s();
        }
      } catch (h) {
        t = { error: h };
      } finally {
        try {
          a && !a.done && (n = r.return) && n.call(r);
        } finally {
          if (t) throw t.error;
        }
      }
    }, e;
  }(Ve)
);
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var Et = (
  /** @class */
  function(i) {
    ue(e, i);
    function e(t) {
      var n = i.call(this, t) || this;
      return n.handleClick = n.handleClick.bind(n), n;
    }
    return e.prototype.init = function() {
      this.observe(this.adapter.state, {
        disabled: this.stopProcessingIfDisabled,
        processing: this.stopProcessingIfDisabled
      });
    }, e.prototype.handleClick = function() {
      this.adapter.state.disabled || (this.adapter.state.selected = !this.adapter.state.selected);
    }, e.prototype.stopProcessingIfDisabled = function() {
      this.adapter.state.disabled && (this.adapter.state.processing = !1);
    }, e;
  }(It)
), Pt = (
  /** @class */
  function(i) {
    ue(e, i);
    function e() {
      return i !== null && i.apply(this, arguments) || this;
    }
    return e.prototype.init = function() {
      i.prototype.init.call(this), this.observe(this.adapter.state, {
        disabled: this.onDisabledChange,
        processing: this.onProcessingChange,
        selected: this.onSelectedChange
      });
    }, e.prototype.initFromDOM = function() {
      this.setObserversEnabled(this.adapter.state, !1), this.adapter.state.selected = this.adapter.hasClass(Z.SELECTED), this.onSelectedChange(), this.adapter.state.disabled = this.adapter.isDisabled(), this.adapter.state.processing = this.adapter.hasClass(Z.PROCESSING), this.setObserversEnabled(this.adapter.state, !0), this.stopProcessingIfDisabled();
    }, e.prototype.onDisabledChange = function() {
      this.adapter.setDisabled(this.adapter.state.disabled);
    }, e.prototype.onProcessingChange = function() {
      this.toggleClass(this.adapter.state.processing, Z.PROCESSING);
    }, e.prototype.onSelectedChange = function() {
      this.adapter.setAriaChecked(String(this.adapter.state.selected)), this.toggleClass(this.adapter.state.selected, Z.SELECTED), this.toggleClass(!this.adapter.state.selected, Z.UNSELECTED);
    }, e.prototype.toggleClass = function(t, n) {
      t ? this.adapter.addClass(n) : this.adapter.removeClass(n);
    }, e;
  }(Et)
);
function le(i) {
  return Object.entries(i).filter(([e, t]) => e !== "" && t).map(([e]) => e).join(" ");
}
function ie(i, e, t, n = { bubbles: !0 }, r = !1) {
  if (typeof Event > "u")
    throw new Error("Event not defined.");
  if (!i)
    throw new Error("Tried to dipatch event without element.");
  const a = new CustomEvent(e, Object.assign(Object.assign({}, n), { detail: t }));
  if (i == null || i.dispatchEvent(a), r && e.startsWith("SMUI")) {
    const s = new CustomEvent(e.replace(/^SMUI/g, () => "MDC"), Object.assign(Object.assign({}, n), { detail: t }));
    i == null || i.dispatchEvent(s), s.defaultPrevented && a.preventDefault();
  }
  return a;
}
function Oe(i, e) {
  let t = Object.getOwnPropertyNames(i);
  const n = {};
  for (let r = 0; r < t.length; r++) {
    const a = t[r], s = a.indexOf("$");
    s !== -1 && e.indexOf(a.substring(0, s + 1)) !== -1 || e.indexOf(a) === -1 && (n[a] = i[a]);
  }
  return n;
}
const Re = /^[a-z]+(?::(?:preventDefault|stopPropagation|passive|nonpassive|capture|once|self))+$/, jt = /^[^$]+(?:\$(?:preventDefault|stopPropagation|passive|nonpassive|capture|once|self))+$/;
function Gt(i) {
  let e, t = [];
  i.$on = (r, a) => {
    let s = r, h = () => {
    };
    return e ? h = e(s, a) : t.push([s, a]), s.match(Re) && console && console.warn('Event modifiers in SMUI now use "$" instead of ":", so that all events can be bound with modifiers. Please update your event binding: ', s), () => {
      h();
    };
  };
  function n(r) {
    const a = i.$$.callbacks[r.type];
    a && a.slice().forEach((s) => s.call(this, r));
  }
  return (r) => {
    const a = [], s = {};
    e = (h, o) => {
      let c = h, v = o, f = !1;
      const C = c.match(Re), u = c.match(jt), l = C || u;
      if (c.match(/^SMUI:\w+:/)) {
        const w = c.split(":");
        let y = "";
        for (let S = 0; S < w.length; S++)
          y += S === w.length - 1 ? ":" + w[S] : w[S].split("-").map((k) => k.slice(0, 1).toUpperCase() + k.slice(1)).join("");
        console.warn(`The event ${c.split("$")[0]} has been renamed to ${y.split("$")[0]}.`), c = y;
      }
      if (l) {
        const w = c.split(C ? ":" : "$");
        c = w[0];
        const y = w.slice(1).reduce((S, k) => (S[k] = !0, S), {});
        y.passive && (f = f || {}, f.passive = !0), y.nonpassive && (f = f || {}, f.passive = !1), y.capture && (f = f || {}, f.capture = !0), y.once && (f = f || {}, f.once = !0), y.preventDefault && (v = Bt(v)), y.stopPropagation && (v = zt(v)), y.stopImmediatePropagation && (v = qt(v)), y.self && (v = Xt(r, v)), y.trusted && (v = Wt(v));
      }
      const d = Fe(r, c, v, f), _ = () => {
        d();
        const w = a.indexOf(_);
        w > -1 && a.splice(w, 1);
      };
      return a.push(_), c in s || (s[c] = Fe(r, c, n)), _;
    };
    for (let h = 0; h < t.length; h++)
      e(t[h][0], t[h][1]);
    return {
      destroy: () => {
        for (let h = 0; h < a.length; h++)
          a[h]();
        for (let h of Object.entries(s))
          h[1]();
      }
    };
  };
}
function Fe(i, e, t, n) {
  return i.addEventListener(e, t, n), () => i.removeEventListener(e, t, n);
}
function Bt(i) {
  return function(e) {
    return e.preventDefault(), i.call(this, e);
  };
}
function zt(i) {
  return function(e) {
    return e.stopPropagation(), i.call(this, e);
  };
}
function qt(i) {
  return function(e) {
    return e.stopImmediatePropagation(), i.call(this, e);
  };
}
function Xt(i, e) {
  return function(t) {
    if (t.target === i)
      return e.call(this, t);
  };
}
function Wt(i) {
  return function(e) {
    if (e.isTrusted)
      return i.call(this, e);
  };
}
function He(i, e) {
  let t = Object.getOwnPropertyNames(i);
  const n = {};
  for (let r = 0; r < t.length; r++) {
    const a = t[r];
    a.substring(0, e.length) === e && (n[a.substring(e.length)] = i[a]);
  }
  return n;
}
function Ze(i, e) {
  let t = [];
  if (e)
    for (let n = 0; n < e.length; n++) {
      const r = e[n], a = Array.isArray(r) ? r[0] : r;
      Array.isArray(r) && r.length > 1 ? t.push(a(i, r[1])) : t.push(a(i));
    }
  return {
    update(n) {
      if ((n && n.length || 0) != t.length)
        throw new Error("You must not change the length of an actions array.");
      if (n)
        for (let r = 0; r < n.length; r++) {
          const a = t[r];
          if (a && a.update) {
            const s = n[r];
            Array.isArray(s) && s.length > 1 ? a.update(s[1]) : a.update();
          }
        }
    },
    destroy() {
      for (let n = 0; n < t.length; n++) {
        const r = t[n];
        r && r.destroy && r.destroy();
      }
    }
  };
}
const { getContext: Vt } = window.__gradio__svelte__internal, { applyPassive: ne } = wt, { matches: xt } = At;
function Zt(i, { ripple: e = !0, surface: t = !1, unbounded: n = !1, disabled: r = !1, color: a, active: s, rippleElement: h, eventTarget: o, activeTarget: c, addClass: v = (l) => i.classList.add(l), removeClass: f = (l) => i.classList.remove(l), addStyle: C = (l, d) => i.style.setProperty(l, d), initPromise: u = Promise.resolve() } = {}) {
  let l, d = Vt("SMUI:addLayoutListener"), _, w = s, y = o, S = c;
  function k() {
    t ? (v("mdc-ripple-surface"), a === "primary" ? (v("smui-ripple-surface--primary"), f("smui-ripple-surface--secondary")) : a === "secondary" ? (f("smui-ripple-surface--primary"), v("smui-ripple-surface--secondary")) : (f("smui-ripple-surface--primary"), f("smui-ripple-surface--secondary"))) : (f("mdc-ripple-surface"), f("smui-ripple-surface--primary"), f("smui-ripple-surface--secondary")), l && w !== s && (w = s, s ? l.activate() : s === !1 && l.deactivate()), e && !l ? (l = new Rt({
      addClass: v,
      browserSupportsCssVars: () => Mt(window),
      computeBoundingRect: () => (h || i).getBoundingClientRect(),
      containsEventTarget: (p) => i.contains(p),
      deregisterDocumentInteractionHandler: (p, A) => document.documentElement.removeEventListener(p, A, ne()),
      deregisterInteractionHandler: (p, A) => (o || i).removeEventListener(p, A, ne()),
      deregisterResizeHandler: (p) => window.removeEventListener("resize", p),
      getWindowPageOffset: () => ({
        x: window.pageXOffset,
        y: window.pageYOffset
      }),
      isSurfaceActive: () => s ?? xt(c || i, ":active"),
      isSurfaceDisabled: () => !!r,
      isUnbounded: () => !!n,
      registerDocumentInteractionHandler: (p, A) => document.documentElement.addEventListener(p, A, ne()),
      registerInteractionHandler: (p, A) => (o || i).addEventListener(p, A, ne()),
      registerResizeHandler: (p) => window.addEventListener("resize", p),
      removeClass: f,
      updateCssVariable: C
    }), u.then(() => {
      l && (l.init(), l.setUnbounded(n));
    })) : l && !e && u.then(() => {
      l && (l.destroy(), l = void 0);
    }), l && (y !== o || S !== c) && (y = o, S = c, l.destroy(), requestAnimationFrame(() => {
      l && (l.init(), l.setUnbounded(n));
    })), !e && n && v("mdc-ripple-upgraded--unbounded");
  }
  k(), d && (_ = d(g));
  function g() {
    l && l.layout();
  }
  return {
    update(p) {
      ({
        ripple: e,
        surface: t,
        unbounded: n,
        disabled: r,
        color: a,
        active: s,
        rippleElement: h,
        eventTarget: o,
        activeTarget: c,
        addClass: v,
        removeClass: f,
        addStyle: C,
        initPromise: u
      } = Object.assign({ ripple: !0, surface: !1, unbounded: !1, disabled: !1, color: void 0, active: void 0, rippleElement: void 0, eventTarget: void 0, activeTarget: void 0, addClass: (A) => i.classList.add(A), removeClass: (A) => i.classList.remove(A), addStyle: (A, q) => i.style.setProperty(A, q), initPromise: Promise.resolve() }, p)), k();
    },
    destroy() {
      l && (l.destroy(), l = void 0, f("mdc-ripple-surface"), f("smui-ripple-surface--primary"), f("smui-ripple-surface--secondary")), _ && _();
    }
  };
}
const {
  SvelteComponent: Jt,
  action_destroyer: oe,
  append: U,
  assign: ce,
  attr: G,
  binding_callbacks: Le,
  compute_rest_props: Ue,
  detach: ge,
  element: W,
  exclude_internal_props: Kt,
  get_spread_update: Je,
  init: Qt,
  insert: be,
  is_function: me,
  listen: Tt,
  noop: Ie,
  run_all: Nt,
  safe_not_equal: Yt,
  set_attributes: de,
  space: N,
  svg_element: re
} = window.__gradio__svelte__internal, { onMount: $t, getContext: ei } = window.__gradio__svelte__internal, { get_current_component: ti } = window.__gradio__svelte__internal;
function Ee(i) {
  let e, t, n, r, a, s, h, o, c, v, f = [
    {
      class: h = le({
        [
          /*icons$class*/
          i[8]
        ]: !0,
        "mdc-switch__icons": !0
      })
    },
    He(
      /*$$restProps*/
      i[19],
      "icons$"
    )
  ], C = {};
  for (let u = 0; u < f.length; u += 1)
    C = ce(C, f[u]);
  return {
    c() {
      e = W("div"), t = re("svg"), n = re("path"), r = N(), a = re("svg"), s = re("path"), G(n, "d", "M19.69,5.23L8.96,15.96l-4.23-4.23L2.96,13.5l6,6L21.46,7L19.69,5.23z"), G(t, "class", "mdc-switch__icon mdc-switch__icon--on"), G(t, "viewBox", "0 0 24 24"), G(s, "d", "M20 13H4v-2h16v2z"), G(a, "class", "mdc-switch__icon mdc-switch__icon--off"), G(a, "viewBox", "0 0 24 24"), de(e, C);
    },
    m(u, l) {
      be(u, e, l), U(e, t), U(t, n), U(e, r), U(e, a), U(a, s), c || (v = oe(o = Ze.call(
        null,
        e,
        /*icons$use*/
        i[7]
      )), c = !0);
    },
    p(u, l) {
      de(e, C = Je(f, [
        l[0] & /*icons$class*/
        256 && h !== (h = le({
          [
            /*icons$class*/
            u[8]
          ]: !0,
          "mdc-switch__icons": !0
        })) && { class: h },
        l[0] & /*$$restProps*/
        524288 && He(
          /*$$restProps*/
          u[19],
          "icons$"
        )
      ])), o && me(o.update) && l[0] & /*icons$use*/
      128 && o.update.call(
        null,
        /*icons$use*/
        u[7]
      );
    },
    d(u) {
      u && ge(e), c = !1, v();
    }
  };
}
function Pe(i) {
  let e;
  return {
    c() {
      e = W("div"), e.innerHTML = '<div class="mdc-switch__focus-ring"></div>', G(e, "class", "mdc-switch__focus-ring-wrapper");
    },
    m(t, n) {
      be(t, e, n);
    },
    d(t) {
      t && ge(e);
    }
  };
}
function ii(i) {
  let e, t, n, r, a, s, h, o, c, v, f, C, u, l, d, _, w = (
    /*icons*/
    i[6] && Ee(i)
  ), y = (
    /*focusRing*/
    i[4] && Pe()
  ), S = [
    {
      class: f = le({
        [
          /*className*/
          i[3]
        ]: !0,
        "mdc-switch": !0,
        "mdc-switch--unselected": !/*selected*/
        i[10],
        "mdc-switch--selected": (
          /*selected*/
          i[10]
        ),
        "mdc-switch--processing": (
          /*processing*/
          i[1]
        ),
        "smui-switch--color-secondary": (
          /*color*/
          i[5] === "secondary"
        ),
        .../*internalClasses*/
        i[12]
      })
    },
    { type: "button" },
    { role: "switch" },
    {
      "aria-checked": C = /*selected*/
      i[10] ? "true" : "false"
    },
    { disabled: (
      /*disabled*/
      i[0]
    ) },
    /*inputProps*/
    i[16],
    Oe(
      /*$$restProps*/
      i[19],
      ["icons$"]
    )
  ], k = {};
  for (let g = 0; g < S.length; g += 1)
    k = ce(k, S[g]);
  return {
    c() {
      e = W("button"), t = W("div"), n = N(), r = W("div"), a = W("div"), s = W("div"), s.innerHTML = '<div class="mdc-elevation-overlay"></div>', h = N(), o = W("div"), c = N(), w && w.c(), v = N(), y && y.c(), G(t, "class", "mdc-switch__track"), G(s, "class", "mdc-switch__shadow"), G(o, "class", "mdc-switch__ripple"), G(a, "class", "mdc-switch__handle"), G(r, "class", "mdc-switch__handle-track"), de(e, k);
    },
    m(g, p) {
      be(g, e, p), U(e, t), U(e, n), U(e, r), U(r, a), U(a, s), U(a, h), U(a, o), i[28](o), U(a, c), w && w.m(a, null), U(e, v), y && y.m(e, null), e.autofocus && e.focus(), i[29](e), d || (_ = [
        oe(u = Ze.call(
          null,
          e,
          /*use*/
          i[2]
        )),
        oe(
          /*forwardEvents*/
          i[15].call(null, e)
        ),
        oe(l = Zt.call(null, e, {
          unbounded: !0,
          color: (
            /*color*/
            i[5]
          ),
          active: (
            /*rippleActive*/
            i[14]
          ),
          rippleElement: (
            /*rippleElement*/
            i[13]
          ),
          disabled: (
            /*disabled*/
            i[0]
          ),
          addClass: (
            /*addClass*/
            i[17]
          ),
          removeClass: (
            /*removeClass*/
            i[18]
          )
        })),
        Tt(
          e,
          "click",
          /*click_handler*/
          i[30]
        )
      ], d = !0);
    },
    p(g, p) {
      /*icons*/
      g[6] ? w ? w.p(g, p) : (w = Ee(g), w.c(), w.m(a, null)) : w && (w.d(1), w = null), /*focusRing*/
      g[4] ? y || (y = Pe(), y.c(), y.m(e, null)) : y && (y.d(1), y = null), de(e, k = Je(S, [
        p[0] & /*className, selected, processing, color, internalClasses*/
        5162 && f !== (f = le({
          [
            /*className*/
            g[3]
          ]: !0,
          "mdc-switch": !0,
          "mdc-switch--unselected": !/*selected*/
          g[10],
          "mdc-switch--selected": (
            /*selected*/
            g[10]
          ),
          "mdc-switch--processing": (
            /*processing*/
            g[1]
          ),
          "smui-switch--color-secondary": (
            /*color*/
            g[5] === "secondary"
          ),
          .../*internalClasses*/
          g[12]
        })) && { class: f },
        { type: "button" },
        { role: "switch" },
        p[0] & /*selected*/
        1024 && C !== (C = /*selected*/
        g[10] ? "true" : "false") && {
          "aria-checked": C
        },
        p[0] & /*disabled*/
        1 && { disabled: (
          /*disabled*/
          g[0]
        ) },
        /*inputProps*/
        g[16],
        p[0] & /*$$restProps*/
        524288 && Oe(
          /*$$restProps*/
          g[19],
          ["icons$"]
        )
      ])), u && me(u.update) && p[0] & /*use*/
      4 && u.update.call(
        null,
        /*use*/
        g[2]
      ), l && me(l.update) && p[0] & /*color, rippleActive, rippleElement, disabled*/
      24609 && l.update.call(null, {
        unbounded: !0,
        color: (
          /*color*/
          g[5]
        ),
        active: (
          /*rippleActive*/
          g[14]
        ),
        rippleElement: (
          /*rippleElement*/
          g[13]
        ),
        disabled: (
          /*disabled*/
          g[0]
        ),
        addClass: (
          /*addClass*/
          g[17]
        ),
        removeClass: (
          /*removeClass*/
          g[18]
        )
      });
    },
    i: Ie,
    o: Ie,
    d(g) {
      g && ge(e), i[28](null), w && w.d(), y && y.d(), i[29](null), d = !1, Nt(_);
    }
  };
}
function ni(i, e, t) {
  const n = [
    "use",
    "class",
    "disabled",
    "focusRing",
    "color",
    "group",
    "checked",
    "value",
    "processing",
    "icons",
    "icons$use",
    "icons$class",
    "getId",
    "getElement"
  ];
  let r = Ue(e, n);
  var a;
  const s = Gt(ti());
  let h = () => {
  };
  function o(m) {
    return m === h;
  }
  let { use: c = [] } = e, { class: v = "" } = e, { disabled: f = !1 } = e, { focusRing: C = !1 } = e, { color: u = "primary" } = e, { group: l = h } = e, { checked: d = h } = e, { value: _ = null } = e, { processing: w = !1 } = e, { icons: y = !0 } = e, { icons$use: S = [] } = e, { icons$class: k = "" } = e, g, p, A = {}, q, b = !1, F = (a = ei("SMUI:generic:input:props")) !== null && a !== void 0 ? a : {}, D = o(l) ? o(d) ? !1 : d : l.indexOf(_) !== -1, E = {
    get disabled() {
      return f;
    },
    set disabled(m) {
      t(0, f = m);
    },
    get processing() {
      return w;
    },
    set processing(m) {
      t(1, w = m);
    },
    get selected() {
      return D;
    },
    set selected(m) {
      t(10, D = m);
    }
  }, M = d, O = o(l) ? [] : [...l], L = D;
  $t(() => {
    t(11, p = new Pt({
      addClass: $,
      hasClass: J,
      isDisabled: () => f,
      removeClass: K,
      setAriaChecked: () => {
      },
      // Handled automatically.
      setDisabled: (j) => {
        t(0, f = j);
      },
      state: E
    }));
    const m = {
      get element() {
        return x();
      },
      get checked() {
        return D;
      },
      set checked(j) {
        D !== j && (E.selected = j, g && ie(g, "SMUISwitch:change", { selected: j, value: _ }));
      },
      activateRipple() {
        f || t(14, b = !0);
      },
      deactivateRipple() {
        t(14, b = !1);
      }
    };
    return ie(g, "SMUIGenericInput:mount", m), p.init(), p.initFromDOM(), () => {
      ie(g, "SMUIGenericInput:unmount", m), p.destroy();
    };
  });
  function J(m) {
    return m in A ? A[m] : x().classList.contains(m);
  }
  function $(m) {
    A[m] || t(12, A[m] = !0, A);
  }
  function K(m) {
    (!(m in A) || A[m]) && t(12, A[m] = !1, A);
  }
  function X() {
    return F && F.id;
  }
  function x() {
    return g;
  }
  function Ne(m) {
    Le[m ? "unshift" : "push"](() => {
      q = m, t(13, q);
    });
  }
  function Ye(m) {
    Le[m ? "unshift" : "push"](() => {
      g = m, t(9, g);
    });
  }
  const $e = () => p && p.handleClick();
  return i.$$set = (m) => {
    e = ce(ce({}, e), Kt(m)), t(19, r = Ue(e, n)), "use" in m && t(2, c = m.use), "class" in m && t(3, v = m.class), "disabled" in m && t(0, f = m.disabled), "focusRing" in m && t(4, C = m.focusRing), "color" in m && t(5, u = m.color), "group" in m && t(20, l = m.group), "checked" in m && t(21, d = m.checked), "value" in m && t(22, _ = m.value), "processing" in m && t(1, w = m.processing), "icons" in m && t(6, y = m.icons), "icons$use" in m && t(7, S = m.icons$use), "icons$class" in m && t(8, k = m.icons$class);
  }, i.$$.update = () => {
    if (i.$$.dirty[0] & /*group, previousSelected, selected, value, previousGroup, checked, previousChecked, element*/
    242222592) {
      let m = !1;
      if (!o(l))
        if (L !== D) {
          const j = l.indexOf(_);
          D && j === -1 ? (l.push(_), t(20, l), t(27, L), t(10, D), t(22, _), t(26, O), t(21, d), t(25, M), t(9, g)) : !D && j !== -1 && (l.splice(j, 1), t(20, l), t(27, L), t(10, D), t(22, _), t(26, O), t(21, d), t(25, M), t(9, g)), m = !0;
        } else {
          const j = O.indexOf(_), we = l.indexOf(_);
          j > -1 && we === -1 ? E.selected = !1 : we > -1 && j === -1 && (E.selected = !0);
        }
      o(d) ? L !== D && (m = !0) : d !== D && (d === M ? (t(21, d = D), m = !0) : E.selected = d), t(25, M = d), t(26, O = o(l) ? [] : [...l]), t(27, L = D), m && g && ie(g, "SMUISwitch:change", { selected: D, value: _ });
    }
  }, [
    f,
    w,
    c,
    v,
    C,
    u,
    y,
    S,
    k,
    g,
    D,
    p,
    A,
    q,
    b,
    s,
    F,
    $,
    K,
    r,
    l,
    d,
    _,
    X,
    x,
    M,
    O,
    L,
    Ne,
    Ye,
    $e
  ];
}
class ri extends Jt {
  constructor(e) {
    super(), Qt(
      this,
      e,
      ni,
      ii,
      Yt,
      {
        use: 2,
        class: 3,
        disabled: 0,
        focusRing: 4,
        color: 5,
        group: 20,
        checked: 21,
        value: 22,
        processing: 1,
        icons: 6,
        icons$use: 7,
        icons$class: 8,
        getId: 23,
        getElement: 24
      },
      null,
      [-1, -1]
    );
  }
  get getId() {
    return this.$$.ctx[23];
  }
  get getElement() {
    return this.$$.ctx[24];
  }
}
const {
  SvelteComponent: ai,
  add_flush_callback: si,
  append: R,
  attr: I,
  bind: oi,
  binding_callbacks: li,
  check_outros: ci,
  create_component: Ke,
  destroy_component: Qe,
  destroy_each: je,
  detach: _e,
  element: B,
  ensure_array_like: ae,
  flush: H,
  group_outros: di,
  init: fi,
  insert: ye,
  listen: ui,
  mount_component: Te,
  noop: hi,
  safe_not_equal: pi,
  set_data: he,
  space: Q,
  text: pe,
  transition_in: Y,
  transition_out: fe
} = window.__gradio__svelte__internal;
function Ge(i, e, t) {
  const n = i.slice();
  return n[25] = e[t], n[26] = e, n[9] = t, n;
}
function Be(i, e, t) {
  const n = i.slice();
  return n[27] = e[t], n;
}
function ze(i) {
  let e;
  return {
    c() {
      e = B("th"), e.textContent = `${/*header*/
      i[27]}`;
    },
    m(t, n) {
      ye(t, e, n);
    },
    p: hi,
    d(t) {
      t && _e(e);
    }
  };
}
function qe(i) {
  var E;
  let e, t, n = (
    /*data*/
    i[25].ligandA + ""
  ), r, a, s, h = (
    /*data*/
    i[25].ligandB + ""
  ), o, c, v, f = (
    /*data*/
    ((E = i[25].similarity) == null ? void 0 : E.toFixed(3)) + ""
  ), C, u, l, d, _, w, y, S, k, g, p, A;
  function q(M) {
    i[18](
      M,
      /*data*/
      i[25]
    );
  }
  function b(...M) {
    return (
      /*SMUISwitch_change_handler*/
      i[19](
        /*data*/
        i[25],
        /*index*/
        i[9],
        ...M
      )
    );
  }
  let F = {};
  /*data*/
  i[25].link !== void 0 && (F.checked = /*data*/
  i[25].link), d = new ri({ props: F }), li.push(() => oi(d, "checked", q)), d.$on("SMUISwitch:change", b);
  function D() {
    return (
      /*click_handler*/
      i[20](
        /*data*/
        i[25],
        /*index*/
        i[9]
      )
    );
  }
  return {
    c() {
      e = B("tr"), t = B("td"), r = pe(n), a = Q(), s = B("td"), o = pe(h), c = Q(), v = B("td"), C = pe(f), u = Q(), l = B("td"), Ke(d.$$.fragment), w = Q(), y = B("td"), S = B("button"), S.innerHTML = '<svg width="1em" height="1em" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1.75 5.83398C1.75 3.50065 2.91667 2.33398 5.25 2.33398" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 2"></path><path d="M11.6641 8.75C11.6641 11.0833 10.4974 12.25 8.16406 12.25" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 2"></path><path d="M8.16406 5.25065C8.16406 3.63983 9.46991 2.33398 11.0807 2.33398H12.2474V6.41732H8.16406V5.25065Z" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"></path><path d="M1.75 8.16602H5.83333V9.33268C5.83333 10.9435 4.52748 12.2493 2.91667 12.2493H1.75V8.16602Z" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"></path></svg>', k = Q(), I(t, "class", "svelte-1dgkx0j"), I(s, "class", "svelte-1dgkx0j"), I(v, "class", "svelte-1dgkx0j"), I(l, "class", "svelte-1dgkx0j"), I(y, "class", "svelte-1dgkx0j"), I(e, "class", "svelte-1dgkx0j");
    },
    m(M, O) {
      ye(M, e, O), R(e, t), R(t, r), R(e, a), R(e, s), R(s, o), R(e, c), R(e, v), R(v, C), R(e, u), R(e, l), Te(d, l, null), R(e, w), R(e, y), R(y, S), R(e, k), g = !0, p || (A = ui(S, "click", D), p = !0);
    },
    p(M, O) {
      var J;
      i = M, (!g || O & /*tableData*/
      256) && n !== (n = /*data*/
      i[25].ligandA + "") && he(r, n), (!g || O & /*tableData*/
      256) && h !== (h = /*data*/
      i[25].ligandB + "") && he(o, h), (!g || O & /*tableData*/
      256) && f !== (f = /*data*/
      ((J = i[25].similarity) == null ? void 0 : J.toFixed(3)) + "") && he(C, f);
      const L = {};
      !_ && O & /*tableData*/
      256 && (_ = !0, L.checked = /*data*/
      i[25].link, si(() => _ = !1)), d.$set(L);
    },
    i(M) {
      g || (Y(d.$$.fragment, M), g = !0);
    },
    o(M) {
      fe(d.$$.fragment, M), g = !1;
    },
    d(M) {
      M && _e(e), Qe(d), p = !1, A();
    }
  };
}
function vi(i) {
  let e, t, n, r, a, s, h, o = ae(
    /*headers*/
    i[10]
  ), c = [];
  for (let u = 0; u < o.length; u += 1)
    c[u] = ze(Be(i, o, u));
  let v = ae(
    /*tableData*/
    i[8]
  ), f = [];
  for (let u = 0; u < v.length; u += 1)
    f[u] = qe(Ge(i, v, u));
  const C = (u) => fe(f[u], 1, 1, () => {
    f[u] = null;
  });
  return {
    c() {
      e = B("div"), t = B("table"), n = B("tr");
      for (let u = 0; u < c.length; u += 1)
        c[u].c();
      r = Q();
      for (let u = 0; u < f.length; u += 1)
        f[u].c();
      I(n, "class", "svelte-1dgkx0j"), I(t, "border", "1"), I(t, "class", "fep-pair-table svelte-1dgkx0j"), I(t, "id", a = "fep-pair-table-update" + /*index*/
      i[9]), I(e, "class", "fep-pair-container svelte-1dgkx0j"), I(e, "style", s = /*max_height*/
      i[7] ? `max-height: ${/*max_height*/
      i[7]}px` : "");
    },
    m(u, l) {
      ye(u, e, l), R(e, t), R(t, n);
      for (let d = 0; d < c.length; d += 1)
        c[d] && c[d].m(n, null);
      R(t, r);
      for (let d = 0; d < f.length; d += 1)
        f[d] && f[d].m(t, null);
      h = !0;
    },
    p(u, l) {
      if (l & /*headers*/
      1024) {
        o = ae(
          /*headers*/
          u[10]
        );
        let d;
        for (d = 0; d < o.length; d += 1) {
          const _ = Be(u, o, d);
          c[d] ? c[d].p(_, l) : (c[d] = ze(_), c[d].c(), c[d].m(n, null));
        }
        for (; d < c.length; d += 1)
          c[d].d(1);
        c.length = o.length;
      }
      if (l & /*value, JSON, tableData, gradio*/
      259) {
        v = ae(
          /*tableData*/
          u[8]
        );
        let d;
        for (d = 0; d < v.length; d += 1) {
          const _ = Ge(u, v, d);
          f[d] ? (f[d].p(_, l), Y(f[d], 1)) : (f[d] = qe(_), f[d].c(), Y(f[d], 1), f[d].m(t, null));
        }
        for (di(), d = v.length; d < f.length; d += 1)
          C(d);
        ci();
      }
      (!h || l & /*index*/
      512 && a !== (a = "fep-pair-table-update" + /*index*/
      u[9])) && I(t, "id", a), (!h || l & /*max_height*/
      128 && s !== (s = /*max_height*/
      u[7] ? `max-height: ${/*max_height*/
      u[7]}px` : "")) && I(e, "style", s);
    },
    i(u) {
      if (!h) {
        for (let l = 0; l < v.length; l += 1)
          Y(f[l]);
        h = !0;
      }
    },
    o(u) {
      f = f.filter(Boolean);
      for (let l = 0; l < f.length; l += 1)
        fe(f[l]);
      h = !1;
    },
    d(u) {
      u && _e(e), je(c, u), je(f, u);
    }
  };
}
function mi(i) {
  let e, t;
  return e = new vt({
    props: {
      visible: (
        /*visible*/
        i[4]
      ),
      elem_id: (
        /*elem_id*/
        i[2]
      ),
      elem_classes: (
        /*elem_classes*/
        i[3]
      ),
      scale: (
        /*scale*/
        i[5]
      ),
      min_width: (
        /*min_width*/
        i[6]
      ),
      allow_overflow: !1,
      padding: !0,
      $$slots: { default: [vi] },
      $$scope: { ctx: i }
    }
  }), {
    c() {
      Ke(e.$$.fragment);
    },
    m(n, r) {
      Te(e, n, r), t = !0;
    },
    p(n, [r]) {
      const a = {};
      r & /*visible*/
      16 && (a.visible = /*visible*/
      n[4]), r & /*elem_id*/
      4 && (a.elem_id = /*elem_id*/
      n[2]), r & /*elem_classes*/
      8 && (a.elem_classes = /*elem_classes*/
      n[3]), r & /*scale*/
      32 && (a.scale = /*scale*/
      n[5]), r & /*min_width*/
      64 && (a.min_width = /*min_width*/
      n[6]), r & /*$$scope, max_height, index, tableData, value, gradio*/
      1073742723 && (a.$$scope = { dirty: r, ctx: n }), e.$set(a);
    },
    i(n) {
      t || (Y(e.$$.fragment, n), t = !0);
    },
    o(n) {
      fe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Qe(e, n);
    }
  };
}
function gi(i, e, t) {
  this && this.__awaiter;
  let { gradio: n } = e, { label: r = "Textbox" } = e, { elem_id: a = "" } = e, { elem_classes: s = [] } = e, { visible: h = !0 } = e, { value: o = "" } = e, { placeholder: c = "" } = e, { show_label: v } = e, { scale: f = null } = e, { min_width: C = void 0 } = e, { loading_status: u = void 0 } = e, { value_is_output: l = !1 } = e, { interactive: d } = e, { rtl: _ = !1 } = e, { max_height: w } = e;
  const y = ["LigandA", "LigandB", "Similarity", "Link", "Mapping"];
  let S = [], k = 1;
  const g = () => {
    const { pairs: b } = JSON.parse(c);
    t(8, S = [...b, ...b, ...b, ...b]), t(9, k++, k);
  };
  function p(b, F) {
    i.$$.not_equal(F.link, b) && (F.link = b, t(8, S));
  }
  const A = (b, F, D) => {
    t(0, o = JSON.stringify({
      res: { ...b, link: S[F].link },
      type: "Link",
      index: F
    })), n.dispatch("change");
  }, q = (b, F) => {
    t(0, o = JSON.stringify({ res: b, type: "Mapping", index: F })), n.dispatch("change");
  };
  return i.$$set = (b) => {
    "gradio" in b && t(1, n = b.gradio), "label" in b && t(11, r = b.label), "elem_id" in b && t(2, a = b.elem_id), "elem_classes" in b && t(3, s = b.elem_classes), "visible" in b && t(4, h = b.visible), "value" in b && t(0, o = b.value), "placeholder" in b && t(12, c = b.placeholder), "show_label" in b && t(13, v = b.show_label), "scale" in b && t(5, f = b.scale), "min_width" in b && t(6, C = b.min_width), "loading_status" in b && t(14, u = b.loading_status), "value_is_output" in b && t(15, l = b.value_is_output), "interactive" in b && t(16, d = b.interactive), "rtl" in b && t(17, _ = b.rtl), "max_height" in b && t(7, w = b.max_height);
  }, i.$$.update = () => {
    i.$$.dirty & /*value*/
    1 && o === null && t(0, o = ""), i.$$.dirty & /*value*/
    1, i.$$.dirty & /*placeholder*/
    4096 && g();
  }, [
    o,
    n,
    a,
    s,
    h,
    f,
    C,
    w,
    S,
    k,
    y,
    r,
    c,
    v,
    u,
    l,
    d,
    _,
    p,
    A,
    q
  ];
}
class bi extends ai {
  constructor(e) {
    super(), fi(this, e, gi, mi, pi, {
      gradio: 1,
      label: 11,
      elem_id: 2,
      elem_classes: 3,
      visible: 4,
      value: 0,
      placeholder: 12,
      show_label: 13,
      scale: 5,
      min_width: 6,
      loading_status: 14,
      value_is_output: 15,
      interactive: 16,
      rtl: 17,
      max_height: 7
    });
  }
  get gradio() {
    return this.$$.ctx[1];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), H();
  }
  get label() {
    return this.$$.ctx[11];
  }
  set label(e) {
    this.$$set({ label: e }), H();
  }
  get elem_id() {
    return this.$$.ctx[2];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), H();
  }
  get elem_classes() {
    return this.$$.ctx[3];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), H();
  }
  get visible() {
    return this.$$.ctx[4];
  }
  set visible(e) {
    this.$$set({ visible: e }), H();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), H();
  }
  get placeholder() {
    return this.$$.ctx[12];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), H();
  }
  get show_label() {
    return this.$$.ctx[13];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), H();
  }
  get scale() {
    return this.$$.ctx[5];
  }
  set scale(e) {
    this.$$set({ scale: e }), H();
  }
  get min_width() {
    return this.$$.ctx[6];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), H();
  }
  get loading_status() {
    return this.$$.ctx[14];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), H();
  }
  get value_is_output() {
    return this.$$.ctx[15];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), H();
  }
  get interactive() {
    return this.$$.ctx[16];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), H();
  }
  get rtl() {
    return this.$$.ctx[17];
  }
  set rtl(e) {
    this.$$set({ rtl: e }), H();
  }
  get max_height() {
    return this.$$.ctx[7];
  }
  set max_height(e) {
    this.$$set({ max_height: e }), H();
  }
}
export {
  bi as default
};
