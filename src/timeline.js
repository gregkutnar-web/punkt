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
    var tracks = [], fns = [], camKf = null, cam = opt.cam, VW = opt.vw || 1600, VH = opt.vh || 900, wid = 0;
    /* o = {wipe:'up'|'right' (kf lastnost w 0..1), wob: function(t)->{dx,dy,r,sx,sy} (aditivno)} */
    function track(el, kfs, o) {
      o = o || {};
      var bb = el.getBBox(), T = { el: el, ncx: bb.x + bb.width / 2, ncy: bb.y + bb.height / 2, kfs: kfs.slice().sort(function (a, b) { return a[0] - b[0] }), wob: o.wob || null };
      T.tr = !!T.wob || kfs.some(function (k) { return k[1].cx !== undefined || k[1].cy !== undefined || k[1].sx !== undefined || k[1].sy !== undefined || k[1].r !== undefined });
      if (o.wipe && opt.defs) {
        var NS = 'http://www.w3.org/2000/svg', cp = document.createElementNS(NS, 'clipPath'), r = document.createElementNS(NS, 'rect');
        cp.setAttribute('id', 'tw' + (wid++)); cp.setAttribute('clipPathUnits', 'objectBoundingBox'); cp.appendChild(r); opt.defs.appendChild(cp);
        el.setAttribute('clip-path', 'url(#' + cp.id + ')'); T.wr = r; T.wdir = o.wipe;
      }
      tracks.push(T);
    }
    function fn(f) { fns.push(f) }
    function nc(el) { var bb = el.getBBox(); return { x: bb.x + bb.width / 2, y: bb.y + bb.height / 2 } }
    function setCam(kfs) { camKf = kfs.slice().sort(function (a, b) { return a[0] - b[0] }) }
    function render(p) {
      tracks.forEach(function (T) {
        var el = T.el;
        if (T.tr) {
          var cx = value(T.kfs, 'cx', p, T.ncx), cy = value(T.kfs, 'cy', p, T.ncy), sx = value(T.kfs, 'sx', p, 1), sy = value(T.kfs, 'sy', p, 1), r = value(T.kfs, 'r', p, 0);
          if (T.wob) { var w = T.wob(p); if (w) { cx += w.dx || 0; cy += w.dy || 0; r += w.r || 0; sx *= w.sx || 1; sy *= w.sy || 1 } }
          el.setAttribute('transform', 'translate(' + (cx - T.ncx).toFixed(2) + ' ' + (cy - T.ncy).toFixed(2) + ') translate(' + T.ncx.toFixed(2) + ' ' + T.ncy.toFixed(2) + ') rotate(' + r.toFixed(2) + ') scale(' + sx.toFixed(4) + ' ' + sy.toFixed(4) + ') translate(' + (-T.ncx).toFixed(2) + ' ' + (-T.ncy).toFixed(2) + ')');
        }
        var o = value(T.kfs, 'o', p, 1); el.setAttribute('opacity', o <= 0 ? 0 : o.toFixed(3));
        el.style.display = o <= 0.001 ? 'none' : '';
        var f = value(T.kfs, 'f', p, null); if (f) el.style.color = f;
        if (T.wr) { var wv = Math.max(0, Math.min(1, value(T.kfs, 'w', p, 1))); if (T.wdir === 'up') { T.wr.setAttribute('x', 0); T.wr.setAttribute('y', 1 - wv); T.wr.setAttribute('width', 1); T.wr.setAttribute('height', wv) } else { T.wr.setAttribute('x', 0); T.wr.setAttribute('y', 0); T.wr.setAttribute('width', wv); T.wr.setAttribute('height', 1) } }
      });
      for (var i = 0; i < fns.length; i++) fns[i](p);
      if (camKf && cam) {
        var x = value(camKf, 'cx', p, VW / 2), y = value(camKf, 'cy', p, VH / 2), s = value(camKf, 'sx', p, 1);
        cam.setAttribute('transform', 'translate(' + VW / 2 + ' ' + VH / 2 + ') scale(' + s.toFixed(4) + ') translate(' + (-x).toFixed(2) + ' ' + (-y).toFixed(2) + ')');
      }
    }
    return { track: track, cam: setCam, fn: fn, nc: nc, render: render };
  }
  W.Timeline = { create: create, ease: EASE };
})(window);
