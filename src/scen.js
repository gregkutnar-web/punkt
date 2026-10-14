/* Scenarija animacij razvoja: [ime dela, [[artboard, pot, opcije], ...]]
   opcije: x = prelitje (druga oblika), flip = zrcaljenje, from = od kod pride, out = kam odide,
   d = zakasnitev (0..1), wipe = nariše se, s0 = začetna velikost.  Pot = indeksi (0-based) po nivojih. */
(function (W) {
  var FL = { flip: 1 }, R = [];
  function add(name, list) { R.push([name, list]) }
  function range(n) { var a = []; for (var i = 0; i < n; i++) a.push(i); return a }

  /* ---------- osnutek 1 (14 artboardov) ---------- */
  var S1 = [], SP = { from: [110, 0], d: .1 };
  R = S1;
  add('P', [[0, '0_0_0'], [1, '1_0_0'], [2, '2_0_0'], [3, '3_0', { out: [-170, 0] }]]);
  add('K', [[0, '0_0_3'], [1, '1_0_2'], [2, '2_0_1'], [3, '3_1', { out: [170, 0] }]]);
  add('T', [[0, '0_0_4'], [1, '1_0_3'], [2, '2_0_2'], [3, '3_2', { out: [190, 0] }]]);
  add('N', [[0, '0_0_2']]);
  // ligatura UN -> znak -> leva enota znaka (L) skozi vse artboarde
  add('L', [[0, '0_0_1'], [1, '1_0_1', { x: 1 }], [2, '2_0_3'], [3, '3_3'], [4, '4_0'], [5, '5_0'], [6, '6_0', { x: 1 }], [7, '7_0_1', { x: 1 }],
    [8, '8_3_1'], [9, '9_0_1'], [10, '10_0_1', FL], [11, '11_0_1'], [12, '12_1_0_0_1', FL], [13, '13_0_0_0_1', { x: 1 }]]);
  add('Rt', [[7, '7_0_0', SP], [8, '8_3_0'], [9, '9_0_0'], [10, '10_0_0', FL], [11, '11_0_0'], [12, '12_1_0_0_0', FL], [13, '13_0_0_0_0', { x: 1 }]]);
  add('gU', [[3, '3_4_0', { wipe: 1 }], [4, '4_1_0']]);
  add('gN', [[3, '3_4_1', { wipe: 1, d: .25 }], [4, '4_1_1']]);
  // artboard 9: tri različice napisa + oznake
  add('r1', [[8, '8_0_0'], ]); add('r1b', [[8, '8_0_1']]); add('r1c', [[8, '8_0_2']]); add('r1d', [[8, '8_0_3']]);
  add('alt', [[8, '8_1', { d: .1 }]]);
  add('r2', [[8, '8_2_0']]); add('r2b', [[8, '8_2_1']]); add('r2c', [[8, '8_2_2']]); add('r2d', [[8, '8_2_3']]);
  add('novi', [[8, '8_8', { from: [0, -14] }]]);
  add('oC', [[8, '8_9', { d: .5, s0: .6 }]]); add('oT', [[8, '8_10', { d: .6 }]]); add('oX', [[8, '8_11', { d: .55, s0: .5 }]]);
  // napis PUNKT (črke) skozi artboarde
  add('Wp', [[8, '8_4', { from: [0, 14] }], [9, '9_1_0'], [10, '10_1'], [12, '12_1_0_1_0', { from: [-110, 0] }], [13, '13_0_0_1_0']]);
  add('Wu', [[8, '8_5', { from: [0, 14] }], [9, '9_1_1', { x: 1 }], [10, '10_2'], [12, '12_1_0_1_1', { from: [-110, 0], d: .1 }], [13, '13_0_0_1_1']]);
  add('Wn', [[9, '9_1_2', { d: .15 }], [10, '10_3'], [12, '12_1_0_1_2', { from: [-110, 0], d: .15 }], [13, '13_0_0_1_2']]);
  add('Wk', [[8, '8_6', { from: [0, 14] }], [9, '9_1_3'], [10, '10_4'], [12, '12_1_0_1_3', { from: [-110, 0], d: .2 }], [13, '13_0_0_1_3']]);
  add('Wt', [[8, '8_7', { from: [0, 14] }], [9, '9_1_4'], [10, '10_5'], [12, '12_1_0_1_4', { from: [-110, 0], d: .25 }], [13, '13_0_0_1_4']]);
  range(13).forEach(function (k) {
    add('B' + k, [[9, '9_2_' + k, { from: [0, 10], d: .2 + k * .04 }], [12, '12_1_1_' + k, { from: [0, 10], d: .3 + k * .03 }], [13, '13_0_1_' + k]]);
  });
  range(4).forEach(function (k) { add('D' + k, [[11, '11_1_' + k, { from: [0, 40], d: .2 + k * .14, s0: .4 }]]) });
  // artboard 14: kombinacije z »novi« in križci
  add('v2', [[13, '13_0_2', { from: [0, -10] }]]); add('x2', [[13, '13_3', { d: .5, s0: .4 }]]);
  add('v1', [[13, '13_1_0', { d: .1 }]]); add('v1n', [[13, '13_1_1', { d: .2 }]]); add('x1', [[13, '13_2', { d: .55, s0: .4 }]]);

  /* ---------- osnutek 2 (10 artboardov) ---------- */
  var S2 = []; R = S2;
  add('BAN', [[8, '8_1', { from: [-120, 0] }]]);   // podlaga (trak) pod lockupom
  add('SUN', [[0, '0_0_2']]);
  var rayD0 = { 0: '0_0_0', 1: '0_0_1', 6: '0_0_3', 7: '0_0_4', 8: '0_0_5', 9: '0_0_6', 10: '0_0_7', 11: '0_0_8' };
  range(12).forEach(function (i) {
    var l = [];
    if (rayD0[i]) l.push([0, rayD0[i]]);
    l.push([1, '1_0_' + i, rayD0[i] ? {} : { d: .2 }]); l.push([2, '2_1_' + i, { x: 1 }]);
    add('R' + i, l);
  });
  range(12).forEach(function (i) {
    add('S' + i, [[2, '2_0_' + i, { d: i * .03 }], [3, '3_0_' + i], [4, '4_0_0_' + i], [5, '5_0_' + i], [6, '6_0_' + i], [7, '7_2_' + i], [8, '8_2_0_' + i], [9, '9_0_' + i]]);
  });
  range(5).forEach(function (j) {
    add('P' + j, [[4, '4_0_1_' + j, { from: [0, 14], d: .1 + j * .06 }], [5, '5_1_' + j], [6, '6_1_' + j], [7, '7_1_' + j], [8, '8_2_1_0_' + j], [9, '9_3_' + j]]);
    add('V' + j, [[4, '4_1_0_' + j, { from: [0, 14], d: .2 + j * .06 }]]);
  });
  range(12).forEach(function (i) { add('VM' + i, [[4, '4_1_1_' + i, { d: .2 + i * .02 }]]) });
  range(13).forEach(function (k) {
    add('B' + k, [[5, '5_2_' + k, { from: [0, 8], d: .3 + k * .03 }], [6, '6_2_' + k], [8, '8_2_1_1_' + k, { from: [0, 8], d: .3 + k * .02 }], [9, '9_4_' + k]]);
  });
  range(4).forEach(function (j) { add('N' + j, [[7, '7_0_' + j, { from: [0, -12], d: .2 + j * .08 }], [9, '9_2_0_' + j, { from: [0, -8], d: .2 + j * .05 }]]) });
  // temna različica: dodatni lockupi
  range(12).forEach(function (i) {
    add('DT' + i, [[9, '9_1_0_' + i, { d: .2 + i * .02 }]]);
    add('DM' + i, [[9, '9_2_2_' + i, { d: .3 + i * .02 }]]);
  });
  range(5).forEach(function (j) {
    add('DW' + j, [[9, '9_1_1_' + j, { from: [0, 10], d: .3 + j * .05 }]]);
    add('DP' + j, [[9, '9_2_1_' + j, { from: [0, 10], d: .4 + j * .05 }]]);
  });
  range(13).forEach(function (k) { add('DB' + k, [[9, '9_5_' + k, { from: [0, 6], d: .4 + k * .02 }]]) });

  W.SCEN = {
    1: { actors: S1, pattern: { board: 12, src: 'a1_12_0' } },
    2: { actors: S2, pattern: { board: 8, src: 'a2_8_0' }, camera: [null, null, null, null, null, null, null, null, { s: 3.3, x: 0, y: 0 }] }
  };
})(window);
