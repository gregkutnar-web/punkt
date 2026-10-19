/* Scenarija časovnic za »Pravi Punkt«. Koordinate = koordinate strani v PDF-ju (1200×1200). */
(function (W) {
  'use strict';
  var T = Timeline, GRAY = '#e5e5e5', TEAL = '#00868f', LET = ['P', 'N', 'K', 'T'];
  function $(id) { return document.getElementById(id) }

  /* ---------- Ideja: nakup -> košarica -> U ---------- */
  function idea(svg) {
    var tl = T.create({ cam: svg.querySelector('.cam') });
    var cart = $('i_cart'), basket = $('i_basket'), bag = $('i_bag');
    // ikone se pojavijo
    tl.track(cart, [[0, { o: 0, cx: 236.5, cy: 720, sx: .6, sy: .6 }], [.09, { o: 1, cx: 236.5, cy: 666, sx: 1, sy: 1, e: 'back' }], [.20, { cx: 236.5, cy: 666 }],
      [.32, { cx: 582.5, cy: 650, e: 'io' }],
      [.395, { sx: 1, sy: 1 }], [.405, { sx: 1.05, sy: .92 }], [.425, { sx: 1, sy: 1 }],
      [.455, { sx: 1, sy: 1 }], [.465, { sx: 1.05, sy: .92 }], [.485, { sx: 1, sy: 1 }],
      [.515, { sx: 1, sy: 1 }], [.525, { sx: 1.06, sy: .9 }], [.55, { cx: 582.5, cy: 650, sx: 1, sy: 1, o: 1 }],
      [.70, { cx: 411, cy: 618, sx: .8, sy: .72, o: 0, e: 'io' }]]);
    tl.track(basket, [[0, { o: 0, cx: 615, cy: 700 }], [.05, { o: 1, cx: 615, cy: 666, e: 'back' }], [.20, { o: 1, cx: 615, cy: 666 }], [.30, { o: 0, cx: 615, cy: 760, e: 'io' }]]);
    tl.track(bag, [[0, { o: 0, cx: 949, cy: 700 }], [.07, { o: 1, cx: 949, cy: 642, e: 'back' }], [.20, { o: 1, cx: 949, cy: 642 }], [.30, { o: 0, cx: 949, cy: 740, e: 'io' }]]);
    [['i_b1', .08], ['i_b2', .11], ['i_b3', .14]].forEach(function (b) {
      tl.track($(b[0]), [[b[1] - .03, { o: 0, sx: 0, sy: 0 }], [b[1] + .03, { o: 1, sx: 1, sy: 1, e: 'back' }], [.20, { o: 1, sx: 1, sy: 1 }], [.27, { o: 0, sx: .2, sy: .2, e: 'in' }]]);
    });
    // pike (izdelki) padajo v voziček
    var DS = .5686;
    tl.track($('i_d1'), [[.32, { o: 0, cx: 568, cy: 340, sx: DS, sy: DS }], [.33, { o: 1 }], [.40, { cx: 570, cy: 640, o: 1, e: 'in' }], [.415, { o: 0 }]]);
    tl.track($('i_d2'), [[.38, { o: 0, cx: 648, cy: 340, sx: DS, sy: DS }], [.39, { o: 1 }], [.46, { cx: 646, cy: 645, o: 1, e: 'in' }], [.475, { o: 0 }]]);
    tl.track($('i_dot'), [[.44, { o: 0, cx: 616.5, cy: 340, sx: DS, sy: DS }], [.45, { o: 1 }], [.52, { cx: 616.5, cy: 650.5, e: 'in' }], [.56, { cx: 616.5, cy: 650.5 }],
      [.70, { cx: 427.5, cy: 605.5, sx: 1, sy: 1, e: 'io' }]]);
    // U se vzpostavi, voziček izgine
    tl.track($('i_U'), [[.62, { o: 0, cx: 428, cy: 618, sx: 1.2, sy: 1.35 }], [.72, { o: 1, sx: 1, sy: 1, e: 'out' }]]);
    // siva črka PUNKT okoli U
    LET.forEach(function (L, i) {
      var el = $('i_' + L), s = .64 + i * .02;
      tl.track(el, [[s, { o: 0, f: GRAY }], [s + .10, { o: 1, f: GRAY, e: 'out' }]]);
    });
    for (var j = 0; j < 5; j++) {
      tl.track($('i_pr' + j), [[.74 + j * .012, { o: 0, f: GRAY, cy: 400 }], [.84 + j * .012, { o: 1, f: GRAY, cy: 471, e: 'out' }]]);
    }
    var sk = [561, 595, 628, 662, 695, 704, 738, 783, 816, 850, 884, 917, 955, 988, 1022];
    for (var k = 0; k < 15; k++) {
      var el = $('i_sk' + k), bb = el.getBBox(), cx = bb.x + bb.width / 2;
      tl.track(el, [[.78, { o: 0, f: GRAY, cx: cx + (k - 7) * 16 }], [.90 + k * .004, { o: 1, f: GRAY, cx: cx, e: 'out' }]]);
    }
    tl.cam([[0, { cx: 600, cy: 650, sx: 1.42 }], [.20, { cx: 600, cy: 650, sx: 1.42 }], [.32, { cx: 580, cy: 560, sx: 2.1, e: 'io' }], [.54, { cx: 580, cy: 560, sx: 2.1 }],
      [.66, { cx: 600, cy: 600, sx: 1.3, e: 'io' }], [1, { cx: 600, cy: 600, sx: 1.3 }]]);
    return { tl: tl, steps: [
      { t: 0, label: 'Nakup' }, { t: .20, label: 'Košarica' }, { t: .56, label: 'U' }, { t: .68, label: 'Pika' }, { t: .96, label: 'Logotip' }] ,
      caps: [[0, 'Nakup'], [.20, 'Košarica'], [.56, 'U = košarica'], [.68, 'Pika = nakup'], [.84, 'Pravi Punkt']] };
  }

  /* ---------- Logotip: siva -> črna -> poudarek -> končno ---------- */
  function logo(svg) {
    var tl = T.create({ cam: svg.querySelector('.cam') });
    LET.forEach(function (L) { tl.track($('l_' + L), [[0, { f: GRAY }], [.14, { f: GRAY }], [.34, { f: '#000000', e: 'io' }], [1, { f: '#000000' }]]) });
    for (var j = 0; j < 5; j++) tl.track($('l_pr' + j), [[0, { f: GRAY }], [.14 + j * .01, { f: GRAY }], [.34, { f: '#000000', e: 'io' }], [1, { f: '#000000' }]]);
    for (var k = 0; k < 15; k++) {
      tl.track($('l_sk' + k), [[0, { f: GRAY }], [.14 + k * .004, { f: GRAY }], [.34, { f: '#000000', e: 'io' }], [.50, { f: '#000000' }], [.67, { f: TEAL, e: 'io' }], [1, { f: TEAL }]]);
    }
    tl.track($('l_U'), [[0, { f: TEAL }], [1, { f: TEAL }]]);
    tl.track($('l_dot'), [[0, { f: TEAL }], [1, { f: TEAL }]]);
    tl.track($('l_hl'), [[0, { o: 0, sx: .5, sy: .5 }], [.50, { o: 0, sx: .5, sy: .5 }], [.67, { o: .4, sx: 1, sy: 1, e: 'back' }], [.78, { o: .4, sx: 1, sy: 1 }], [.90, { o: 0, sx: 1.15, sy: 1.15, e: 'io' }], [1, { o: 0 }]]);
    tl.cam([[0, { cx: 600, cy: 600, sx: 1.3 }], [.50, { cx: 600, cy: 600, sx: 1.3 }], [.67, { cx: 470, cy: 610, sx: 1.75, e: 'io' }], [.78, { cx: 470, cy: 610, sx: 1.75 }], [.92, { cx: 600, cy: 600, sx: 1.3, e: 'io' }], [1, { cx: 600, cy: 600, sx: 1.3 }]]);
    return { tl: tl, steps: [{ t: 0, label: 'Siva' }, { t: .34, label: 'Črna' }, { t: .67, label: 'Poudarek' }, { t: 1, label: 'Končno' }],
      caps: [[0, 'Siva'], [.30, 'Črna'], [.60, 'Poudarek'], [.92, 'Končno']] };
  }
  W.PraviScen = { idea: idea, logo: logo };
})(window);
