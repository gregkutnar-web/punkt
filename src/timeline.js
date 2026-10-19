/* Mini časovnica za scrubane animacije (SVG). Sledi = ključne točke [t, {cx,cy,sx,sy,r,o,f,e}].
   cx,cy = ciljno središče v koordinatah sveta (privzeto izvirno), sx,sy = merilo, r = rotacija (°),
   o = prosojnost, f = barva (hex), e = lajšanje segmenta, ki se konča v tej točki. Lastnosti so redke:
   vsaka se interpolira med točkama, ki jo določata. */
(function (W) {
  'use strict';
  var EASE = {
    lin: function (t) { return t },
    io: function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2 },
    in: function (t) { return t * t },
    out: function (t) { return 1 - Math.pow(1 - t, 3) },
    back: function (t) { var c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2) }
  };
  function lerp(a, b, t) { return a + (b - a) * t }
  function rgb(c) { return [parseInt(c.substr(1, 2), 16), parseInt(c.substr(3, 2), 16), parseInt(c.substr(5, 2), 16)] }
  function mixc(a, b, t) { var x = rgb(a), y = rgb(b); return 'rgb(' + Math.round(lerp(x[0], y[0], t)) + ',' + Math.round(lerp(x[1], y[1], t)) + ',' + Math.round(lerp(x[2], y[2], t)) + ')' }
  var KEYS = ['cx', 'cy', 'sx', 'sy', 'r', 'o', 'f'];

  function value(kfs, key, t, def) {
    var prev = null, next = null;
    for (var i = 0; i < kfs.length; i++) {
      var k = kfs[i]; if (k[1][key] === undefined) continue;
      if (k[0] <= t) prev = k; else { next = k; break }
    }
    if (!prev && !next) return def;
    if (!prev) return next[1][key];
    if (!next) return prev[1][key];
    var u = (t - prev[0]) / (next[0] - prev[0]), e = EASE[next[1].e || 'io'](Math.max(0, Math.min(1, u)));
    return key === 'f' ? mixc(prev[1].f, next[1].f, e) : lerp(prev[1][key], next[1][key], e);
  }

  function create(opt) {
    var tracks = [], camKf = null, cam = opt.cam, VW = opt.vw || 1600, VH = opt.vh || 900;
    function track(el, kfs) {
      var bb = el.getBBox();
      tracks.push({ el: el, ncx: bb.x + bb.width / 2, ncy: bb.y + bb.height / 2, kfs: kfs.slice().sort(function (a, b) { return a[0] - b[0] }), tr: kfs.some(function (k) { return k[1].cx !== undefined || k[1].cy !== undefined || k[1].sx !== undefined || k[1].sy !== undefined || k[1].r !== undefined }) });
    }
    function setCam(kfs) { camKf = kfs.slice().sort(function (a, b) { return a[0] - b[0] }) }
    function render(p) {
      tracks.forEach(function (T) {
        var el = T.el;
        if (T.tr) {
          var cx = value(T.kfs, 'cx', p, T.ncx), cy = value(T.kfs, 'cy', p, T.ncy), sx = value(T.kfs, 'sx', p, 1), sy = value(T.kfs, 'sy', p, 1), r = value(T.kfs, 'r', p, 0);
          el.setAttribute('transform', 'translate(' + (cx - T.ncx).toFixed(2) + ' ' + (cy - T.ncy).toFixed(2) + ') translate(' + T.ncx.toFixed(2) + ' ' + T.ncy.toFixed(2) + ') rotate(' + r.toFixed(2) + ') scale(' + sx.toFixed(4) + ' ' + sy.toFixed(4) + ') translate(' + (-T.ncx).toFixed(2) + ' ' + (-T.ncy).toFixed(2) + ')');
        }
        var o = value(T.kfs, 'o', p, 1); el.setAttribute('opacity', o <= 0 ? 0 : o.toFixed(3));
        el.style.display = o <= 0.001 ? 'none' : '';
        var f = value(T.kfs, 'f', p, null); if (f) el.style.color = f;
      });
      if (camKf && cam) {
        var x = value(camKf, 'cx', p, VW / 2), y = value(camKf, 'cy', p, VH / 2), s = value(camKf, 'sx', p, 1);
        cam.setAttribute('transform', 'translate(' + VW / 2 + ' ' + VH / 2 + ') scale(' + s.toFixed(4) + ') translate(' + (-x).toFixed(2) + ' ' + (-y).toFixed(2) + ')');
      }
    }
    return { track: track, cam: setCam, render: render };
  }
  W.Timeline = { create: create, ease: EASE };
})(window);
