const {
  SvelteComponent: $t,
  assign: el,
  create_slot: tl,
  detach: ll,
  element: nl,
  get_all_dirty_from_scope: il,
  get_slot_changes: fl,
  get_spread_update: ol,
  init: sl,
  insert: al,
  safe_not_equal: rl,
  set_dynamic_element_data: xe,
  set_style: I,
  toggle_class: Y,
  transition_in: Nt,
  transition_out: It,
  update_slot_base: _l
} = window.__gradio__svelte__internal;
function ul(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), f = tl(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let o = [
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
  ], r = {};
  for (let s = 0; s < o.length; s += 1)
    r = el(r, o[s]);
  return {
    c() {
      e = nl(
        /*tag*/
        n[14]
      ), f && f.c(), xe(
        /*tag*/
        n[14]
      )(e, r), Y(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), Y(
        e,
        "padded",
        /*padding*/
        n[6]
      ), Y(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), Y(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), Y(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), I(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), I(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), I(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), I(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), I(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), I(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), I(e, "border-width", "var(--block-border-width)");
    },
    m(s, a) {
      al(s, e, a), f && f.m(e, null), l = !0;
    },
    p(s, a) {
      f && f.p && (!l || a & /*$$scope*/
      131072) && _l(
        f,
        i,
        s,
        /*$$scope*/
        s[17],
        l ? fl(
          i,
          /*$$scope*/
          s[17],
          a,
          null
        ) : il(
          /*$$scope*/
          s[17]
        ),
        null
      ), xe(
        /*tag*/
        s[14]
      )(e, r = ol(o, [
        (!l || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!l || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!l || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Y(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), Y(
        e,
        "padded",
        /*padding*/
        s[6]
      ), Y(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), Y(
        e,
        "border_contrast",
        /*border_mode*/
        s[5] === "contrast"
      ), Y(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), a & /*height*/
      1 && I(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), a & /*width*/
      2 && I(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), a & /*variant*/
      16 && I(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), a & /*allow_overflow*/
      2048 && I(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && I(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), a & /*min_width*/
      8192 && I(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      l || (Nt(f, s), l = !0);
    },
    o(s) {
      It(f, s), l = !1;
    },
    d(s) {
      s && ll(e), f && f.d(s);
    }
  };
}
function cl(n) {
  let e, t = (
    /*tag*/
    n[14] && ul(n)
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
      e || (Nt(t, l), e = !0);
    },
    o(l) {
      It(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function dl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: o = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: s = [] } = e, { variant: a = "solid" } = e, { border_mode: _ = "base" } = e, { padding: u = !0 } = e, { type: h = "normal" } = e, { test_id: d = void 0 } = e, { explicit_call: c = !1 } = e, { container: q = !0 } = e, { visible: p = !0 } = e, { allow_overflow: C = !0 } = e, { scale: m = null } = e, { min_width: b = 0 } = e, M = h === "fieldset" ? "fieldset" : "div";
  const z = (w) => {
    if (w !== void 0) {
      if (typeof w == "number")
        return w + "px";
      if (typeof w == "string")
        return w;
    }
  };
  return n.$$set = (w) => {
    "height" in w && t(0, f = w.height), "width" in w && t(1, o = w.width), "elem_id" in w && t(2, r = w.elem_id), "elem_classes" in w && t(3, s = w.elem_classes), "variant" in w && t(4, a = w.variant), "border_mode" in w && t(5, _ = w.border_mode), "padding" in w && t(6, u = w.padding), "type" in w && t(16, h = w.type), "test_id" in w && t(7, d = w.test_id), "explicit_call" in w && t(8, c = w.explicit_call), "container" in w && t(9, q = w.container), "visible" in w && t(10, p = w.visible), "allow_overflow" in w && t(11, C = w.allow_overflow), "scale" in w && t(12, m = w.scale), "min_width" in w && t(13, b = w.min_width), "$$scope" in w && t(17, i = w.$$scope);
  }, [
    f,
    o,
    r,
    s,
    a,
    _,
    u,
    d,
    c,
    q,
    p,
    C,
    m,
    b,
    M,
    z,
    h,
    i,
    l
  ];
}
class ml extends $t {
  constructor(e) {
    super(), sl(this, e, dl, cl, rl, {
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
  SvelteComponent: bl,
  attr: hl,
  create_slot: gl,
  detach: wl,
  element: pl,
  get_all_dirty_from_scope: kl,
  get_slot_changes: vl,
  init: yl,
  insert: ql,
  safe_not_equal: Cl,
  transition_in: Ml,
  transition_out: Fl,
  update_slot_base: jl
} = window.__gradio__svelte__internal;
function Ll(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[1].default
  ), i = gl(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = pl("div"), i && i.c(), hl(e, "class", "svelte-1hnfib2");
    },
    m(f, o) {
      ql(f, e, o), i && i.m(e, null), t = !0;
    },
    p(f, [o]) {
      i && i.p && (!t || o & /*$$scope*/
      1) && jl(
        i,
        l,
        f,
        /*$$scope*/
        f[0],
        t ? vl(
          l,
          /*$$scope*/
          f[0],
          o,
          null
        ) : kl(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      t || (Ml(i, f), t = !0);
    },
    o(f) {
      Fl(i, f), t = !1;
    },
    d(f) {
      f && wl(e), i && i.d(f);
    }
  };
}
function Sl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  return n.$$set = (f) => {
    "$$scope" in f && t(0, i = f.$$scope);
  }, [i, l];
}
class zl extends bl {
  constructor(e) {
    super(), yl(this, e, Sl, Ll, Cl, {});
  }
}
const {
  SvelteComponent: Vl,
  attr: $e,
  check_outros: Nl,
  create_component: Il,
  create_slot: Zl,
  destroy_component: Al,
  detach: Le,
  element: Bl,
  empty: El,
  get_all_dirty_from_scope: Pl,
  get_slot_changes: Dl,
  group_outros: Tl,
  init: Kl,
  insert: Se,
  mount_component: Ol,
  safe_not_equal: Xl,
  set_data: Yl,
  space: Gl,
  text: Rl,
  toggle_class: oe,
  transition_in: be,
  transition_out: ze,
  update_slot_base: Hl
} = window.__gradio__svelte__internal;
function et(n) {
  let e, t;
  return e = new zl({
    props: {
      $$slots: { default: [Jl] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Il(e.$$.fragment);
    },
    m(l, i) {
      Ol(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (be(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ze(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Al(e, l);
    }
  };
}
function Jl(n) {
  let e;
  return {
    c() {
      e = Rl(
        /*info*/
        n[1]
      );
    },
    m(t, l) {
      Se(t, e, l);
    },
    p(t, l) {
      l & /*info*/
      2 && Yl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Le(e);
    }
  };
}
function Ql(n) {
  let e, t, l, i;
  const f = (
    /*#slots*/
    n[2].default
  ), o = Zl(
    f,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let r = (
    /*info*/
    n[1] && et(n)
  );
  return {
    c() {
      e = Bl("span"), o && o.c(), t = Gl(), r && r.c(), l = El(), $e(e, "data-testid", "block-info"), $e(e, "class", "svelte-22c38v"), oe(e, "sr-only", !/*show_label*/
      n[0]), oe(e, "hide", !/*show_label*/
      n[0]), oe(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(s, a) {
      Se(s, e, a), o && o.m(e, null), Se(s, t, a), r && r.m(s, a), Se(s, l, a), i = !0;
    },
    p(s, [a]) {
      o && o.p && (!i || a & /*$$scope*/
      8) && Hl(
        o,
        f,
        s,
        /*$$scope*/
        s[3],
        i ? Dl(
          f,
          /*$$scope*/
          s[3],
          a,
          null
        ) : Pl(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || a & /*show_label*/
      1) && oe(e, "sr-only", !/*show_label*/
      s[0]), (!i || a & /*show_label*/
      1) && oe(e, "hide", !/*show_label*/
      s[0]), (!i || a & /*info*/
      2) && oe(
        e,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? r ? (r.p(s, a), a & /*info*/
      2 && be(r, 1)) : (r = et(s), r.c(), be(r, 1), r.m(l.parentNode, l)) : r && (Tl(), ze(r, 1, 1, () => {
        r = null;
      }), Nl());
    },
    i(s) {
      i || (be(o, s), be(r), i = !0);
    },
    o(s) {
      ze(o, s), ze(r), i = !1;
    },
    d(s) {
      s && (Le(e), Le(t), Le(l)), o && o.d(s), r && r.d(s);
    }
  };
}
function Ul(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_label: f = !0 } = e, { info: o = void 0 } = e;
  return n.$$set = (r) => {
    "show_label" in r && t(0, f = r.show_label), "info" in r && t(1, o = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [f, o, l, i];
}
class Wl extends Vl {
  constructor(e) {
    super(), Kl(this, e, Ul, Ql, Xl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: xl,
  append: Ke,
  attr: U,
  bubble: $l,
  create_component: en,
  destroy_component: tn,
  detach: Zt,
  element: Oe,
  init: ln,
  insert: At,
  listen: nn,
  mount_component: fn,
  safe_not_equal: on,
  set_data: sn,
  set_style: se,
  space: an,
  text: rn,
  toggle_class: V,
  transition_in: _n,
  transition_out: un
} = window.__gradio__svelte__internal;
function tt(n) {
  let e, t;
  return {
    c() {
      e = Oe("span"), t = rn(
        /*label*/
        n[1]
      ), U(e, "class", "svelte-1lrphxw");
    },
    m(l, i) {
      At(l, e, i), Ke(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && sn(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && Zt(e);
    }
  };
}
function cn(n) {
  let e, t, l, i, f, o, r, s = (
    /*show_label*/
    n[2] && tt(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Oe("button"), s && s.c(), t = an(), l = Oe("div"), en(i.$$.fragment), U(l, "class", "svelte-1lrphxw"), V(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), V(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), V(
        l,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], U(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), U(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), U(
        e,
        "title",
        /*label*/
        n[1]
      ), U(e, "class", "svelte-1lrphxw"), V(
        e,
        "pending",
        /*pending*/
        n[3]
      ), V(
        e,
        "padded",
        /*padded*/
        n[5]
      ), V(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), V(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), se(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), se(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), se(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(a, _) {
      At(a, e, _), s && s.m(e, null), Ke(e, t), Ke(e, l), fn(i, l, null), f = !0, o || (r = nn(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), o = !0);
    },
    p(a, [_]) {
      /*show_label*/
      a[2] ? s ? s.p(a, _) : (s = tt(a), s.c(), s.m(e, t)) : s && (s.d(1), s = null), (!f || _ & /*size*/
      16) && V(
        l,
        "small",
        /*size*/
        a[4] === "small"
      ), (!f || _ & /*size*/
      16) && V(
        l,
        "large",
        /*size*/
        a[4] === "large"
      ), (!f || _ & /*size*/
      16) && V(
        l,
        "medium",
        /*size*/
        a[4] === "medium"
      ), (!f || _ & /*disabled*/
      128) && (e.disabled = /*disabled*/
      a[7]), (!f || _ & /*label*/
      2) && U(
        e,
        "aria-label",
        /*label*/
        a[1]
      ), (!f || _ & /*hasPopup*/
      256) && U(
        e,
        "aria-haspopup",
        /*hasPopup*/
        a[8]
      ), (!f || _ & /*label*/
      2) && U(
        e,
        "title",
        /*label*/
        a[1]
      ), (!f || _ & /*pending*/
      8) && V(
        e,
        "pending",
        /*pending*/
        a[3]
      ), (!f || _ & /*padded*/
      32) && V(
        e,
        "padded",
        /*padded*/
        a[5]
      ), (!f || _ & /*highlight*/
      64) && V(
        e,
        "highlight",
        /*highlight*/
        a[6]
      ), (!f || _ & /*transparent*/
      512) && V(
        e,
        "transparent",
        /*transparent*/
        a[9]
      ), _ & /*disabled, _color*/
      4224 && se(e, "color", !/*disabled*/
      a[7] && /*_color*/
      a[12] ? (
        /*_color*/
        a[12]
      ) : "var(--block-label-text-color)"), _ & /*disabled, background*/
      1152 && se(e, "--bg-color", /*disabled*/
      a[7] ? "auto" : (
        /*background*/
        a[10]
      )), _ & /*offset*/
      2048 && se(
        e,
        "margin-left",
        /*offset*/
        a[11] + "px"
      );
    },
    i(a) {
      f || (_n(i.$$.fragment, a), f = !0);
    },
    o(a) {
      un(i.$$.fragment, a), f = !1;
    },
    d(a) {
      a && Zt(e), s && s.d(), tn(i), o = !1, r();
    }
  };
}
function dn(n, e, t) {
  let l, { Icon: i } = e, { label: f = "" } = e, { show_label: o = !1 } = e, { pending: r = !1 } = e, { size: s = "small" } = e, { padded: a = !0 } = e, { highlight: _ = !1 } = e, { disabled: u = !1 } = e, { hasPopup: h = !1 } = e, { color: d = "var(--block-label-text-color)" } = e, { transparent: c = !1 } = e, { background: q = "var(--background-fill-primary)" } = e, { offset: p = 0 } = e;
  function C(m) {
    $l.call(this, n, m);
  }
  return n.$$set = (m) => {
    "Icon" in m && t(0, i = m.Icon), "label" in m && t(1, f = m.label), "show_label" in m && t(2, o = m.show_label), "pending" in m && t(3, r = m.pending), "size" in m && t(4, s = m.size), "padded" in m && t(5, a = m.padded), "highlight" in m && t(6, _ = m.highlight), "disabled" in m && t(7, u = m.disabled), "hasPopup" in m && t(8, h = m.hasPopup), "color" in m && t(13, d = m.color), "transparent" in m && t(9, c = m.transparent), "background" in m && t(10, q = m.background), "offset" in m && t(11, p = m.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, l = _ ? "var(--color-accent)" : d);
  }, [
    i,
    f,
    o,
    r,
    s,
    a,
    _,
    u,
    h,
    c,
    q,
    p,
    l,
    d,
    C
  ];
}
class mn extends xl {
  constructor(e) {
    super(), ln(this, e, dn, cn, on, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: bn,
  append: Ee,
  attr: D,
  detach: hn,
  init: gn,
  insert: wn,
  noop: Pe,
  safe_not_equal: pn,
  set_style: G,
  svg_element: Me
} = window.__gradio__svelte__internal;
function kn(n) {
  let e, t, l, i;
  return {
    c() {
      e = Me("svg"), t = Me("g"), l = Me("path"), i = Me("path"), D(l, "d", "M18,6L6.087,17.913"), G(l, "fill", "none"), G(l, "fill-rule", "nonzero"), G(l, "stroke-width", "2px"), D(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), D(i, "d", "M4.364,4.364L19.636,19.636"), G(i, "fill", "none"), G(i, "fill-rule", "nonzero"), G(i, "stroke-width", "2px"), D(e, "width", "100%"), D(e, "height", "100%"), D(e, "viewBox", "0 0 24 24"), D(e, "version", "1.1"), D(e, "xmlns", "http://www.w3.org/2000/svg"), D(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), D(e, "xml:space", "preserve"), D(e, "stroke", "currentColor"), G(e, "fill-rule", "evenodd"), G(e, "clip-rule", "evenodd"), G(e, "stroke-linecap", "round"), G(e, "stroke-linejoin", "round");
    },
    m(f, o) {
      wn(f, e, o), Ee(e, t), Ee(t, l), Ee(e, i);
    },
    p: Pe,
    i: Pe,
    o: Pe,
    d(f) {
      f && hn(e);
    }
  };
}
class vn extends bn {
  constructor(e) {
    super(), gn(this, e, null, kn, pn, {});
  }
}
const yn = [
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
], lt = {
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
yn.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: lt[e][t],
      secondary: lt[e][l]
    }
  }),
  {}
);
function re(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function Ve() {
}
function qn(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const Bt = typeof window < "u";
let nt = Bt ? () => window.performance.now() : () => Date.now(), Et = Bt ? (n) => requestAnimationFrame(n) : Ve;
const ue = /* @__PURE__ */ new Set();
function Pt(n) {
  ue.forEach((e) => {
    e.c(n) || (ue.delete(e), e.f());
  }), ue.size !== 0 && Et(Pt);
}
function Cn(n) {
  let e;
  return ue.size === 0 && Et(Pt), {
    promise: new Promise((t) => {
      ue.add(e = { c: n, f: t });
    }),
    abort() {
      ue.delete(e);
    }
  };
}
const ae = [];
function Mn(n, e = Ve) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(r) {
    if (qn(n, r) && (n = r, t)) {
      const s = !ae.length;
      for (const a of l)
        a[1](), ae.push(a, n);
      if (s) {
        for (let a = 0; a < ae.length; a += 2)
          ae[a][0](ae[a + 1]);
        ae.length = 0;
      }
    }
  }
  function f(r) {
    i(r(n));
  }
  function o(r, s = Ve) {
    const a = [r, s];
    return l.add(a), l.size === 1 && (t = e(i, f) || Ve), r(n), () => {
      l.delete(a), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: o };
}
function it(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function Xe(n, e, t, l) {
  if (typeof t == "number" || it(t)) {
    const i = l - t, f = (t - e) / (n.dt || 1 / 60), o = n.opts.stiffness * i, r = n.opts.damping * f, s = (o - r) * n.inv_mass, a = (f + s) * n.dt;
    return Math.abs(a) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, it(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => Xe(n, e[f], t[f], l[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = Xe(n, e[f], t[f], l[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function ft(n, e = {}) {
  const t = Mn(n), { stiffness: l = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let o, r, s, a = n, _ = n, u = 1, h = 0, d = !1;
  function c(p, C = {}) {
    _ = p;
    const m = s = {};
    return n == null || C.hard || q.stiffness >= 1 && q.damping >= 1 ? (d = !0, o = nt(), a = p, t.set(n = _), Promise.resolve()) : (C.soft && (h = 1 / ((C.soft === !0 ? 0.5 : +C.soft) * 60), u = 0), r || (o = nt(), d = !1, r = Cn((b) => {
      if (d)
        return d = !1, r = null, !1;
      u = Math.min(u + h, 1);
      const M = {
        inv_mass: u,
        opts: q,
        settled: !0,
        dt: (b - o) * 60 / 1e3
      }, z = Xe(M, a, n, _);
      return o = b, a = n, t.set(n = z), M.settled && (r = null), !M.settled;
    })), new Promise((b) => {
      r.promise.then(() => {
        m === s && b();
      });
    }));
  }
  const q = {
    set: c,
    update: (p, C) => c(p(_, n), C),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: f
  };
  return q;
}
const {
  SvelteComponent: Fn,
  append: T,
  attr: F,
  component_subscribe: ot,
  detach: jn,
  element: Ln,
  init: Sn,
  insert: zn,
  noop: st,
  safe_not_equal: Vn,
  set_style: Fe,
  svg_element: K,
  toggle_class: at
} = window.__gradio__svelte__internal, { onMount: Nn } = window.__gradio__svelte__internal;
function In(n) {
  let e, t, l, i, f, o, r, s, a, _, u, h;
  return {
    c() {
      e = Ln("div"), t = K("svg"), l = K("g"), i = K("path"), f = K("path"), o = K("path"), r = K("path"), s = K("g"), a = K("path"), _ = K("path"), u = K("path"), h = K("path"), F(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), F(i, "fill", "#FF7C00"), F(i, "fill-opacity", "0.4"), F(i, "class", "svelte-43sxxs"), F(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), F(f, "fill", "#FF7C00"), F(f, "class", "svelte-43sxxs"), F(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), F(o, "fill", "#FF7C00"), F(o, "fill-opacity", "0.4"), F(o, "class", "svelte-43sxxs"), F(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), F(r, "fill", "#FF7C00"), F(r, "class", "svelte-43sxxs"), Fe(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), F(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), F(a, "fill", "#FF7C00"), F(a, "fill-opacity", "0.4"), F(a, "class", "svelte-43sxxs"), F(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), F(_, "fill", "#FF7C00"), F(_, "class", "svelte-43sxxs"), F(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), F(u, "fill", "#FF7C00"), F(u, "fill-opacity", "0.4"), F(u, "class", "svelte-43sxxs"), F(h, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), F(h, "fill", "#FF7C00"), F(h, "class", "svelte-43sxxs"), Fe(s, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), F(t, "viewBox", "-1200 -1200 3000 3000"), F(t, "fill", "none"), F(t, "xmlns", "http://www.w3.org/2000/svg"), F(t, "class", "svelte-43sxxs"), F(e, "class", "svelte-43sxxs"), at(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(d, c) {
      zn(d, e, c), T(e, t), T(t, l), T(l, i), T(l, f), T(l, o), T(l, r), T(t, s), T(s, a), T(s, _), T(s, u), T(s, h);
    },
    p(d, [c]) {
      c & /*$top*/
      2 && Fe(l, "transform", "translate(" + /*$top*/
      d[1][0] + "px, " + /*$top*/
      d[1][1] + "px)"), c & /*$bottom*/
      4 && Fe(s, "transform", "translate(" + /*$bottom*/
      d[2][0] + "px, " + /*$bottom*/
      d[2][1] + "px)"), c & /*margin*/
      1 && at(
        e,
        "margin",
        /*margin*/
        d[0]
      );
    },
    i: st,
    o: st,
    d(d) {
      d && jn(e);
    }
  };
}
function Zn(n, e, t) {
  let l, i;
  var f = this && this.__awaiter || function(d, c, q, p) {
    function C(m) {
      return m instanceof q ? m : new q(function(b) {
        b(m);
      });
    }
    return new (q || (q = Promise))(function(m, b) {
      function M(L) {
        try {
          w(p.next(L));
        } catch (P) {
          b(P);
        }
      }
      function z(L) {
        try {
          w(p.throw(L));
        } catch (P) {
          b(P);
        }
      }
      function w(L) {
        L.done ? m(L.value) : C(L.value).then(M, z);
      }
      w((p = p.apply(d, c || [])).next());
    });
  };
  let { margin: o = !0 } = e;
  const r = ft([0, 0]);
  ot(n, r, (d) => t(1, l = d));
  const s = ft([0, 0]);
  ot(n, s, (d) => t(2, i = d));
  let a;
  function _() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), s.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), s.set([125, -140])]), yield Promise.all([r.set([-125, 0]), s.set([125, -0])]), yield Promise.all([r.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function u() {
    return f(this, void 0, void 0, function* () {
      yield _(), a || u();
    });
  }
  function h() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), s.set([-125, 0])]), u();
    });
  }
  return Nn(() => (h(), () => a = !0)), n.$$set = (d) => {
    "margin" in d && t(0, o = d.margin);
  }, [o, l, i, r, s];
}
class An extends Fn {
  constructor(e) {
    super(), Sn(this, e, Zn, In, Vn, { margin: 0 });
  }
}
const {
  SvelteComponent: Bn,
  append: ne,
  attr: X,
  binding_callbacks: rt,
  check_outros: Ye,
  create_component: Dt,
  create_slot: Tt,
  destroy_component: Kt,
  destroy_each: Ot,
  detach: k,
  element: R,
  empty: ce,
  ensure_array_like: Ie,
  get_all_dirty_from_scope: Xt,
  get_slot_changes: Yt,
  group_outros: Ge,
  init: En,
  insert: v,
  mount_component: Gt,
  noop: Re,
  safe_not_equal: Pn,
  set_data: E,
  set_style: te,
  space: B,
  text: j,
  toggle_class: A,
  transition_in: O,
  transition_out: H,
  update_slot_base: Rt
} = window.__gradio__svelte__internal, { tick: Dn } = window.__gradio__svelte__internal, { onDestroy: Tn } = window.__gradio__svelte__internal, { createEventDispatcher: Kn } = window.__gradio__svelte__internal, On = (n) => ({}), _t = (n) => ({}), Xn = (n) => ({}), ut = (n) => ({});
function ct(n, e, t) {
  const l = n.slice();
  return l[41] = e[t], l[43] = t, l;
}
function dt(n, e, t) {
  const l = n.slice();
  return l[41] = e[t], l;
}
function Yn(n) {
  let e, t, l, i, f = (
    /*i18n*/
    n[1]("common.error") + ""
  ), o, r, s;
  t = new mn({
    props: {
      Icon: vn,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const a = (
    /*#slots*/
    n[30].error
  ), _ = Tt(
    a,
    n,
    /*$$scope*/
    n[29],
    _t
  );
  return {
    c() {
      e = R("div"), Dt(t.$$.fragment), l = B(), i = R("span"), o = j(f), r = B(), _ && _.c(), X(e, "class", "clear-status svelte-16nch4a"), X(i, "class", "error svelte-16nch4a");
    },
    m(u, h) {
      v(u, e, h), Gt(t, e, null), v(u, l, h), v(u, i, h), ne(i, o), v(u, r, h), _ && _.m(u, h), s = !0;
    },
    p(u, h) {
      const d = {};
      h[0] & /*i18n*/
      2 && (d.label = /*i18n*/
      u[1]("common.clear")), t.$set(d), (!s || h[0] & /*i18n*/
      2) && f !== (f = /*i18n*/
      u[1]("common.error") + "") && E(o, f), _ && _.p && (!s || h[0] & /*$$scope*/
      536870912) && Rt(
        _,
        a,
        u,
        /*$$scope*/
        u[29],
        s ? Yt(
          a,
          /*$$scope*/
          u[29],
          h,
          On
        ) : Xt(
          /*$$scope*/
          u[29]
        ),
        _t
      );
    },
    i(u) {
      s || (O(t.$$.fragment, u), O(_, u), s = !0);
    },
    o(u) {
      H(t.$$.fragment, u), H(_, u), s = !1;
    },
    d(u) {
      u && (k(e), k(l), k(i), k(r)), Kt(t), _ && _.d(u);
    }
  };
}
function Gn(n) {
  let e, t, l, i, f, o, r, s, a, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && mt(n)
  );
  function u(b, M) {
    if (
      /*progress*/
      b[7]
    )
      return Jn;
    if (
      /*queue_position*/
      b[2] !== null && /*queue_size*/
      b[3] !== void 0 && /*queue_position*/
      b[2] >= 0
    )
      return Hn;
    if (
      /*queue_position*/
      b[2] === 0
    )
      return Rn;
  }
  let h = u(n), d = h && h(n), c = (
    /*timer*/
    n[5] && gt(n)
  );
  const q = [xn, Wn], p = [];
  function C(b, M) {
    return (
      /*last_progress_level*/
      b[15] != null ? 0 : (
        /*show_progress*/
        b[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = C(n)) && (o = p[f] = q[f](n));
  let m = !/*timer*/
  n[5] && Ct(n);
  return {
    c() {
      _ && _.c(), e = B(), t = R("div"), d && d.c(), l = B(), c && c.c(), i = B(), o && o.c(), r = B(), m && m.c(), s = ce(), X(t, "class", "progress-text svelte-16nch4a"), A(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), A(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(b, M) {
      _ && _.m(b, M), v(b, e, M), v(b, t, M), d && d.m(t, null), ne(t, l), c && c.m(t, null), v(b, i, M), ~f && p[f].m(b, M), v(b, r, M), m && m.m(b, M), v(b, s, M), a = !0;
    },
    p(b, M) {
      /*variant*/
      b[8] === "default" && /*show_eta_bar*/
      b[18] && /*show_progress*/
      b[6] === "full" ? _ ? _.p(b, M) : (_ = mt(b), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), h === (h = u(b)) && d ? d.p(b, M) : (d && d.d(1), d = h && h(b), d && (d.c(), d.m(t, l))), /*timer*/
      b[5] ? c ? c.p(b, M) : (c = gt(b), c.c(), c.m(t, null)) : c && (c.d(1), c = null), (!a || M[0] & /*variant*/
      256) && A(
        t,
        "meta-text-center",
        /*variant*/
        b[8] === "center"
      ), (!a || M[0] & /*variant*/
      256) && A(
        t,
        "meta-text",
        /*variant*/
        b[8] === "default"
      );
      let z = f;
      f = C(b), f === z ? ~f && p[f].p(b, M) : (o && (Ge(), H(p[z], 1, 1, () => {
        p[z] = null;
      }), Ye()), ~f ? (o = p[f], o ? o.p(b, M) : (o = p[f] = q[f](b), o.c()), O(o, 1), o.m(r.parentNode, r)) : o = null), /*timer*/
      b[5] ? m && (Ge(), H(m, 1, 1, () => {
        m = null;
      }), Ye()) : m ? (m.p(b, M), M[0] & /*timer*/
      32 && O(m, 1)) : (m = Ct(b), m.c(), O(m, 1), m.m(s.parentNode, s));
    },
    i(b) {
      a || (O(o), O(m), a = !0);
    },
    o(b) {
      H(o), H(m), a = !1;
    },
    d(b) {
      b && (k(e), k(t), k(i), k(r), k(s)), _ && _.d(b), d && d.d(), c && c.d(), ~f && p[f].d(b), m && m.d(b);
    }
  };
}
function mt(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = R("div"), X(e, "class", "eta-bar svelte-16nch4a"), te(e, "transform", t);
    },
    m(l, i) {
      v(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && te(e, "transform", t);
    },
    d(l) {
      l && k(e);
    }
  };
}
function Rn(n) {
  let e;
  return {
    c() {
      e = j("processing |");
    },
    m(t, l) {
      v(t, e, l);
    },
    p: Re,
    d(t) {
      t && k(e);
    }
  };
}
function Hn(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, f, o;
  return {
    c() {
      e = j("queue: "), l = j(t), i = j("/"), f = j(
        /*queue_size*/
        n[3]
      ), o = j(" |");
    },
    m(r, s) {
      v(r, e, s), v(r, l, s), v(r, i, s), v(r, f, s), v(r, o, s);
    },
    p(r, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && E(l, t), s[0] & /*queue_size*/
      8 && E(
        f,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (k(e), k(l), k(i), k(f), k(o));
    }
  };
}
function Jn(n) {
  let e, t = Ie(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = ht(dt(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = ce();
    },
    m(i, f) {
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(i, f);
      v(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = Ie(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const r = dt(i, t, o);
          l[o] ? l[o].p(r, f) : (l[o] = ht(r), l[o].c(), l[o].m(e.parentNode, e));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && k(e), Ot(l, i);
    }
  };
}
function bt(n) {
  let e, t = (
    /*p*/
    n[41].unit + ""
  ), l, i, f = " ", o;
  function r(_, u) {
    return (
      /*p*/
      _[41].length != null ? Un : Qn
    );
  }
  let s = r(n), a = s(n);
  return {
    c() {
      a.c(), e = B(), l = j(t), i = j(" | "), o = j(f);
    },
    m(_, u) {
      a.m(_, u), v(_, e, u), v(_, l, u), v(_, i, u), v(_, o, u);
    },
    p(_, u) {
      s === (s = r(_)) && a ? a.p(_, u) : (a.d(1), a = s(_), a && (a.c(), a.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[41].unit + "") && E(l, t);
    },
    d(_) {
      _ && (k(e), k(l), k(i), k(o)), a.d(_);
    }
  };
}
function Qn(n) {
  let e = re(
    /*p*/
    n[41].index || 0
  ) + "", t;
  return {
    c() {
      t = j(e);
    },
    m(l, i) {
      v(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = re(
        /*p*/
        l[41].index || 0
      ) + "") && E(t, e);
    },
    d(l) {
      l && k(t);
    }
  };
}
function Un(n) {
  let e = re(
    /*p*/
    n[41].index || 0
  ) + "", t, l, i = re(
    /*p*/
    n[41].length
  ) + "", f;
  return {
    c() {
      t = j(e), l = j("/"), f = j(i);
    },
    m(o, r) {
      v(o, t, r), v(o, l, r), v(o, f, r);
    },
    p(o, r) {
      r[0] & /*progress*/
      128 && e !== (e = re(
        /*p*/
        o[41].index || 0
      ) + "") && E(t, e), r[0] & /*progress*/
      128 && i !== (i = re(
        /*p*/
        o[41].length
      ) + "") && E(f, i);
    },
    d(o) {
      o && (k(t), k(l), k(f));
    }
  };
}
function ht(n) {
  let e, t = (
    /*p*/
    n[41].index != null && bt(n)
  );
  return {
    c() {
      t && t.c(), e = ce();
    },
    m(l, i) {
      t && t.m(l, i), v(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[41].index != null ? t ? t.p(l, i) : (t = bt(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && k(e), t && t.d(l);
    }
  };
}
function gt(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = j(
        /*formatted_timer*/
        n[20]
      ), l = j(t), i = j("s");
    },
    m(f, o) {
      v(f, e, o), v(f, l, o), v(f, i, o);
    },
    p(f, o) {
      o[0] & /*formatted_timer*/
      1048576 && E(
        e,
        /*formatted_timer*/
        f[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && E(l, t);
    },
    d(f) {
      f && (k(e), k(l), k(i));
    }
  };
}
function Wn(n) {
  let e, t;
  return e = new An({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Dt(e.$$.fragment);
    },
    m(l, i) {
      Gt(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      l[8] === "default"), e.$set(f);
    },
    i(l) {
      t || (O(e.$$.fragment, l), t = !0);
    },
    o(l) {
      H(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Kt(e, l);
    }
  };
}
function xn(n) {
  let e, t, l, i, f, o = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && wt(n)
  );
  return {
    c() {
      e = R("div"), t = R("div"), r && r.c(), l = B(), i = R("div"), f = R("div"), X(t, "class", "progress-level-inner svelte-16nch4a"), X(f, "class", "progress-bar svelte-16nch4a"), te(f, "width", o), X(i, "class", "progress-bar-wrap svelte-16nch4a"), X(e, "class", "progress-level svelte-16nch4a");
    },
    m(s, a) {
      v(s, e, a), ne(e, t), r && r.m(t, null), ne(e, l), ne(e, i), ne(i, f), n[31](f);
    },
    p(s, a) {
      /*progress*/
      s[7] != null ? r ? r.p(s, a) : (r = wt(s), r.c(), r.m(t, null)) : r && (r.d(1), r = null), a[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      s[15] * 100}%`) && te(f, "width", o);
    },
    i: Re,
    o: Re,
    d(s) {
      s && k(e), r && r.d(), n[31](null);
    }
  };
}
function wt(n) {
  let e, t = Ie(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = qt(ct(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = ce();
    },
    m(i, f) {
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(i, f);
      v(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = Ie(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const r = ct(i, t, o);
          l[o] ? l[o].p(r, f) : (l[o] = qt(r), l[o].c(), l[o].m(e.parentNode, e));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && k(e), Ot(l, i);
    }
  };
}
function pt(n) {
  let e, t, l, i, f = (
    /*i*/
    n[43] !== 0 && $n()
  ), o = (
    /*p*/
    n[41].desc != null && kt(n)
  ), r = (
    /*p*/
    n[41].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null && vt()
  ), s = (
    /*progress_level*/
    n[14] != null && yt(n)
  );
  return {
    c() {
      f && f.c(), e = B(), o && o.c(), t = B(), r && r.c(), l = B(), s && s.c(), i = ce();
    },
    m(a, _) {
      f && f.m(a, _), v(a, e, _), o && o.m(a, _), v(a, t, _), r && r.m(a, _), v(a, l, _), s && s.m(a, _), v(a, i, _);
    },
    p(a, _) {
      /*p*/
      a[41].desc != null ? o ? o.p(a, _) : (o = kt(a), o.c(), o.m(t.parentNode, t)) : o && (o.d(1), o = null), /*p*/
      a[41].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[43]
      ] != null ? r || (r = vt(), r.c(), r.m(l.parentNode, l)) : r && (r.d(1), r = null), /*progress_level*/
      a[14] != null ? s ? s.p(a, _) : (s = yt(a), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(a) {
      a && (k(e), k(t), k(l), k(i)), f && f.d(a), o && o.d(a), r && r.d(a), s && s.d(a);
    }
  };
}
function $n(n) {
  let e;
  return {
    c() {
      e = j(" /");
    },
    m(t, l) {
      v(t, e, l);
    },
    d(t) {
      t && k(e);
    }
  };
}
function kt(n) {
  let e = (
    /*p*/
    n[41].desc + ""
  ), t;
  return {
    c() {
      t = j(e);
    },
    m(l, i) {
      v(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[41].desc + "") && E(t, e);
    },
    d(l) {
      l && k(t);
    }
  };
}
function vt(n) {
  let e;
  return {
    c() {
      e = j("-");
    },
    m(t, l) {
      v(t, e, l);
    },
    d(t) {
      t && k(e);
    }
  };
}
function yt(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[43]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = j(e), l = j("%");
    },
    m(i, f) {
      v(i, t, f), v(i, l, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && E(t, e);
    },
    d(i) {
      i && (k(t), k(l));
    }
  };
}
function qt(n) {
  let e, t = (
    /*p*/
    (n[41].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null) && pt(n)
  );
  return {
    c() {
      t && t.c(), e = ce();
    },
    m(l, i) {
      t && t.m(l, i), v(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[41].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[43]
      ] != null ? t ? t.p(l, i) : (t = pt(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && k(e), t && t.d(l);
    }
  };
}
function Ct(n) {
  let e, t, l, i;
  const f = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), o = Tt(
    f,
    n,
    /*$$scope*/
    n[29],
    ut
  );
  return {
    c() {
      e = R("p"), t = j(
        /*loading_text*/
        n[9]
      ), l = B(), o && o.c(), X(e, "class", "loading svelte-16nch4a");
    },
    m(r, s) {
      v(r, e, s), ne(e, t), v(r, l, s), o && o.m(r, s), i = !0;
    },
    p(r, s) {
      (!i || s[0] & /*loading_text*/
      512) && E(
        t,
        /*loading_text*/
        r[9]
      ), o && o.p && (!i || s[0] & /*$$scope*/
      536870912) && Rt(
        o,
        f,
        r,
        /*$$scope*/
        r[29],
        i ? Yt(
          f,
          /*$$scope*/
          r[29],
          s,
          Xn
        ) : Xt(
          /*$$scope*/
          r[29]
        ),
        ut
      );
    },
    i(r) {
      i || (O(o, r), i = !0);
    },
    o(r) {
      H(o, r), i = !1;
    },
    d(r) {
      r && (k(e), k(l)), o && o.d(r);
    }
  };
}
function ei(n) {
  let e, t, l, i, f;
  const o = [Gn, Yn], r = [];
  function s(a, _) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(n)) && (l = r[t] = o[t](n)), {
    c() {
      e = R("div"), l && l.c(), X(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-16nch4a"), A(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), A(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), A(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), A(
        e,
        "border",
        /*border*/
        n[12]
      ), te(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), te(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, _) {
      v(a, e, _), ~t && r[t].m(e, null), n[33](e), f = !0;
    },
    p(a, _) {
      let u = t;
      t = s(a), t === u ? ~t && r[t].p(a, _) : (l && (Ge(), H(r[u], 1, 1, () => {
        r[u] = null;
      }), Ye()), ~t ? (l = r[t], l ? l.p(a, _) : (l = r[t] = o[t](a), l.c()), O(l, 1), l.m(e, null)) : l = null), (!f || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-16nch4a")) && X(e, "class", i), (!f || _[0] & /*variant, show_progress, status, show_progress*/
      336) && A(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!f || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && A(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!f || _[0] & /*variant, show_progress, status*/
      336) && A(
        e,
        "generating",
        /*status*/
        a[4] === "generating"
      ), (!f || _[0] & /*variant, show_progress, border*/
      4416) && A(
        e,
        "border",
        /*border*/
        a[12]
      ), _[0] & /*absolute*/
      1024 && te(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && te(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      f || (O(l), f = !0);
    },
    o(a) {
      H(l), f = !1;
    },
    d(a) {
      a && k(e), ~t && r[t].d(), n[33](null);
    }
  };
}
var ti = function(n, e, t, l) {
  function i(f) {
    return f instanceof t ? f : new t(function(o) {
      o(f);
    });
  }
  return new (t || (t = Promise))(function(f, o) {
    function r(_) {
      try {
        a(l.next(_));
      } catch (u) {
        o(u);
      }
    }
    function s(_) {
      try {
        a(l.throw(_));
      } catch (u) {
        o(u);
      }
    }
    function a(_) {
      _.done ? f(_.value) : i(_.value).then(r, s);
    }
    a((l = l.apply(n, e || [])).next());
  });
};
let je = [], De = !1;
function li(n) {
  return ti(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (je.push(e), !De)
        De = !0;
      else
        return;
      yield Dn(), requestAnimationFrame(() => {
        let l = [0, 0];
        for (let i = 0; i < je.length; i++) {
          const o = je[i].getBoundingClientRect();
          (i === 0 || o.top + window.scrollY <= l[0]) && (l[0] = o.top + window.scrollY, l[1] = i);
        }
        window.scrollTo({ top: l[0] - 20, behavior: "smooth" }), De = !1, je = [];
      });
    }
  });
}
function ni(n, e, t) {
  let l, { $$slots: i = {}, $$scope: f } = e;
  this && this.__awaiter;
  const o = Kn();
  let { i18n: r } = e, { eta: s = null } = e, { queue_position: a } = e, { queue_size: _ } = e, { status: u } = e, { scroll_to_output: h = !1 } = e, { timer: d = !0 } = e, { show_progress: c = "full" } = e, { message: q = null } = e, { progress: p = null } = e, { variant: C = "default" } = e, { loading_text: m = "Loading..." } = e, { absolute: b = !0 } = e, { translucent: M = !1 } = e, { border: z = !1 } = e, { autoscroll: w } = e, L, P = !1, ie = 0, J = 0, W = null, y = null, x = 0, S = null, Z, N = null, $ = !0;
  const fe = () => {
    t(0, s = t(27, W = t(19, ee = null))), t(25, ie = performance.now()), t(26, J = 0), P = !0, ke();
  };
  function ke() {
    requestAnimationFrame(() => {
      t(26, J = (performance.now() - ie) / 1e3), P && ke();
    });
  }
  function ve() {
    t(26, J = 0), t(0, s = t(27, W = t(19, ee = null))), P && (P = !1);
  }
  Tn(() => {
    P && ve();
  });
  let ee = null;
  function Q(g) {
    rt[g ? "unshift" : "push"](() => {
      N = g, t(16, N), t(7, p), t(14, S), t(15, Z);
    });
  }
  const de = () => {
    o("clear_status");
  };
  function Jt(g) {
    rt[g ? "unshift" : "push"](() => {
      L = g, t(13, L);
    });
  }
  return n.$$set = (g) => {
    "i18n" in g && t(1, r = g.i18n), "eta" in g && t(0, s = g.eta), "queue_position" in g && t(2, a = g.queue_position), "queue_size" in g && t(3, _ = g.queue_size), "status" in g && t(4, u = g.status), "scroll_to_output" in g && t(22, h = g.scroll_to_output), "timer" in g && t(5, d = g.timer), "show_progress" in g && t(6, c = g.show_progress), "message" in g && t(23, q = g.message), "progress" in g && t(7, p = g.progress), "variant" in g && t(8, C = g.variant), "loading_text" in g && t(9, m = g.loading_text), "absolute" in g && t(10, b = g.absolute), "translucent" in g && t(11, M = g.translucent), "border" in g && t(12, z = g.border), "autoscroll" in g && t(24, w = g.autoscroll), "$$scope" in g && t(29, f = g.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && t(0, s = W), s != null && W !== s && (t(28, y = (performance.now() - ie) / 1e3 + s), t(19, ee = y.toFixed(1)), t(27, W = s))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, x = y === null || y <= 0 || !J ? null : Math.min(J / y, 1)), n.$$.dirty[0] & /*progress*/
    128 && p != null && t(18, $ = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (p != null ? t(14, S = p.map((g) => {
      if (g.index != null && g.length != null)
        return g.index / g.length;
      if (g.progress != null)
        return g.progress;
    })) : t(14, S = null), S ? (t(15, Z = S[S.length - 1]), N && (Z === 0 ? t(16, N.style.transition = "0", N) : t(16, N.style.transition = "150ms", N))) : t(15, Z = void 0)), n.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? fe() : ve()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && L && h && (u === "pending" || u === "complete") && li(L, w), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, l = J.toFixed(1));
  }, [
    s,
    r,
    a,
    _,
    u,
    d,
    c,
    p,
    C,
    m,
    b,
    M,
    z,
    L,
    S,
    Z,
    N,
    x,
    $,
    ee,
    l,
    o,
    h,
    q,
    w,
    ie,
    J,
    W,
    y,
    f,
    i,
    Q,
    de,
    Jt
  ];
}
class ii extends Bn {
  constructor(e) {
    super(), En(
      this,
      e,
      ni,
      ei,
      Pn,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: fi,
  add_render_callback: oi,
  append: he,
  assign: si,
  attr: Ne,
  check_outros: ai,
  create_component: He,
  destroy_component: Je,
  destroy_each: ri,
  detach: we,
  element: Ze,
  ensure_array_like: Mt,
  get_spread_object: _i,
  get_spread_update: ui,
  group_outros: ci,
  init: di,
  insert: pe,
  listen: mi,
  mount_component: Qe,
  safe_not_equal: bi,
  select_option: Ft,
  select_value: hi,
  set_data: Ue,
  set_input_value: jt,
  space: Te,
  text: We,
  toggle_class: gi,
  transition_in: _e,
  transition_out: ge
} = window.__gradio__svelte__internal, { onMount: wi } = window.__gradio__svelte__internal;
function Lt(n, e, t) {
  const l = n.slice();
  return l[25] = e[t], l;
}
function St(n) {
  let e, t;
  const l = [
    {
      autoscroll: (
        /*gradio*/
        n[10].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[10].i18n
    ) },
    /*loading_status*/
    n[9]
  ];
  let i = {};
  for (let f = 0; f < l.length; f += 1)
    i = si(i, l[f]);
  return e = new ii({ props: i }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    n[18]
  ), {
    c() {
      He(e.$$.fragment);
    },
    m(f, o) {
      Qe(e, f, o), t = !0;
    },
    p(f, o) {
      const r = o & /*gradio, loading_status*/
      1536 ? ui(l, [
        o & /*gradio*/
        1024 && {
          autoscroll: (
            /*gradio*/
            f[10].autoscroll
          )
        },
        o & /*gradio*/
        1024 && { i18n: (
          /*gradio*/
          f[10].i18n
        ) },
        o & /*loading_status*/
        512 && _i(
          /*loading_status*/
          f[9]
        )
      ]) : {};
      e.$set(r);
    },
    i(f) {
      t || (_e(e.$$.fragment, f), t = !0);
    },
    o(f) {
      ge(e.$$.fragment, f), t = !1;
    },
    d(f) {
      Je(e, f);
    }
  };
}
function pi(n) {
  let e;
  return {
    c() {
      e = We(
        /*label*/
        n[4]
      );
    },
    m(t, l) {
      pe(t, e, l);
    },
    p(t, l) {
      l & /*label*/
      16 && Ue(
        e,
        /*label*/
        t[4]
      );
    },
    d(t) {
      t && we(e);
    }
  };
}
function zt(n) {
  let e, t = (
    /*item*/
    n[25][0] + ""
  ), l, i;
  return {
    c() {
      e = Ze("option"), l = We(t), e.__value = i = /*item*/
      n[25][1], jt(e, e.__value);
    },
    m(f, o) {
      pe(f, e, o), he(e, l);
    },
    p(f, o) {
      o & /*options*/
      8192 && t !== (t = /*item*/
      f[25][0] + "") && Ue(l, t), o & /*options*/
      8192 && i !== (i = /*item*/
      f[25][1]) && (e.__value = i, jt(e, e.__value));
    },
    d(f) {
      f && we(e);
    }
  };
}
function Vt(n) {
  let e, t;
  return {
    c() {
      e = Ze("span"), t = We(
        /*errMsg*/
        n[11]
      ), Ne(e, "class", "dp_project--error svelte-l3vjji");
    },
    m(l, i) {
      pe(l, e, i), he(e, t);
    },
    p(l, i) {
      i & /*errMsg*/
      2048 && Ue(
        t,
        /*errMsg*/
        l[11]
      );
    },
    d(l) {
      l && we(e);
    }
  };
}
function ki(n) {
  let e, t, l, i, f, o, r, s, a, _ = (
    /*loading_status*/
    n[9] && St(n)
  );
  l = new Wl({
    props: {
      show_label: (
        /*show_label*/
        n[6]
      ),
      info: void 0,
      $$slots: { default: [pi] },
      $$scope: { ctx: n }
    }
  });
  let u = Mt(
    /*options*/
    n[13]
  ), h = [];
  for (let c = 0; c < u.length; c += 1)
    h[c] = zt(Lt(n, u, c));
  let d = (
    /*isError*/
    n[12] && Vt(n)
  );
  return {
    c() {
      _ && _.c(), e = Te(), t = Ze("label"), He(l.$$.fragment), i = Te(), f = Ze("select");
      for (let c = 0; c < h.length; c += 1)
        h[c].c();
      o = Te(), d && d.c(), Ne(
        f,
        "placeholder",
        /*placeholder*/
        n[5]
      ), Ne(f, "class", "svelte-l3vjji"), /*value*/
      n[0] === void 0 && oi(() => (
        /*select_change_handler*/
        n[19].call(f)
      )), gi(t, "container", Ht);
    },
    m(c, q) {
      _ && _.m(c, q), pe(c, e, q), pe(c, t, q), Qe(l, t, null), he(t, i), he(t, f);
      for (let p = 0; p < h.length; p += 1)
        h[p] && h[p].m(f, null);
      Ft(
        f,
        /*value*/
        n[0],
        !0
      ), he(t, o), d && d.m(t, null), r = !0, s || (a = mi(
        f,
        "change",
        /*select_change_handler*/
        n[19]
      ), s = !0);
    },
    p(c, q) {
      /*loading_status*/
      c[9] ? _ ? (_.p(c, q), q & /*loading_status*/
      512 && _e(_, 1)) : (_ = St(c), _.c(), _e(_, 1), _.m(e.parentNode, e)) : _ && (ci(), ge(_, 1, 1, () => {
        _ = null;
      }), ai());
      const p = {};
      if (q & /*show_label*/
      64 && (p.show_label = /*show_label*/
      c[6]), q & /*$$scope, label*/
      268435472 && (p.$$scope = { dirty: q, ctx: c }), l.$set(p), q & /*options*/
      8192) {
        u = Mt(
          /*options*/
          c[13]
        );
        let C;
        for (C = 0; C < u.length; C += 1) {
          const m = Lt(c, u, C);
          h[C] ? h[C].p(m, q) : (h[C] = zt(m), h[C].c(), h[C].m(f, null));
        }
        for (; C < h.length; C += 1)
          h[C].d(1);
        h.length = u.length;
      }
      (!r || q & /*placeholder*/
      32) && Ne(
        f,
        "placeholder",
        /*placeholder*/
        c[5]
      ), q & /*value, options*/
      8193 && Ft(
        f,
        /*value*/
        c[0]
      ), /*isError*/
      c[12] ? d ? d.p(c, q) : (d = Vt(c), d.c(), d.m(t, null)) : d && (d.d(1), d = null);
    },
    i(c) {
      r || (_e(_), _e(l.$$.fragment, c), r = !0);
    },
    o(c) {
      ge(_), ge(l.$$.fragment, c), r = !1;
    },
    d(c) {
      c && (we(e), we(t)), _ && _.d(c), Je(l), ri(h, c), d && d.d(), s = !1, a();
    }
  };
}
function vi(n) {
  let e, t;
  return e = new ml({
    props: {
      visible: (
        /*visible*/
        n[3]
      ),
      elem_id: (
        /*elem_id*/
        n[1]
      ),
      elem_classes: (
        /*elem_classes*/
        n[2]
      ),
      padding: Ht,
      allow_overflow: !1,
      scale: (
        /*scale*/
        n[7]
      ),
      min_width: (
        /*min_width*/
        n[8]
      ),
      $$slots: { default: [ki] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      He(e.$$.fragment);
    },
    m(l, i) {
      Qe(e, l, i), t = !0;
    },
    p(l, [i]) {
      const f = {};
      i & /*visible*/
      8 && (f.visible = /*visible*/
      l[3]), i & /*elem_id*/
      2 && (f.elem_id = /*elem_id*/
      l[1]), i & /*elem_classes*/
      4 && (f.elem_classes = /*elem_classes*/
      l[2]), i & /*scale*/
      128 && (f.scale = /*scale*/
      l[7]), i & /*min_width*/
      256 && (f.min_width = /*min_width*/
      l[8]), i & /*$$scope, errMsg, isError, placeholder, value, options, show_label, label, gradio, loading_status*/
      268451441 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (_e(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ge(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Je(e, l);
    }
  };
}
const Ht = !0;
function yi(n, e, t) {
  var l = this && this.__awaiter || function(y, x, S, Z) {
    function N($) {
      return $ instanceof S ? $ : new S(function(fe) {
        fe($);
      });
    }
    return new (S || (S = Promise))(function($, fe) {
      function ke(Q) {
        try {
          ee(Z.next(Q));
        } catch (de) {
          fe(de);
        }
      }
      function ve(Q) {
        try {
          ee(Z.throw(Q));
        } catch (de) {
          fe(de);
        }
      }
      function ee(Q) {
        Q.done ? $(Q.value) : N(Q.value).then(ke, ve);
      }
      ee((Z = Z.apply(y, x || [])).next());
    });
  };
  let { elem_id: i = "" } = e, { elem_classes: f = [] } = e, { visible: o = !0 } = e, { value: r } = e, { value_is_output: s = !1 } = e, { choices: a } = e, { label: _ = "project" } = e, { placeholder: u = "Select a project" } = e, { show_label: h } = e, { scale: d = null } = e, { min_width: c = void 0 } = e, { loading_status: q } = e, { gradio: p } = e, { interactive: C } = e, m = !1, { errMsg: b = "Please select a project" } = e;
  function M() {
    return t(12, m = !r), m;
  }
  let z = /* @__PURE__ */ new Map();
  function w() {
    document.cookie.split(";").forEach((y) => {
      const [x, S] = y.trim().split("=");
      z.set(x, S);
    });
  }
  let L = [];
  function P() {
    return l(this, void 0, void 0, function* () {
      const y = z.get("appAccessKey"), x = z.get("clientName"), S = yield fetch("https://openapi.dp.tech/openapi/v1/open/user/project/list", {
        headers: { accessKey: y, "x-app-key": x }
      });
      if (S.ok) {
        const Z = yield S.json();
        t(13, L = Z.data.items.map((N) => [N.project_name, N.project_id]));
      }
    });
  }
  wi(() => {
    w(), P();
  });
  function ie() {
    p.dispatch("change"), s || p.dispatch("input");
  }
  const J = () => p.dispatch("clear_status", q);
  function W() {
    r = hi(this), t(0, r), t(13, L);
  }
  return n.$$set = (y) => {
    "elem_id" in y && t(1, i = y.elem_id), "elem_classes" in y && t(2, f = y.elem_classes), "visible" in y && t(3, o = y.visible), "value" in y && t(0, r = y.value), "value_is_output" in y && t(14, s = y.value_is_output), "choices" in y && t(15, a = y.choices), "label" in y && t(4, _ = y.label), "placeholder" in y && t(5, u = y.placeholder), "show_label" in y && t(6, h = y.show_label), "scale" in y && t(7, d = y.scale), "min_width" in y && t(8, c = y.min_width), "loading_status" in y && t(9, q = y.loading_status), "gradio" in y && t(10, p = y.gradio), "interactive" in y && t(16, C = y.interactive), "errMsg" in y && t(11, b = y.errMsg);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    1 && (M(), ie());
  }, [
    r,
    i,
    f,
    o,
    _,
    u,
    h,
    d,
    c,
    q,
    p,
    b,
    m,
    L,
    s,
    a,
    C,
    M,
    J,
    W
  ];
}
class qi extends fi {
  constructor(e) {
    super(), di(this, e, yi, vi, bi, {
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 0,
      value_is_output: 14,
      choices: 15,
      label: 4,
      placeholder: 5,
      show_label: 6,
      scale: 7,
      min_width: 8,
      loading_status: 9,
      gradio: 10,
      interactive: 16,
      errMsg: 11,
      validate: 17
    });
  }
  get validate() {
    return this.$$.ctx[17];
  }
}
export {
  qi as default
};
