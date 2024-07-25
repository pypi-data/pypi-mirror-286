const { setContext: $l, getContext: Bn } = window.__gradio__svelte__internal, Xn = "WORKER_PROXY_CONTEXT_KEY";
function Yn() {
  return Bn(Xn);
}
function Hn(n) {
  return n.host === window.location.host || n.host === "localhost:7860" || n.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  n.host === "lite.local";
}
function Dn(n, e) {
  const t = e.toLowerCase();
  for (const [i, s] of Object.entries(n))
    if (i.toLowerCase() === t)
      return s;
}
function Rn(n) {
  if (n == null)
    return !1;
  const e = new URL(n, window.location.href);
  return !(!Hn(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
async function Ln(n) {
  if (n == null || !Rn(n))
    return n;
  const e = Yn();
  if (e == null)
    return n;
  const i = new URL(n, window.location.href).pathname;
  return e.httpRequest({
    method: "GET",
    path: i,
    headers: {},
    query_string: ""
  }).then((s) => {
    if (s.status !== 200)
      throw new Error(`Failed to get file ${i} from the Wasm worker.`);
    const l = new Blob([s.body], {
      type: Dn(s.headers, "content-type")
    });
    return URL.createObjectURL(l);
  });
}
const {
  SvelteComponent: Tn,
  append: J,
  attr: k,
  detach: qn,
  init: On,
  insert: In,
  noop: st,
  safe_not_equal: Un,
  set_style: Z,
  svg_element: K
} = window.__gradio__svelte__internal;
function Wn(n) {
  let e, t, i, s, l, r, a, o, u;
  return {
    c() {
      e = K("svg"), t = K("rect"), i = K("rect"), s = K("rect"), l = K("rect"), r = K("line"), a = K("line"), o = K("line"), u = K("line"), k(t, "x", "2"), k(t, "y", "2"), k(t, "width", "5"), k(t, "height", "5"), k(t, "rx", "1"), k(t, "ry", "1"), k(t, "stroke-width", "2"), k(t, "fill", "none"), k(i, "x", "17"), k(i, "y", "2"), k(i, "width", "5"), k(i, "height", "5"), k(i, "rx", "1"), k(i, "ry", "1"), k(i, "stroke-width", "2"), k(i, "fill", "none"), k(s, "x", "2"), k(s, "y", "17"), k(s, "width", "5"), k(s, "height", "5"), k(s, "rx", "1"), k(s, "ry", "1"), k(s, "stroke-width", "2"), k(s, "fill", "none"), k(l, "x", "17"), k(l, "y", "17"), k(l, "width", "5"), k(l, "height", "5"), k(l, "rx", "1"), k(l, "ry", "1"), k(l, "stroke-width", "2"), k(l, "fill", "none"), k(r, "x1", "7.5"), k(r, "y1", "4.5"), k(r, "x2", "16"), k(r, "y2", "4.5"), Z(r, "stroke-width", "2px"), k(a, "x1", "7.5"), k(a, "y1", "19.5"), k(a, "x2", "16"), k(a, "y2", "19.5"), Z(a, "stroke-width", "2px"), k(o, "x1", "4.5"), k(o, "y1", "8"), k(o, "x2", "4.5"), k(o, "y2", "16"), Z(o, "stroke-width", "2px"), k(u, "x1", "19.5"), k(u, "y1", "8"), k(u, "x2", "19.5"), k(u, "y2", "16"), Z(u, "stroke-width", "2px"), k(e, "width", "100%"), k(e, "height", "100%"), k(e, "viewBox", "0 0 24 24"), k(e, "version", "1.1"), k(e, "xmlns", "http://www.w3.org/2000/svg"), k(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), k(e, "xml:space", "preserve"), k(e, "stroke", "currentColor"), Z(e, "fill-rule", "evenodd"), Z(e, "clip-rule", "evenodd"), Z(e, "stroke-linecap", "round"), Z(e, "stroke-linejoin", "round");
    },
    m(f, c) {
      In(f, e, c), J(e, t), J(e, i), J(e, s), J(e, l), J(e, r), J(e, a), J(e, o), J(e, u);
    },
    p: st,
    i: st,
    o: st,
    d(f) {
      f && qn(e);
    }
  };
}
class jn extends Tn {
  constructor(e) {
    super(), On(this, e, null, Wn, Un, {});
  }
}
const {
  SvelteComponent: Nn,
  append: Vn,
  attr: N,
  detach: Fn,
  init: Pn,
  insert: Kn,
  noop: lt,
  safe_not_equal: Gn,
  set_style: Re,
  svg_element: Mt
} = window.__gradio__svelte__internal;
function Jn(n) {
  let e, t;
  return {
    c() {
      e = Mt("svg"), t = Mt("path"), N(t, "d", "M 14.4 2.85 V 11.1 V 3.95 C 14.4 3.0387 15.1388 2.3 16.05 2.3 C 16.9612 2.3 17.7 3.0387 17.7 3.95 V 11.1 V 7.25 C 17.7 6.3387 18.4388 5.6 19.35 5.6 C 20.2612 5.6 21 6.3387 21 7.25 V 16.6 C 21 20.2451 18.0451 23.2 14.4 23.2 H 13.16 C 11.4831 23.2 9.8692 22.5618 8.6459 21.4149 L 3.1915 16.3014 C 2.403 15.5622 2.3829 14.3171 3.1472 13.5528 C 3.8943 12.8057 5.1057 12.8057 5.8528 13.5528 L 7.8 15.5 V 6.15 C 7.8 5.2387 8.5387 4.5 9.45 4.5 C 10.3612 4.5 11.1 5.2387 11.1 6.15 V 11.1 V 2.85 C 11.1 1.9387 11.8388 1.2 12.75 1.2 C 13.6612 1.2 14.4 1.9387 14.4 2.85 Z"), N(t, "fill", "none"), N(t, "stroke-width", "2"), N(e, "width", "100%"), N(e, "height", "100%"), N(e, "viewBox", "0 0 24 24"), N(e, "version", "1.1"), N(e, "xmlns", "http://www.w3.org/2000/svg"), N(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), N(e, "xml:space", "preserve"), N(e, "stroke", "currentColor"), Re(e, "fill-rule", "evenodd"), Re(e, "clip-rule", "evenodd"), Re(e, "stroke-linecap", "round"), Re(e, "stroke-linejoin", "round");
    },
    m(i, s) {
      Kn(i, e, s), Vn(e, t);
    },
    p: lt,
    i: lt,
    o: lt,
    d(i) {
      i && Fn(e);
    }
  };
}
class Zn extends Nn {
  constructor(e) {
    super(), Pn(this, e, null, Jn, Gn, {});
  }
}
const {
  SvelteComponent: Qn,
  attr: $n,
  create_slot: ei,
  detach: ti,
  element: ni,
  get_all_dirty_from_scope: ii,
  get_slot_changes: si,
  init: li,
  insert: oi,
  safe_not_equal: ai,
  transition_in: ri,
  transition_out: fi,
  update_slot_base: ci
} = window.__gradio__svelte__internal;
function ui(n) {
  let e, t;
  const i = (
    /*#slots*/
    n[1].default
  ), s = ei(
    i,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = ni("div"), s && s.c(), $n(e, "class", "svelte-1hnfib2");
    },
    m(l, r) {
      oi(l, e, r), s && s.m(e, null), t = !0;
    },
    p(l, [r]) {
      s && s.p && (!t || r & /*$$scope*/
      1) && ci(
        s,
        i,
        l,
        /*$$scope*/
        l[0],
        t ? si(
          i,
          /*$$scope*/
          l[0],
          r,
          null
        ) : ii(
          /*$$scope*/
          l[0]
        ),
        null
      );
    },
    i(l) {
      t || (ri(s, l), t = !0);
    },
    o(l) {
      fi(s, l), t = !1;
    },
    d(l) {
      l && ti(e), s && s.d(l);
    }
  };
}
function hi(n, e, t) {
  let { $$slots: i = {}, $$scope: s } = e;
  return n.$$set = (l) => {
    "$$scope" in l && t(0, s = l.$$scope);
  }, [s, i];
}
class mi extends Qn {
  constructor(e) {
    super(), li(this, e, hi, ui, ai, {});
  }
}
const {
  SvelteComponent: _i,
  attr: Bt,
  check_outros: di,
  create_component: bi,
  create_slot: gi,
  destroy_component: wi,
  detach: Ie,
  element: yi,
  empty: vi,
  get_all_dirty_from_scope: ki,
  get_slot_changes: pi,
  group_outros: xi,
  init: Ci,
  insert: Ue,
  mount_component: Si,
  safe_not_equal: zi,
  set_data: Ei,
  space: Ai,
  text: Mi,
  toggle_class: oe,
  transition_in: we,
  transition_out: We,
  update_slot_base: Bi
} = window.__gradio__svelte__internal;
function Xt(n) {
  let e, t;
  return e = new mi({
    props: {
      $$slots: { default: [Xi] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      bi(e.$$.fragment);
    },
    m(i, s) {
      Si(e, i, s), t = !0;
    },
    p(i, s) {
      const l = {};
      s & /*$$scope, info*/
      10 && (l.$$scope = { dirty: s, ctx: i }), e.$set(l);
    },
    i(i) {
      t || (we(e.$$.fragment, i), t = !0);
    },
    o(i) {
      We(e.$$.fragment, i), t = !1;
    },
    d(i) {
      wi(e, i);
    }
  };
}
function Xi(n) {
  let e;
  return {
    c() {
      e = Mi(
        /*info*/
        n[1]
      );
    },
    m(t, i) {
      Ue(t, e, i);
    },
    p(t, i) {
      i & /*info*/
      2 && Ei(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Ie(e);
    }
  };
}
function Yi(n) {
  let e, t, i, s;
  const l = (
    /*#slots*/
    n[2].default
  ), r = gi(
    l,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let a = (
    /*info*/
    n[1] && Xt(n)
  );
  return {
    c() {
      e = yi("span"), r && r.c(), t = Ai(), a && a.c(), i = vi(), Bt(e, "data-testid", "block-info"), Bt(e, "class", "svelte-22c38v"), oe(e, "sr-only", !/*show_label*/
      n[0]), oe(e, "hide", !/*show_label*/
      n[0]), oe(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(o, u) {
      Ue(o, e, u), r && r.m(e, null), Ue(o, t, u), a && a.m(o, u), Ue(o, i, u), s = !0;
    },
    p(o, [u]) {
      r && r.p && (!s || u & /*$$scope*/
      8) && Bi(
        r,
        l,
        o,
        /*$$scope*/
        o[3],
        s ? pi(
          l,
          /*$$scope*/
          o[3],
          u,
          null
        ) : ki(
          /*$$scope*/
          o[3]
        ),
        null
      ), (!s || u & /*show_label*/
      1) && oe(e, "sr-only", !/*show_label*/
      o[0]), (!s || u & /*show_label*/
      1) && oe(e, "hide", !/*show_label*/
      o[0]), (!s || u & /*info*/
      2) && oe(
        e,
        "has-info",
        /*info*/
        o[1] != null
      ), /*info*/
      o[1] ? a ? (a.p(o, u), u & /*info*/
      2 && we(a, 1)) : (a = Xt(o), a.c(), we(a, 1), a.m(i.parentNode, i)) : a && (xi(), We(a, 1, 1, () => {
        a = null;
      }), di());
    },
    i(o) {
      s || (we(r, o), we(a), s = !0);
    },
    o(o) {
      We(r, o), We(a), s = !1;
    },
    d(o) {
      o && (Ie(e), Ie(t), Ie(i)), r && r.d(o), a && a.d(o);
    }
  };
}
function Hi(n, e, t) {
  let { $$slots: i = {}, $$scope: s } = e, { show_label: l = !0 } = e, { info: r = void 0 } = e;
  return n.$$set = (a) => {
    "show_label" in a && t(0, l = a.show_label), "info" in a && t(1, r = a.info), "$$scope" in a && t(3, s = a.$$scope);
  }, [l, r, i, s];
}
class ln extends _i {
  constructor(e) {
    super(), Ci(this, e, Hi, Yi, zi, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Di,
  append: Ri,
  attr: ae,
  detach: Li,
  init: Ti,
  insert: qi,
  noop: ot,
  safe_not_equal: Oi,
  svg_element: Yt
} = window.__gradio__svelte__internal;
function Ii(n) {
  let e, t;
  return {
    c() {
      e = Yt("svg"), t = Yt("path"), ae(t, "d", "M5 8l4 4 4-4z"), ae(e, "class", "dropdown-arrow svelte-145leq6"), ae(e, "xmlns", "http://www.w3.org/2000/svg"), ae(e, "width", "100%"), ae(e, "height", "100%"), ae(e, "viewBox", "0 0 18 18");
    },
    m(i, s) {
      qi(i, e, s), Ri(e, t);
    },
    p: ot,
    i: ot,
    o: ot,
    d(i) {
      i && Li(e);
    }
  };
}
class Ui extends Di {
  constructor(e) {
    super(), Ti(this, e, null, Ii, Oi, {});
  }
}
const Wi = [
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
], Ht = {
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
Wi.reduce(
  (n, { color: e, primary: t, secondary: i }) => ({
    ...n,
    [e]: {
      primary: Ht[e][t],
      secondary: Ht[e][i]
    }
  }),
  {}
);
const {
  SvelteComponent: ji,
  append: Dt,
  attr: at,
  bubble: Rt,
  create_component: Ni,
  destroy_component: Vi,
  detach: on,
  element: Lt,
  init: Fi,
  insert: an,
  listen: rt,
  mount_component: Pi,
  run_all: Ki,
  safe_not_equal: Gi,
  set_data: Ji,
  set_input_value: Tt,
  space: Zi,
  text: Qi,
  transition_in: $i,
  transition_out: es
} = window.__gradio__svelte__internal, { createEventDispatcher: ts, afterUpdate: ns } = window.__gradio__svelte__internal;
function is(n) {
  let e;
  return {
    c() {
      e = Qi(
        /*label*/
        n[1]
      );
    },
    m(t, i) {
      an(t, e, i);
    },
    p(t, i) {
      i & /*label*/
      2 && Ji(
        e,
        /*label*/
        t[1]
      );
    },
    d(t) {
      t && on(e);
    }
  };
}
function ss(n) {
  let e, t, i, s, l, r, a;
  return t = new ln({
    props: {
      show_label: (
        /*show_label*/
        n[4]
      ),
      info: (
        /*info*/
        n[2]
      ),
      $$slots: { default: [is] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      e = Lt("label"), Ni(t.$$.fragment), i = Zi(), s = Lt("input"), at(s, "type", "color"), s.disabled = /*disabled*/
      n[3], at(s, "class", "svelte-16l8u73"), at(e, "class", "block");
    },
    m(o, u) {
      an(o, e, u), Pi(t, e, null), Dt(e, i), Dt(e, s), Tt(
        s,
        /*value*/
        n[0]
      ), l = !0, r || (a = [
        rt(
          s,
          "input",
          /*input_input_handler*/
          n[8]
        ),
        rt(
          s,
          "focus",
          /*focus_handler*/
          n[6]
        ),
        rt(
          s,
          "blur",
          /*blur_handler*/
          n[7]
        )
      ], r = !0);
    },
    p(o, [u]) {
      const f = {};
      u & /*show_label*/
      16 && (f.show_label = /*show_label*/
      o[4]), u & /*info*/
      4 && (f.info = /*info*/
      o[2]), u & /*$$scope, label*/
      2050 && (f.$$scope = { dirty: u, ctx: o }), t.$set(f), (!l || u & /*disabled*/
      8) && (s.disabled = /*disabled*/
      o[3]), u & /*value*/
      1 && Tt(
        s,
        /*value*/
        o[0]
      );
    },
    i(o) {
      l || ($i(t.$$.fragment, o), l = !0);
    },
    o(o) {
      es(t.$$.fragment, o), l = !1;
    },
    d(o) {
      o && on(e), Vi(t), r = !1, Ki(a);
    }
  };
}
function ls(n, e, t) {
  let { value: i = "#000000" } = e, { value_is_output: s = !1 } = e, { label: l } = e, { info: r = void 0 } = e, { disabled: a = !1 } = e, { show_label: o = !0 } = e;
  const u = ts();
  function f() {
    u("change", i), s || u("input");
  }
  ns(() => {
    t(5, s = !1);
  });
  function c(v) {
    Rt.call(this, n, v);
  }
  function w(v) {
    Rt.call(this, n, v);
  }
  function g() {
    i = this.value, t(0, i);
  }
  return n.$$set = (v) => {
    "value" in v && t(0, i = v.value), "value_is_output" in v && t(5, s = v.value_is_output), "label" in v && t(1, l = v.label), "info" in v && t(2, r = v.info), "disabled" in v && t(3, a = v.disabled), "show_label" in v && t(4, o = v.show_label);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    1 && f();
  }, [
    i,
    l,
    r,
    a,
    o,
    s,
    c,
    w,
    g
  ];
}
class os extends ji {
  constructor(e) {
    super(), Fi(this, e, ls, ss, Gi, {
      value: 0,
      value_is_output: 5,
      label: 1,
      info: 2,
      disabled: 3,
      show_label: 4
    });
  }
}
function qt(n) {
  const e = typeof n == "string" && n.match(/^\s*(-?[\d.]+)([^\s]*)\s*$/);
  return e ? [parseFloat(e[1]), e[2] || "px"] : [
    /** @type {number} */
    n,
    "px"
  ];
}
function as(n) {
  const e = n - 1;
  return e * e * e + 1;
}
function Ot(n, { delay: e = 0, duration: t = 400, easing: i = as, x: s = 0, y: l = 0, opacity: r = 0 } = {}) {
  const a = getComputedStyle(n), o = +a.opacity, u = a.transform === "none" ? "" : a.transform, f = o * (1 - r), [c, w] = qt(s), [g, v] = qt(l);
  return {
    delay: e,
    duration: t,
    easing: i,
    css: (_, d) => `
			transform: ${u} translate(${(1 - _) * c}${w}, ${(1 - _) * g}${v});
			opacity: ${o - f * d}`
  };
}
const {
  SvelteComponent: rs,
  append: rn,
  attr: X,
  bubble: fs,
  check_outros: cs,
  create_slot: fn,
  detach: Ae,
  element: $e,
  empty: us,
  get_all_dirty_from_scope: cn,
  get_slot_changes: un,
  group_outros: hs,
  init: ms,
  insert: Me,
  listen: _s,
  safe_not_equal: ds,
  set_style: T,
  space: hn,
  src_url_equal: Fe,
  toggle_class: de,
  transition_in: Pe,
  transition_out: Ke,
  update_slot_base: mn
} = window.__gradio__svelte__internal;
function bs(n) {
  let e, t, i, s, l, r, a = (
    /*icon*/
    n[7] && It(n)
  );
  const o = (
    /*#slots*/
    n[12].default
  ), u = fn(
    o,
    n,
    /*$$scope*/
    n[11],
    null
  );
  return {
    c() {
      e = $e("button"), a && a.c(), t = hn(), u && u.c(), X(e, "class", i = /*size*/
      n[4] + " " + /*variant*/
      n[3] + " " + /*elem_classes*/
      n[1].join(" ") + " svelte-8huxfn"), X(
        e,
        "id",
        /*elem_id*/
        n[0]
      ), e.disabled = /*disabled*/
      n[8], de(e, "hidden", !/*visible*/
      n[2]), T(
        e,
        "flex-grow",
        /*scale*/
        n[9]
      ), T(
        e,
        "width",
        /*scale*/
        n[9] === 0 ? "fit-content" : null
      ), T(e, "min-width", typeof /*min_width*/
      n[10] == "number" ? `calc(min(${/*min_width*/
      n[10]}px, 100%))` : null);
    },
    m(f, c) {
      Me(f, e, c), a && a.m(e, null), rn(e, t), u && u.m(e, null), s = !0, l || (r = _s(
        e,
        "click",
        /*click_handler*/
        n[13]
      ), l = !0);
    },
    p(f, c) {
      /*icon*/
      f[7] ? a ? a.p(f, c) : (a = It(f), a.c(), a.m(e, t)) : a && (a.d(1), a = null), u && u.p && (!s || c & /*$$scope*/
      2048) && mn(
        u,
        o,
        f,
        /*$$scope*/
        f[11],
        s ? un(
          o,
          /*$$scope*/
          f[11],
          c,
          null
        ) : cn(
          /*$$scope*/
          f[11]
        ),
        null
      ), (!s || c & /*size, variant, elem_classes*/
      26 && i !== (i = /*size*/
      f[4] + " " + /*variant*/
      f[3] + " " + /*elem_classes*/
      f[1].join(" ") + " svelte-8huxfn")) && X(e, "class", i), (!s || c & /*elem_id*/
      1) && X(
        e,
        "id",
        /*elem_id*/
        f[0]
      ), (!s || c & /*disabled*/
      256) && (e.disabled = /*disabled*/
      f[8]), (!s || c & /*size, variant, elem_classes, visible*/
      30) && de(e, "hidden", !/*visible*/
      f[2]), c & /*scale*/
      512 && T(
        e,
        "flex-grow",
        /*scale*/
        f[9]
      ), c & /*scale*/
      512 && T(
        e,
        "width",
        /*scale*/
        f[9] === 0 ? "fit-content" : null
      ), c & /*min_width*/
      1024 && T(e, "min-width", typeof /*min_width*/
      f[10] == "number" ? `calc(min(${/*min_width*/
      f[10]}px, 100%))` : null);
    },
    i(f) {
      s || (Pe(u, f), s = !0);
    },
    o(f) {
      Ke(u, f), s = !1;
    },
    d(f) {
      f && Ae(e), a && a.d(), u && u.d(f), l = !1, r();
    }
  };
}
function gs(n) {
  let e, t, i, s, l = (
    /*icon*/
    n[7] && Ut(n)
  );
  const r = (
    /*#slots*/
    n[12].default
  ), a = fn(
    r,
    n,
    /*$$scope*/
    n[11],
    null
  );
  return {
    c() {
      e = $e("a"), l && l.c(), t = hn(), a && a.c(), X(
        e,
        "href",
        /*link*/
        n[6]
      ), X(e, "rel", "noopener noreferrer"), X(
        e,
        "aria-disabled",
        /*disabled*/
        n[8]
      ), X(e, "class", i = /*size*/
      n[4] + " " + /*variant*/
      n[3] + " " + /*elem_classes*/
      n[1].join(" ") + " svelte-8huxfn"), X(
        e,
        "id",
        /*elem_id*/
        n[0]
      ), de(e, "hidden", !/*visible*/
      n[2]), de(
        e,
        "disabled",
        /*disabled*/
        n[8]
      ), T(
        e,
        "flex-grow",
        /*scale*/
        n[9]
      ), T(
        e,
        "pointer-events",
        /*disabled*/
        n[8] ? "none" : null
      ), T(
        e,
        "width",
        /*scale*/
        n[9] === 0 ? "fit-content" : null
      ), T(e, "min-width", typeof /*min_width*/
      n[10] == "number" ? `calc(min(${/*min_width*/
      n[10]}px, 100%))` : null);
    },
    m(o, u) {
      Me(o, e, u), l && l.m(e, null), rn(e, t), a && a.m(e, null), s = !0;
    },
    p(o, u) {
      /*icon*/
      o[7] ? l ? l.p(o, u) : (l = Ut(o), l.c(), l.m(e, t)) : l && (l.d(1), l = null), a && a.p && (!s || u & /*$$scope*/
      2048) && mn(
        a,
        r,
        o,
        /*$$scope*/
        o[11],
        s ? un(
          r,
          /*$$scope*/
          o[11],
          u,
          null
        ) : cn(
          /*$$scope*/
          o[11]
        ),
        null
      ), (!s || u & /*link*/
      64) && X(
        e,
        "href",
        /*link*/
        o[6]
      ), (!s || u & /*disabled*/
      256) && X(
        e,
        "aria-disabled",
        /*disabled*/
        o[8]
      ), (!s || u & /*size, variant, elem_classes*/
      26 && i !== (i = /*size*/
      o[4] + " " + /*variant*/
      o[3] + " " + /*elem_classes*/
      o[1].join(" ") + " svelte-8huxfn")) && X(e, "class", i), (!s || u & /*elem_id*/
      1) && X(
        e,
        "id",
        /*elem_id*/
        o[0]
      ), (!s || u & /*size, variant, elem_classes, visible*/
      30) && de(e, "hidden", !/*visible*/
      o[2]), (!s || u & /*size, variant, elem_classes, disabled*/
      282) && de(
        e,
        "disabled",
        /*disabled*/
        o[8]
      ), u & /*scale*/
      512 && T(
        e,
        "flex-grow",
        /*scale*/
        o[9]
      ), u & /*disabled*/
      256 && T(
        e,
        "pointer-events",
        /*disabled*/
        o[8] ? "none" : null
      ), u & /*scale*/
      512 && T(
        e,
        "width",
        /*scale*/
        o[9] === 0 ? "fit-content" : null
      ), u & /*min_width*/
      1024 && T(e, "min-width", typeof /*min_width*/
      o[10] == "number" ? `calc(min(${/*min_width*/
      o[10]}px, 100%))` : null);
    },
    i(o) {
      s || (Pe(a, o), s = !0);
    },
    o(o) {
      Ke(a, o), s = !1;
    },
    d(o) {
      o && Ae(e), l && l.d(), a && a.d(o);
    }
  };
}
function It(n) {
  let e, t, i;
  return {
    c() {
      e = $e("img"), X(e, "class", "button-icon svelte-8huxfn"), Fe(e.src, t = /*icon*/
      n[7].url) || X(e, "src", t), X(e, "alt", i = `${/*value*/
      n[5]} icon`);
    },
    m(s, l) {
      Me(s, e, l);
    },
    p(s, l) {
      l & /*icon*/
      128 && !Fe(e.src, t = /*icon*/
      s[7].url) && X(e, "src", t), l & /*value*/
      32 && i !== (i = `${/*value*/
      s[5]} icon`) && X(e, "alt", i);
    },
    d(s) {
      s && Ae(e);
    }
  };
}
function Ut(n) {
  let e, t, i;
  return {
    c() {
      e = $e("img"), X(e, "class", "button-icon svelte-8huxfn"), Fe(e.src, t = /*icon*/
      n[7].url) || X(e, "src", t), X(e, "alt", i = `${/*value*/
      n[5]} icon`);
    },
    m(s, l) {
      Me(s, e, l);
    },
    p(s, l) {
      l & /*icon*/
      128 && !Fe(e.src, t = /*icon*/
      s[7].url) && X(e, "src", t), l & /*value*/
      32 && i !== (i = `${/*value*/
      s[5]} icon`) && X(e, "alt", i);
    },
    d(s) {
      s && Ae(e);
    }
  };
}
function ws(n) {
  let e, t, i, s;
  const l = [gs, bs], r = [];
  function a(o, u) {
    return (
      /*link*/
      o[6] && /*link*/
      o[6].length > 0 ? 0 : 1
    );
  }
  return e = a(n), t = r[e] = l[e](n), {
    c() {
      t.c(), i = us();
    },
    m(o, u) {
      r[e].m(o, u), Me(o, i, u), s = !0;
    },
    p(o, [u]) {
      let f = e;
      e = a(o), e === f ? r[e].p(o, u) : (hs(), Ke(r[f], 1, 1, () => {
        r[f] = null;
      }), cs(), t = r[e], t ? t.p(o, u) : (t = r[e] = l[e](o), t.c()), Pe(t, 1), t.m(i.parentNode, i));
    },
    i(o) {
      s || (Pe(t), s = !0);
    },
    o(o) {
      Ke(t), s = !1;
    },
    d(o) {
      o && Ae(i), r[e].d(o);
    }
  };
}
function ys(n, e, t) {
  let { $$slots: i = {}, $$scope: s } = e, { elem_id: l = "" } = e, { elem_classes: r = [] } = e, { visible: a = !0 } = e, { variant: o = "secondary" } = e, { size: u = "lg" } = e, { value: f = null } = e, { link: c = null } = e, { icon: w = null } = e, { disabled: g = !1 } = e, { scale: v = null } = e, { min_width: _ = void 0 } = e;
  function d(m) {
    fs.call(this, n, m);
  }
  return n.$$set = (m) => {
    "elem_id" in m && t(0, l = m.elem_id), "elem_classes" in m && t(1, r = m.elem_classes), "visible" in m && t(2, a = m.visible), "variant" in m && t(3, o = m.variant), "size" in m && t(4, u = m.size), "value" in m && t(5, f = m.value), "link" in m && t(6, c = m.link), "icon" in m && t(7, w = m.icon), "disabled" in m && t(8, g = m.disabled), "scale" in m && t(9, v = m.scale), "min_width" in m && t(10, _ = m.min_width), "$$scope" in m && t(11, s = m.$$scope);
  }, [
    l,
    r,
    a,
    o,
    u,
    f,
    c,
    w,
    g,
    v,
    _,
    s,
    i,
    d
  ];
}
class bt extends rs {
  constructor(e) {
    super(), ms(this, e, ys, ws, ds, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
const {
  SvelteComponent: vs,
  add_render_callback: _n,
  append: Le,
  attr: O,
  binding_callbacks: Wt,
  check_outros: ks,
  create_bidirectional_transition: jt,
  destroy_each: ps,
  detach: Ce,
  element: Ge,
  empty: xs,
  ensure_array_like: Nt,
  group_outros: Cs,
  init: Ss,
  insert: Se,
  listen: gt,
  prevent_default: zs,
  run_all: Es,
  safe_not_equal: As,
  set_data: Ms,
  set_style: re,
  space: wt,
  text: Bs,
  toggle_class: V,
  transition_in: ft,
  transition_out: Vt
} = window.__gradio__svelte__internal, { createEventDispatcher: Xs } = window.__gradio__svelte__internal;
function Ft(n, e, t) {
  const i = n.slice();
  return i[26] = e[t], i;
}
function Pt(n) {
  let e, t, i, s, l, r = Nt(
    /*filtered_indices*/
    n[1]
  ), a = [];
  for (let o = 0; o < r.length; o += 1)
    a[o] = Kt(Ft(n, r, o));
  return {
    c() {
      e = Ge("ul");
      for (let o = 0; o < a.length; o += 1)
        a[o].c();
      O(e, "class", "options svelte-yuohum"), O(e, "role", "listbox"), re(
        e,
        "bottom",
        /*bottom*/
        n[9]
      ), re(e, "max-height", `calc(${/*max_height*/
      n[10]}px - var(--window-padding))`), re(
        e,
        "width",
        /*input_width*/
        n[8] + "px"
      );
    },
    m(o, u) {
      Se(o, e, u);
      for (let f = 0; f < a.length; f += 1)
        a[f] && a[f].m(e, null);
      n[22](e), i = !0, s || (l = gt(e, "mousedown", zs(
        /*mousedown_handler*/
        n[21]
      )), s = !0);
    },
    p(o, u) {
      if (u & /*filtered_indices, choices, selected_indices, active_index*/
      51) {
        r = Nt(
          /*filtered_indices*/
          o[1]
        );
        let f;
        for (f = 0; f < r.length; f += 1) {
          const c = Ft(o, r, f);
          a[f] ? a[f].p(c, u) : (a[f] = Kt(c), a[f].c(), a[f].m(e, null));
        }
        for (; f < a.length; f += 1)
          a[f].d(1);
        a.length = r.length;
      }
      u & /*bottom*/
      512 && re(
        e,
        "bottom",
        /*bottom*/
        o[9]
      ), u & /*max_height*/
      1024 && re(e, "max-height", `calc(${/*max_height*/
      o[10]}px - var(--window-padding))`), u & /*input_width*/
      256 && re(
        e,
        "width",
        /*input_width*/
        o[8] + "px"
      );
    },
    i(o) {
      i || (o && _n(() => {
        i && (t || (t = jt(e, Ot, { duration: 200, y: 5 }, !0)), t.run(1));
      }), i = !0);
    },
    o(o) {
      o && (t || (t = jt(e, Ot, { duration: 200, y: 5 }, !1)), t.run(0)), i = !1;
    },
    d(o) {
      o && Ce(e), ps(a, o), n[22](null), o && t && t.end(), s = !1, l();
    }
  };
}
function Kt(n) {
  let e, t, i, s = (
    /*choices*/
    n[0][
      /*index*/
      n[26]
    ][0] + ""
  ), l, r, a, o, u;
  return {
    c() {
      e = Ge("li"), t = Ge("span"), t.textContent = "✓", i = wt(), l = Bs(s), r = wt(), O(t, "class", "inner-item svelte-yuohum"), V(t, "hide", !/*selected_indices*/
      n[4].includes(
        /*index*/
        n[26]
      )), O(e, "class", "item svelte-yuohum"), O(e, "data-index", a = /*index*/
      n[26]), O(e, "aria-label", o = /*choices*/
      n[0][
        /*index*/
        n[26]
      ][0]), O(e, "data-testid", "dropdown-option"), O(e, "role", "option"), O(e, "aria-selected", u = /*selected_indices*/
      n[4].includes(
        /*index*/
        n[26]
      )), V(
        e,
        "selected",
        /*selected_indices*/
        n[4].includes(
          /*index*/
          n[26]
        )
      ), V(
        e,
        "active",
        /*index*/
        n[26] === /*active_index*/
        n[5]
      ), V(
        e,
        "bg-gray-100",
        /*index*/
        n[26] === /*active_index*/
        n[5]
      ), V(
        e,
        "dark:bg-gray-600",
        /*index*/
        n[26] === /*active_index*/
        n[5]
      );
    },
    m(f, c) {
      Se(f, e, c), Le(e, t), Le(e, i), Le(e, l), Le(e, r);
    },
    p(f, c) {
      c & /*selected_indices, filtered_indices*/
      18 && V(t, "hide", !/*selected_indices*/
      f[4].includes(
        /*index*/
        f[26]
      )), c & /*choices, filtered_indices*/
      3 && s !== (s = /*choices*/
      f[0][
        /*index*/
        f[26]
      ][0] + "") && Ms(l, s), c & /*filtered_indices*/
      2 && a !== (a = /*index*/
      f[26]) && O(e, "data-index", a), c & /*choices, filtered_indices*/
      3 && o !== (o = /*choices*/
      f[0][
        /*index*/
        f[26]
      ][0]) && O(e, "aria-label", o), c & /*selected_indices, filtered_indices*/
      18 && u !== (u = /*selected_indices*/
      f[4].includes(
        /*index*/
        f[26]
      )) && O(e, "aria-selected", u), c & /*selected_indices, filtered_indices*/
      18 && V(
        e,
        "selected",
        /*selected_indices*/
        f[4].includes(
          /*index*/
          f[26]
        )
      ), c & /*filtered_indices, active_index*/
      34 && V(
        e,
        "active",
        /*index*/
        f[26] === /*active_index*/
        f[5]
      ), c & /*filtered_indices, active_index*/
      34 && V(
        e,
        "bg-gray-100",
        /*index*/
        f[26] === /*active_index*/
        f[5]
      ), c & /*filtered_indices, active_index*/
      34 && V(
        e,
        "dark:bg-gray-600",
        /*index*/
        f[26] === /*active_index*/
        f[5]
      );
    },
    d(f) {
      f && Ce(e);
    }
  };
}
function Ys(n) {
  let e, t, i, s, l;
  _n(
    /*onwindowresize*/
    n[19]
  );
  let r = (
    /*show_options*/
    n[2] && !/*disabled*/
    n[3] && Pt(n)
  );
  return {
    c() {
      e = Ge("div"), t = wt(), r && r.c(), i = xs(), O(e, "class", "reference");
    },
    m(a, o) {
      Se(a, e, o), n[20](e), Se(a, t, o), r && r.m(a, o), Se(a, i, o), s || (l = [
        gt(
          window,
          "scroll",
          /*scroll_listener*/
          n[12]
        ),
        gt(
          window,
          "resize",
          /*onwindowresize*/
          n[19]
        )
      ], s = !0);
    },
    p(a, [o]) {
      /*show_options*/
      a[2] && !/*disabled*/
      a[3] ? r ? (r.p(a, o), o & /*show_options, disabled*/
      12 && ft(r, 1)) : (r = Pt(a), r.c(), ft(r, 1), r.m(i.parentNode, i)) : r && (Cs(), Vt(r, 1, 1, () => {
        r = null;
      }), ks());
    },
    i(a) {
      ft(r);
    },
    o(a) {
      Vt(r);
    },
    d(a) {
      a && (Ce(e), Ce(t), Ce(i)), n[20](null), r && r.d(a), s = !1, Es(l);
    }
  };
}
function Hs(n, e, t) {
  var i, s;
  let { choices: l } = e, { filtered_indices: r } = e, { show_options: a = !1 } = e, { disabled: o = !1 } = e, { selected_indices: u = [] } = e, { active_index: f = null } = e, c, w, g, v, _, d, m, y, h;
  function x() {
    const { top: z, bottom: U } = _.getBoundingClientRect();
    t(16, c = z), t(17, w = h - U);
  }
  let p = null;
  function M() {
    a && (p !== null && clearTimeout(p), p = setTimeout(
      () => {
        x(), p = null;
      },
      10
    ));
  }
  const A = Xs();
  function C() {
    t(11, h = window.innerHeight);
  }
  function B(z) {
    Wt[z ? "unshift" : "push"](() => {
      _ = z, t(6, _);
    });
  }
  const D = (z) => A("change", z);
  function G(z) {
    Wt[z ? "unshift" : "push"](() => {
      d = z, t(7, d);
    });
  }
  return n.$$set = (z) => {
    "choices" in z && t(0, l = z.choices), "filtered_indices" in z && t(1, r = z.filtered_indices), "show_options" in z && t(2, a = z.show_options), "disabled" in z && t(3, o = z.disabled), "selected_indices" in z && t(4, u = z.selected_indices), "active_index" in z && t(5, f = z.active_index);
  }, n.$$.update = () => {
    if (n.$$.dirty & /*show_options, refElement, listElement, selected_indices, _a, _b, distance_from_bottom, distance_from_top, input_height*/
    508116) {
      if (a && _) {
        if (d && u.length > 0) {
          let U = d.querySelectorAll("li");
          for (const R of Array.from(U))
            if (R.getAttribute("data-index") === u[0].toString()) {
              t(14, i = d == null ? void 0 : d.scrollTo) === null || i === void 0 || i.call(d, 0, R.offsetTop);
              break;
            }
        }
        x();
        const z = t(15, s = _.parentElement) === null || s === void 0 ? void 0 : s.getBoundingClientRect();
        t(18, g = (z == null ? void 0 : z.height) || 0), t(8, v = (z == null ? void 0 : z.width) || 0);
      }
      w > c ? (t(10, y = w), t(9, m = null)) : (t(9, m = `${w + g}px`), t(10, y = c - g));
    }
  }, [
    l,
    r,
    a,
    o,
    u,
    f,
    _,
    d,
    v,
    m,
    y,
    h,
    M,
    A,
    i,
    s,
    c,
    w,
    g,
    C,
    B,
    D,
    G
  ];
}
class Ds extends vs {
  constructor(e) {
    super(), Ss(this, e, Hs, Ys, As, {
      choices: 0,
      filtered_indices: 1,
      show_options: 2,
      disabled: 3,
      selected_indices: 4,
      active_index: 5
    });
  }
}
function Rs(n, e) {
  return (n % e + e) % e;
}
function Gt(n, e) {
  return n.reduce((t, i, s) => ((!e || i[0].toLowerCase().includes(e.toLowerCase())) && t.push(s), t), []);
}
function Ls(n, e, t) {
  n("change", e), t || n("input");
}
function Ts(n, e, t) {
  if (n.key === "Escape")
    return [!1, e];
  if ((n.key === "ArrowDown" || n.key === "ArrowUp") && t.length >= 0)
    if (e === null)
      e = n.key === "ArrowDown" ? t[0] : t[t.length - 1];
    else {
      const i = t.indexOf(e), s = n.key === "ArrowUp" ? -1 : 1;
      e = t[Rs(i + s, t.length)];
    }
  return [!0, e];
}
const {
  SvelteComponent: qs,
  append: ie,
  attr: q,
  binding_callbacks: Os,
  check_outros: Is,
  create_component: yt,
  destroy_component: vt,
  detach: xt,
  element: ue,
  group_outros: Us,
  init: Ws,
  insert: Ct,
  listen: ge,
  mount_component: kt,
  run_all: js,
  safe_not_equal: Ns,
  set_data: Vs,
  set_input_value: Jt,
  space: ct,
  text: Fs,
  toggle_class: fe,
  transition_in: he,
  transition_out: ye
} = window.__gradio__svelte__internal, { onMount: Ps } = window.__gradio__svelte__internal, { createEventDispatcher: Ks, afterUpdate: Gs } = window.__gradio__svelte__internal;
function Js(n) {
  let e;
  return {
    c() {
      e = Fs(
        /*label*/
        n[0]
      );
    },
    m(t, i) {
      Ct(t, e, i);
    },
    p(t, i) {
      i[0] & /*label*/
      1 && Vs(
        e,
        /*label*/
        t[0]
      );
    },
    d(t) {
      t && xt(e);
    }
  };
}
function Zt(n) {
  let e, t, i;
  return t = new Ui({}), {
    c() {
      e = ue("div"), yt(t.$$.fragment), q(e, "class", "icon-wrap svelte-1m1zvyj");
    },
    m(s, l) {
      Ct(s, e, l), kt(t, e, null), i = !0;
    },
    i(s) {
      i || (he(t.$$.fragment, s), i = !0);
    },
    o(s) {
      ye(t.$$.fragment, s), i = !1;
    },
    d(s) {
      s && xt(e), vt(t);
    }
  };
}
function Zs(n) {
  let e, t, i, s, l, r, a, o, u, f, c, w, g, v;
  t = new ln({
    props: {
      show_label: (
        /*show_label*/
        n[4]
      ),
      info: (
        /*info*/
        n[1]
      ),
      $$slots: { default: [Js] },
      $$scope: { ctx: n }
    }
  });
  let _ = !/*disabled*/
  n[3] && Zt();
  return c = new Ds({
    props: {
      show_options: (
        /*show_options*/
        n[12]
      ),
      choices: (
        /*choices*/
        n[2]
      ),
      filtered_indices: (
        /*filtered_indices*/
        n[10]
      ),
      disabled: (
        /*disabled*/
        n[3]
      ),
      selected_indices: (
        /*selected_index*/
        n[11] === null ? [] : [
          /*selected_index*/
          n[11]
        ]
      ),
      active_index: (
        /*active_index*/
        n[14]
      )
    }
  }), c.$on(
    "change",
    /*handle_option_selected*/
    n[16]
  ), {
    c() {
      e = ue("div"), yt(t.$$.fragment), i = ct(), s = ue("div"), l = ue("div"), r = ue("div"), a = ue("input"), u = ct(), _ && _.c(), f = ct(), yt(c.$$.fragment), q(a, "role", "listbox"), q(a, "aria-controls", "dropdown-options"), q(
        a,
        "aria-expanded",
        /*show_options*/
        n[12]
      ), q(
        a,
        "aria-label",
        /*label*/
        n[0]
      ), q(a, "class", "border-none svelte-1m1zvyj"), a.disabled = /*disabled*/
      n[3], q(a, "autocomplete", "off"), a.readOnly = o = !/*filterable*/
      n[7], fe(a, "subdued", !/*choices_names*/
      n[13].includes(
        /*input_text*/
        n[9]
      ) && !/*allow_custom_value*/
      n[6]), q(r, "class", "secondary-wrap svelte-1m1zvyj"), q(l, "class", "wrap-inner svelte-1m1zvyj"), fe(
        l,
        "show_options",
        /*show_options*/
        n[12]
      ), q(s, "class", "wrap svelte-1m1zvyj"), q(e, "class", "svelte-1m1zvyj"), fe(
        e,
        "container",
        /*container*/
        n[5]
      );
    },
    m(d, m) {
      Ct(d, e, m), kt(t, e, null), ie(e, i), ie(e, s), ie(s, l), ie(l, r), ie(r, a), Jt(
        a,
        /*input_text*/
        n[9]
      ), n[29](a), ie(r, u), _ && _.m(r, null), ie(s, f), kt(c, s, null), w = !0, g || (v = [
        ge(
          a,
          "input",
          /*input_input_handler*/
          n[28]
        ),
        ge(
          a,
          "keydown",
          /*handle_key_down*/
          n[19]
        ),
        ge(
          a,
          "keyup",
          /*keyup_handler*/
          n[30]
        ),
        ge(
          a,
          "blur",
          /*handle_blur*/
          n[18]
        ),
        ge(
          a,
          "focus",
          /*handle_focus*/
          n[17]
        )
      ], g = !0);
    },
    p(d, m) {
      const y = {};
      m[0] & /*show_label*/
      16 && (y.show_label = /*show_label*/
      d[4]), m[0] & /*info*/
      2 && (y.info = /*info*/
      d[1]), m[0] & /*label*/
      1 | m[1] & /*$$scope*/
      4 && (y.$$scope = { dirty: m, ctx: d }), t.$set(y), (!w || m[0] & /*show_options*/
      4096) && q(
        a,
        "aria-expanded",
        /*show_options*/
        d[12]
      ), (!w || m[0] & /*label*/
      1) && q(
        a,
        "aria-label",
        /*label*/
        d[0]
      ), (!w || m[0] & /*disabled*/
      8) && (a.disabled = /*disabled*/
      d[3]), (!w || m[0] & /*filterable*/
      128 && o !== (o = !/*filterable*/
      d[7])) && (a.readOnly = o), m[0] & /*input_text*/
      512 && a.value !== /*input_text*/
      d[9] && Jt(
        a,
        /*input_text*/
        d[9]
      ), (!w || m[0] & /*choices_names, input_text, allow_custom_value*/
      8768) && fe(a, "subdued", !/*choices_names*/
      d[13].includes(
        /*input_text*/
        d[9]
      ) && !/*allow_custom_value*/
      d[6]), /*disabled*/
      d[3] ? _ && (Us(), ye(_, 1, 1, () => {
        _ = null;
      }), Is()) : _ ? m[0] & /*disabled*/
      8 && he(_, 1) : (_ = Zt(), _.c(), he(_, 1), _.m(r, null)), (!w || m[0] & /*show_options*/
      4096) && fe(
        l,
        "show_options",
        /*show_options*/
        d[12]
      );
      const h = {};
      m[0] & /*show_options*/
      4096 && (h.show_options = /*show_options*/
      d[12]), m[0] & /*choices*/
      4 && (h.choices = /*choices*/
      d[2]), m[0] & /*filtered_indices*/
      1024 && (h.filtered_indices = /*filtered_indices*/
      d[10]), m[0] & /*disabled*/
      8 && (h.disabled = /*disabled*/
      d[3]), m[0] & /*selected_index*/
      2048 && (h.selected_indices = /*selected_index*/
      d[11] === null ? [] : [
        /*selected_index*/
        d[11]
      ]), m[0] & /*active_index*/
      16384 && (h.active_index = /*active_index*/
      d[14]), c.$set(h), (!w || m[0] & /*container*/
      32) && fe(
        e,
        "container",
        /*container*/
        d[5]
      );
    },
    i(d) {
      w || (he(t.$$.fragment, d), he(_), he(c.$$.fragment, d), w = !0);
    },
    o(d) {
      ye(t.$$.fragment, d), ye(_), ye(c.$$.fragment, d), w = !1;
    },
    d(d) {
      d && xt(e), vt(t), n[29](null), _ && _.d(), vt(c), g = !1, js(v);
    }
  };
}
function Qs(n, e, t) {
  let { label: i } = e, { info: s = void 0 } = e, { value: l = [] } = e, r = [], { value_is_output: a = !1 } = e, { choices: o } = e, u, { disabled: f = !1 } = e, { show_label: c } = e, { container: w = !0 } = e, { allow_custom_value: g = !1 } = e, { filterable: v = !0 } = e, _, d = !1, m, y, h = "", x = "", p = !1, M = [], A = null, C = null, B;
  const D = Ks();
  l ? (B = o.map((S) => S[1]).indexOf(l), C = B, C === -1 ? (r = l, C = null) : ([h, r] = o[C], x = h), z()) : o.length > 0 && (B = 0, C = 0, [h, l] = o[C], r = l, x = h);
  function G() {
    t(13, m = o.map((S) => S[0])), t(24, y = o.map((S) => S[1]));
  }
  function z() {
    G(), l === void 0 || Array.isArray(l) && l.length === 0 ? (t(9, h = ""), t(11, C = null)) : y.includes(l) ? (t(9, h = m[y.indexOf(l)]), t(11, C = y.indexOf(l))) : g ? (t(9, h = l), t(11, C = null)) : (t(9, h = ""), t(11, C = null)), t(27, B = C);
  }
  function U(S) {
    if (t(11, C = parseInt(S.detail.target.dataset.index)), isNaN(C)) {
      t(11, C = null);
      return;
    }
    t(12, d = !1), t(14, A = null), _.blur();
  }
  function R(S) {
    t(10, M = o.map((it, Ye) => Ye)), t(12, d = !0), D("focus");
  }
  function ne() {
    g ? t(20, l = h) : t(9, h = m[y.indexOf(l)]), t(12, d = !1), t(14, A = null), D("blur");
  }
  function et(S) {
    t(12, [d, A] = Ts(S, A, M), d, (t(14, A), t(2, o), t(23, u), t(6, g), t(9, h), t(10, M), t(8, _), t(25, x), t(11, C), t(27, B), t(26, p), t(24, y))), S.key === "Enter" && (A !== null ? (t(11, C = A), t(12, d = !1), _.blur(), t(14, A = null)) : m.includes(h) ? (t(11, C = m.indexOf(h)), t(12, d = !1), t(14, A = null), _.blur()) : g && (t(20, l = h), t(11, C = null), t(12, d = !1), t(14, A = null), _.blur()), D("enter", l));
  }
  Gs(() => {
    t(21, a = !1), t(26, p = !0);
  }), Ps(() => {
    _.focus();
  });
  function tt() {
    h = this.value, t(9, h), t(11, C), t(27, B), t(26, p), t(2, o), t(24, y);
  }
  function nt(S) {
    Os[S ? "unshift" : "push"](() => {
      _ = S, t(8, _);
    });
  }
  const be = (S) => D("key_up", { key: S.key, input_value: h });
  return n.$$set = (S) => {
    "label" in S && t(0, i = S.label), "info" in S && t(1, s = S.info), "value" in S && t(20, l = S.value), "value_is_output" in S && t(21, a = S.value_is_output), "choices" in S && t(2, o = S.choices), "disabled" in S && t(3, f = S.disabled), "show_label" in S && t(4, c = S.show_label), "container" in S && t(5, w = S.container), "allow_custom_value" in S && t(6, g = S.allow_custom_value), "filterable" in S && t(7, v = S.filterable);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*selected_index, old_selected_index, initialized, choices, choices_values*/
    218105860 && C !== B && C !== null && p && (t(9, [h, l] = o[C], h, (t(20, l), t(11, C), t(27, B), t(26, p), t(2, o), t(24, y))), t(27, B = C), D("select", {
      index: C,
      value: y[C],
      selected: !0
    })), n.$$.dirty[0] & /*value, old_value, value_is_output*/
    7340032 && l != r && (z(), Ls(D, l, a), t(22, r = l)), n.$$.dirty[0] & /*choices*/
    4 && G(), n.$$.dirty[0] & /*choices, old_choices, allow_custom_value, input_text, filtered_indices, filter_input*/
    8390468 && o !== u && (g || z(), t(23, u = o), t(10, M = Gt(o, h)), !g && M.length > 0 && t(14, A = M[0]), _ == document.activeElement && t(12, d = !0)), n.$$.dirty[0] & /*input_text, old_input_text, choices, allow_custom_value, filtered_indices*/
    33556036 && h !== x && (t(10, M = Gt(o, h)), t(25, x = h), !g && M.length > 0 && t(14, A = M[0]));
  }, [
    i,
    s,
    o,
    f,
    c,
    w,
    g,
    v,
    _,
    h,
    M,
    C,
    d,
    m,
    A,
    D,
    U,
    R,
    ne,
    et,
    l,
    a,
    r,
    u,
    y,
    x,
    p,
    B,
    tt,
    nt,
    be
  ];
}
class $s extends qs {
  constructor(e) {
    super(), Ws(
      this,
      e,
      Qs,
      Zs,
      Ns,
      {
        label: 0,
        info: 1,
        value: 20,
        value_is_output: 21,
        choices: 2,
        disabled: 3,
        show_label: 4,
        container: 5,
        allow_custom_value: 6,
        filterable: 7
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: el,
  append: F,
  attr: Te,
  check_outros: tl,
  create_component: ve,
  destroy_component: ke,
  detach: Be,
  element: $,
  group_outros: nl,
  init: il,
  insert: Xe,
  mount_component: pe,
  safe_not_equal: sl,
  set_style: xe,
  space: qe,
  text: St,
  transition_in: ee,
  transition_out: se
} = window.__gradio__svelte__internal, { createEventDispatcher: ll } = window.__gradio__svelte__internal, { onMount: ol, onDestroy: al } = window.__gradio__svelte__internal;
function rl(n) {
  let e;
  return {
    c() {
      e = St("Cancel");
    },
    m(t, i) {
      Xe(t, e, i);
    },
    d(t) {
      t && Be(e);
    }
  };
}
function Qt(n) {
  let e, t, i;
  return t = new bt({
    props: {
      variant: "stop",
      $$slots: { default: [fl] },
      $$scope: { ctx: n }
    }
  }), t.$on(
    "click",
    /*click_handler_1*/
    n[12]
  ), {
    c() {
      e = $("div"), ve(t.$$.fragment), xe(e, "margin-right", "8px");
    },
    m(s, l) {
      Xe(s, e, l), pe(t, e, null), i = !0;
    },
    p(s, l) {
      const r = {};
      l & /*$$scope*/
      65536 && (r.$$scope = { dirty: l, ctx: s }), t.$set(r);
    },
    i(s) {
      i || (ee(t.$$.fragment, s), i = !0);
    },
    o(s) {
      se(t.$$.fragment, s), i = !1;
    },
    d(s) {
      s && Be(e), ke(t);
    }
  };
}
function fl(n) {
  let e;
  return {
    c() {
      e = St("Remove");
    },
    m(t, i) {
      Xe(t, e, i);
    },
    d(t) {
      t && Be(e);
    }
  };
}
function cl(n) {
  let e;
  return {
    c() {
      e = St("OK");
    },
    m(t, i) {
      Xe(t, e, i);
    },
    d(t) {
      t && Be(e);
    }
  };
}
function ul(n) {
  let e, t, i, s, l, r, a, o, u, f, c, w, g, v, _, d;
  l = new $s({
    props: {
      value: (
        /*currentLabel*/
        n[0]
      ),
      label: "Label",
      choices: (
        /*choices*/
        n[2]
      ),
      show_label: !1,
      allow_custom_value: !0
    }
  }), l.$on(
    "change",
    /*onDropDownChange*/
    n[5]
  ), l.$on(
    "enter",
    /*onDropDownEnter*/
    n[7]
  ), o = new os({
    props: {
      value: (
        /*currentColor*/
        n[1]
      ),
      label: "Color",
      show_label: !1
    }
  }), o.$on(
    "change",
    /*onColorChange*/
    n[6]
  ), c = new bt({
    props: {
      $$slots: { default: [rl] },
      $$scope: { ctx: n }
    }
  }), c.$on(
    "click",
    /*click_handler*/
    n[11]
  );
  let m = (
    /*showRemove*/
    n[3] && Qt(n)
  );
  return _ = new bt({
    props: {
      variant: "primary",
      $$slots: { default: [cl] },
      $$scope: { ctx: n }
    }
  }), _.$on(
    "click",
    /*click_handler_2*/
    n[13]
  ), {
    c() {
      e = $("div"), t = $("div"), i = $("span"), s = $("div"), ve(l.$$.fragment), r = qe(), a = $("div"), ve(o.$$.fragment), u = qe(), f = $("div"), ve(c.$$.fragment), w = qe(), m && m.c(), g = qe(), v = $("div"), ve(_.$$.fragment), xe(s, "margin-right", "10px"), xe(a, "margin-right", "40px"), xe(a, "margin-bottom", "8px"), xe(f, "margin-right", "8px"), Te(i, "class", "model-content svelte-hkn2q1"), Te(t, "class", "modal-container svelte-hkn2q1"), Te(e, "class", "modal svelte-hkn2q1"), Te(e, "id", "model-box-edit");
    },
    m(y, h) {
      Xe(y, e, h), F(e, t), F(t, i), F(i, s), pe(l, s, null), F(i, r), F(i, a), pe(o, a, null), F(i, u), F(i, f), pe(c, f, null), F(i, w), m && m.m(i, null), F(i, g), F(i, v), pe(_, v, null), d = !0;
    },
    p(y, [h]) {
      const x = {};
      h & /*currentLabel*/
      1 && (x.value = /*currentLabel*/
      y[0]), h & /*choices*/
      4 && (x.choices = /*choices*/
      y[2]), l.$set(x);
      const p = {};
      h & /*currentColor*/
      2 && (p.value = /*currentColor*/
      y[1]), o.$set(p);
      const M = {};
      h & /*$$scope*/
      65536 && (M.$$scope = { dirty: h, ctx: y }), c.$set(M), /*showRemove*/
      y[3] ? m ? (m.p(y, h), h & /*showRemove*/
      8 && ee(m, 1)) : (m = Qt(y), m.c(), ee(m, 1), m.m(i, g)) : m && (nl(), se(m, 1, 1, () => {
        m = null;
      }), tl());
      const A = {};
      h & /*$$scope*/
      65536 && (A.$$scope = { dirty: h, ctx: y }), _.$set(A);
    },
    i(y) {
      d || (ee(l.$$.fragment, y), ee(o.$$.fragment, y), ee(c.$$.fragment, y), ee(m), ee(_.$$.fragment, y), d = !0);
    },
    o(y) {
      se(l.$$.fragment, y), se(o.$$.fragment, y), se(c.$$.fragment, y), se(m), se(_.$$.fragment, y), d = !1;
    },
    d(y) {
      y && Be(e), ke(l), ke(o), ke(c), m && m.d(), ke(_);
    }
  };
}
function hl(n, e, t) {
  let { label: i = "" } = e, { currentLabel: s = "" } = e, { choices: l = [] } = e, { choicesColors: r = [] } = e, { color: a = "" } = e, { currentColor: o = "" } = e, { showRemove: u = !0 } = e;
  const f = ll();
  function c(h) {
    f("change", {
      label: s,
      color: o,
      ret: h
      // -1: remove, 0: cancel, 1: change
    });
  }
  function w(h) {
    const { detail: x } = h;
    let p = x;
    Number.isInteger(p) ? (Array.isArray(r) && p < r.length && t(1, o = r[p]), Array.isArray(l) && p < l.length && t(0, s = l[p][0])) : t(0, s = p);
  }
  function g(h) {
    const { detail: x } = h;
    t(1, o = x);
  }
  function v(h) {
    w(h), c(1);
  }
  function _(h) {
    switch (h.key) {
      case "Enter":
        c(1);
        break;
    }
  }
  ol(() => {
    document.addEventListener("keydown", _), t(0, s = i), t(1, o = a);
  }), al(() => {
    document.removeEventListener("keydown", _);
  });
  const d = () => c(0), m = () => c(-1), y = () => c(1);
  return n.$$set = (h) => {
    "label" in h && t(8, i = h.label), "currentLabel" in h && t(0, s = h.currentLabel), "choices" in h && t(2, l = h.choices), "choicesColors" in h && t(9, r = h.choicesColors), "color" in h && t(10, a = h.color), "currentColor" in h && t(1, o = h.currentColor), "showRemove" in h && t(3, u = h.showRemove);
  }, [
    s,
    o,
    l,
    u,
    c,
    w,
    g,
    v,
    i,
    r,
    a,
    d,
    m,
    y
  ];
}
class dn extends el {
  constructor(e) {
    super(), il(this, e, hl, ul, sl, {
      label: 8,
      currentLabel: 0,
      choices: 2,
      choicesColors: 9,
      color: 10,
      currentColor: 1,
      showRemove: 3
    });
  }
}
const H = (n, e, t) => Math.min(Math.max(n, e), t);
function ut(n, e) {
  if (n.startsWith("rgba"))
    return n.replace(/[\d.]+$/, e.toString());
  const t = n.match(/\d+/g);
  if (!t || t.length !== 3)
    return `rgba(50, 50, 50, ${e})`;
  const [i, s, l] = t;
  return `rgba(${i}, ${s}, ${l}, ${e})`;
}
class ht {
  constructor(e, t, i, s, l, r, a, o, u, f, c, w = "rgb(255, 255, 255)", g = 0.5, v = 25, _ = 8, d = 2, m = 4, y = 1) {
    this.stopDrag = () => {
      this.isDragging = !1, document.removeEventListener("mousemove", this.handleDrag), document.removeEventListener("mouseup", this.stopDrag);
    }, this.handleDrag = (h) => {
      if (this.isDragging) {
        let x = h.clientX - this.offsetMouseX - this.xmin, p = h.clientY - this.offsetMouseY - this.ymin;
        const M = this.canvasXmax - this.canvasXmin, A = this.canvasYmax - this.canvasYmin;
        x = H(x, -this.xmin, M - this.xmax), p = H(p, -this.ymin, A - this.ymax), this.xmin += x, this.ymin += p, this.xmax += x, this.ymax += p, this.updateHandles(), this.renderCallBack();
      }
    }, this.handleCreating = (h) => {
      if (this.isCreating) {
        let [x, p] = this.toBoxCoordinates(h.clientX, h.clientY);
        x -= this.offsetMouseX, p -= this.offsetMouseY, x > this.xmax ? (this.creatingAnchorX == "xmax" && (this.xmin = this.xmax), this.xmax = x, this.creatingAnchorX = "xmin") : x > this.xmin && x < this.xmax && this.creatingAnchorX == "xmin" ? this.xmax = x : x > this.xmin && x < this.xmax && this.creatingAnchorX == "xmax" ? this.xmin = x : x < this.xmin && (this.creatingAnchorX == "xmin" && (this.xmax = this.xmin), this.xmin = x, this.creatingAnchorX = "xmax"), p > this.ymax ? (this.creatingAnchorY == "ymax" && (this.ymin = this.ymax), this.ymax = p, this.creatingAnchorY = "ymin") : p > this.ymin && p < this.ymax && this.creatingAnchorY == "ymin" ? this.ymax = p : p > this.ymin && p < this.ymax && this.creatingAnchorY == "ymax" ? this.ymin = p : p < this.ymin && (this.creatingAnchorY == "ymin" && (this.ymax = this.ymin), this.ymin = p, this.creatingAnchorY = "ymax"), this.updateHandles(), this.renderCallBack();
      }
    }, this.stopCreating = (h) => {
      if (this.isCreating = !1, document.removeEventListener("mousemove", this.handleCreating), document.removeEventListener("mouseup", this.stopCreating), this.getArea() > 0) {
        const x = this.canvasXmax - this.canvasXmin, p = this.canvasYmax - this.canvasYmin;
        this.xmin = H(this.xmin, 0, x - this.minSize), this.ymin = H(this.ymin, 0, p - this.minSize), this.xmax = H(this.xmax, this.minSize, x), this.ymax = H(this.ymax, this.minSize, p), this.minSize > 0 && (this.getWidth() < this.minSize && (this.creatingAnchorX == "xmin" ? this.xmax = this.xmin + this.minSize : this.xmin = this.xmax - this.minSize), this.getHeight() < this.minSize && (this.creatingAnchorY == "ymin" ? this.ymax = this.ymin + this.minSize : this.ymin = this.ymax - this.minSize), this.xmax > x ? (this.xmin -= this.xmax - x, this.xmax = x) : this.xmin < 0 && (this.xmax -= this.xmin, this.xmin = 0), this.ymax > p ? (this.ymin -= this.ymax - p, this.ymax = p) : this.ymin < 0 && (this.ymax -= this.ymin, this.ymin = 0)), this.updateHandles(), this.renderCallBack();
      }
      this.onFinishCreation();
    }, this.handleResize = (h) => {
      if (this.isResizing) {
        const x = h.clientX, p = h.clientY, M = x - this.resizeHandles[this.resizingHandleIndex].xmin - this.offsetMouseX, A = p - this.resizeHandles[this.resizingHandleIndex].ymin - this.offsetMouseY, C = this.canvasXmax - this.canvasXmin, B = this.canvasYmax - this.canvasYmin;
        switch (this.resizingHandleIndex) {
          case 0:
            this.xmin += M, this.ymin += A, this.xmin = H(this.xmin, 0, this.xmax - this.minSize), this.ymin = H(this.ymin, 0, this.ymax - this.minSize);
            break;
          case 1:
            this.xmax += M, this.ymin += A, this.xmax = H(this.xmax, this.xmin + this.minSize, C), this.ymin = H(this.ymin, 0, this.ymax - this.minSize);
            break;
          case 2:
            this.xmax += M, this.ymax += A, this.xmax = H(this.xmax, this.xmin + this.minSize, C), this.ymax = H(this.ymax, this.ymin + this.minSize, B);
            break;
          case 3:
            this.xmin += M, this.ymax += A, this.xmin = H(this.xmin, 0, this.xmax - this.minSize), this.ymax = H(this.ymax, this.ymin + this.minSize, B);
            break;
          case 4:
            this.ymin += A, this.ymin = H(this.ymin, 0, this.ymax - this.minSize);
            break;
          case 5:
            this.xmax += M, this.xmax = H(this.xmax, this.xmin + this.minSize, C);
            break;
          case 6:
            this.ymax += A, this.ymax = H(this.ymax, this.ymin + this.minSize, B);
            break;
          case 7:
            this.xmin += M, this.xmin = H(this.xmin, 0, this.xmax - this.minSize);
            break;
        }
        this.updateHandles(), this.renderCallBack();
      }
    }, this.stopResize = () => {
      this.isResizing = !1, document.removeEventListener("mousemove", this.handleResize), document.removeEventListener("mouseup", this.stopResize);
    }, this.renderCallBack = e, this.onFinishCreation = t, this.canvasXmin = i, this.canvasYmin = s, this.canvasXmax = l, this.canvasYmax = r, this.scaleFactor = y, this.label = a, this.isDragging = !1, this.isCreating = !1, this.xmin = o, this.ymin = u, this.xmax = f, this.ymax = c, this.isResizing = !1, this.isSelected = !1, this.offsetMouseX = 0, this.offsetMouseY = 0, this.resizeHandleSize = _, this.thickness = d, this.selectedThickness = m, this.updateHandles(), this.resizingHandleIndex = -1, this.minSize = v, this.color = w, this.alpha = g, this.creatingAnchorX = "xmin", this.creatingAnchorY = "ymin";
  }
  toJSON() {
    return {
      label: this.label,
      xmin: this.xmin,
      ymin: this.ymin,
      xmax: this.xmax,
      ymax: this.ymax,
      color: this.color,
      scaleFactor: this.scaleFactor
    };
  }
  setSelected(e) {
    this.isSelected = e;
  }
  setScaleFactor(e) {
    let t = e / this.scaleFactor;
    this.xmin = Math.round(this.xmin * t), this.ymin = Math.round(this.ymin * t), this.xmax = Math.round(this.xmax * t), this.ymax = Math.round(this.ymax * t), this.updateHandles(), this.scaleFactor = e;
  }
  updateHandles() {
    const e = this.resizeHandleSize / 2, t = this.getWidth(), i = this.getHeight();
    this.resizeHandles = [
      {
        // Top left
        xmin: this.xmin - e,
        ymin: this.ymin - e,
        xmax: this.xmin + e,
        ymax: this.ymin + e
      },
      {
        // Top right
        xmin: this.xmax - e,
        ymin: this.ymin - e,
        xmax: this.xmax + e,
        ymax: this.ymin + e
      },
      {
        // Bottom right
        xmin: this.xmax - e,
        ymin: this.ymax - e,
        xmax: this.xmax + e,
        ymax: this.ymax + e
      },
      {
        // Bottom left
        xmin: this.xmin - e,
        ymin: this.ymax - e,
        xmax: this.xmin + e,
        ymax: this.ymax + e
      },
      {
        // Top center
        xmin: this.xmin + t / 2 - e,
        ymin: this.ymin - e,
        xmax: this.xmin + t / 2 + e,
        ymax: this.ymin + e
      },
      {
        // Right center
        xmin: this.xmax - e,
        ymin: this.ymin + i / 2 - e,
        xmax: this.xmax + e,
        ymax: this.ymin + i / 2 + e
      },
      {
        // Bottom center
        xmin: this.xmin + t / 2 - e,
        ymin: this.ymax - e,
        xmax: this.xmin + t / 2 + e,
        ymax: this.ymax + e
      },
      {
        // Left center
        xmin: this.xmin - e,
        ymin: this.ymin + i / 2 - e,
        xmax: this.xmin + e,
        ymax: this.ymin + i / 2 + e
      }
    ];
  }
  getWidth() {
    return this.xmax - this.xmin;
  }
  getHeight() {
    return this.ymax - this.ymin;
  }
  getArea() {
    return this.getWidth() * this.getHeight();
  }
  toCanvasCoordinates(e, t) {
    return e = e + this.canvasXmin, t = t + this.canvasYmin, [e, t];
  }
  toBoxCoordinates(e, t) {
    return e = e - this.canvasXmin, t = t - this.canvasYmin, [e, t];
  }
  render(e) {
    let t, i;
    if (e.beginPath(), [t, i] = this.toCanvasCoordinates(this.xmin, this.ymin), e.rect(t, i, this.getWidth(), this.getHeight()), e.fillStyle = ut(this.color, this.alpha), e.fill(), this.isSelected ? e.lineWidth = this.selectedThickness : e.lineWidth = this.thickness, e.strokeStyle = ut(this.color, 1), e.stroke(), e.closePath(), this.label !== null && this.label.trim() !== "") {
      this.isSelected ? e.font = "bold 14px Arial" : e.font = "12px Arial";
      const s = e.measureText(this.label).width + 10, l = 20;
      let r = this.xmin, a = this.ymin - l;
      e.fillStyle = "white", [r, a] = this.toCanvasCoordinates(r, a), e.fillRect(r, a, s, l), e.lineWidth = 1, e.strokeStyle = "black", e.strokeRect(r, a, s, l), e.fillStyle = "black", e.fillText(this.label, r + 5, a + 15);
    }
    e.fillStyle = ut(this.color, 1);
    for (const s of this.resizeHandles)
      [t, i] = this.toCanvasCoordinates(s.xmin, s.ymin), e.fillRect(
        t,
        i,
        s.xmax - s.xmin,
        s.ymax - s.ymin
      );
  }
  startDrag(e) {
    this.isDragging = !0, this.offsetMouseX = e.clientX - this.xmin, this.offsetMouseY = e.clientY - this.ymin, document.addEventListener("mousemove", this.handleDrag), document.addEventListener("mouseup", this.stopDrag);
  }
  isPointInsideBox(e, t) {
    return [e, t] = this.toBoxCoordinates(e, t), e >= this.xmin && e <= this.xmax && t >= this.ymin && t <= this.ymax;
  }
  indexOfPointInsideHandle(e, t) {
    [e, t] = this.toBoxCoordinates(e, t);
    for (let i = 0; i < this.resizeHandles.length; i++) {
      const s = this.resizeHandles[i];
      if (e >= s.xmin && e <= s.xmax && t >= s.ymin && t <= s.ymax)
        return this.resizingHandleIndex = i, i;
    }
    return -1;
  }
  startCreating(e, t, i) {
    this.isCreating = !0, this.offsetMouseX = t, this.offsetMouseY = i, document.addEventListener("mousemove", this.handleCreating), document.addEventListener("mouseup", this.stopCreating);
  }
  startResize(e, t) {
    this.resizingHandleIndex = e, this.isResizing = !0, this.offsetMouseX = t.clientX - this.resizeHandles[e].xmin, this.offsetMouseY = t.clientY - this.resizeHandles[e].ymin, document.addEventListener("mousemove", this.handleResize), document.addEventListener("mouseup", this.stopResize);
  }
}
const ce = [
  "rgb(255, 168, 77)",
  "rgb(92, 172, 238)",
  "rgb(255, 99, 71)",
  "rgb(118, 238, 118)",
  "rgb(255, 145, 164)",
  "rgb(0, 191, 255)",
  "rgb(255, 218, 185)",
  "rgb(255, 69, 0)",
  "rgb(34, 139, 34)",
  "rgb(255, 240, 245)",
  "rgb(255, 193, 37)",
  "rgb(255, 193, 7)",
  "rgb(255, 250, 138)"
], {
  SvelteComponent: ml,
  append: je,
  attr: te,
  binding_callbacks: _l,
  bubble: $t,
  check_outros: mt,
  create_component: Je,
  destroy_component: Ze,
  detach: me,
  element: ze,
  empty: dl,
  group_outros: _t,
  init: bl,
  insert: _e,
  listen: le,
  mount_component: Qe,
  run_all: bn,
  safe_not_equal: gl,
  space: Ne,
  toggle_class: Oe,
  transition_in: I,
  transition_out: P
} = window.__gradio__svelte__internal, { onMount: wl, onDestroy: yl, createEventDispatcher: vl } = window.__gradio__svelte__internal;
function en(n) {
  let e, t, i, s, l, r, a, o, u;
  return i = new jn({}), r = new Zn({}), {
    c() {
      e = ze("span"), t = ze("button"), Je(i.$$.fragment), s = Ne(), l = ze("button"), Je(r.$$.fragment), te(t, "class", "icon svelte-10jprmi"), te(t, "aria-label", "Create box"), Oe(
        t,
        "selected",
        /*mode*/
        n[7] === /*Mode*/
        n[4].creation
      ), te(l, "class", "icon svelte-10jprmi"), te(l, "aria-label", "Edit boxes"), Oe(
        l,
        "selected",
        /*mode*/
        n[7] === /*Mode*/
        n[4].drag
      ), te(e, "class", "canvas-control svelte-10jprmi");
    },
    m(f, c) {
      _e(f, e, c), je(e, t), Qe(i, t, null), je(e, s), je(e, l), Qe(r, l, null), a = !0, o || (u = [
        le(
          t,
          "click",
          /*click_handler*/
          n[27]
        ),
        le(
          l,
          "click",
          /*click_handler_1*/
          n[28]
        )
      ], o = !0);
    },
    p(f, c) {
      (!a || c[0] & /*mode, Mode*/
      144) && Oe(
        t,
        "selected",
        /*mode*/
        f[7] === /*Mode*/
        f[4].creation
      ), (!a || c[0] & /*mode, Mode*/
      144) && Oe(
        l,
        "selected",
        /*mode*/
        f[7] === /*Mode*/
        f[4].drag
      );
    },
    i(f) {
      a || (I(i.$$.fragment, f), I(r.$$.fragment, f), a = !0);
    },
    o(f) {
      P(i.$$.fragment, f), P(r.$$.fragment, f), a = !1;
    },
    d(f) {
      f && me(e), Ze(i), Ze(r), o = !1, bn(u);
    }
  };
}
function tn(n) {
  let e, t;
  return e = new dn({
    props: {
      choices: (
        /*choices*/
        n[2]
      ),
      choicesColors: (
        /*choicesColors*/
        n[3]
      ),
      label: (
        /*selectedBox*/
        n[6] >= 0 && /*selectedBox*/
        n[6] < /*value*/
        n[0].boxes.length ? (
          /*value*/
          n[0].boxes[
            /*selectedBox*/
            n[6]
          ].label
        ) : ""
      ),
      color: (
        /*selectedBox*/
        n[6] >= 0 && /*selectedBox*/
        n[6] < /*value*/
        n[0].boxes.length ? Ee(
          /*value*/
          n[0].boxes[
            /*selectedBox*/
            n[6]
          ].color
        ) : ""
      )
    }
  }), e.$on(
    "change",
    /*onModalEditChange*/
    n[15]
  ), e.$on(
    "enter{onModalEditChange}",
    /*enter_onModalEditChange_handler*/
    n[29]
  ), {
    c() {
      Je(e.$$.fragment);
    },
    m(i, s) {
      Qe(e, i, s), t = !0;
    },
    p(i, s) {
      const l = {};
      s[0] & /*choices*/
      4 && (l.choices = /*choices*/
      i[2]), s[0] & /*choicesColors*/
      8 && (l.choicesColors = /*choicesColors*/
      i[3]), s[0] & /*selectedBox, value*/
      65 && (l.label = /*selectedBox*/
      i[6] >= 0 && /*selectedBox*/
      i[6] < /*value*/
      i[0].boxes.length ? (
        /*value*/
        i[0].boxes[
          /*selectedBox*/
          i[6]
        ].label
      ) : ""), s[0] & /*selectedBox, value*/
      65 && (l.color = /*selectedBox*/
      i[6] >= 0 && /*selectedBox*/
      i[6] < /*value*/
      i[0].boxes.length ? Ee(
        /*value*/
        i[0].boxes[
          /*selectedBox*/
          i[6]
        ].color
      ) : ""), e.$set(l);
    },
    i(i) {
      t || (I(e.$$.fragment, i), t = !0);
    },
    o(i) {
      P(e.$$.fragment, i), t = !1;
    },
    d(i) {
      Ze(e, i);
    }
  };
}
function nn(n) {
  let e, t;
  return e = new dn({
    props: {
      choices: (
        /*choices*/
        n[2]
      ),
      showRemove: !1,
      choicesColors: (
        /*choicesColors*/
        n[3]
      ),
      label: (
        /*selectedBox*/
        n[6] >= 0 && /*selectedBox*/
        n[6] < /*value*/
        n[0].boxes.length ? (
          /*value*/
          n[0].boxes[
            /*selectedBox*/
            n[6]
          ].label
        ) : ""
      ),
      color: (
        /*selectedBox*/
        n[6] >= 0 && /*selectedBox*/
        n[6] < /*value*/
        n[0].boxes.length ? Ee(
          /*value*/
          n[0].boxes[
            /*selectedBox*/
            n[6]
          ].color
        ) : ""
      )
    }
  }), e.$on(
    "change",
    /*onModalNewChange*/
    n[16]
  ), e.$on(
    "enter{onModalNewChange}",
    /*enter_onModalNewChange_handler*/
    n[30]
  ), {
    c() {
      Je(e.$$.fragment);
    },
    m(i, s) {
      Qe(e, i, s), t = !0;
    },
    p(i, s) {
      const l = {};
      s[0] & /*choices*/
      4 && (l.choices = /*choices*/
      i[2]), s[0] & /*choicesColors*/
      8 && (l.choicesColors = /*choicesColors*/
      i[3]), s[0] & /*selectedBox, value*/
      65 && (l.label = /*selectedBox*/
      i[6] >= 0 && /*selectedBox*/
      i[6] < /*value*/
      i[0].boxes.length ? (
        /*value*/
        i[0].boxes[
          /*selectedBox*/
          i[6]
        ].label
      ) : ""), s[0] & /*selectedBox, value*/
      65 && (l.color = /*selectedBox*/
      i[6] >= 0 && /*selectedBox*/
      i[6] < /*value*/
      i[0].boxes.length ? Ee(
        /*value*/
        i[0].boxes[
          /*selectedBox*/
          i[6]
        ].color
      ) : ""), e.$set(l);
    },
    i(i) {
      t || (I(e.$$.fragment, i), t = !0);
    },
    o(i) {
      P(e.$$.fragment, i), t = !1;
    },
    d(i) {
      Ze(e, i);
    }
  };
}
function kl(n) {
  let e, t, i, s, l, r, a, o, u, f = (
    /*interactive*/
    n[1] && en(n)
  ), c = (
    /*editModalVisible*/
    n[8] && tn(n)
  ), w = (
    /*newModalVisible*/
    n[9] && nn(n)
  );
  return {
    c() {
      e = ze("div"), t = ze("canvas"), i = Ne(), f && f.c(), s = Ne(), c && c.c(), l = Ne(), w && w.c(), r = dl(), te(t, "class", "canvas-annotator svelte-10jprmi"), te(e, "class", "canvas-container svelte-10jprmi"), te(e, "tabindex", "-1");
    },
    m(g, v) {
      _e(g, e, v), je(e, t), n[26](t), _e(g, i, v), f && f.m(g, v), _e(g, s, v), c && c.m(g, v), _e(g, l, v), w && w.m(g, v), _e(g, r, v), a = !0, o || (u = [
        le(
          t,
          "mousedown",
          /*handleMouseDown*/
          n[10]
        ),
        le(
          t,
          "mouseup",
          /*handleMouseUp*/
          n[11]
        ),
        le(
          t,
          "dblclick",
          /*handleDoubleClick*/
          n[14]
        ),
        le(
          e,
          "focusin",
          /*handleCanvasFocus*/
          n[17]
        ),
        le(
          e,
          "focusout",
          /*handleCanvasBlur*/
          n[18]
        )
      ], o = !0);
    },
    p(g, v) {
      /*interactive*/
      g[1] ? f ? (f.p(g, v), v[0] & /*interactive*/
      2 && I(f, 1)) : (f = en(g), f.c(), I(f, 1), f.m(s.parentNode, s)) : f && (_t(), P(f, 1, 1, () => {
        f = null;
      }), mt()), /*editModalVisible*/
      g[8] ? c ? (c.p(g, v), v[0] & /*editModalVisible*/
      256 && I(c, 1)) : (c = tn(g), c.c(), I(c, 1), c.m(l.parentNode, l)) : c && (_t(), P(c, 1, 1, () => {
        c = null;
      }), mt()), /*newModalVisible*/
      g[9] ? w ? (w.p(g, v), v[0] & /*newModalVisible*/
      512 && I(w, 1)) : (w = nn(g), w.c(), I(w, 1), w.m(r.parentNode, r)) : w && (_t(), P(w, 1, 1, () => {
        w = null;
      }), mt());
    },
    i(g) {
      a || (I(f), I(c), I(w), a = !0);
    },
    o(g) {
      P(f), P(c), P(w), a = !1;
    },
    d(g) {
      g && (me(e), me(i), me(s), me(l), me(r)), n[26](null), f && f.d(g), c && c.d(g), w && w.d(g), o = !1, bn(u);
    }
  };
}
function dt(n) {
  var e = parseInt(n.slice(1, 3), 16), t = parseInt(n.slice(3, 5), 16), i = parseInt(n.slice(5, 7), 16);
  return "rgb(" + e + ", " + t + ", " + i + ")";
}
function Ee(n) {
  const e = n.match(/(\d+(\.\d+)?)/g), t = parseInt(e[0]), i = parseInt(e[1]), s = parseInt(e[2]);
  return "#" + (1 << 24 | t << 16 | i << 8 | s).toString(16).slice(1);
}
function pl(n, e, t) {
  var i;
  (function(b) {
    b[b.creation = 0] = "creation", b[b.drag = 1] = "drag";
  })(i || (i = {}));
  let { imageUrl: s = null } = e, { interactive: l } = e, { boxAlpha: r = 0.5 } = e, { boxMinSize: a = 25 } = e, { handleSize: o } = e, { boxThickness: u } = e, { boxSelectedThickness: f } = e, { value: c } = e, { choices: w = [] } = e, { choicesColors: g = [] } = e, { disableEditBoxes: v = !1 } = e, _, d, m = null, y = -1, h = i.drag;
  c !== null && c.boxes.length == 0 && (h = i.creation);
  let x = 0, p = 0, M = 0, A = 0, C = 1, B = 0, D = 0, G = !1, z = !1;
  const U = vl();
  function R() {
    if (d) {
      d.clearRect(0, 0, _.width, _.height), m !== null && d.drawImage(m, x, p, B, D);
      for (const b of c.boxes.slice().reverse())
        b.render(d);
    }
  }
  function ne(b) {
    t(6, y = b), c.boxes.forEach((E) => {
      E.setSelected(!1);
    }), b >= 0 && b < c.boxes.length && c.boxes[b].setSelected(!0), R();
  }
  function et(b) {
    l && (h === i.creation ? S(b) : h === i.drag && tt(b));
  }
  function tt(b) {
    const E = _.getBoundingClientRect(), Y = b.clientX - E.left, W = b.clientY - E.top;
    for (const [j, L] of c.boxes.entries()) {
      const At = L.indexOfPointInsideHandle(Y, W);
      if (At >= 0) {
        ne(j), L.startResize(At, b);
        return;
      }
    }
    for (const [j, L] of c.boxes.entries())
      if (L.isPointInsideBox(Y, W)) {
        ne(j), L.startDrag(b);
        return;
      }
    ne(-1);
  }
  function nt(b) {
    U("change");
  }
  function be(b) {
    if (l)
      switch (b.key) {
        case "Delete":
          He();
          break;
      }
  }
  function S(b) {
    const E = _.getBoundingClientRect(), Y = (b.clientX - E.left - x) / C, W = (b.clientY - E.top - p) / C;
    let j;
    g.length > 0 ? j = dt(g[0]) : j = ce[c.boxes.length % ce.length];
    let L = new ht(R, zt, x, p, M, A, "", Y, W, Y, W, j, r, a, o, u, f);
    L.startCreating(b, E.left, E.top), t(0, c.boxes = [L, ...c.boxes], c), ne(0), R(), U("change");
  }
  function it() {
    t(7, h = i.creation), t(5, _.style.cursor = "crosshair", _);
  }
  function Ye() {
    t(7, h = i.drag), t(5, _.style.cursor = "default", _);
  }
  function zt() {
    y >= 0 && y < c.boxes.length && (c.boxes[y].getArea() < 1 ? He() : v || t(9, z = !0));
  }
  function gn() {
    y >= 0 && y < c.boxes.length && !v && t(8, G = !0);
  }
  function wn(b) {
    l && gn();
  }
  function yn(b) {
    t(8, G = !1);
    const { detail: E } = b;
    let Y = E.label, W = E.color, j = E.ret;
    if (y >= 0 && y < c.boxes.length) {
      let L = c.boxes[y];
      j == 1 ? (L.label = Y, L.color = dt(W), R(), U("change")) : j == -1 && He();
    }
  }
  function vn(b) {
    t(9, z = !1);
    const { detail: E } = b;
    let Y = E.label, W = E.color, j = E.ret;
    if (y >= 0 && y < c.boxes.length) {
      let L = c.boxes[y];
      j == 1 ? (L.label = Y, L.color = dt(W), R(), U("change")) : He();
    }
  }
  function He() {
    y >= 0 && y < c.boxes.length && (c.boxes.splice(y, 1), ne(-1), U("change"));
  }
  function De() {
    if (_) {
      if (C = 1, t(5, _.width = _.clientWidth, _), m !== null)
        if (m.width > _.width)
          C = _.width / m.width, B = m.width * C, D = m.height * C, x = 0, p = 0, M = B, A = D, t(5, _.height = D, _);
        else {
          B = m.width, D = m.height;
          var b = (_.width - B) / 2;
          x = b, p = 0, M = b + B, A = m.height, t(5, _.height = D, _);
        }
      else
        x = 0, p = 0, M = _.width, A = _.height, t(5, _.height = _.clientHeight, _);
      if (M > 0 && A > 0)
        for (const E of c.boxes)
          E.canvasXmin = x, E.canvasYmin = p, E.canvasXmax = M, E.canvasYmax = A, E.setScaleFactor(C);
      R(), U("change");
    }
  }
  const kn = new ResizeObserver(De);
  function pn() {
    for (let b = 0; b < c.boxes.length; b++) {
      let E = c.boxes[b];
      if (!(E instanceof ht)) {
        let Y = "", W = "";
        E.hasOwnProperty("color") ? (Y = E.color, Array.isArray(Y) && Y.length === 3 && (Y = `rgb(${Y[0]}, ${Y[1]}, ${Y[2]})`)) : Y = ce[b % ce.length], E.hasOwnProperty("label") && (W = E.label), E = new ht(R, zt, x, p, M, A, W, E.xmin, E.ymin, E.xmax, E.ymax, Y, r, a, o, u, f), t(0, c.boxes[b] = E, c);
      }
    }
  }
  function Et() {
    s !== null && (m === null || m.src != s) && (m = new Image(), m.src = s, m.onload = function() {
      De(), R();
    });
  }
  wl(() => {
    if (Array.isArray(w) && w.length > 0 && (!Array.isArray(g) || g.length == 0))
      for (let b = 0; b < w.length; b++) {
        let E = ce[b % ce.length];
        g.push(Ee(E));
      }
    d = _.getContext("2d"), kn.observe(_), Et(), De(), R();
  });
  function xn() {
    document.addEventListener("keydown", be);
  }
  function Cn() {
    document.removeEventListener("keydown", be);
  }
  yl(() => {
    document.removeEventListener("keydown", be);
  });
  function Sn(b) {
    _l[b ? "unshift" : "push"](() => {
      _ = b, t(5, _);
    });
  }
  const zn = () => it(), En = () => Ye();
  function An(b) {
    $t.call(this, n, b);
  }
  function Mn(b) {
    $t.call(this, n, b);
  }
  return n.$$set = (b) => {
    "imageUrl" in b && t(19, s = b.imageUrl), "interactive" in b && t(1, l = b.interactive), "boxAlpha" in b && t(20, r = b.boxAlpha), "boxMinSize" in b && t(21, a = b.boxMinSize), "handleSize" in b && t(22, o = b.handleSize), "boxThickness" in b && t(23, u = b.boxThickness), "boxSelectedThickness" in b && t(24, f = b.boxSelectedThickness), "value" in b && t(0, c = b.value), "choices" in b && t(2, w = b.choices), "choicesColors" in b && t(3, g = b.choicesColors), "disableEditBoxes" in b && t(25, v = b.disableEditBoxes);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*value*/
    1 && (Et(), pn(), De(), R());
  }, [
    c,
    l,
    w,
    g,
    i,
    _,
    y,
    h,
    G,
    z,
    et,
    nt,
    it,
    Ye,
    wn,
    yn,
    vn,
    xn,
    Cn,
    s,
    r,
    a,
    o,
    u,
    f,
    v,
    Sn,
    zn,
    En,
    An,
    Mn
  ];
}
class xl extends ml {
  constructor(e) {
    super(), bl(
      this,
      e,
      pl,
      kl,
      gl,
      {
        imageUrl: 19,
        interactive: 1,
        boxAlpha: 20,
        boxMinSize: 21,
        handleSize: 22,
        boxThickness: 23,
        boxSelectedThickness: 24,
        value: 0,
        choices: 2,
        choicesColors: 3,
        disableEditBoxes: 25
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Cl,
  add_flush_callback: Sl,
  bind: zl,
  binding_callbacks: El,
  create_component: Al,
  destroy_component: Ml,
  init: Bl,
  mount_component: Xl,
  safe_not_equal: Yl,
  transition_in: Hl,
  transition_out: Dl
} = window.__gradio__svelte__internal, { createEventDispatcher: Rl } = window.__gradio__svelte__internal;
function Ll(n) {
  let e, t, i;
  function s(r) {
    n[14](r);
  }
  let l = {
    interactive: (
      /*interactive*/
      n[1]
    ),
    boxAlpha: (
      /*boxesAlpha*/
      n[2]
    ),
    choices: (
      /*labelList*/
      n[3]
    ),
    choicesColors: (
      /*labelColors*/
      n[4]
    ),
    boxMinSize: (
      /*boxMinSize*/
      n[5]
    ),
    handleSize: (
      /*handleSize*/
      n[6]
    ),
    boxThickness: (
      /*boxThickness*/
      n[7]
    ),
    boxSelectedThickness: (
      /*boxSelectedThickness*/
      n[8]
    ),
    disableEditBoxes: (
      /*disableEditBoxes*/
      n[9]
    ),
    imageUrl: (
      /*resolved_src*/
      n[10]
    )
  };
  return (
    /*value*/
    n[0] !== void 0 && (l.value = /*value*/
    n[0]), e = new xl({ props: l }), El.push(() => zl(e, "value", s)), e.$on(
      "change",
      /*change_handler*/
      n[15]
    ), {
      c() {
        Al(e.$$.fragment);
      },
      m(r, a) {
        Xl(e, r, a), i = !0;
      },
      p(r, [a]) {
        const o = {};
        a & /*interactive*/
        2 && (o.interactive = /*interactive*/
        r[1]), a & /*boxesAlpha*/
        4 && (o.boxAlpha = /*boxesAlpha*/
        r[2]), a & /*labelList*/
        8 && (o.choices = /*labelList*/
        r[3]), a & /*labelColors*/
        16 && (o.choicesColors = /*labelColors*/
        r[4]), a & /*boxMinSize*/
        32 && (o.boxMinSize = /*boxMinSize*/
        r[5]), a & /*handleSize*/
        64 && (o.handleSize = /*handleSize*/
        r[6]), a & /*boxThickness*/
        128 && (o.boxThickness = /*boxThickness*/
        r[7]), a & /*boxSelectedThickness*/
        256 && (o.boxSelectedThickness = /*boxSelectedThickness*/
        r[8]), a & /*disableEditBoxes*/
        512 && (o.disableEditBoxes = /*disableEditBoxes*/
        r[9]), a & /*resolved_src*/
        1024 && (o.imageUrl = /*resolved_src*/
        r[10]), !t && a & /*value*/
        1 && (t = !0, o.value = /*value*/
        r[0], Sl(() => t = !1)), e.$set(o);
      },
      i(r) {
        i || (Hl(e.$$.fragment, r), i = !0);
      },
      o(r) {
        Dl(e.$$.fragment, r), i = !1;
      },
      d(r) {
        Ml(e, r);
      }
    }
  );
}
function Tl(n, e, t) {
  let { src: i = void 0 } = e, { interactive: s } = e, { boxesAlpha: l } = e, { labelList: r } = e, { labelColors: a } = e, { boxMinSize: o } = e, { handleSize: u } = e, { boxThickness: f } = e, { boxSelectedThickness: c } = e, { value: w } = e, { disableEditBoxes: g } = e, v, _;
  const d = Rl();
  function m(h) {
    w = h, t(0, w);
  }
  const y = () => d("change");
  return n.$$set = (h) => {
    "src" in h && t(12, i = h.src), "interactive" in h && t(1, s = h.interactive), "boxesAlpha" in h && t(2, l = h.boxesAlpha), "labelList" in h && t(3, r = h.labelList), "labelColors" in h && t(4, a = h.labelColors), "boxMinSize" in h && t(5, o = h.boxMinSize), "handleSize" in h && t(6, u = h.handleSize), "boxThickness" in h && t(7, f = h.boxThickness), "boxSelectedThickness" in h && t(8, c = h.boxSelectedThickness), "value" in h && t(0, w = h.value), "disableEditBoxes" in h && t(9, g = h.disableEditBoxes);
  }, n.$$.update = () => {
    if (n.$$.dirty & /*src, latest_src*/
    12288) {
      t(10, v = i), t(13, _ = i);
      const h = i;
      Ln(h).then((x) => {
        _ === h && t(10, v = x);
      });
    }
  }, [
    w,
    s,
    l,
    r,
    a,
    o,
    u,
    f,
    c,
    g,
    v,
    d,
    i,
    _,
    m,
    y
  ];
}
class ql extends Cl {
  constructor(e) {
    super(), Bl(this, e, Tl, Ll, Yl, {
      src: 12,
      interactive: 1,
      boxesAlpha: 2,
      labelList: 3,
      labelColors: 4,
      boxMinSize: 5,
      handleSize: 6,
      boxThickness: 7,
      boxSelectedThickness: 8,
      value: 0,
      disableEditBoxes: 9
    });
  }
}
const {
  SvelteComponent: Ol,
  attr: Il,
  check_outros: Ul,
  create_component: Wl,
  destroy_component: jl,
  detach: Nl,
  element: Vl,
  group_outros: Fl,
  init: Pl,
  insert: Kl,
  mount_component: Gl,
  safe_not_equal: Jl,
  toggle_class: Q,
  transition_in: Ve,
  transition_out: pt
} = window.__gradio__svelte__internal;
function sn(n) {
  let e, t;
  return e = new ql({
    props: {
      src: (
        /*samples_dir*/
        n[1] + /*value*/
        n[0].path
      ),
      alt: ""
    }
  }), {
    c() {
      Wl(e.$$.fragment);
    },
    m(i, s) {
      Gl(e, i, s), t = !0;
    },
    p(i, s) {
      const l = {};
      s & /*samples_dir, value*/
      3 && (l.src = /*samples_dir*/
      i[1] + /*value*/
      i[0].path), e.$set(l);
    },
    i(i) {
      t || (Ve(e.$$.fragment, i), t = !0);
    },
    o(i) {
      pt(e.$$.fragment, i), t = !1;
    },
    d(i) {
      jl(e, i);
    }
  };
}
function Zl(n) {
  let e, t, i = (
    /*value*/
    n[0] && sn(n)
  );
  return {
    c() {
      e = Vl("div"), i && i.c(), Il(e, "class", "container svelte-1sgcyba"), Q(
        e,
        "table",
        /*type*/
        n[2] === "table"
      ), Q(
        e,
        "gallery",
        /*type*/
        n[2] === "gallery"
      ), Q(
        e,
        "selected",
        /*selected*/
        n[3]
      ), Q(
        e,
        "border",
        /*value*/
        n[0]
      );
    },
    m(s, l) {
      Kl(s, e, l), i && i.m(e, null), t = !0;
    },
    p(s, [l]) {
      /*value*/
      s[0] ? i ? (i.p(s, l), l & /*value*/
      1 && Ve(i, 1)) : (i = sn(s), i.c(), Ve(i, 1), i.m(e, null)) : i && (Fl(), pt(i, 1, 1, () => {
        i = null;
      }), Ul()), (!t || l & /*type*/
      4) && Q(
        e,
        "table",
        /*type*/
        s[2] === "table"
      ), (!t || l & /*type*/
      4) && Q(
        e,
        "gallery",
        /*type*/
        s[2] === "gallery"
      ), (!t || l & /*selected*/
      8) && Q(
        e,
        "selected",
        /*selected*/
        s[3]
      ), (!t || l & /*value*/
      1) && Q(
        e,
        "border",
        /*value*/
        s[0]
      );
    },
    i(s) {
      t || (Ve(i), t = !0);
    },
    o(s) {
      pt(i), t = !1;
    },
    d(s) {
      s && Nl(e), i && i.d();
    }
  };
}
function Ql(n, e, t) {
  let { value: i } = e, { samples_dir: s } = e, { type: l } = e, { selected: r = !1 } = e;
  return n.$$set = (a) => {
    "value" in a && t(0, i = a.value), "samples_dir" in a && t(1, s = a.samples_dir), "type" in a && t(2, l = a.type), "selected" in a && t(3, r = a.selected);
  }, [i, s, l, r];
}
class eo extends Ol {
  constructor(e) {
    super(), Pl(this, e, Ql, Zl, Jl, {
      value: 0,
      samples_dir: 1,
      type: 2,
      selected: 3
    });
  }
}
export {
  eo as default
};
