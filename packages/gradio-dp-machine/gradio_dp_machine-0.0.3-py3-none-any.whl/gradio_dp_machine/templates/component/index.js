const {
  SvelteComponent: il,
  assign: fl,
  create_slot: ol,
  detach: sl,
  element: al,
  get_all_dirty_from_scope: rl,
  get_slot_changes: _l,
  get_spread_update: cl,
  init: ul,
  insert: dl,
  safe_not_equal: ml,
  set_dynamic_element_data: lt,
  set_style: I,
  toggle_class: Y,
  transition_in: Et,
  transition_out: Dt,
  update_slot_base: bl
} = window.__gradio__svelte__internal;
function hl(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), f = ol(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let s = [
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
  for (let o = 0; o < s.length; o += 1)
    r = fl(r, s[o]);
  return {
    c() {
      e = al(
        /*tag*/
        n[14]
      ), f && f.c(), lt(
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
    m(o, a) {
      dl(o, e, a), f && f.m(e, null), l = !0;
    },
    p(o, a) {
      f && f.p && (!l || a & /*$$scope*/
      131072) && bl(
        f,
        i,
        o,
        /*$$scope*/
        o[17],
        l ? _l(
          i,
          /*$$scope*/
          o[17],
          a,
          null
        ) : rl(
          /*$$scope*/
          o[17]
        ),
        null
      ), lt(
        /*tag*/
        o[14]
      )(e, r = cl(s, [
        (!l || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!l || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!l || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Y(
        e,
        "hidden",
        /*visible*/
        o[10] === !1
      ), Y(
        e,
        "padded",
        /*padding*/
        o[6]
      ), Y(
        e,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), Y(
        e,
        "border_contrast",
        /*border_mode*/
        o[5] === "contrast"
      ), Y(e, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), a & /*height*/
      1 && I(
        e,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), a & /*width*/
      2 && I(e, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), a & /*variant*/
      16 && I(
        e,
        "border-style",
        /*variant*/
        o[4]
      ), a & /*allow_overflow*/
      2048 && I(
        e,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && I(
        e,
        "flex-grow",
        /*scale*/
        o[12]
      ), a & /*min_width*/
      8192 && I(e, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      l || (Et(f, o), l = !0);
    },
    o(o) {
      Dt(f, o), l = !1;
    },
    d(o) {
      o && sl(e), f && f.d(o);
    }
  };
}
function gl(n) {
  let e, t = (
    /*tag*/
    n[14] && hl(n)
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
      e || (Et(t, l), e = !0);
    },
    o(l) {
      Dt(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function pl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: s = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: o = [] } = e, { variant: a = "solid" } = e, { border_mode: _ = "base" } = e, { padding: d = !0 } = e, { type: p = "normal" } = e, { test_id: m = void 0 } = e, { explicit_call: k = !1 } = e, { container: w = !0 } = e, { visible: q = !0 } = e, { allow_overflow: M = !0 } = e, { scale: u = null } = e, { min_width: c = 0 } = e, h = p === "fieldset" ? "fieldset" : "div";
  const L = (b) => {
    if (b !== void 0) {
      if (typeof b == "number")
        return b + "px";
      if (typeof b == "string")
        return b;
    }
  };
  return n.$$set = (b) => {
    "height" in b && t(0, f = b.height), "width" in b && t(1, s = b.width), "elem_id" in b && t(2, r = b.elem_id), "elem_classes" in b && t(3, o = b.elem_classes), "variant" in b && t(4, a = b.variant), "border_mode" in b && t(5, _ = b.border_mode), "padding" in b && t(6, d = b.padding), "type" in b && t(16, p = b.type), "test_id" in b && t(7, m = b.test_id), "explicit_call" in b && t(8, k = b.explicit_call), "container" in b && t(9, w = b.container), "visible" in b && t(10, q = b.visible), "allow_overflow" in b && t(11, M = b.allow_overflow), "scale" in b && t(12, u = b.scale), "min_width" in b && t(13, c = b.min_width), "$$scope" in b && t(17, i = b.$$scope);
  }, [
    f,
    s,
    r,
    o,
    a,
    _,
    d,
    m,
    k,
    w,
    q,
    M,
    u,
    c,
    h,
    L,
    p,
    i,
    l
  ];
}
class wl extends il {
  constructor(e) {
    super(), ul(this, e, pl, gl, ml, {
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
  SvelteComponent: kl,
  attr: vl,
  create_slot: yl,
  detach: ql,
  element: Cl,
  get_all_dirty_from_scope: Ml,
  get_slot_changes: Fl,
  init: Ll,
  insert: Sl,
  safe_not_equal: zl,
  transition_in: Nl,
  transition_out: Vl,
  update_slot_base: Il
} = window.__gradio__svelte__internal;
function Pl(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[1].default
  ), i = yl(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = Cl("div"), i && i.c(), vl(e, "class", "svelte-1hnfib2");
    },
    m(f, s) {
      Sl(f, e, s), i && i.m(e, null), t = !0;
    },
    p(f, [s]) {
      i && i.p && (!t || s & /*$$scope*/
      1) && Il(
        i,
        l,
        f,
        /*$$scope*/
        f[0],
        t ? Fl(
          l,
          /*$$scope*/
          f[0],
          s,
          null
        ) : Ml(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      t || (Nl(i, f), t = !0);
    },
    o(f) {
      Vl(i, f), t = !1;
    },
    d(f) {
      f && ql(e), i && i.d(f);
    }
  };
}
function Tl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  return n.$$set = (f) => {
    "$$scope" in f && t(0, i = f.$$scope);
  }, [i, l];
}
class jl extends kl {
  constructor(e) {
    super(), Ll(this, e, Tl, Pl, zl, {});
  }
}
const {
  SvelteComponent: Zl,
  attr: nt,
  check_outros: Al,
  create_component: Bl,
  create_slot: El,
  destroy_component: Dl,
  detach: Pe,
  element: Kl,
  empty: Rl,
  get_all_dirty_from_scope: Ul,
  get_slot_changes: Gl,
  group_outros: Ol,
  init: Xl,
  insert: Te,
  mount_component: Yl,
  safe_not_equal: Hl,
  set_data: Jl,
  space: Ql,
  text: Wl,
  toggle_class: re,
  transition_in: ke,
  transition_out: je,
  update_slot_base: xl
} = window.__gradio__svelte__internal;
function it(n) {
  let e, t;
  return e = new jl({
    props: {
      $$slots: { default: [$l] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Bl(e.$$.fragment);
    },
    m(l, i) {
      Yl(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (ke(e.$$.fragment, l), t = !0);
    },
    o(l) {
      je(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Dl(e, l);
    }
  };
}
function $l(n) {
  let e;
  return {
    c() {
      e = Wl(
        /*info*/
        n[1]
      );
    },
    m(t, l) {
      Te(t, e, l);
    },
    p(t, l) {
      l & /*info*/
      2 && Jl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Pe(e);
    }
  };
}
function en(n) {
  let e, t, l, i;
  const f = (
    /*#slots*/
    n[2].default
  ), s = El(
    f,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let r = (
    /*info*/
    n[1] && it(n)
  );
  return {
    c() {
      e = Kl("span"), s && s.c(), t = Ql(), r && r.c(), l = Rl(), nt(e, "data-testid", "block-info"), nt(e, "class", "svelte-22c38v"), re(e, "sr-only", !/*show_label*/
      n[0]), re(e, "hide", !/*show_label*/
      n[0]), re(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(o, a) {
      Te(o, e, a), s && s.m(e, null), Te(o, t, a), r && r.m(o, a), Te(o, l, a), i = !0;
    },
    p(o, [a]) {
      s && s.p && (!i || a & /*$$scope*/
      8) && xl(
        s,
        f,
        o,
        /*$$scope*/
        o[3],
        i ? Gl(
          f,
          /*$$scope*/
          o[3],
          a,
          null
        ) : Ul(
          /*$$scope*/
          o[3]
        ),
        null
      ), (!i || a & /*show_label*/
      1) && re(e, "sr-only", !/*show_label*/
      o[0]), (!i || a & /*show_label*/
      1) && re(e, "hide", !/*show_label*/
      o[0]), (!i || a & /*info*/
      2) && re(
        e,
        "has-info",
        /*info*/
        o[1] != null
      ), /*info*/
      o[1] ? r ? (r.p(o, a), a & /*info*/
      2 && ke(r, 1)) : (r = it(o), r.c(), ke(r, 1), r.m(l.parentNode, l)) : r && (Ol(), je(r, 1, 1, () => {
        r = null;
      }), Al());
    },
    i(o) {
      i || (ke(s, o), ke(r), i = !0);
    },
    o(o) {
      je(s, o), je(r), i = !1;
    },
    d(o) {
      o && (Pe(e), Pe(t), Pe(l)), s && s.d(o), r && r.d(o);
    }
  };
}
function tn(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_label: f = !0 } = e, { info: s = void 0 } = e;
  return n.$$set = (r) => {
    "show_label" in r && t(0, f = r.show_label), "info" in r && t(1, s = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [f, s, l, i];
}
class ln extends Zl {
  constructor(e) {
    super(), Xl(this, e, tn, en, Hl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: nn,
  append: Oe,
  attr: x,
  bubble: fn,
  create_component: on,
  destroy_component: sn,
  detach: Kt,
  element: Xe,
  init: an,
  insert: Rt,
  listen: rn,
  mount_component: _n,
  safe_not_equal: cn,
  set_data: un,
  set_style: _e,
  space: dn,
  text: mn,
  toggle_class: V,
  transition_in: bn,
  transition_out: hn
} = window.__gradio__svelte__internal;
function ft(n) {
  let e, t;
  return {
    c() {
      e = Xe("span"), t = mn(
        /*label*/
        n[1]
      ), x(e, "class", "svelte-1lrphxw");
    },
    m(l, i) {
      Rt(l, e, i), Oe(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && un(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && Kt(e);
    }
  };
}
function gn(n) {
  let e, t, l, i, f, s, r, o = (
    /*show_label*/
    n[2] && ft(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Xe("button"), o && o.c(), t = dn(), l = Xe("div"), on(i.$$.fragment), x(l, "class", "svelte-1lrphxw"), V(
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
      n[7], x(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), x(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), x(
        e,
        "title",
        /*label*/
        n[1]
      ), x(e, "class", "svelte-1lrphxw"), V(
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
      ), _e(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), _e(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), _e(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(a, _) {
      Rt(a, e, _), o && o.m(e, null), Oe(e, t), Oe(e, l), _n(i, l, null), f = !0, s || (r = rn(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), s = !0);
    },
    p(a, [_]) {
      /*show_label*/
      a[2] ? o ? o.p(a, _) : (o = ft(a), o.c(), o.m(e, t)) : o && (o.d(1), o = null), (!f || _ & /*size*/
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
      2) && x(
        e,
        "aria-label",
        /*label*/
        a[1]
      ), (!f || _ & /*hasPopup*/
      256) && x(
        e,
        "aria-haspopup",
        /*hasPopup*/
        a[8]
      ), (!f || _ & /*label*/
      2) && x(
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
      4224 && _e(e, "color", !/*disabled*/
      a[7] && /*_color*/
      a[12] ? (
        /*_color*/
        a[12]
      ) : "var(--block-label-text-color)"), _ & /*disabled, background*/
      1152 && _e(e, "--bg-color", /*disabled*/
      a[7] ? "auto" : (
        /*background*/
        a[10]
      )), _ & /*offset*/
      2048 && _e(
        e,
        "margin-left",
        /*offset*/
        a[11] + "px"
      );
    },
    i(a) {
      f || (bn(i.$$.fragment, a), f = !0);
    },
    o(a) {
      hn(i.$$.fragment, a), f = !1;
    },
    d(a) {
      a && Kt(e), o && o.d(), sn(i), s = !1, r();
    }
  };
}
function pn(n, e, t) {
  let l, { Icon: i } = e, { label: f = "" } = e, { show_label: s = !1 } = e, { pending: r = !1 } = e, { size: o = "small" } = e, { padded: a = !0 } = e, { highlight: _ = !1 } = e, { disabled: d = !1 } = e, { hasPopup: p = !1 } = e, { color: m = "var(--block-label-text-color)" } = e, { transparent: k = !1 } = e, { background: w = "var(--background-fill-primary)" } = e, { offset: q = 0 } = e;
  function M(u) {
    fn.call(this, n, u);
  }
  return n.$$set = (u) => {
    "Icon" in u && t(0, i = u.Icon), "label" in u && t(1, f = u.label), "show_label" in u && t(2, s = u.show_label), "pending" in u && t(3, r = u.pending), "size" in u && t(4, o = u.size), "padded" in u && t(5, a = u.padded), "highlight" in u && t(6, _ = u.highlight), "disabled" in u && t(7, d = u.disabled), "hasPopup" in u && t(8, p = u.hasPopup), "color" in u && t(13, m = u.color), "transparent" in u && t(9, k = u.transparent), "background" in u && t(10, w = u.background), "offset" in u && t(11, q = u.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, l = _ ? "var(--color-accent)" : m);
  }, [
    i,
    f,
    s,
    r,
    o,
    a,
    _,
    d,
    p,
    k,
    w,
    q,
    l,
    m,
    M
  ];
}
class wn extends nn {
  constructor(e) {
    super(), an(this, e, pn, gn, cn, {
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
  SvelteComponent: kn,
  append: Re,
  attr: K,
  detach: vn,
  init: yn,
  insert: qn,
  noop: Ue,
  safe_not_equal: Cn,
  set_style: H,
  svg_element: Le
} = window.__gradio__svelte__internal;
function Mn(n) {
  let e, t, l, i;
  return {
    c() {
      e = Le("svg"), t = Le("g"), l = Le("path"), i = Le("path"), K(l, "d", "M18,6L6.087,17.913"), H(l, "fill", "none"), H(l, "fill-rule", "nonzero"), H(l, "stroke-width", "2px"), K(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), K(i, "d", "M4.364,4.364L19.636,19.636"), H(i, "fill", "none"), H(i, "fill-rule", "nonzero"), H(i, "stroke-width", "2px"), K(e, "width", "100%"), K(e, "height", "100%"), K(e, "viewBox", "0 0 24 24"), K(e, "version", "1.1"), K(e, "xmlns", "http://www.w3.org/2000/svg"), K(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), K(e, "xml:space", "preserve"), K(e, "stroke", "currentColor"), H(e, "fill-rule", "evenodd"), H(e, "clip-rule", "evenodd"), H(e, "stroke-linecap", "round"), H(e, "stroke-linejoin", "round");
    },
    m(f, s) {
      qn(f, e, s), Re(e, t), Re(t, l), Re(e, i);
    },
    p: Ue,
    i: Ue,
    o: Ue,
    d(f) {
      f && vn(e);
    }
  };
}
class Fn extends kn {
  constructor(e) {
    super(), yn(this, e, null, Mn, Cn, {});
  }
}
const Ln = [
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
], ot = {
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
Ln.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: ot[e][t],
      secondary: ot[e][l]
    }
  }),
  {}
);
function ue(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function Ze() {
}
function Sn(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const Ut = typeof window < "u";
let st = Ut ? () => window.performance.now() : () => Date.now(), Gt = Ut ? (n) => requestAnimationFrame(n) : Ze;
const me = /* @__PURE__ */ new Set();
function Ot(n) {
  me.forEach((e) => {
    e.c(n) || (me.delete(e), e.f());
  }), me.size !== 0 && Gt(Ot);
}
function zn(n) {
  let e;
  return me.size === 0 && Gt(Ot), {
    promise: new Promise((t) => {
      me.add(e = { c: n, f: t });
    }),
    abort() {
      me.delete(e);
    }
  };
}
const ce = [];
function Nn(n, e = Ze) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(r) {
    if (Sn(n, r) && (n = r, t)) {
      const o = !ce.length;
      for (const a of l)
        a[1](), ce.push(a, n);
      if (o) {
        for (let a = 0; a < ce.length; a += 2)
          ce[a][0](ce[a + 1]);
        ce.length = 0;
      }
    }
  }
  function f(r) {
    i(r(n));
  }
  function s(r, o = Ze) {
    const a = [r, o];
    return l.add(a), l.size === 1 && (t = e(i, f) || Ze), r(n), () => {
      l.delete(a), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: s };
}
function at(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function Ye(n, e, t, l) {
  if (typeof t == "number" || at(t)) {
    const i = l - t, f = (t - e) / (n.dt || 1 / 60), s = n.opts.stiffness * i, r = n.opts.damping * f, o = (s - r) * n.inv_mass, a = (f + o) * n.dt;
    return Math.abs(a) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, at(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => Ye(n, e[f], t[f], l[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = Ye(n, e[f], t[f], l[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function rt(n, e = {}) {
  const t = Nn(n), { stiffness: l = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let s, r, o, a = n, _ = n, d = 1, p = 0, m = !1;
  function k(q, M = {}) {
    _ = q;
    const u = o = {};
    return n == null || M.hard || w.stiffness >= 1 && w.damping >= 1 ? (m = !0, s = st(), a = q, t.set(n = _), Promise.resolve()) : (M.soft && (p = 1 / ((M.soft === !0 ? 0.5 : +M.soft) * 60), d = 0), r || (s = st(), m = !1, r = zn((c) => {
      if (m)
        return m = !1, r = null, !1;
      d = Math.min(d + p, 1);
      const h = {
        inv_mass: d,
        opts: w,
        settled: !0,
        dt: (c - s) * 60 / 1e3
      }, L = Ye(h, a, n, _);
      return s = c, a = n, t.set(n = L), h.settled && (r = null), !h.settled;
    })), new Promise((c) => {
      r.promise.then(() => {
        u === o && c();
      });
    }));
  }
  const w = {
    set: k,
    update: (q, M) => k(q(_, n), M),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: f
  };
  return w;
}
const {
  SvelteComponent: Vn,
  append: R,
  attr: F,
  component_subscribe: _t,
  detach: In,
  element: Pn,
  init: Tn,
  insert: jn,
  noop: ct,
  safe_not_equal: Zn,
  set_style: Se,
  svg_element: U,
  toggle_class: ut
} = window.__gradio__svelte__internal, { onMount: An } = window.__gradio__svelte__internal;
function Bn(n) {
  let e, t, l, i, f, s, r, o, a, _, d, p;
  return {
    c() {
      e = Pn("div"), t = U("svg"), l = U("g"), i = U("path"), f = U("path"), s = U("path"), r = U("path"), o = U("g"), a = U("path"), _ = U("path"), d = U("path"), p = U("path"), F(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), F(i, "fill", "#FF7C00"), F(i, "fill-opacity", "0.4"), F(i, "class", "svelte-43sxxs"), F(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), F(f, "fill", "#FF7C00"), F(f, "class", "svelte-43sxxs"), F(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), F(s, "fill", "#FF7C00"), F(s, "fill-opacity", "0.4"), F(s, "class", "svelte-43sxxs"), F(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), F(r, "fill", "#FF7C00"), F(r, "class", "svelte-43sxxs"), Se(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), F(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), F(a, "fill", "#FF7C00"), F(a, "fill-opacity", "0.4"), F(a, "class", "svelte-43sxxs"), F(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), F(_, "fill", "#FF7C00"), F(_, "class", "svelte-43sxxs"), F(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), F(d, "fill", "#FF7C00"), F(d, "fill-opacity", "0.4"), F(d, "class", "svelte-43sxxs"), F(p, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), F(p, "fill", "#FF7C00"), F(p, "class", "svelte-43sxxs"), Se(o, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), F(t, "viewBox", "-1200 -1200 3000 3000"), F(t, "fill", "none"), F(t, "xmlns", "http://www.w3.org/2000/svg"), F(t, "class", "svelte-43sxxs"), F(e, "class", "svelte-43sxxs"), ut(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(m, k) {
      jn(m, e, k), R(e, t), R(t, l), R(l, i), R(l, f), R(l, s), R(l, r), R(t, o), R(o, a), R(o, _), R(o, d), R(o, p);
    },
    p(m, [k]) {
      k & /*$top*/
      2 && Se(l, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), k & /*$bottom*/
      4 && Se(o, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), k & /*margin*/
      1 && ut(
        e,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: ct,
    o: ct,
    d(m) {
      m && In(e);
    }
  };
}
function En(n, e, t) {
  let l, i;
  var f = this && this.__awaiter || function(m, k, w, q) {
    function M(u) {
      return u instanceof w ? u : new w(function(c) {
        c(u);
      });
    }
    return new (w || (w = Promise))(function(u, c) {
      function h(S) {
        try {
          b(q.next(S));
        } catch (P) {
          c(P);
        }
      }
      function L(S) {
        try {
          b(q.throw(S));
        } catch (P) {
          c(P);
        }
      }
      function b(S) {
        S.done ? u(S.value) : M(S.value).then(h, L);
      }
      b((q = q.apply(m, k || [])).next());
    });
  };
  let { margin: s = !0 } = e;
  const r = rt([0, 0]);
  _t(n, r, (m) => t(1, l = m));
  const o = rt([0, 0]);
  _t(n, o, (m) => t(2, i = m));
  let a;
  function _() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), o.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), o.set([125, -140])]), yield Promise.all([r.set([-125, 0]), o.set([125, -0])]), yield Promise.all([r.set([125, 0]), o.set([-125, 0])]);
    });
  }
  function d() {
    return f(this, void 0, void 0, function* () {
      yield _(), a || d();
    });
  }
  function p() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), o.set([-125, 0])]), d();
    });
  }
  return An(() => (p(), () => a = !0)), n.$$set = (m) => {
    "margin" in m && t(0, s = m.margin);
  }, [s, l, i, r, o];
}
class Dn extends Vn {
  constructor(e) {
    super(), Tn(this, e, En, Bn, Zn, { margin: 0 });
  }
}
const {
  SvelteComponent: Kn,
  append: se,
  attr: O,
  binding_callbacks: dt,
  check_outros: He,
  create_component: Xt,
  create_slot: Yt,
  destroy_component: Ht,
  destroy_each: Jt,
  detach: v,
  element: J,
  empty: ge,
  ensure_array_like: Be,
  get_all_dirty_from_scope: Qt,
  get_slot_changes: Wt,
  group_outros: Je,
  init: Rn,
  insert: y,
  mount_component: xt,
  noop: Qe,
  safe_not_equal: Un,
  set_data: B,
  set_style: ie,
  space: A,
  text: z,
  toggle_class: Z,
  transition_in: G,
  transition_out: Q,
  update_slot_base: $t
} = window.__gradio__svelte__internal, { tick: Gn } = window.__gradio__svelte__internal, { onDestroy: On } = window.__gradio__svelte__internal, { createEventDispatcher: Xn } = window.__gradio__svelte__internal, Yn = (n) => ({}), mt = (n) => ({}), Hn = (n) => ({}), bt = (n) => ({});
function ht(n, e, t) {
  const l = n.slice();
  return l[41] = e[t], l[43] = t, l;
}
function gt(n, e, t) {
  const l = n.slice();
  return l[41] = e[t], l;
}
function Jn(n) {
  let e, t, l, i, f = (
    /*i18n*/
    n[1]("common.error") + ""
  ), s, r, o;
  t = new wn({
    props: {
      Icon: Fn,
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
  ), _ = Yt(
    a,
    n,
    /*$$scope*/
    n[29],
    mt
  );
  return {
    c() {
      e = J("div"), Xt(t.$$.fragment), l = A(), i = J("span"), s = z(f), r = A(), _ && _.c(), O(e, "class", "clear-status svelte-16nch4a"), O(i, "class", "error svelte-16nch4a");
    },
    m(d, p) {
      y(d, e, p), xt(t, e, null), y(d, l, p), y(d, i, p), se(i, s), y(d, r, p), _ && _.m(d, p), o = !0;
    },
    p(d, p) {
      const m = {};
      p[0] & /*i18n*/
      2 && (m.label = /*i18n*/
      d[1]("common.clear")), t.$set(m), (!o || p[0] & /*i18n*/
      2) && f !== (f = /*i18n*/
      d[1]("common.error") + "") && B(s, f), _ && _.p && (!o || p[0] & /*$$scope*/
      536870912) && $t(
        _,
        a,
        d,
        /*$$scope*/
        d[29],
        o ? Wt(
          a,
          /*$$scope*/
          d[29],
          p,
          Yn
        ) : Qt(
          /*$$scope*/
          d[29]
        ),
        mt
      );
    },
    i(d) {
      o || (G(t.$$.fragment, d), G(_, d), o = !0);
    },
    o(d) {
      Q(t.$$.fragment, d), Q(_, d), o = !1;
    },
    d(d) {
      d && (v(e), v(l), v(i), v(r)), Ht(t), _ && _.d(d);
    }
  };
}
function Qn(n) {
  let e, t, l, i, f, s, r, o, a, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && pt(n)
  );
  function d(c, h) {
    if (
      /*progress*/
      c[7]
    ) return $n;
    if (
      /*queue_position*/
      c[2] !== null && /*queue_size*/
      c[3] !== void 0 && /*queue_position*/
      c[2] >= 0
    ) return xn;
    if (
      /*queue_position*/
      c[2] === 0
    ) return Wn;
  }
  let p = d(n), m = p && p(n), k = (
    /*timer*/
    n[5] && vt(n)
  );
  const w = [ni, li], q = [];
  function M(c, h) {
    return (
      /*last_progress_level*/
      c[15] != null ? 0 : (
        /*show_progress*/
        c[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = M(n)) && (s = q[f] = w[f](n));
  let u = !/*timer*/
  n[5] && St(n);
  return {
    c() {
      _ && _.c(), e = A(), t = J("div"), m && m.c(), l = A(), k && k.c(), i = A(), s && s.c(), r = A(), u && u.c(), o = ge(), O(t, "class", "progress-text svelte-16nch4a"), Z(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), Z(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(c, h) {
      _ && _.m(c, h), y(c, e, h), y(c, t, h), m && m.m(t, null), se(t, l), k && k.m(t, null), y(c, i, h), ~f && q[f].m(c, h), y(c, r, h), u && u.m(c, h), y(c, o, h), a = !0;
    },
    p(c, h) {
      /*variant*/
      c[8] === "default" && /*show_eta_bar*/
      c[18] && /*show_progress*/
      c[6] === "full" ? _ ? _.p(c, h) : (_ = pt(c), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), p === (p = d(c)) && m ? m.p(c, h) : (m && m.d(1), m = p && p(c), m && (m.c(), m.m(t, l))), /*timer*/
      c[5] ? k ? k.p(c, h) : (k = vt(c), k.c(), k.m(t, null)) : k && (k.d(1), k = null), (!a || h[0] & /*variant*/
      256) && Z(
        t,
        "meta-text-center",
        /*variant*/
        c[8] === "center"
      ), (!a || h[0] & /*variant*/
      256) && Z(
        t,
        "meta-text",
        /*variant*/
        c[8] === "default"
      );
      let L = f;
      f = M(c), f === L ? ~f && q[f].p(c, h) : (s && (Je(), Q(q[L], 1, 1, () => {
        q[L] = null;
      }), He()), ~f ? (s = q[f], s ? s.p(c, h) : (s = q[f] = w[f](c), s.c()), G(s, 1), s.m(r.parentNode, r)) : s = null), /*timer*/
      c[5] ? u && (Je(), Q(u, 1, 1, () => {
        u = null;
      }), He()) : u ? (u.p(c, h), h[0] & /*timer*/
      32 && G(u, 1)) : (u = St(c), u.c(), G(u, 1), u.m(o.parentNode, o));
    },
    i(c) {
      a || (G(s), G(u), a = !0);
    },
    o(c) {
      Q(s), Q(u), a = !1;
    },
    d(c) {
      c && (v(e), v(t), v(i), v(r), v(o)), _ && _.d(c), m && m.d(), k && k.d(), ~f && q[f].d(c), u && u.d(c);
    }
  };
}
function pt(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = J("div"), O(e, "class", "eta-bar svelte-16nch4a"), ie(e, "transform", t);
    },
    m(l, i) {
      y(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && ie(e, "transform", t);
    },
    d(l) {
      l && v(e);
    }
  };
}
function Wn(n) {
  let e;
  return {
    c() {
      e = z("processing |");
    },
    m(t, l) {
      y(t, e, l);
    },
    p: Qe,
    d(t) {
      t && v(e);
    }
  };
}
function xn(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, f, s;
  return {
    c() {
      e = z("queue: "), l = z(t), i = z("/"), f = z(
        /*queue_size*/
        n[3]
      ), s = z(" |");
    },
    m(r, o) {
      y(r, e, o), y(r, l, o), y(r, i, o), y(r, f, o), y(r, s, o);
    },
    p(r, o) {
      o[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && B(l, t), o[0] & /*queue_size*/
      8 && B(
        f,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (v(e), v(l), v(i), v(f), v(s));
    }
  };
}
function $n(n) {
  let e, t = Be(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = kt(gt(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = ge();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = Be(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = gt(i, t, s);
          l[s] ? l[s].p(r, f) : (l[s] = kt(r), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && v(e), Jt(l, i);
    }
  };
}
function wt(n) {
  let e, t = (
    /*p*/
    n[41].unit + ""
  ), l, i, f = " ", s;
  function r(_, d) {
    return (
      /*p*/
      _[41].length != null ? ti : ei
    );
  }
  let o = r(n), a = o(n);
  return {
    c() {
      a.c(), e = A(), l = z(t), i = z(" | "), s = z(f);
    },
    m(_, d) {
      a.m(_, d), y(_, e, d), y(_, l, d), y(_, i, d), y(_, s, d);
    },
    p(_, d) {
      o === (o = r(_)) && a ? a.p(_, d) : (a.d(1), a = o(_), a && (a.c(), a.m(e.parentNode, e))), d[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[41].unit + "") && B(l, t);
    },
    d(_) {
      _ && (v(e), v(l), v(i), v(s)), a.d(_);
    }
  };
}
function ei(n) {
  let e = ue(
    /*p*/
    n[41].index || 0
  ) + "", t;
  return {
    c() {
      t = z(e);
    },
    m(l, i) {
      y(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = ue(
        /*p*/
        l[41].index || 0
      ) + "") && B(t, e);
    },
    d(l) {
      l && v(t);
    }
  };
}
function ti(n) {
  let e = ue(
    /*p*/
    n[41].index || 0
  ) + "", t, l, i = ue(
    /*p*/
    n[41].length
  ) + "", f;
  return {
    c() {
      t = z(e), l = z("/"), f = z(i);
    },
    m(s, r) {
      y(s, t, r), y(s, l, r), y(s, f, r);
    },
    p(s, r) {
      r[0] & /*progress*/
      128 && e !== (e = ue(
        /*p*/
        s[41].index || 0
      ) + "") && B(t, e), r[0] & /*progress*/
      128 && i !== (i = ue(
        /*p*/
        s[41].length
      ) + "") && B(f, i);
    },
    d(s) {
      s && (v(t), v(l), v(f));
    }
  };
}
function kt(n) {
  let e, t = (
    /*p*/
    n[41].index != null && wt(n)
  );
  return {
    c() {
      t && t.c(), e = ge();
    },
    m(l, i) {
      t && t.m(l, i), y(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[41].index != null ? t ? t.p(l, i) : (t = wt(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && v(e), t && t.d(l);
    }
  };
}
function vt(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = z(
        /*formatted_timer*/
        n[20]
      ), l = z(t), i = z("s");
    },
    m(f, s) {
      y(f, e, s), y(f, l, s), y(f, i, s);
    },
    p(f, s) {
      s[0] & /*formatted_timer*/
      1048576 && B(
        e,
        /*formatted_timer*/
        f[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && B(l, t);
    },
    d(f) {
      f && (v(e), v(l), v(i));
    }
  };
}
function li(n) {
  let e, t;
  return e = new Dn({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Xt(e.$$.fragment);
    },
    m(l, i) {
      xt(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      l[8] === "default"), e.$set(f);
    },
    i(l) {
      t || (G(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Q(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Ht(e, l);
    }
  };
}
function ni(n) {
  let e, t, l, i, f, s = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && yt(n)
  );
  return {
    c() {
      e = J("div"), t = J("div"), r && r.c(), l = A(), i = J("div"), f = J("div"), O(t, "class", "progress-level-inner svelte-16nch4a"), O(f, "class", "progress-bar svelte-16nch4a"), ie(f, "width", s), O(i, "class", "progress-bar-wrap svelte-16nch4a"), O(e, "class", "progress-level svelte-16nch4a");
    },
    m(o, a) {
      y(o, e, a), se(e, t), r && r.m(t, null), se(e, l), se(e, i), se(i, f), n[31](f);
    },
    p(o, a) {
      /*progress*/
      o[7] != null ? r ? r.p(o, a) : (r = yt(o), r.c(), r.m(t, null)) : r && (r.d(1), r = null), a[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      o[15] * 100}%`) && ie(f, "width", s);
    },
    i: Qe,
    o: Qe,
    d(o) {
      o && v(e), r && r.d(), n[31](null);
    }
  };
}
function yt(n) {
  let e, t = Be(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Lt(ht(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = ge();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = Be(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = ht(i, t, s);
          l[s] ? l[s].p(r, f) : (l[s] = Lt(r), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && v(e), Jt(l, i);
    }
  };
}
function qt(n) {
  let e, t, l, i, f = (
    /*i*/
    n[43] !== 0 && ii()
  ), s = (
    /*p*/
    n[41].desc != null && Ct(n)
  ), r = (
    /*p*/
    n[41].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null && Mt()
  ), o = (
    /*progress_level*/
    n[14] != null && Ft(n)
  );
  return {
    c() {
      f && f.c(), e = A(), s && s.c(), t = A(), r && r.c(), l = A(), o && o.c(), i = ge();
    },
    m(a, _) {
      f && f.m(a, _), y(a, e, _), s && s.m(a, _), y(a, t, _), r && r.m(a, _), y(a, l, _), o && o.m(a, _), y(a, i, _);
    },
    p(a, _) {
      /*p*/
      a[41].desc != null ? s ? s.p(a, _) : (s = Ct(a), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      a[41].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[43]
      ] != null ? r || (r = Mt(), r.c(), r.m(l.parentNode, l)) : r && (r.d(1), r = null), /*progress_level*/
      a[14] != null ? o ? o.p(a, _) : (o = Ft(a), o.c(), o.m(i.parentNode, i)) : o && (o.d(1), o = null);
    },
    d(a) {
      a && (v(e), v(t), v(l), v(i)), f && f.d(a), s && s.d(a), r && r.d(a), o && o.d(a);
    }
  };
}
function ii(n) {
  let e;
  return {
    c() {
      e = z(" /");
    },
    m(t, l) {
      y(t, e, l);
    },
    d(t) {
      t && v(e);
    }
  };
}
function Ct(n) {
  let e = (
    /*p*/
    n[41].desc + ""
  ), t;
  return {
    c() {
      t = z(e);
    },
    m(l, i) {
      y(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[41].desc + "") && B(t, e);
    },
    d(l) {
      l && v(t);
    }
  };
}
function Mt(n) {
  let e;
  return {
    c() {
      e = z("-");
    },
    m(t, l) {
      y(t, e, l);
    },
    d(t) {
      t && v(e);
    }
  };
}
function Ft(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[43]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = z(e), l = z("%");
    },
    m(i, f) {
      y(i, t, f), y(i, l, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && B(t, e);
    },
    d(i) {
      i && (v(t), v(l));
    }
  };
}
function Lt(n) {
  let e, t = (
    /*p*/
    (n[41].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null) && qt(n)
  );
  return {
    c() {
      t && t.c(), e = ge();
    },
    m(l, i) {
      t && t.m(l, i), y(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[41].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[43]
      ] != null ? t ? t.p(l, i) : (t = qt(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && v(e), t && t.d(l);
    }
  };
}
function St(n) {
  let e, t, l, i;
  const f = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), s = Yt(
    f,
    n,
    /*$$scope*/
    n[29],
    bt
  );
  return {
    c() {
      e = J("p"), t = z(
        /*loading_text*/
        n[9]
      ), l = A(), s && s.c(), O(e, "class", "loading svelte-16nch4a");
    },
    m(r, o) {
      y(r, e, o), se(e, t), y(r, l, o), s && s.m(r, o), i = !0;
    },
    p(r, o) {
      (!i || o[0] & /*loading_text*/
      512) && B(
        t,
        /*loading_text*/
        r[9]
      ), s && s.p && (!i || o[0] & /*$$scope*/
      536870912) && $t(
        s,
        f,
        r,
        /*$$scope*/
        r[29],
        i ? Wt(
          f,
          /*$$scope*/
          r[29],
          o,
          Hn
        ) : Qt(
          /*$$scope*/
          r[29]
        ),
        bt
      );
    },
    i(r) {
      i || (G(s, r), i = !0);
    },
    o(r) {
      Q(s, r), i = !1;
    },
    d(r) {
      r && (v(e), v(l)), s && s.d(r);
    }
  };
}
function fi(n) {
  let e, t, l, i, f;
  const s = [Qn, Jn], r = [];
  function o(a, _) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = o(n)) && (l = r[t] = s[t](n)), {
    c() {
      e = J("div"), l && l.c(), O(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-16nch4a"), Z(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), Z(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), Z(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), Z(
        e,
        "border",
        /*border*/
        n[12]
      ), ie(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), ie(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, _) {
      y(a, e, _), ~t && r[t].m(e, null), n[33](e), f = !0;
    },
    p(a, _) {
      let d = t;
      t = o(a), t === d ? ~t && r[t].p(a, _) : (l && (Je(), Q(r[d], 1, 1, () => {
        r[d] = null;
      }), He()), ~t ? (l = r[t], l ? l.p(a, _) : (l = r[t] = s[t](a), l.c()), G(l, 1), l.m(e, null)) : l = null), (!f || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-16nch4a")) && O(e, "class", i), (!f || _[0] & /*variant, show_progress, status, show_progress*/
      336) && Z(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!f || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && Z(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!f || _[0] & /*variant, show_progress, status*/
      336) && Z(
        e,
        "generating",
        /*status*/
        a[4] === "generating"
      ), (!f || _[0] & /*variant, show_progress, border*/
      4416) && Z(
        e,
        "border",
        /*border*/
        a[12]
      ), _[0] & /*absolute*/
      1024 && ie(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && ie(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      f || (G(l), f = !0);
    },
    o(a) {
      Q(l), f = !1;
    },
    d(a) {
      a && v(e), ~t && r[t].d(), n[33](null);
    }
  };
}
var oi = function(n, e, t, l) {
  function i(f) {
    return f instanceof t ? f : new t(function(s) {
      s(f);
    });
  }
  return new (t || (t = Promise))(function(f, s) {
    function r(_) {
      try {
        a(l.next(_));
      } catch (d) {
        s(d);
      }
    }
    function o(_) {
      try {
        a(l.throw(_));
      } catch (d) {
        s(d);
      }
    }
    function a(_) {
      _.done ? f(_.value) : i(_.value).then(r, o);
    }
    a((l = l.apply(n, e || [])).next());
  });
};
let ze = [], Ge = !1;
function si(n) {
  return oi(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (ze.push(e), !Ge) Ge = !0;
      else return;
      yield Gn(), requestAnimationFrame(() => {
        let l = [0, 0];
        for (let i = 0; i < ze.length; i++) {
          const s = ze[i].getBoundingClientRect();
          (i === 0 || s.top + window.scrollY <= l[0]) && (l[0] = s.top + window.scrollY, l[1] = i);
        }
        window.scrollTo({ top: l[0] - 20, behavior: "smooth" }), Ge = !1, ze = [];
      });
    }
  });
}
function ai(n, e, t) {
  let l, { $$slots: i = {}, $$scope: f } = e;
  this && this.__awaiter;
  const s = Xn();
  let { i18n: r } = e, { eta: o = null } = e, { queue_position: a } = e, { queue_size: _ } = e, { status: d } = e, { scroll_to_output: p = !1 } = e, { timer: m = !0 } = e, { show_progress: k = "full" } = e, { message: w = null } = e, { progress: q = null } = e, { variant: M = "default" } = e, { loading_text: u = "Loading..." } = e, { absolute: c = !0 } = e, { translucent: h = !1 } = e, { border: L = !1 } = e, { autoscroll: b } = e, S, P = !1, fe = 0, X = 0, ee = null, te = null, ye = 0, C = null, E, N = null, W = !0;
  const pe = () => {
    t(0, o = t(27, ee = t(19, le = null))), t(25, fe = performance.now()), t(26, X = 0), P = !0, D();
  };
  function D() {
    requestAnimationFrame(() => {
      t(26, X = (performance.now() - fe) / 1e3), P && D();
    });
  }
  function T() {
    t(26, X = 0), t(0, o = t(27, ee = t(19, le = null))), P && (P = !1);
  }
  On(() => {
    P && T();
  });
  let le = null;
  function qe(g) {
    dt[g ? "unshift" : "push"](() => {
      N = g, t(16, N), t(7, q), t(14, C), t(15, E);
    });
  }
  const ne = () => {
    s("clear_status");
  };
  function j(g) {
    dt[g ? "unshift" : "push"](() => {
      S = g, t(13, S);
    });
  }
  return n.$$set = (g) => {
    "i18n" in g && t(1, r = g.i18n), "eta" in g && t(0, o = g.eta), "queue_position" in g && t(2, a = g.queue_position), "queue_size" in g && t(3, _ = g.queue_size), "status" in g && t(4, d = g.status), "scroll_to_output" in g && t(22, p = g.scroll_to_output), "timer" in g && t(5, m = g.timer), "show_progress" in g && t(6, k = g.show_progress), "message" in g && t(23, w = g.message), "progress" in g && t(7, q = g.progress), "variant" in g && t(8, M = g.variant), "loading_text" in g && t(9, u = g.loading_text), "absolute" in g && t(10, c = g.absolute), "translucent" in g && t(11, h = g.translucent), "border" in g && t(12, L = g.border), "autoscroll" in g && t(24, b = g.autoscroll), "$$scope" in g && t(29, f = g.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (o === null && t(0, o = ee), o != null && ee !== o && (t(28, te = (performance.now() - fe) / 1e3 + o), t(19, le = te.toFixed(1)), t(27, ee = o))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, ye = te === null || te <= 0 || !X ? null : Math.min(X / te, 1)), n.$$.dirty[0] & /*progress*/
    128 && q != null && t(18, W = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (q != null ? t(14, C = q.map((g) => {
      if (g.index != null && g.length != null)
        return g.index / g.length;
      if (g.progress != null)
        return g.progress;
    })) : t(14, C = null), C ? (t(15, E = C[C.length - 1]), N && (E === 0 ? t(16, N.style.transition = "0", N) : t(16, N.style.transition = "150ms", N))) : t(15, E = void 0)), n.$$.dirty[0] & /*status*/
    16 && (d === "pending" ? pe() : T()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && S && p && (d === "pending" || d === "complete") && si(S, b), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, l = X.toFixed(1));
  }, [
    o,
    r,
    a,
    _,
    d,
    m,
    k,
    q,
    M,
    u,
    c,
    h,
    L,
    S,
    C,
    E,
    N,
    ye,
    W,
    le,
    l,
    s,
    p,
    w,
    b,
    fe,
    X,
    ee,
    te,
    f,
    i,
    qe,
    ne,
    j
  ];
}
class ri extends Kn {
  constructor(e) {
    super(), Rn(
      this,
      e,
      ai,
      fi,
      Un,
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
  SvelteComponent: _i,
  add_render_callback: zt,
  append: $,
  assign: ci,
  attr: Ae,
  check_outros: ui,
  create_component: xe,
  destroy_component: $e,
  destroy_each: Nt,
  detach: be,
  element: ae,
  ensure_array_like: Ne,
  get_spread_object: di,
  get_spread_update: mi,
  group_outros: bi,
  init: hi,
  insert: he,
  listen: Vt,
  mount_component: et,
  noop: gi,
  run_all: pi,
  safe_not_equal: wi,
  select_option: Ve,
  select_value: It,
  set_data: tt,
  set_input_value: We,
  space: Ie,
  text: Ee,
  transition_in: de,
  transition_out: ve
} = window.__gradio__svelte__internal, { onMount: ki } = window.__gradio__svelte__internal;
function Pt(n, e, t) {
  const l = n.slice();
  return l[27] = e[t], l;
}
function Tt(n, e, t) {
  const l = n.slice();
  return l[27] = e[t], l;
}
function jt(n) {
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
    i = ci(i, l[f]);
  return e = new ri({ props: i }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    n[19]
  ), {
    c() {
      xe(e.$$.fragment);
    },
    m(f, s) {
      et(e, f, s), t = !0;
    },
    p(f, s) {
      const r = s[0] & /*gradio, loading_status*/
      1536 ? mi(l, [
        s[0] & /*gradio*/
        1024 && {
          autoscroll: (
            /*gradio*/
            f[10].autoscroll
          )
        },
        s[0] & /*gradio*/
        1024 && { i18n: (
          /*gradio*/
          f[10].i18n
        ) },
        s[0] & /*loading_status*/
        512 && di(
          /*loading_status*/
          f[9]
        )
      ]) : {};
      e.$set(r);
    },
    i(f) {
      t || (de(e.$$.fragment, f), t = !0);
    },
    o(f) {
      ve(e.$$.fragment, f), t = !1;
    },
    d(f) {
      $e(e, f);
    }
  };
}
function vi(n) {
  let e;
  return {
    c() {
      e = Ee(
        /*label*/
        n[2]
      );
    },
    m(t, l) {
      he(t, e, l);
    },
    p(t, l) {
      l[0] & /*label*/
      4 && tt(
        e,
        /*label*/
        t[2]
      );
    },
    d(t) {
      t && be(e);
    }
  };
}
function Zt(n) {
  let e, t = (
    /*item*/
    n[27] + ""
  ), l;
  return {
    c() {
      e = ae("option"), l = Ee(t), e.__value = /*item*/
      n[27], We(e, e.__value);
    },
    m(i, f) {
      he(i, e, f), $(e, l);
    },
    p: gi,
    d(i) {
      i && be(e);
    }
  };
}
function At(n) {
  let e, t = (
    /*item*/
    n[27][0] + ""
  ), l, i;
  return {
    c() {
      e = ae("option"), l = Ee(t), e.__value = i = /*item*/
      n[27][1], We(e, e.__value);
    },
    m(f, s) {
      he(f, e, s), $(e, l);
    },
    p(f, s) {
      s[0] & /*machineList*/
      4096 && t !== (t = /*item*/
      f[27][0] + "") && tt(l, t), s[0] & /*machineList*/
      4096 && i !== (i = /*item*/
      f[27][1]) && (e.__value = i, We(e, e.__value));
    },
    d(f) {
      f && be(e);
    }
  };
}
function Bt(n) {
  let e, t;
  return {
    c() {
      e = ae("div"), t = Ee(
        /*errMsg*/
        n[11]
      ), Ae(e, "class", "dp_machine--error svelte-1qtc7pq");
    },
    m(l, i) {
      he(l, e, i), $(e, t);
    },
    p(l, i) {
      i[0] & /*errMsg*/
      2048 && tt(
        t,
        /*errMsg*/
        l[11]
      );
    },
    d(l) {
      l && be(e);
    }
  };
}
function yi(n) {
  let e, t, l, i, f, s, r, o, a, _, d, p, m = (
    /*loading_status*/
    n[9] && jt(n)
  );
  l = new ln({
    props: {
      show_label: (
        /*show_label*/
        n[6]
      ),
      info: void 0,
      $$slots: { default: [vi] },
      $$scope: { ctx: n }
    }
  });
  let k = Ne(
    /*machineTypeOptions*/
    n[14]
  ), w = [];
  for (let c = 0; c < k.length; c += 1)
    w[c] = Zt(Tt(n, k, c));
  let q = Ne(
    /*machineList*/
    n[12]
  ), M = [];
  for (let c = 0; c < q.length; c += 1)
    M[c] = At(Pt(n, q, c));
  let u = (
    /*isError*/
    n[13] && Bt(n)
  );
  return {
    c() {
      m && m.c(), e = Ie(), t = ae("div"), xe(l.$$.fragment), i = Ie(), f = ae("select");
      for (let c = 0; c < w.length; c += 1)
        w[c].c();
      s = Ie(), r = ae("div"), o = ae("select");
      for (let c = 0; c < M.length; c += 1)
        M[c].c();
      a = Ie(), u && u.c(), Ae(f, "class", "dp_machine-type svelte-1qtc7pq"), /*machineType*/
      n[1] === void 0 && zt(() => (
        /*select0_change_handler*/
        n[20].call(f)
      )), Ae(o, "class", "dp_machine-sku svelte-1qtc7pq"), /*value*/
      n[0] === void 0 && zt(() => (
        /*select1_change_handler*/
        n[21].call(o)
      )), Ae(r, "class", "dp_machine-container svelte-1qtc7pq");
    },
    m(c, h) {
      m && m.m(c, h), he(c, e, h), he(c, t, h), et(l, t, null), $(t, i), $(t, f);
      for (let L = 0; L < w.length; L += 1)
        w[L] && w[L].m(f, null);
      Ve(
        f,
        /*machineType*/
        n[1],
        !0
      ), $(t, s), $(t, r), $(r, o);
      for (let L = 0; L < M.length; L += 1)
        M[L] && M[L].m(o, null);
      Ve(
        o,
        /*value*/
        n[0],
        !0
      ), $(r, a), u && u.m(r, null), _ = !0, d || (p = [
        Vt(
          f,
          "change",
          /*select0_change_handler*/
          n[20]
        ),
        Vt(
          o,
          "change",
          /*select1_change_handler*/
          n[21]
        )
      ], d = !0);
    },
    p(c, h) {
      /*loading_status*/
      c[9] ? m ? (m.p(c, h), h[0] & /*loading_status*/
      512 && de(m, 1)) : (m = jt(c), m.c(), de(m, 1), m.m(e.parentNode, e)) : m && (bi(), ve(m, 1, 1, () => {
        m = null;
      }), ui());
      const L = {};
      if (h[0] & /*show_label*/
      64 && (L.show_label = /*show_label*/
      c[6]), h[0] & /*label*/
      4 | h[1] & /*$$scope*/
      2 && (L.$$scope = { dirty: h, ctx: c }), l.$set(L), h[0] & /*machineTypeOptions*/
      16384) {
        k = Ne(
          /*machineTypeOptions*/
          c[14]
        );
        let b;
        for (b = 0; b < k.length; b += 1) {
          const S = Tt(c, k, b);
          w[b] ? w[b].p(S, h) : (w[b] = Zt(S), w[b].c(), w[b].m(f, null));
        }
        for (; b < w.length; b += 1)
          w[b].d(1);
        w.length = k.length;
      }
      if (h[0] & /*machineType, machineTypeOptions*/
      16386 && Ve(
        f,
        /*machineType*/
        c[1]
      ), h[0] & /*machineList*/
      4096) {
        q = Ne(
          /*machineList*/
          c[12]
        );
        let b;
        for (b = 0; b < q.length; b += 1) {
          const S = Pt(c, q, b);
          M[b] ? M[b].p(S, h) : (M[b] = At(S), M[b].c(), M[b].m(o, null));
        }
        for (; b < M.length; b += 1)
          M[b].d(1);
        M.length = q.length;
      }
      h[0] & /*value, machineList*/
      4097 && Ve(
        o,
        /*value*/
        c[0]
      ), /*isError*/
      c[13] ? u ? u.p(c, h) : (u = Bt(c), u.c(), u.m(r, null)) : u && (u.d(1), u = null);
    },
    i(c) {
      _ || (de(m), de(l.$$.fragment, c), _ = !0);
    },
    o(c) {
      ve(m), ve(l.$$.fragment, c), _ = !1;
    },
    d(c) {
      c && (be(e), be(t)), m && m.d(c), $e(l), Nt(w, c), Nt(M, c), u && u.d(), d = !1, pi(p);
    }
  };
}
function qi(n) {
  let e, t;
  return e = new wl({
    props: {
      visible: (
        /*visible*/
        n[5]
      ),
      elem_id: (
        /*elem_id*/
        n[3]
      ),
      elem_classes: (
        /*elem_classes*/
        n[4]
      ),
      allow_overflow: !1,
      scale: (
        /*scale*/
        n[7]
      ),
      min_width: (
        /*min_width*/
        n[8]
      ),
      $$slots: { default: [yi] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      xe(e.$$.fragment);
    },
    m(l, i) {
      et(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i[0] & /*visible*/
      32 && (f.visible = /*visible*/
      l[5]), i[0] & /*elem_id*/
      8 && (f.elem_id = /*elem_id*/
      l[3]), i[0] & /*elem_classes*/
      16 && (f.elem_classes = /*elem_classes*/
      l[4]), i[0] & /*scale*/
      128 && (f.scale = /*scale*/
      l[7]), i[0] & /*min_width*/
      256 && (f.min_width = /*min_width*/
      l[8]), i[0] & /*errMsg, isError, value, machineList, machineType, show_label, label, gradio, loading_status*/
      15943 | i[1] & /*$$scope*/
      2 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (de(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ve(e.$$.fragment, l), t = !1;
    },
    d(l) {
      $e(e, l);
    }
  };
}
function Ci(n, e, t) {
  var l = this && this.__awaiter || function(C, E, N, W) {
    function pe(D) {
      return D instanceof N ? D : new N(function(T) {
        T(D);
      });
    }
    return new (N || (N = Promise))(function(D, T) {
      function le(j) {
        try {
          ne(W.next(j));
        } catch (g) {
          T(g);
        }
      }
      function qe(j) {
        try {
          ne(W.throw(j));
        } catch (g) {
          T(g);
        }
      }
      function ne(j) {
        j.done ? D(j.value) : pe(j.value).then(le, qe);
      }
      ne((W = W.apply(C, E || [])).next());
    });
  };
  let { label: i = "machine" } = e, { elem_id: f = "" } = e, { elem_classes: s = [] } = e, { visible: r = !0 } = e, { value: o } = e, { show_label: a } = e, { scale: _ = null } = e, { min_width: d = void 0 } = e, { loading_status: p } = e, { gradio: m } = e, { interactive: k } = e, { machineType: w } = e, q = ["CPU", "GPU"], M = /* @__PURE__ */ new Map();
  function u() {
    document.cookie.split(";").forEach((C) => {
      const [E, N] = C.trim().split("=");
      M.set(E, N);
    });
  }
  let c = [], h = [], L = [];
  function b() {
    return l(this, void 0, void 0, function* () {
      const C = M.get("appAccessKey"), E = M.get("clientName"), N = (T) => fetch(`https://openapi.dp.tech/openapi/v1/open/sku/list?chooseType=${T}`, {
        headers: { accessKey: C, "x-app-key": E }
      }), [W, pe] = yield Promise.all([N("cpu"), N("gpu")]), D = (T, le) => l(this, void 0, void 0, function* () {
        if (T.ok) {
          const ne = (yield T.json()).data.items.map((j) => [j.skuName, j.skuId]);
          le ? t(17, c = ne) : t(18, h = ne);
        }
      });
      D(W, !0), D(pe, !1);
    });
  }
  ki(() => {
    u(), b();
  });
  let S = !1, { errMsg: P = "Please select a machine" } = e;
  function fe() {
    return t(13, S = !o), S;
  }
  function X() {
    m.dispatch("change");
  }
  const ee = () => m.dispatch("clear_status", p);
  function te() {
    w = It(this), t(1, w), t(14, q);
  }
  function ye() {
    o = It(this), t(0, o), t(1, w), t(12, L), t(1, w), t(17, c), t(18, h);
  }
  return n.$$set = (C) => {
    "label" in C && t(2, i = C.label), "elem_id" in C && t(3, f = C.elem_id), "elem_classes" in C && t(4, s = C.elem_classes), "visible" in C && t(5, r = C.visible), "value" in C && t(0, o = C.value), "show_label" in C && t(6, a = C.show_label), "scale" in C && t(7, _ = C.scale), "min_width" in C && t(8, d = C.min_width), "loading_status" in C && t(9, p = C.loading_status), "gradio" in C && t(10, m = C.gradio), "interactive" in C && t(15, k = C.interactive), "machineType" in C && t(1, w = C.machineType), "errMsg" in C && t(11, P = C.errMsg);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*machineType, cpuList, gpuList*/
    393218 && (w === "CPU" ? t(12, L = c) : t(12, L = h)), n.$$.dirty[0] & /*machineType*/
    2 && (t(0, o = void 0), X()), n.$$.dirty[0] & /*value*/
    1 && (fe(), X());
  }, [
    o,
    w,
    i,
    f,
    s,
    r,
    a,
    _,
    d,
    p,
    m,
    P,
    L,
    S,
    q,
    k,
    fe,
    c,
    h,
    ee,
    te,
    ye
  ];
}
class Mi extends _i {
  constructor(e) {
    super(), hi(
      this,
      e,
      Ci,
      qi,
      wi,
      {
        label: 2,
        elem_id: 3,
        elem_classes: 4,
        visible: 5,
        value: 0,
        show_label: 6,
        scale: 7,
        min_width: 8,
        loading_status: 9,
        gradio: 10,
        interactive: 15,
        machineType: 1,
        errMsg: 11,
        validate: 16
      },
      null,
      [-1, -1]
    );
  }
  get validate() {
    return this.$$.ctx[16];
  }
}
export {
  Mi as default
};
