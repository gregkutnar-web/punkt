(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s) }, $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)) };
  var reduce = matchMedia('(prefers-reduced-motion:reduce)').matches, D = document.body.dataset;

  /* ---------- lebdeča navigacija ---------- */
  var nav = $('#nav'), links = $$('#nav a'), pill = $('#nav .pill');
  setTimeout(function () { nav.classList.add('on') }, reduce ? 0 : 1300);
  var secs = links.map(function (a) { return $(a.getAttribute('href')) }), curIdx = -1;
  function movePill() { var a = links[curIdx]; if (!a) { pill.classList.remove('on'); return } pill.style.left = a.offsetLeft + 'px'; pill.style.width = a.offsetWidth + 'px'; pill.classList.add('on') }
  function spy() {
    var line = innerHeight * .5, idx = -1;
    secs.forEach(function (s, i) { var r = s.getBoundingClientRect(); if (r.top <= line && r.bottom > line) idx = i });
    if (idx !== curIdx) { curIdx = idx; links.forEach(function (a, i) { a.classList.toggle('cur', i === idx) }); movePill() }
  }
  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: $(a.getAttribute('href')).getBoundingClientRect().top + scrollY, behavior: reduce ? 'auto' : 'smooth' });
    });
  });
  addEventListener('resize', movePill);
  var ticking = false;
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; spy() }) } }
  addEventListener('scroll', req, { passive: true }); addEventListener('resize', req); spy();

  /* ---------- logotip: usmeritev, ozadje, barva ---------- */
  var HEX = { t: '#00868f', k: '#000000', w: '#ffffff' };
  var VALID = { w: ['t', 'k'], k: ['t', 'w'], t: ['w'] };
  var plate = $('#plate'), seg = { o: $$('#oseg button'), bg: $$('#bseg button'), c: $$('#cseg button') };
  function sync() {
    var bg = plate.dataset.bg;
    if (VALID[bg].indexOf(plate.dataset.c) < 0) plate.dataset.c = VALID[bg][0];
    seg.bg.forEach(function (b) { b.classList.toggle('on', b.dataset.bg === bg) });
    seg.o.forEach(function (b) { b.classList.toggle('on', b.dataset.o === plate.dataset.o) });
    seg.c.forEach(function (b) { b.classList.toggle('on', b.dataset.c === plate.dataset.c); b.disabled = VALID[bg].indexOf(b.dataset.c) < 0 });
  }
  seg.o.forEach(function (b) { b.addEventListener('click', function () { plate.dataset.o = b.dataset.o; sync() }) });
  seg.bg.forEach(function (b) { b.addEventListener('click', function () { plate.dataset.bg = b.dataset.bg; sync() }) });
  seg.c.forEach(function (b) { b.addEventListener('click', function () { if (!b.disabled) { plate.dataset.c = b.dataset.c; sync() } }) });
  sync();

  function svgText() {
    var s = $('.lgx[data-o="' + plate.dataset.o + '"] svg', plate).cloneNode(true);
    s.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    s.removeAttribute('class'); s.removeAttribute('aria-hidden');
    var col = HEX[plate.dataset.c];
    $$('[fill="currentColor"]', s).forEach(function (p) { p.setAttribute('fill', col) });
    var vb = s.getAttribute('viewBox').split(' ').map(Number), w = 1200;
    s.setAttribute('width', w); s.setAttribute('height', Math.round(w * vb[3] / vb[2]));
    return { text: '<?xml version="1.0" encoding="UTF-8"?>\n' + new XMLSerializer().serializeToString(s), w: w, h: Math.round(w * vb[3] / vb[2]) };
  }
  function save(blob, name) { var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href) }, 4000) }
  function fname(ext) { return 'odiseja-' + plate.dataset.o + '-' + plate.dataset.c + '.' + ext }
  $('#dlsvg').addEventListener('click', function () { save(new Blob([svgText().text], { type: 'image/svg+xml' }), fname('svg')) });
  $('#dlpng').addEventListener('click', function () {
    var s = svgText(), img = new Image(), k = 2;
    img.onload = function () {
      var c = document.createElement('canvas'); c.width = s.w * k; c.height = s.h * k;
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      c.toBlob(function (b) { save(b, fname('png')) }, 'image/png');
    };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(s.text);
  });

  /* ---------- najmanjša velikost ---------- */
  var PXMM = 96 / 25.4, rng = $('#msz'), mpx = $('#mpx');
  function size() {
    var v = +rng.value;
    $('#sh').style.width = v + 'px'; $('#sv').style.width = v + 'px';
    mpx.textContent = v + ' px · ' + (v / PXMM).toFixed(0) + ' mm';
    [['sh_s', 40], ['sv_s', 23]].forEach(function (m) {
      var ok = v / PXMM >= m[1], e = $('#' + m[0]);
      e.textContent = ok ? '✓ ' + D.ok : '✕ ' + D.small; e.className = ok ? 'ok' : 'bad';
    });
  }
  rng.addEventListener('input', size); size();

  /* ---------- kopiranje barv ---------- */
  $$('.swc').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.dataset.hex, i = $('i', b);
      function done() { i.textContent = D.copied; setTimeout(function () { i.textContent = D.copy }, 1400) }
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, done); else done();
    });
  });
})();
