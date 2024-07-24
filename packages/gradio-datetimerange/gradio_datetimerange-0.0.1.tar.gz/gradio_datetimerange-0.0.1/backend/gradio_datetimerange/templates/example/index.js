const {
  SvelteComponent: o,
  detach: s,
  init: u,
  insert: r,
  noop: l,
  safe_not_equal: _,
  set_data: c,
  text: f
} = window.__gradio__svelte__internal;
function d(i) {
  let e = (
    /*value*/
    (i[0] || "") + ""
  ), n;
  return {
    c() {
      n = f(e);
    },
    m(t, a) {
      r(t, n, a);
    },
    p(t, [a]) {
      a & /*value*/
      1 && e !== (e = /*value*/
      (t[0] || "") + "") && c(n, e);
    },
    i: l,
    o: l,
    d(t) {
      t && s(n);
    }
  };
}
function v(i, e, n) {
  let { value: t } = e;
  return i.$$set = (a) => {
    "value" in a && n(0, t = a.value);
  }, [t];
}
class m extends o {
  constructor(e) {
    super(), u(this, e, v, d, _, { value: 0 });
  }
}
export {
  m as default
};
