const {
  SvelteComponent: it,
  assign: ft,
  create_slot: st,
  detach: at,
  element: ot,
  get_all_dirty_from_scope: _t,
  get_slot_changes: ut,
  get_spread_update: rt,
  init: dt,
  insert: ct,
  safe_not_equal: mt,
  set_dynamic_element_data: ke,
  set_style: B,
  toggle_class: I,
  transition_in: Pe,
  transition_out: Ye,
  update_slot_base: bt
} = window.__gradio__svelte__internal;
function ht(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), s = st(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let _ = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], a = {};
  for (let f = 0; f < _.length; f += 1)
    a = ft(a, _[f]);
  return {
    c() {
      e = ot(
        /*tag*/
        n[14]
      ), s && s.c(), ke(
        /*tag*/
        n[14]
      )(e, a), I(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), I(
        e,
        "padded",
        /*padding*/
        n[6]
      ), I(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), I(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), I(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), B(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), B(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), B(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), B(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), B(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), B(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), B(e, "border-width", "var(--block-border-width)");
    },
    m(f, o) {
      ct(f, e, o), s && s.m(e, null), l = !0;
    },
    p(f, o) {
      s && s.p && (!l || o & /*$$scope*/
      131072) && bt(
        s,
        i,
        f,
        /*$$scope*/
        f[17],
        l ? ut(
          i,
          /*$$scope*/
          f[17],
          o,
          null
        ) : _t(
          /*$$scope*/
          f[17]
        ),
        null
      ), ke(
        /*tag*/
        f[14]
      )(e, a = rt(_, [
        (!l || o & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!l || o & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!l || o & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), I(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), I(
        e,
        "padded",
        /*padding*/
        f[6]
      ), I(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), I(
        e,
        "border_contrast",
        /*border_mode*/
        f[5] === "contrast"
      ), I(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), o & /*height*/
      1 && B(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), o & /*width*/
      2 && B(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), o & /*variant*/
      16 && B(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), o & /*allow_overflow*/
      2048 && B(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), o & /*scale*/
      4096 && B(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), o & /*min_width*/
      8192 && B(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      l || (Pe(s, f), l = !0);
    },
    o(f) {
      Ye(s, f), l = !1;
    },
    d(f) {
      f && at(e), s && s.d(f);
    }
  };
}
function gt(n) {
  let e, t = (
    /*tag*/
    n[14] && ht(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (Pe(t, l), e = !0);
    },
    o(l) {
      Ye(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function wt(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: _ = void 0 } = e, { elem_id: a = "" } = e, { elem_classes: f = [] } = e, { variant: o = "solid" } = e, { border_mode: d = "base" } = e, { padding: g = !0 } = e, { type: w = "normal" } = e, { test_id: C = void 0 } = e, { explicit_call: q = !1 } = e, { container: v = !0 } = e, { visible: m = !0 } = e, { allow_overflow: r = !0 } = e, { scale: k = null } = e, { min_width: y = 0 } = e, j = w === "fieldset" ? "fieldset" : "div";
  const S = (u) => {
    if (u !== void 0) {
      if (typeof u == "number")
        return u + "px";
      if (typeof u == "string")
        return u;
    }
  };
  return n.$$set = (u) => {
    "height" in u && t(0, s = u.height), "width" in u && t(1, _ = u.width), "elem_id" in u && t(2, a = u.elem_id), "elem_classes" in u && t(3, f = u.elem_classes), "variant" in u && t(4, o = u.variant), "border_mode" in u && t(5, d = u.border_mode), "padding" in u && t(6, g = u.padding), "type" in u && t(16, w = u.type), "test_id" in u && t(7, C = u.test_id), "explicit_call" in u && t(8, q = u.explicit_call), "container" in u && t(9, v = u.container), "visible" in u && t(10, m = u.visible), "allow_overflow" in u && t(11, r = u.allow_overflow), "scale" in u && t(12, k = u.scale), "min_width" in u && t(13, y = u.min_width), "$$scope" in u && t(17, i = u.$$scope);
  }, [
    s,
    _,
    a,
    f,
    o,
    d,
    g,
    C,
    q,
    v,
    m,
    r,
    k,
    y,
    j,
    S,
    w,
    i,
    l
  ];
}
let kt = class extends it {
  constructor(e) {
    super(), dt(this, e, wt, gt, mt, {
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
};
const {
  SvelteComponent: vt,
  attr: yt,
  create_slot: qt,
  detach: Ct,
  element: St,
  get_all_dirty_from_scope: jt,
  get_slot_changes: Bt,
  init: zt,
  insert: It,
  safe_not_equal: Tt,
  transition_in: Dt,
  transition_out: Et,
  update_slot_base: Nt
} = window.__gradio__svelte__internal;
function Mt(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[1].default
  ), i = qt(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = St("div"), i && i.c(), yt(e, "class", "svelte-1hnfib2");
    },
    m(s, _) {
      It(s, e, _), i && i.m(e, null), t = !0;
    },
    p(s, [_]) {
      i && i.p && (!t || _ & /*$$scope*/
      1) && Nt(
        i,
        l,
        s,
        /*$$scope*/
        s[0],
        t ? Bt(
          l,
          /*$$scope*/
          s[0],
          _,
          null
        ) : jt(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      t || (Dt(i, s), t = !0);
    },
    o(s) {
      Et(i, s), t = !1;
    },
    d(s) {
      s && Ct(e), i && i.d(s);
    }
  };
}
function Ft(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  return n.$$set = (s) => {
    "$$scope" in s && t(0, i = s.$$scope);
  }, [i, l];
}
let Ht = class extends vt {
  constructor(e) {
    super(), zt(this, e, Ft, Mt, Tt, {});
  }
};
const {
  SvelteComponent: Jt,
  attr: ve,
  check_outros: Lt,
  create_component: Ot,
  create_slot: Pt,
  destroy_component: Yt,
  detach: X,
  element: At,
  empty: Gt,
  get_all_dirty_from_scope: Kt,
  get_slot_changes: Qt,
  group_outros: Rt,
  init: Ut,
  insert: Z,
  mount_component: Vt,
  safe_not_equal: Wt,
  set_data: Xt,
  space: Zt,
  text: pt,
  toggle_class: M,
  transition_in: K,
  transition_out: p,
  update_slot_base: xt
} = window.__gradio__svelte__internal;
function ye(n) {
  let e, t;
  return e = new Ht({
    props: {
      $$slots: { default: [$t] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Ot(e.$$.fragment);
    },
    m(l, i) {
      Vt(e, l, i), t = !0;
    },
    p(l, i) {
      const s = {};
      i & /*$$scope, info*/
      10 && (s.$$scope = { dirty: i, ctx: l }), e.$set(s);
    },
    i(l) {
      t || (K(e.$$.fragment, l), t = !0);
    },
    o(l) {
      p(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Yt(e, l);
    }
  };
}
function $t(n) {
  let e;
  return {
    c() {
      e = pt(
        /*info*/
        n[1]
      );
    },
    m(t, l) {
      Z(t, e, l);
    },
    p(t, l) {
      l & /*info*/
      2 && Xt(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && X(e);
    }
  };
}
function en(n) {
  let e, t, l, i;
  const s = (
    /*#slots*/
    n[2].default
  ), _ = Pt(
    s,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let a = (
    /*info*/
    n[1] && ye(n)
  );
  return {
    c() {
      e = At("span"), _ && _.c(), t = Zt(), a && a.c(), l = Gt(), ve(e, "data-testid", "block-info"), ve(e, "class", "svelte-22c38v"), M(e, "sr-only", !/*show_label*/
      n[0]), M(e, "hide", !/*show_label*/
      n[0]), M(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(f, o) {
      Z(f, e, o), _ && _.m(e, null), Z(f, t, o), a && a.m(f, o), Z(f, l, o), i = !0;
    },
    p(f, [o]) {
      _ && _.p && (!i || o & /*$$scope*/
      8) && xt(
        _,
        s,
        f,
        /*$$scope*/
        f[3],
        i ? Qt(
          s,
          /*$$scope*/
          f[3],
          o,
          null
        ) : Kt(
          /*$$scope*/
          f[3]
        ),
        null
      ), (!i || o & /*show_label*/
      1) && M(e, "sr-only", !/*show_label*/
      f[0]), (!i || o & /*show_label*/
      1) && M(e, "hide", !/*show_label*/
      f[0]), (!i || o & /*info*/
      2) && M(
        e,
        "has-info",
        /*info*/
        f[1] != null
      ), /*info*/
      f[1] ? a ? (a.p(f, o), o & /*info*/
      2 && K(a, 1)) : (a = ye(f), a.c(), K(a, 1), a.m(l.parentNode, l)) : a && (Rt(), p(a, 1, 1, () => {
        a = null;
      }), Lt());
    },
    i(f) {
      i || (K(_, f), K(a), i = !0);
    },
    o(f) {
      p(_, f), p(a), i = !1;
    },
    d(f) {
      f && (X(e), X(t), X(l)), _ && _.d(f), a && a.d(f);
    }
  };
}
function tn(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_label: s = !0 } = e, { info: _ = void 0 } = e;
  return n.$$set = (a) => {
    "show_label" in a && t(0, s = a.show_label), "info" in a && t(1, _ = a.info), "$$scope" in a && t(3, i = a.$$scope);
  }, [s, _, l, i];
}
let nn = class extends Jt {
  constructor(e) {
    super(), Ut(this, e, tn, en, Wt, { show_label: 0, info: 1 });
  }
};
const {
  SvelteComponent: ln,
  append: V,
  attr: h,
  detach: fn,
  init: sn,
  insert: an,
  noop: _e,
  safe_not_equal: on,
  svg_element: G
} = window.__gradio__svelte__internal;
function _n(n) {
  let e, t, l, i, s;
  return {
    c() {
      e = G("svg"), t = G("rect"), l = G("line"), i = G("line"), s = G("line"), h(t, "x", "2"), h(t, "y", "4"), h(t, "width", "20"), h(t, "height", "18"), h(t, "stroke", "currentColor"), h(t, "stroke-width", "2"), h(t, "stroke-linecap", "round"), h(t, "stroke-linejoin", "round"), h(t, "fill", "none"), h(l, "x1", "2"), h(l, "y1", "9"), h(l, "x2", "22"), h(l, "y2", "9"), h(l, "stroke", "currentColor"), h(l, "stroke-width", "2"), h(l, "stroke-linecap", "round"), h(l, "stroke-linejoin", "round"), h(l, "fill", "none"), h(i, "x1", "7"), h(i, "y1", "2"), h(i, "x2", "7"), h(i, "y2", "6"), h(i, "stroke", "currentColor"), h(i, "stroke-width", "2"), h(i, "stroke-linecap", "round"), h(i, "stroke-linejoin", "round"), h(i, "fill", "none"), h(s, "x1", "17"), h(s, "y1", "2"), h(s, "x2", "17"), h(s, "y2", "6"), h(s, "stroke", "currentColor"), h(s, "stroke-width", "2"), h(s, "stroke-linecap", "round"), h(s, "stroke-linejoin", "round"), h(s, "fill", "none"), h(e, "xmlns", "http://www.w3.org/2000/svg"), h(e, "width", "24px"), h(e, "height", "24px"), h(e, "viewBox", "0 0 24 24");
    },
    m(_, a) {
      an(_, e, a), V(e, t), V(e, l), V(e, i), V(e, s);
    },
    p: _e,
    i: _e,
    o: _e,
    d(_) {
      _ && fn(e);
    }
  };
}
class un extends ln {
  constructor(e) {
    super(), sn(this, e, null, _n, on, {});
  }
}
const rn = [
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
], qe = {
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
rn.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: qe[e][t],
      secondary: qe[e][l]
    }
  }),
  {}
);
const {
  SvelteComponent: dn,
  assign: cn,
  create_slot: mn,
  detach: bn,
  element: hn,
  get_all_dirty_from_scope: gn,
  get_slot_changes: wn,
  get_spread_update: kn,
  init: vn,
  insert: yn,
  safe_not_equal: qn,
  set_dynamic_element_data: Ce,
  set_style: z,
  toggle_class: T,
  transition_in: Ae,
  transition_out: Ge,
  update_slot_base: Cn
} = window.__gradio__svelte__internal;
function Sn(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), s = mn(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let _ = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], a = {};
  for (let f = 0; f < _.length; f += 1)
    a = cn(a, _[f]);
  return {
    c() {
      e = hn(
        /*tag*/
        n[14]
      ), s && s.c(), Ce(
        /*tag*/
        n[14]
      )(e, a), T(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), T(
        e,
        "padded",
        /*padding*/
        n[6]
      ), T(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), T(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), T(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), z(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), z(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), z(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), z(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), z(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), z(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), z(e, "border-width", "var(--block-border-width)");
    },
    m(f, o) {
      yn(f, e, o), s && s.m(e, null), l = !0;
    },
    p(f, o) {
      s && s.p && (!l || o & /*$$scope*/
      131072) && Cn(
        s,
        i,
        f,
        /*$$scope*/
        f[17],
        l ? wn(
          i,
          /*$$scope*/
          f[17],
          o,
          null
        ) : gn(
          /*$$scope*/
          f[17]
        ),
        null
      ), Ce(
        /*tag*/
        f[14]
      )(e, a = kn(_, [
        (!l || o & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!l || o & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!l || o & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), T(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), T(
        e,
        "padded",
        /*padding*/
        f[6]
      ), T(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), T(
        e,
        "border_contrast",
        /*border_mode*/
        f[5] === "contrast"
      ), T(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), o & /*height*/
      1 && z(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), o & /*width*/
      2 && z(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), o & /*variant*/
      16 && z(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), o & /*allow_overflow*/
      2048 && z(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), o & /*scale*/
      4096 && z(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), o & /*min_width*/
      8192 && z(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      l || (Ae(s, f), l = !0);
    },
    o(f) {
      Ge(s, f), l = !1;
    },
    d(f) {
      f && bn(e), s && s.d(f);
    }
  };
}
function jn(n) {
  let e, t = (
    /*tag*/
    n[14] && Sn(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (Ae(t, l), e = !0);
    },
    o(l) {
      Ge(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function Bn(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: _ = void 0 } = e, { elem_id: a = "" } = e, { elem_classes: f = [] } = e, { variant: o = "solid" } = e, { border_mode: d = "base" } = e, { padding: g = !0 } = e, { type: w = "normal" } = e, { test_id: C = void 0 } = e, { explicit_call: q = !1 } = e, { container: v = !0 } = e, { visible: m = !0 } = e, { allow_overflow: r = !0 } = e, { scale: k = null } = e, { min_width: y = 0 } = e, j = w === "fieldset" ? "fieldset" : "div";
  const S = (u) => {
    if (u !== void 0) {
      if (typeof u == "number")
        return u + "px";
      if (typeof u == "string")
        return u;
    }
  };
  return n.$$set = (u) => {
    "height" in u && t(0, s = u.height), "width" in u && t(1, _ = u.width), "elem_id" in u && t(2, a = u.elem_id), "elem_classes" in u && t(3, f = u.elem_classes), "variant" in u && t(4, o = u.variant), "border_mode" in u && t(5, d = u.border_mode), "padding" in u && t(6, g = u.padding), "type" in u && t(16, w = u.type), "test_id" in u && t(7, C = u.test_id), "explicit_call" in u && t(8, q = u.explicit_call), "container" in u && t(9, v = u.container), "visible" in u && t(10, m = u.visible), "allow_overflow" in u && t(11, r = u.allow_overflow), "scale" in u && t(12, k = u.scale), "min_width" in u && t(13, y = u.min_width), "$$scope" in u && t(17, i = u.$$scope);
  }, [
    s,
    _,
    a,
    f,
    o,
    d,
    g,
    C,
    q,
    v,
    m,
    r,
    k,
    y,
    j,
    S,
    w,
    i,
    l
  ];
}
class zn extends dn {
  constructor(e) {
    super(), vn(this, e, Bn, jn, qn, {
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
const {
  SvelteComponent: In,
  attr: Tn,
  create_slot: Dn,
  detach: En,
  element: Nn,
  get_all_dirty_from_scope: Mn,
  get_slot_changes: Fn,
  init: Hn,
  insert: Jn,
  safe_not_equal: Ln,
  transition_in: On,
  transition_out: Pn,
  update_slot_base: Yn
} = window.__gradio__svelte__internal;
function An(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[1].default
  ), i = Dn(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = Nn("div"), i && i.c(), Tn(e, "class", "svelte-1hnfib2");
    },
    m(s, _) {
      Jn(s, e, _), i && i.m(e, null), t = !0;
    },
    p(s, [_]) {
      i && i.p && (!t || _ & /*$$scope*/
      1) && Yn(
        i,
        l,
        s,
        /*$$scope*/
        s[0],
        t ? Fn(
          l,
          /*$$scope*/
          s[0],
          _,
          null
        ) : Mn(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      t || (On(i, s), t = !0);
    },
    o(s) {
      Pn(i, s), t = !1;
    },
    d(s) {
      s && En(e), i && i.d(s);
    }
  };
}
function Gn(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  return n.$$set = (s) => {
    "$$scope" in s && t(0, i = s.$$scope);
  }, [i, l];
}
class Kn extends In {
  constructor(e) {
    super(), Hn(this, e, Gn, An, Ln, {});
  }
}
const {
  SvelteComponent: Qn,
  attr: Se,
  check_outros: Rn,
  create_component: Un,
  create_slot: Vn,
  destroy_component: Wn,
  detach: x,
  element: Xn,
  empty: Zn,
  get_all_dirty_from_scope: pn,
  get_slot_changes: xn,
  group_outros: $n,
  init: el,
  insert: $,
  mount_component: tl,
  safe_not_equal: nl,
  set_data: ll,
  space: il,
  text: fl,
  toggle_class: F,
  transition_in: Q,
  transition_out: ee,
  update_slot_base: sl
} = window.__gradio__svelte__internal;
function je(n) {
  let e, t;
  return e = new Kn({
    props: {
      $$slots: { default: [al] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Un(e.$$.fragment);
    },
    m(l, i) {
      tl(e, l, i), t = !0;
    },
    p(l, i) {
      const s = {};
      i & /*$$scope, info*/
      10 && (s.$$scope = { dirty: i, ctx: l }), e.$set(s);
    },
    i(l) {
      t || (Q(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ee(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Wn(e, l);
    }
  };
}
function al(n) {
  let e;
  return {
    c() {
      e = fl(
        /*info*/
        n[1]
      );
    },
    m(t, l) {
      $(t, e, l);
    },
    p(t, l) {
      l & /*info*/
      2 && ll(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && x(e);
    }
  };
}
function ol(n) {
  let e, t, l, i;
  const s = (
    /*#slots*/
    n[2].default
  ), _ = Vn(
    s,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let a = (
    /*info*/
    n[1] && je(n)
  );
  return {
    c() {
      e = Xn("span"), _ && _.c(), t = il(), a && a.c(), l = Zn(), Se(e, "data-testid", "block-info"), Se(e, "class", "svelte-22c38v"), F(e, "sr-only", !/*show_label*/
      n[0]), F(e, "hide", !/*show_label*/
      n[0]), F(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(f, o) {
      $(f, e, o), _ && _.m(e, null), $(f, t, o), a && a.m(f, o), $(f, l, o), i = !0;
    },
    p(f, [o]) {
      _ && _.p && (!i || o & /*$$scope*/
      8) && sl(
        _,
        s,
        f,
        /*$$scope*/
        f[3],
        i ? xn(
          s,
          /*$$scope*/
          f[3],
          o,
          null
        ) : pn(
          /*$$scope*/
          f[3]
        ),
        null
      ), (!i || o & /*show_label*/
      1) && F(e, "sr-only", !/*show_label*/
      f[0]), (!i || o & /*show_label*/
      1) && F(e, "hide", !/*show_label*/
      f[0]), (!i || o & /*info*/
      2) && F(
        e,
        "has-info",
        /*info*/
        f[1] != null
      ), /*info*/
      f[1] ? a ? (a.p(f, o), o & /*info*/
      2 && Q(a, 1)) : (a = je(f), a.c(), Q(a, 1), a.m(l.parentNode, l)) : a && ($n(), ee(a, 1, 1, () => {
        a = null;
      }), Rn());
    },
    i(f) {
      i || (Q(_, f), Q(a), i = !0);
    },
    o(f) {
      ee(_, f), ee(a), i = !1;
    },
    d(f) {
      f && (x(e), x(t), x(l)), _ && _.d(f), a && a.d(f);
    }
  };
}
function _l(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_label: s = !0 } = e, { info: _ = void 0 } = e;
  return n.$$set = (a) => {
    "show_label" in a && t(0, s = a.show_label), "info" in a && t(1, _ = a.info), "$$scope" in a && t(3, i = a.$$scope);
  }, [s, _, l, i];
}
class ul extends Qn {
  constructor(e) {
    super(), el(this, e, _l, ol, nl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: rl,
  append: W,
  attr: D,
  binding_callbacks: Be,
  create_component: re,
  destroy_component: de,
  detach: J,
  element: H,
  init: dl,
  insert: L,
  listen: E,
  mount_component: ce,
  run_all: ge,
  safe_not_equal: cl,
  set_data: ml,
  set_input_value: Y,
  space: ue,
  text: bl,
  toggle_class: ze,
  transition_in: me,
  transition_out: be
} = window.__gradio__svelte__internal;
function hl(n) {
  let e;
  return {
    c() {
      e = bl(
        /*label*/
        n[1]
      );
    },
    m(t, l) {
      L(t, e, l);
    },
    p(t, l) {
      l & /*label*/
      2 && ml(
        e,
        /*label*/
        t[1]
      );
    },
    d(t) {
      t && J(e);
    }
  };
}
function gl(n) {
  let e, t, l;
  return {
    c() {
      e = H("input"), D(e, "type", "date"), D(e, "class", "datetime svelte-1rjvq1p"), D(e, "step", "1");
    },
    m(i, s) {
      L(i, e, s), n[23](e), Y(
        e,
        /*datevalue*/
        n[12]
      ), t || (l = [
        E(
          e,
          "input",
          /*input_input_handler_2*/
          n[24]
        ),
        E(
          e,
          "input",
          /*input_handler_1*/
          n[25]
        )
      ], t = !0);
    },
    p(i, s) {
      s & /*datevalue*/
      4096 && Y(
        e,
        /*datevalue*/
        i[12]
      );
    },
    d(i) {
      i && J(e), n[23](null), t = !1, ge(l);
    }
  };
}
function wl(n) {
  let e, t, l;
  return {
    c() {
      e = H("input"), D(e, "type", "datetime-local"), D(e, "class", "datetime svelte-1rjvq1p"), D(e, "step", "1");
    },
    m(i, s) {
      L(i, e, s), n[20](e), Y(
        e,
        /*datevalue*/
        n[12]
      ), t || (l = [
        E(
          e,
          "input",
          /*input_input_handler_1*/
          n[21]
        ),
        E(
          e,
          "input",
          /*input_handler*/
          n[22]
        )
      ], t = !0);
    },
    p(i, s) {
      s & /*datevalue*/
      4096 && Y(
        e,
        /*datevalue*/
        i[12]
      );
    },
    d(i) {
      i && J(e), n[20](null), t = !1, ge(l);
    }
  };
}
function kl(n) {
  let e, t, l, i, s, _, a, f, o, d, g, w;
  t = new ul({
    props: {
      show_label: (
        /*show_label*/
        n[2]
      ),
      info: (
        /*info*/
        n[3]
      ),
      $$slots: { default: [hl] },
      $$scope: { ctx: n }
    }
  });
  function C(m, r) {
    return (
      /*include_time*/
      m[9] ? wl : gl
    );
  }
  let q = C(n), v = q(n);
  return o = new un({}), {
    c() {
      e = H("div"), re(t.$$.fragment), l = ue(), i = H("div"), s = H("input"), _ = ue(), v.c(), a = ue(), f = H("button"), re(o.$$.fragment), D(e, "class", "label-content svelte-1rjvq1p"), D(s, "class", "time svelte-1rjvq1p"), ze(s, "invalid", !/*valid*/
      n[13]), D(f, "class", "calendar svelte-1rjvq1p"), D(i, "class", "timebox svelte-1rjvq1p");
    },
    m(m, r) {
      L(m, e, r), ce(t, e, null), L(m, l, r), L(m, i, r), W(i, s), Y(
        s,
        /*entered_value*/
        n[10]
      ), W(i, _), v.m(i, null), W(i, a), W(i, f), ce(o, f, null), d = !0, g || (w = [
        E(
          s,
          "input",
          /*input_input_handler*/
          n[18]
        ),
        E(
          s,
          "keydown",
          /*keydown_handler*/
          n[19]
        ),
        E(
          s,
          "blur",
          /*submit_values*/
          n[15]
        ),
        E(
          f,
          "click",
          /*click_handler*/
          n[26]
        )
      ], g = !0);
    },
    p(m, r) {
      const k = {};
      r & /*show_label*/
      4 && (k.show_label = /*show_label*/
      m[2]), r & /*info*/
      8 && (k.info = /*info*/
      m[3]), r & /*$$scope, label*/
      268435458 && (k.$$scope = { dirty: r, ctx: m }), t.$set(k), r & /*entered_value*/
      1024 && s.value !== /*entered_value*/
      m[10] && Y(
        s,
        /*entered_value*/
        m[10]
      ), (!d || r & /*valid*/
      8192) && ze(s, "invalid", !/*valid*/
      m[13]), q === (q = C(m)) && v ? v.p(m, r) : (v.d(1), v = q(m), v && (v.c(), v.m(i, a)));
    },
    i(m) {
      d || (me(t.$$.fragment, m), me(o.$$.fragment, m), d = !0);
    },
    o(m) {
      be(t.$$.fragment, m), be(o.$$.fragment, m), d = !1;
    },
    d(m) {
      m && (J(e), J(l), J(i)), de(t), v.d(), de(o), g = !1, ge(w);
    }
  };
}
function vl(n) {
  let e, t;
  return e = new zn({
    props: {
      visible: (
        /*visible*/
        n[6]
      ),
      elem_id: (
        /*elem_id*/
        n[4]
      ),
      elem_classes: (
        /*elem_classes*/
        n[5]
      ),
      scale: (
        /*scale*/
        n[7]
      ),
      min_width: (
        /*min_width*/
        n[8]
      ),
      allow_overflow: !1,
      padding: !0,
      $$slots: { default: [kl] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      re(e.$$.fragment);
    },
    m(l, i) {
      ce(e, l, i), t = !0;
    },
    p(l, [i]) {
      const s = {};
      i & /*visible*/
      64 && (s.visible = /*visible*/
      l[6]), i & /*elem_id*/
      16 && (s.elem_id = /*elem_id*/
      l[4]), i & /*elem_classes*/
      32 && (s.elem_classes = /*elem_classes*/
      l[5]), i & /*scale*/
      128 && (s.scale = /*scale*/
      l[7]), i & /*min_width*/
      256 && (s.min_width = /*min_width*/
      l[8]), i & /*$$scope, datetime, datevalue, entered_value, include_time, valid, gradio, show_label, info, label*/
      268451343 && (s.$$scope = { dirty: i, ctx: l }), e.$set(s);
    },
    i(l) {
      t || (me(e.$$.fragment, l), t = !0);
    },
    o(l) {
      be(e.$$.fragment, l), t = !1;
    },
    d(l) {
      de(e, l);
    }
  };
}
function yl(n, e, t) {
  let l, { gradio: i } = e, { label: s = "Time" } = e, { show_label: _ = !0 } = e, { info: a = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: o = [] } = e, { visible: d = !0 } = e, { value: g = "" } = e, w = g, { scale: C = null } = e, { min_width: q = void 0 } = e, { include_time: v = !0 } = e;
  const m = (c) => {
    if (c.toJSON() === null) return "";
    const N = (lt) => lt.toString().padStart(2, "0"), ae = c.getFullYear(), oe = N(c.getMonth() + 1), xe = N(c.getDate()), $e = N(c.getHours()), et = N(c.getMinutes()), tt = N(c.getSeconds()), we = `${ae}-${oe}-${xe}`, nt = `${$e}:${et}:${tt}`;
    return v ? `${we} ${nt}` : we;
  };
  let r = g, k, y = g;
  const j = (c) => {
    if (c === "") return !1;
    const N = v ? /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/ : /^\d{4}-\d{2}-\d{2}$/, ae = c.match(N) !== null, oe = c.match(/^(?:\s*now\s*(?:-\s*\d+\s*[dmhs])?)?\s*$/) !== null;
    return ae || oe;
  }, S = () => {
    r !== g && j(r) && (t(17, w = t(16, g = r)), i.dispatch("change"));
  };
  function u() {
    r = this.value, t(10, r), t(16, g), t(17, w), t(0, i);
  }
  const b = (c) => {
    c.key === "Enter" && (S(), i.dispatch("submit"));
  };
  function Re(c) {
    Be[c ? "unshift" : "push"](() => {
      k = c, t(11, k);
    });
  }
  function Ue() {
    y = this.value, t(12, y), t(16, g), t(17, w), t(0, i);
  }
  const Ve = () => {
    const c = new Date(y);
    t(10, r = m(c)), S();
  };
  function We(c) {
    Be[c ? "unshift" : "push"](() => {
      k = c, t(11, k);
    });
  }
  function Xe() {
    y = this.value, t(12, y), t(16, g), t(17, w), t(0, i);
  }
  const Ze = () => {
    const c = new Date(y);
    t(10, r = m(c)), S();
  }, pe = () => {
    k.showPicker();
  };
  return n.$$set = (c) => {
    "gradio" in c && t(0, i = c.gradio), "label" in c && t(1, s = c.label), "show_label" in c && t(2, _ = c.show_label), "info" in c && t(3, a = c.info), "elem_id" in c && t(4, f = c.elem_id), "elem_classes" in c && t(5, o = c.elem_classes), "visible" in c && t(6, d = c.visible), "value" in c && t(16, g = c.value), "scale" in c && t(7, C = c.scale), "min_width" in c && t(8, q = c.min_width), "include_time" in c && t(9, v = c.include_time);
  }, n.$$.update = () => {
    n.$$.dirty & /*value, old_value, gradio*/
    196609 && g !== w && (t(17, w = g), t(10, r = g), t(12, y = g), i.dispatch("change")), n.$$.dirty & /*entered_value*/
    1024 && t(13, l = j(r));
  }, [
    i,
    s,
    _,
    a,
    f,
    o,
    d,
    C,
    q,
    v,
    r,
    k,
    y,
    l,
    m,
    S,
    g,
    w,
    u,
    b,
    Re,
    Ue,
    Ve,
    We,
    Xe,
    Ze,
    pe
  ];
}
let Ie = class extends rl {
  constructor(e) {
    super(), dl(this, e, yl, vl, cl, {
      gradio: 0,
      label: 1,
      show_label: 2,
      info: 3,
      elem_id: 4,
      elem_classes: 5,
      visible: 6,
      value: 16,
      scale: 7,
      min_width: 8,
      include_time: 9
    });
  }
};
const {
  SvelteComponent: ql,
  detach: Cl,
  init: Sl,
  insert: jl,
  noop: Te,
  safe_not_equal: Bl,
  set_data: zl,
  text: Il
} = window.__gradio__svelte__internal;
function Tl(n) {
  let e = (
    /*value*/
    (n[0] || "") + ""
  ), t;
  return {
    c() {
      t = Il(e);
    },
    m(l, i) {
      jl(l, t, i);
    },
    p(l, [i]) {
      i & /*value*/
      1 && e !== (e = /*value*/
      (l[0] || "") + "") && zl(t, e);
    },
    i: Te,
    o: Te,
    d(l) {
      l && Cl(t);
    }
  };
}
function Dl(n, e, t) {
  let { value: l } = e;
  return n.$$set = (i) => {
    "value" in i && t(0, l = i.value);
  }, [l];
}
class Kl extends ql {
  constructor(e) {
    super(), Sl(this, e, Dl, Tl, Bl, { value: 0 });
  }
}
const {
  SvelteComponent: El,
  add_flush_callback: De,
  append: A,
  attr: R,
  bind: Ee,
  binding_callbacks: Ne,
  bubble: Me,
  create_component: te,
  destroy_component: ne,
  destroy_each: Nl,
  detach: O,
  element: U,
  ensure_array_like: Fe,
  init: Ml,
  insert: P,
  listen: Ke,
  mount_component: le,
  safe_not_equal: Fl,
  set_data: Qe,
  set_style: He,
  space: ie,
  text: he,
  transition_in: fe,
  transition_out: se
} = window.__gradio__svelte__internal;
function Je(n, e, t) {
  const l = n.slice();
  return l[20] = e[t], l;
}
function Hl(n) {
  let e;
  return {
    c() {
      e = he(
        /*label*/
        n[2]
      );
    },
    m(t, l) {
      P(t, e, l);
    },
    p(t, l) {
      l & /*label*/
      4 && Qe(
        e,
        /*label*/
        t[2]
      );
    },
    d(t) {
      t && O(e);
    }
  };
}
function Le(n) {
  let e, t, l, i, s, _ = Fe(
    /*quick_ranges*/
    n[11]
  ), a = [];
  for (let f = 0; f < _.length; f += 1)
    a[f] = Oe(Je(n, _, f));
  return {
    c() {
      e = U("div"), t = U("button"), t.textContent = "Back", l = ie();
      for (let f = 0; f < a.length; f += 1)
        a[f].c();
      R(t, "class", "quick-range svelte-11kze5"), He(
        t,
        "display",
        /*range_history*/
        n[12].length <= 1 ? "none" : "block"
      ), R(e, "class", "quick-ranges svelte-11kze5");
    },
    m(f, o) {
      P(f, e, o), A(e, t), A(e, l);
      for (let d = 0; d < a.length; d += 1)
        a[d] && a[d].m(e, null);
      i || (s = Ke(
        t,
        "click",
        /*back_in_history*/
        n[13]
      ), i = !0);
    },
    p(f, o) {
      if (o & /*range_history*/
      4096 && He(
        t,
        "display",
        /*range_history*/
        f[12].length <= 1 ? "none" : "block"
      ), o & /*value, quick_ranges*/
      2049) {
        _ = Fe(
          /*quick_ranges*/
          f[11]
        );
        let d;
        for (d = 0; d < _.length; d += 1) {
          const g = Je(f, _, d);
          a[d] ? a[d].p(g, o) : (a[d] = Oe(g), a[d].c(), a[d].m(e, null));
        }
        for (; d < a.length; d += 1)
          a[d].d(1);
        a.length = _.length;
      }
    },
    d(f) {
      f && O(e), Nl(a, f), i = !1, s();
    }
  };
}
function Oe(n) {
  let e, t, l = (
    /*quick_range*/
    n[20] + ""
  ), i, s, _;
  function a() {
    return (
      /*click_handler*/
      n[15](
        /*quick_range*/
        n[20]
      )
    );
  }
  return {
    c() {
      e = U("button"), t = he("Last "), i = he(l), R(e, "class", "quick-range svelte-11kze5");
    },
    m(f, o) {
      P(f, e, o), A(e, t), A(e, i), s || (_ = Ke(e, "click", a), s = !0);
    },
    p(f, o) {
      n = f, o & /*quick_ranges*/
      2048 && l !== (l = /*quick_range*/
      n[20] + "") && Qe(i, l);
    },
    d(f) {
      f && O(e), s = !1, _();
    }
  };
}
function Jl(n) {
  let e, t, l, i, s, _, a, f, o, d, g;
  t = new nn({
    props: {
      show_label: (
        /*show_label*/
        n[3]
      ),
      info: (
        /*info*/
        n[4]
      ),
      $$slots: { default: [Hl] },
      $$scope: { ctx: n }
    }
  });
  let w = (
    /*show_label*/
    n[3] && Le(n)
  );
  function C(r) {
    n[16](r);
  }
  let q = {
    show_label: !1,
    include_time: (
      /*include_time*/
      n[10]
    ),
    gradio: (
      /*gradio*/
      n[1]
    )
  };
  /*value*/
  n[0][0] !== void 0 && (q.value = /*value*/
  n[0][0]), _ = new Ie({ props: q }), Ne.push(() => Ee(_, "value", C)), _.$on(
    "gradio",
    /*gradio_handler*/
    n[17]
  );
  function v(r) {
    n[18](r);
  }
  let m = {
    show_label: !1,
    include_time: (
      /*include_time*/
      n[10]
    ),
    gradio: (
      /*gradio*/
      n[1]
    )
  };
  return (
    /*value*/
    n[0][1] !== void 0 && (m.value = /*value*/
    n[0][1]), o = new Ie({ props: m }), Ne.push(() => Ee(o, "value", v)), o.$on(
      "gradio",
      /*gradio_handler_1*/
      n[19]
    ), {
      c() {
        e = U("div"), te(t.$$.fragment), l = ie(), w && w.c(), i = ie(), s = U("div"), te(_.$$.fragment), f = ie(), te(o.$$.fragment), R(e, "class", "label-content svelte-11kze5"), R(s, "class", "times svelte-11kze5");
      },
      m(r, k) {
        P(r, e, k), le(t, e, null), A(e, l), w && w.m(e, null), P(r, i, k), P(r, s, k), le(_, s, null), A(s, f), le(o, s, null), g = !0;
      },
      p(r, k) {
        const y = {};
        k & /*show_label*/
        8 && (y.show_label = /*show_label*/
        r[3]), k & /*info*/
        16 && (y.info = /*info*/
        r[4]), k & /*$$scope, label*/
        8388612 && (y.$$scope = { dirty: k, ctx: r }), t.$set(y), /*show_label*/
        r[3] ? w ? w.p(r, k) : (w = Le(r), w.c(), w.m(e, null)) : w && (w.d(1), w = null);
        const j = {};
        k & /*include_time*/
        1024 && (j.include_time = /*include_time*/
        r[10]), k & /*gradio*/
        2 && (j.gradio = /*gradio*/
        r[1]), !a && k & /*value*/
        1 && (a = !0, j.value = /*value*/
        r[0][0], De(() => a = !1)), _.$set(j);
        const S = {};
        k & /*include_time*/
        1024 && (S.include_time = /*include_time*/
        r[10]), k & /*gradio*/
        2 && (S.gradio = /*gradio*/
        r[1]), !d && k & /*value*/
        1 && (d = !0, S.value = /*value*/
        r[0][1], De(() => d = !1)), o.$set(S);
      },
      i(r) {
        g || (fe(t.$$.fragment, r), fe(_.$$.fragment, r), fe(o.$$.fragment, r), g = !0);
      },
      o(r) {
        se(t.$$.fragment, r), se(_.$$.fragment, r), se(o.$$.fragment, r), g = !1;
      },
      d(r) {
        r && (O(e), O(i), O(s)), ne(t), w && w.d(), ne(_), ne(o);
      }
    }
  );
}
function Ll(n) {
  let e, t;
  return e = new kt({
    props: {
      visible: (
        /*visible*/
        n[7]
      ),
      elem_id: (
        /*elem_id*/
        n[5]
      ),
      elem_classes: (
        /*elem_classes*/
        n[6]
      ),
      scale: (
        /*scale*/
        n[8]
      ),
      min_width: (
        /*min_width*/
        n[9]
      ),
      allow_overflow: !1,
      padding: !0,
      $$slots: { default: [Jl] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      te(e.$$.fragment);
    },
    m(l, i) {
      le(e, l, i), t = !0;
    },
    p(l, [i]) {
      const s = {};
      i & /*visible*/
      128 && (s.visible = /*visible*/
      l[7]), i & /*elem_id*/
      32 && (s.elem_id = /*elem_id*/
      l[5]), i & /*elem_classes*/
      64 && (s.elem_classes = /*elem_classes*/
      l[6]), i & /*scale*/
      256 && (s.scale = /*scale*/
      l[8]), i & /*min_width*/
      512 && (s.min_width = /*min_width*/
      l[9]), i & /*$$scope, include_time, gradio, value, quick_ranges, range_history, show_label, info, label*/
      8395807 && (s.$$scope = { dirty: i, ctx: l }), e.$set(s);
    },
    i(l) {
      t || (fe(e.$$.fragment, l), t = !0);
    },
    o(l) {
      se(e.$$.fragment, l), t = !1;
    },
    d(l) {
      ne(e, l);
    }
  };
}
function Ol(n, e, t) {
  let { gradio: l } = e, { label: i = "Time" } = e, { show_label: s = !0 } = e, { info: _ = void 0 } = e, { elem_id: a = "" } = e, { elem_classes: f = [] } = e, { visible: o = !0 } = e, { value: d = ["", ""] } = e, g = d, { scale: w = null } = e, { min_width: C = void 0 } = e, { include_time: q = !0 } = e, { quick_ranges: v = [] } = e, m = [d];
  const r = () => {
    m.pop();
    const b = m.pop();
    b === void 0 ? (t(0, d = ["", ""]), t(12, m = [])) : (t(0, d = b), l.dispatch("change"), t(12, m = [...m]));
  }, k = (b) => {
    t(0, d = ["now - " + b, "now"]);
  };
  function y(b) {
    n.$$.not_equal(d[0], b) && (d[0] = b, t(0, d));
  }
  function j(b) {
    Me.call(this, n, b);
  }
  function S(b) {
    n.$$.not_equal(d[1], b) && (d[1] = b, t(0, d));
  }
  function u(b) {
    Me.call(this, n, b);
  }
  return n.$$set = (b) => {
    "gradio" in b && t(1, l = b.gradio), "label" in b && t(2, i = b.label), "show_label" in b && t(3, s = b.show_label), "info" in b && t(4, _ = b.info), "elem_id" in b && t(5, a = b.elem_id), "elem_classes" in b && t(6, f = b.elem_classes), "visible" in b && t(7, o = b.visible), "value" in b && t(0, d = b.value), "scale" in b && t(8, w = b.scale), "min_width" in b && t(9, C = b.min_width), "include_time" in b && t(10, q = b.include_time), "quick_ranges" in b && t(11, v = b.quick_ranges);
  }, n.$$.update = () => {
    n.$$.dirty & /*value, old_value, range_history*/
    20481 && (d[0] !== g[0] || d[1] !== g[1]) && (t(14, g = d), t(12, m = [...m, d]));
  }, [
    d,
    l,
    i,
    s,
    _,
    a,
    f,
    o,
    w,
    C,
    q,
    v,
    m,
    r,
    g,
    k,
    y,
    j,
    S,
    u
  ];
}
class Ql extends El {
  constructor(e) {
    super(), Ml(this, e, Ol, Ll, Fl, {
      gradio: 1,
      label: 2,
      show_label: 3,
      info: 4,
      elem_id: 5,
      elem_classes: 6,
      visible: 7,
      value: 0,
      scale: 8,
      min_width: 9,
      include_time: 10,
      quick_ranges: 11
    });
  }
}
export {
  Kl as BaseExample,
  Ql as default
};
