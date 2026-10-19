/* Scenarij animacije »Nastanek« (čas v sekundah). Koordinate sveta = koordinate strani PDF (1200×1200).
   Sivo (#d9d9d9) se pojavlja samo kot ghost/odtis v animaciji; končna stanja so črna, bela in turkizna. */
(function (W) {
  'use strict';
  var GH = '#d9d9d9', BK = '#000000', WH = '#ffffff', TEAL = '#00868f', DS = .5686, DUR = 72;
  function S(id) { return document.getElementById(id) }
  function clamp(x) { return x < 0 ? 0 : x > 1 ? 1 : x }

  function build(svg) {
    var tl = Timeline.create({ cam: svg.querySelector('.cam'), defs: svg.querySelector('defs') });
    var K = {}, OPT = {}, NC = {};
    function nc(id) { return NC[id] || (NC[id] = tl.nc(S(id))) }
    function k(id, t, p) { (K[id] = K[id] || []).push([t, p]) }
    function ks(id, arr) { arr.forEach(function (a) { k(id, a[0], a[1]) }) }

    /* ---------- kamera ---------- */
    tl.cam([[0, { cx: 600, cy: 650, sx: 1.42 }], [8.8, { cx: 600, cy: 650, sx: 1.42 }], [10.2, { cx: 430, cy: 600, sx: 1.6 }], [14.5, { cx: 430, cy: 600, sx: 1.6 }],
      [16, { cx: 430, cy: 620, sx: 2.2 }], [22, { cx: 430, cy: 620, sx: 2.2 }], [23.4, { cx: 600, cy: 610, sx: 1.3 }], [44, { cx: 600, cy: 610, sx: 1.3 }],
      [45.1, { cx: 470, cy: 610, sx: 1.75 }], [47, { cx: 470, cy: 610, sx: 1.75 }], [48.2, { cx: 600, cy: 610, sx: 1.3 }], [50, { cx: 480, cy: 610, sx: 2.4 }],
      [52.4, { cx: 525, cy: 600, sx: 1.75 }], [59.6, { cx: 525, cy: 600, sx: 1.75 }], [61.6, { cx: 600, cy: 610, sx: 1.3 }], [67.6, { cx: 600, cy: 618, sx: 1.3 }], [69.2, { cx: 600, cy: 618, sx: 1.0 }], [DUR, { cx: 600, cy: 618, sx: 1.0 }]]);

    /* ---------- ozadje ---------- */
    ks('c_bg', [[0, { f: WH }], [62, { f: WH }], [63, { f: BK }], [65, { f: BK }], [66, { f: TEAL }], [67.6, { f: TEAL }], [68.6, { f: '#f2f2f2' }]]);

    /* ---------- 1. Nakup (0–8 s) ---------- */
    ks('c_basket', [[.5, { o: 0, cx: 615, cy: 726 }], [1.3, { o: 1, cx: 615, cy: 666, e: 'back' }], [7.9, { o: 1, cx: 615, cy: 666 }], [9, { o: 0, cx: 615, cy: 790 }]]);
    OPT.c_basket = { wob: function (t) { return t > 1.4 && t < 8 ? { dy: 3 * Math.sin(t * 1.7) } : null } };
    ks('c_bag', [[.8, { o: 0, cx: 949, cy: 700 }], [1.6, { o: 1, cx: 949, cy: 642, e: 'back' }], [7.9, { o: 1, cx: 949, cy: 642 }], [9.1, { o: 0, cx: 949, cy: 730 }]]);
    OPT.c_bag = { wob: function (t) { return t > 1.6 && t < 8 ? { dy: 3 * Math.sin(t * 1.5 + 1) } : null } };
    [['c_b1', 1.6], ['c_b2', 1.9], ['c_b3', 2.2]].forEach(function (b, i) {
      ks(b[0], [[b[1] - .4, { o: 0, sx: 0, sy: 0 }], [b[1], { o: 1, sx: 1, sy: 1, e: 'back' }], [8, { o: 1, sx: 1, sy: 1 }], [8.6, { o: 0, sx: .2, sy: .2, e: 'in' }]]);
      OPT[b[0]] = { wob: function (t) { if (t < b[1] + .5 || t > 8) return null; var s = 1 + .07 * Math.sin(t * 4 + i * 1.3); return { sx: s, sy: s } } };
    });

    /* ---------- 2. Voziček (8–22 s) ---------- */
    // cesta, senca, odtisi
    ks('c_road', [[0, { o: 0 }], [8.6, { o: 0 }], [9.6, { o: 1 }], [23, { o: 1 }], [24, { o: 0 }]]);
    ks('c_sh', [[0, { o: 0, cx: -282, cy: 752 }], [9.9, { o: 0, cx: -282 }], [10.1, { o: .12, cx: -282 }], [13, { o: .12, cx: 428, e: 'out' }], [24.5, { o: .12, cx: 428 }], [25.6, { o: 0 }]]);
    // voziček: obrat, izvoz, vrnitev, pot, ustavitev
    ks('c_cart', [[0, { o: 0, cx: 236.5, cy: 726, sx: .5, sy: .5 }], [.9, { o: 1, cx: 236.5, cy: 666, sx: 1, sy: 1, e: 'back' }], [8, { cx: 236.5, cy: 666, sx: 1 }],
      [8.15, { sx: -1 }], [9.55, { cx: -430, cy: 666, sx: -1, e: 'in' }], [9.56, { cx: -430, cy: 650, sx: 1 }], [9.9, { cx: -300, cy: 650, sx: 1, sy: 1 }], [13, { cx: 410.5, cy: 650, e: 'out' }],
      [14.1, { sx: 1, sy: 1 }], [14.25, { sx: 1.05, sy: .92 }], [14.55, { sx: 1, sy: 1 }], [25.8, { cx: 410.5, cy: 650, sx: 1, sy: 1, o: 1 }],
      [28.4, { cx: 411, cy: 618, sx: .8, sy: .72, o: 0 }]]);
    OPT.c_cart = { wob: function (t) {
      if (t > 9.9 && t < 13.4) { var env = clamp((13.4 - t) / 3.5); return { dy: 2.4 * Math.sin(t * 21) * env, r: .9 * Math.sin(t * 17) * env } }
      if (t > 14.8 && t < 26.4) { var e2 = clamp((t - 14.8) / .8) * (1 - clamp((t - 25.4) / 1)); return { dy: 2.6 * Math.sin((t - 14.8) * 3.1) * e2 } }
      return null } };
    ks('c_lines', [[0, { o: 1, sx: 1 }], [25, { o: 1, sx: 1 }], [26, { o: 0, sx: .2 }]]);
    // sivi odtisi vozička (str. 2)
    [[0, 10.52, 46], [1, 11.14, 257], [2, 11.76, 365], [3, 12.38, 404]].forEach(function (g) {
      var id = 'c_gc' + g[0];
      ks(id, [[0, { o: 0, cx: g[2], cy: 650 }], [g[1] - .01, { o: 0, cx: g[2], cy: 650 }], [g[1] + .2, { o: .4 }], [g[1] + 1.6, { o: .4 }], [g[1] + 2.4, { o: 0 }]]);
    });
    // pika: ena sama, pade z odbojem
    ks('c_dot', [[0, { o: 0, cx: 452, cy: 300, sx: DS, sy: DS }], [13, { o: 0, cx: 452, cy: 300, sx: DS, sy: DS }], [13.05, { o: 1 }], [14.15, { cx: 444.5, cy: 650.5, e: 'in' }],
      [14.4, { cy: 628, sx: DS * .95, sy: DS * 1.05, e: 'out' }], [14.65, { cy: 650.5, sx: DS * 1.12, sy: DS * .85, e: 'in' }], [14.85, { cx: 444.5, sx: DS, sy: DS, e: 'out' }],
      [26.8, { cx: 444.5, cy: 650.5 }], [28.2, { cx: 427.5, cy: 605.5, sx: 1, sy: 1, e: 'back' }]]);
    OPT.c_dot = { wob: function (t) { return t > 14.8 && t < 26.4 ? { dy: 2.6 * Math.sin((t - 14.8) * 3.1) * clamp((t - 14.8) / .8) * (1 - clamp((t - 25.4) / 1)) } : null } };
    // sivi odtisi padca pike
    [[0, 13.35, 326], [1, 13.6, 387], [2, 13.85, 486], [3, 14.05, 590]].forEach(function (g) {
      var u = (g[1] - 13.05) / 1.1, x = 452 - 7.5 * u;
      ks('c_gd' + g[0], [[0, { o: 0, cx: x, cy: g[2], sx: DS, sy: DS }], [g[1], { o: 0 }], [g[1] + .12, { o: .45 }], [14.4, { o: .45 }], [15.2, { o: 0 }]]);
    });

    /* ---------- 3. U (22–36 s): ghost PUNKT, voziček -> U ---------- */
    var LET = ['P', 'K', 'T', 'N'];
    LET.forEach(function (L, i) {
      var id = 'c_' + L, y = nc(id).y;
      ks(id, [[0, { o: 0, f: GH }], [22.4 + i * .25, { o: 0, cy: y + 40, f: GH }], [23.3 + i * .25, { o: 1, cy: y, f: GH, e: 'out' }]]);
    });
    ks('c_U', [[0, { o: 0, f: TEAL }], [25.8, { o: 0, w: 0 }], [25.81, { o: 1, w: 0 }], [28, { w: 1, e: 'out' }]]);
    OPT.c_U = { wipe: 'up' };

    /* ---------- 4. Logotip (36–50 s): PRAVI, SKUPINA, val črnine, poudarek ---------- */
    var ORDER = [];
    for (var i = 0; i < 5; i++) {
      var id = 'c_pr' + i, y = nc(id).y;
      ks(id, [[0, { o: 0, f: GH }], [36 + i * .1, { o: 0, cy: y - 77, f: GH }], [36.9 + i * .1, { o: 1, cy: y, f: GH, e: 'out' }]]);
      ORDER.push(id);
    }
    ['c_P', 'c_N', 'c_K', 'c_T'].forEach(function (id) { ORDER.push(id) });
    for (var j = 0; j < 15; j++) {
      var sid = 'c_sk' + j, cx = nc(sid).x;
      ks(sid, [[0, { o: 0, f: GH }], [37, { o: 0, cx: cx + (j - 7) * 18, f: GH }], [38.6 + j * .03, { o: 1, cx: cx, f: GH, e: 'out' }]]);
      ORDER.push(sid);
      ks(sid, [[44.6 + j * .07, { f: BK }], [45.1 + j * .07, { f: TEAL, e: 'out' }]]);
    }
    ORDER.forEach(function (id, n) { var s = 39.6 + n * .16; k(id, s, { f: GH }); k(id, s + .5, { f: BK, e: 'out' }) });
    ks('c_hl', [[0, { o: 0 }], [44.2, { o: 0, sx: .5, sy: .5 }], [45, { o: .4, sx: 1, sy: 1, e: 'back' }], [47, { o: .4 }], [47.9, { o: 0, sx: 1.12, sy: 1.12 }],
      [49.8, { o: 0, sx: .9, sy: .9 }], [50.6, { o: 1, sx: 1, sy: 1, e: 'out' }]]);

    /* ---------- 5. Ikona (50–60 s) ---------- */
    var OUT = ['c_P', 'c_N', 'c_K', 'c_T'].concat([0, 1, 2, 3, 4].map(function (n) { return 'c_pr' + n }), [].concat.apply([], [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14].map(function (n) { return 'c_sk' + n })]));
    OUT.forEach(function (id) {
      var p = nc(id), dir = p.x < 428 ? -1 : 1, sk = id.indexOf('sk') > 0, f = sk ? TEAL : BK;
      ks(id, [[49.9, { o: 1, cx: p.x, f: f }], [50.9, { o: 0, cx: p.x + dir * 260, e: 'in' }], [60.6, { o: 0, cx: p.x + dir * 260, f: f }], [61.6, { o: 1, cx: p.x, f: f, e: 'out' }]]);
    });
    // U in pika postaneta bela ter se skupaj z ikono pomakneta levo, nato nazaj
    var uc = nc('c_U'), dc = { x: 427.5, y: 605.5 }, hc = nc('c_hl');
    ks('c_U', [[49.9, { f: TEAL, cx: uc.x, cy: uc.y }], [50.9, { f: WH }], [52.6, { cx: 330, cy: uc.y - 18.5 }], [59.8, { cx: 330, cy: uc.y - 18.5, f: WH }], [60.2, { f: WH }], [61.4, { cx: uc.x, cy: uc.y, f: TEAL }]]);
    ks('c_dot', [[49.9, { f: TEAL, cx: dc.x, cy: dc.y, sx: 1, sy: 1 }], [50.9, { f: WH }], [52.6, { cx: dc.x - 98, cy: dc.y - 18.5 }],
      [55.4, { cx: dc.x - 98, cy: dc.y - 18.5, sx: 1, sy: 1 }], [55.65, { cy: dc.y - 60, sx: .95, sy: 1.08, e: 'out' }], [55.9, { cy: dc.y - 18.5, sx: 1.12, sy: .85, e: 'in' }], [56.15, { sx: 1, sy: 1, e: 'out' }],
      [59.8, { cx: dc.x - 98, cy: dc.y - 18.5 }], [60.2, { f: WH }], [61.4, { cx: dc.x, cy: dc.y, f: TEAL }]]);
    ks('c_hl', [[52.6, { cx: hc.x - 98, cy: hc.y - 18.5 }], [59.8, { cx: hc.x - 98, cy: hc.y - 18.5, o: 1, sx: 1, sy: 1 }], [61.4, { cx: hc.x, cy: hc.y, o: 0, sx: .85, sy: .85 }]]);
    ks('c_ic2', [[0, { o: 0, cx: 900, cy: 600 }], [52.2, { o: 0, cx: 900, cy: 600 }], [52.3, { o: 1 }], [53.6, { cx: 720, cy: 600, e: 'out' }], [59.8, { cx: 720, cy: 600, o: 1 }], [61, { cx: 1100, cy: 600, o: 0, e: 'in' }]]);
    var d2 = nc('c_id2');
    ks('c_id2', [[55.4, { cy: d2.y }], [55.65, { cy: d2.y - 42, sx: .95, sy: 1.08, e: 'out' }], [55.9, { cy: d2.y, sx: 1.12, sy: .85, e: 'in' }], [56.15, { sx: 1, sy: 1, e: 'out' }]]);
    [['c_l1', 329.5], ['c_l2', 720]].forEach(function (l) { ks(l[0], [[0, { o: 0 }], [53.6, { o: 0 }], [54.6, { o: 1 }], [59.8, { o: 1 }], [60.3, { o: 0 }]]) });

    /* ---------- 6. Barve (60–72 s) ---------- */
    ['c_P', 'c_N', 'c_K', 'c_T', 'c_pr0', 'c_pr1', 'c_pr2', 'c_pr3', 'c_pr4'].forEach(function (id) { k(id, 62, { f: BK }); k(id, 63, { f: WH }); k(id, 67.6, { f: WH }); k(id, 68.6, { f: BK }) });
    ['c_U', 'c_dot'].forEach(function (id) { k(id, 65, { f: TEAL }); k(id, 66, { f: BK }); k(id, 67.6, { f: BK }); k(id, 68.6, { f: TEAL }) });
    for (var m = 0; m < 15; m++) { var s2 = 'c_sk' + m; k(s2, 65, { f: TEAL }); k(s2, 66, { f: BK }); k(s2, 67.6, { f: BK }); k(s2, 68.6, { f: TEAL }) }
    ks('c_disc', [[0, { o: 0 }], [67.8, { o: 0, sx: .2, sy: .2 }], [69, { o: 1, sx: 1, sy: 1, e: 'back' }]]);
    var lc = nc('c_lock');
    ks('c_lock', [[0, { cx: lc.x, cy: lc.y, sx: 1, sy: 1 }], [67.8, { cx: lc.x, cy: lc.y, sx: 1, sy: 1 }], [69.2, { cx: 600, cy: 618, sx: .765, sy: .765 }]]);

    // registracija sledi
    Object.keys(K).forEach(function (id) { var el = S(id); if (!el) { console.warn('manjka', id); return } tl.track(el, K[id], OPT[id]) });
    ['c_gc0', 'c_gc1', 'c_gc2', 'c_gc3'].forEach(function () { });

    /* ---------- vetrne črte ---------- */
    var wy = [585, 610, 640, 672, 700, 728];
    tl.fn(function (t) {
      var u = clamp((t - 9.9) / 3.1), speed = Math.pow(1 - u, 2), on = t > 9.9 && t < 13.6, cartx = -300 + 710 * (1 - Math.pow(1 - u, 3)) + 17.5 - 102;
      for (var i = 0; i < 6; i++) {
        var el = S('c_w' + i); if (!el) continue;
        if (!on) { el.setAttribute('opacity', 0); continue }
        var len = 30 + 240 * speed, x2 = cartx - 40 - i * 16;
        el.setAttribute('x1', (x2 - len).toFixed(1)); el.setAttribute('x2', x2.toFixed(1)); el.setAttribute('y1', wy[i]); el.setAttribute('y2', wy[i]);
        el.setAttribute('opacity', (.55 * clamp(speed * 2.2)).toFixed(3));
      }
    });

    /* ---------- iskre ---------- */
    var BURSTS = [[14.15, 444, 640, 10, TEAL], [28.3, 427, 608, 12, TEAL], [48.5, 427, 606, 12, TEAL], [55.9, 232, 588, 8, WH], [55.9, 720, 586, 8, TEAL], [69.2, 600, 618, 16, TEAL]];
    var POOL = 60, sp = [];
    for (var q = 0; q < POOL; q++) sp.push(S('c_s' + q));
    var assign = [], base = 0;
    BURSTS.forEach(function (b, bi) { for (var n = 0; n < b[3]; n++) assign.push({ b: b, n: n, i: base + n }); base += b[3] });
    tl.fn(function (t) {
      sp.forEach(function (el) { if (el) el.setAttribute('opacity', 0) });
      assign.forEach(function (a) {
        var el = sp[a.i]; if (!el) return; var u = (t - a.b[0]) / .95; if (u < 0 || u > 1) return;
        var ang = (a.n / a.b[3]) * Math.PI * 2 + (a.n % 3) * .4, v = 70 + (a.n * 37 % 60);
        el.setAttribute('cx', (a.b[1] + Math.cos(ang) * v * u).toFixed(1)); el.setAttribute('cy', (a.b[2] + Math.sin(ang) * v * u + 90 * u * u).toFixed(1));
        el.setAttribute('r', (7 * (1 - u) + 2).toFixed(1)); el.setAttribute('opacity', (1 - u).toFixed(3)); el.style.color = a.b[4];
      });
    });

    return {
      tl: tl, duration: DUR,
      chapters: [{ t: 0, label: 'Nakup' }, { t: 8, label: 'Voziček' }, { t: 22, label: 'U' }, { t: 36, label: 'Logotip' }, { t: 50, label: 'Ikona' }, { t: 60, label: 'Barve' }],
      caps: [[0, 'Nakup'], [8, 'Voziček'], [14.2, 'Izdelek = pika'], [26.5, 'U = košarica'], [32, 'Pika = nakup'], [36, 'Pravi Punkt'], [44.5, 'Poudarek'], [50, 'Ikona'], [60, 'Barve'], [62.2, 'Črno', '#ffffff'], [65.4, 'Turkizno', '#ffffff'], [68.2, 'Krog'], [69.8, 'Pravi Punkt']]
    };
  }
  W.Cine = { build: build };
})(window);
