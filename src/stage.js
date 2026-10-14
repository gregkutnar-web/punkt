/* ===== Motor delov (FLIP) za animacijo razvoja logotipa =====
   Vsak artboard je razdeljen na dele (id a<osnutek>_<artboard>_<pot>). Del, ki ima ustreznik tudi
   v naslednjem artboardu, se premakne/poveča/zrcali; del z drugačno obliko se prelije; novi se
   pojavijo, manjkajoči ugasnejo. Kamera sama obkroži vsebino vsakega artboarda. */
(function (W) {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x }
  function lerp(a, b, t) { return a + (b - a) * t }
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2 }
  function rgb(c) {
    if (c.charAt(0) === '#') { if (c.length === 4) c = '#' + c[1] + c[1] + c[2] + c[2] + c[3] + c[3]; return [parseInt(c.substr(1, 2), 16), parseInt(c.substr(3, 2), 16), parseInt(c.substr(5, 2), 16)] }
    return [0, 0, 0];
  }
  function mix(a, b, t) { var x = rgb(a), y = rgb(b); return 'rgb(' + Math.round(lerp(x[0], y[0], t)) + ',' + Math.round(lerp(x[1], y[1], t)) + ',' + Math.round(lerp(x[2], y[2], t)) + ')' }
  function mk(tag, attrs) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e }

  /* cfg: {svg, idea, boards:[{cx,cy,bg}], actors:[[ime,[[artboard,pot,opcije]]]], pattern:{board,src}, hold, margin, onPos(pos,act)} */
  function createStage(cfg) {
    var svg = typeof cfg.svg === 'string' ? document.querySelector(cfg.svg) : cfg.svg;
    var N = cfg.boards.length, HOLD = cfg.hold == null ? .45 : cfg.hold, MARGIN = cfg.margin || .74;
    var VW = 1600, VH = 900;
    var bgRect = mk('rect', { width: VW, height: VH, fill: cfg.boards[0].bg });
    var cam = mk('g', {}), patG = mk('g', {}), patUse = mk('use', {}), layer = mk('g', {});
    var defs = mk('defs', {}), clip = mk('clipPath', { id: 'pc' + cfg.idea }), circ = mk('circle', { cx: 0, cy: 0, r: 0 });
    clip.appendChild(circ); defs.appendChild(clip);
    svg.appendChild(defs); svg.appendChild(bgRect); svg.appendChild(cam); cam.appendChild(patG); cam.appendChild(layer);
    patG.appendChild(patUse); patG.setAttribute('clip-path', 'url(#pc' + cfg.idea + ')'); patG.style.display = 'none';

    function sid(b, p) { return 'a' + cfg.idea + '_' + p }
    function colorOf(el) {
      var c = el.getAttribute('data-c'); if (c) return c;
      var d = el.querySelector && el.querySelector('[data-c]'); return d ? d.getAttribute('data-c') : null;
    }
    var actors = [], ext = [];                       // ext: obseg vsebine na artboard
    for (var i = 0; i < N; i++) ext.push(null);
    function actor(name, list) {
      var a = { name: name, kf: [], wipe: null };
      list.forEach(function (it) {
        var b = it[0], el = document.getElementById(sid(b, it[1]));
        if (!el) { console.warn('manjka del', cfg.idea, b, it[1]); return }
        var bb = el.getBBox(), cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
        var t = el.transform && el.transform.baseVal && el.transform.baseVal.numberOfItems ? el.transform.baseVal.consolidate() : null;
        var w = bb.width, h = bb.height;
        if (t) { var m = t.matrix; var nx = m.a * cx + m.c * cy + m.e, ny = m.b * cx + m.d * cy + m.f; cx = nx; cy = ny; w *= Math.abs(m.a); h *= Math.abs(m.d); }
        var bc = cfg.boards[b];
        a.kf[b] = { id: el.id, o: it[2] || {}, ncx: cx, ncy: cy, w: w, h: h, cx: cx - bc.cx, cy: cy - bc.cy, color: colorOf(el) };
        var e = ext[b], x0 = cx - bc.cx - w / 2, x1 = cx - bc.cx + w / 2, y0 = cy - bc.cy - h / 2, y1 = cy - bc.cy + h / 2;
        ext[b] = e ? [Math.min(e[0], x0), Math.min(e[1], y0), Math.max(e[2], x1), Math.max(e[3], y1)] : [x0, y0, x1, y1];
        if (it[2] && it[2].wipe && !a.wipe) {
          var cp = mk('clipPath', { id: 'wp' + cfg.idea + '_' + name, clipPathUnits: 'objectBoundingBox' });
          a.rect = mk('rect', { x: 0, y: 0, width: 0, height: 1 }); cp.appendChild(a.rect); defs.appendChild(cp); a.wipe = cp.id;
        }
      });
      a.g = mk('g', {}); a.under = mk('use', {}); a.over = mk('use', {});
      a.under.style.display = a.over.style.display = 'none';
      a.g.appendChild(a.under); a.g.appendChild(a.over); layer.appendChild(a.g); actors.push(a);
    }
    cfg.actors.forEach(function (a) { actor(a[0], a[1]) });

    // kamera: obkroži vsebino artboarda
    var camT = cfg.boards.map(function (bd, i) {
      var e = ext[i] || [-100, -50, 100, 50];
      var w = Math.max(e[2] - e[0], 40), h = Math.max(e[3] - e[1], 20);
      var s = Math.min(VW * MARGIN / w, VH * MARGIN / h, cfg.maxScale || 7.5);
      return { s: s, x: (e[0] + e[2]) / 2, y: (e[1] + e[3]) / 2 };
    });
    if (cfg.camera) cfg.camera.forEach(function (c, i) { if (c) for (var k in c) camT[i][k] = c[k] });

    var pat = cfg.pattern;
    if (pat) {
      var pel = document.getElementById(pat.src), pb = cfg.boards[pat.board];
      patUse.style.color = colorOf(pel) || '#e6e6e6'; patUse.setAttribute('href', '#' + pat.src); patUse.setAttribute('transform', 'translate(' + (-pb.cx) + ' ' + (-pb.cy) + ')');
    }

    function place(u, kf, x, y, sx, sy, color, op, clipId) {
      u.setAttribute('href', '#' + kf.id);
      u.setAttribute('transform', 'translate(' + x.toFixed(2) + ' ' + y.toFixed(2) + ') scale(' + sx.toFixed(4) + ' ' + sy.toFixed(4) + ') translate(' + (-kf.ncx).toFixed(2) + ' ' + (-kf.ncy).toFixed(2) + ')');
      u.style.color = color || '';
      u.style.opacity = op <= 0 ? 0 : op;
      if (clipId) u.setAttribute('clip-path', 'url(#' + clipId + ')'); else u.removeAttribute('clip-path');
      u.style.display = '';
    }
    function draw(a, k, t) {
      a.under.style.display = 'none'; a.over.style.display = 'none';
      var A = a.kf[k], B = k < N - 1 ? a.kf[k + 1] : null;
      if (A && B) {
        var o = B.o, d = o.d || 0, tt = ease(cl((t - d) / (1 - d)));
        var cx = lerp(A.cx, B.cx, tt), cy = lerp(A.cy, B.cy, tt);
        if (!o.x) {
          var sg = Math.max(B.w, B.h) / Math.max(A.w, A.h), s = lerp(1, sg, tt), fx = o.flip ? 1 - 2 * tt : 1;
          place(a.over, A, cx, cy, s * fx, s, A.color && B.color ? mix(A.color, B.color, tt) : A.color, 1);
        } else {
          place(a.under, B, cx, cy, 1, 1, B.color, cl(tt * 3));
          place(a.over, A, cx, cy, 1, 1, A.color, 1 - cl((tt - .3) / .7));
        }
      } else if (A) {
        var out = A.o.out || [0, 0], te = ease(t);
        place(a.over, A, A.cx + out[0] * te, A.cy + out[1] * te, 1, 1, A.color, 1 - cl(t * 1.6));
      } else if (B) {
        var ob = B.o, db = ob.d || 0, tb = ease(cl((t - db) / (1 - db))), fr = ob.from || [0, 0], s0 = ob.s0 || .94, sc = lerp(s0, 1, tb);
        if (ob.wipe && a.rect) { a.rect.setAttribute('width', tb.toFixed(4)); place(a.under, B, B.cx, B.cy, 1, 1, B.color, tb > 0 ? 1 : 0, a.wipe) }
        else place(a.under, B, B.cx + fr[0] * (1 - tb), B.cy + fr[1] * (1 - tb), sc, sc, B.color, tb);
      }
    }

    var pos = -1, last = null;
    function setPos(p) {
      p = Math.max(0, Math.min(N - 1, p));
      var k = Math.min(N - 1, Math.floor(p + 1e-9)), u = p - k, tl = 0;
      if (k < N - 1 && u > HOLD) tl = (u - HOLD) / (1 - HOLD);
      var key = k + ':' + tl.toFixed(4);
      if (key === last) return; last = key; pos = p;
      var te = ease(tl), k1 = Math.min(N - 1, k + 1), c0 = camT[k], c1 = camT[k1];
      var s = lerp(c0.s, c1.s, te), x = lerp(c0.x, c1.x, te), y = lerp(c0.y, c1.y, te);
      cam.setAttribute('transform', 'translate(' + VW / 2 + ' ' + VH / 2 + ') scale(' + s.toFixed(4) + ') translate(' + (-x).toFixed(2) + ' ' + (-y).toFixed(2) + ')');
      bgRect.setAttribute('fill', mix(cfg.boards[k].bg, cfg.boards[k1].bg, te));
      for (var i = 0; i < actors.length; i++) draw(actors[i], k, tl);
      if (pat) {
        var pb2 = pat.board, show = false, r = 0, op = 1;
        if (k === pb2 - 1) { show = tl > 0; r = 900 * te }
        else if (k === pb2) { show = true; r = 900; op = 1 - te }
        patG.style.display = show ? '' : 'none'; patG.style.opacity = op; circ.setAttribute('r', r.toFixed(1));
      }
      if (cfg.onPos) cfg.onPos(p, Math.min(N - 1, Math.round(p)));
    }
    setPos(0);
    return { N: N, setPos: setPos, getPos: function () { return pos }, svg: svg };
  }

  /* minijature artboardov (iz skritega probe svg) za filmski trak */
  function thumbs(idea, boards, host, onClick) {
    var out = [];
    boards.forEach(function (bd, b) {
      var src = document.getElementById('ab' + idea + '_' + b), btn = document.createElement('button');
      btn.className = 'th'; btn.setAttribute('aria-label', 'Artboard ' + (b + 1));
      var s = mk('svg', { viewBox: bd.x + ' ' + bd.y + ' ' + bd.w + ' ' + bd.h, preserveAspectRatio: 'xMidYMid slice' });
      s.appendChild(mk('rect', { x: bd.x, y: bd.y, width: bd.w, height: bd.h, fill: bd.bg }));
      var g = src.cloneNode(true); g.removeAttribute('id');
      [].slice.call(g.querySelectorAll('[id]')).forEach(function (e) { e.removeAttribute('id') });
      [].slice.call(g.querySelectorAll('[data-c]')).forEach(function (e) { e.style.color = e.getAttribute('data-c') });
      s.appendChild(g); btn.appendChild(s); btn.onclick = function () { onClick(b) }; host.appendChild(btn); out.push(btn);
    });
    return out;
  }
  W.Stage = { create: createStage, thumbs: thumbs, mix: mix, ease: ease, lerp: lerp, cl: cl };
})(window);
