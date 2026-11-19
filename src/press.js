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
  var HEX = { t: '#00b1bc', k: '#000000', w: '#ffffff' };
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
  $('#dlsvg').addEventListener('click', function () { gate(function () { save(new Blob([svgText().text], { type: 'image/svg+xml' }), fname('svg')) }) });
  $('#dlpng').addEventListener('click', function () { gate(function () {
    var s = svgText(), img = new Image(), k = 2;
    img.onload = function () {
      var c = document.createElement('canvas'); c.width = s.w * k; c.height = s.h * k;
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      c.toBlob(function (b) { save(b, fname('png')) }, 'image/png');
    };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(s.text);
  }) });


  /* ---------- pogoji uporabe: pred vsakim prenosom ---------- */
  var tm = $('#tmodal'), chk = $('#tchk'), tok = $('#tok'), pending = null, accepted = false, lastFocus = null;
  function openT(fn) {
    pending = fn || null; lastFocus = document.activeElement; chk.checked = false; tok.disabled = true;
    $('#tbody').scrollTop = 0; tm.hidden = false; document.body.style.overflow = 'hidden'; $('#tbody').focus();
  }
  function closeT() { tm.hidden = true; document.body.style.overflow = ''; pending = null; if (lastFocus && lastFocus.focus) lastFocus.focus() }
  function gate(fn) { if (accepted) fn(); else openT(fn) }
  chk.addEventListener('change', function () { tok.disabled = !chk.checked });
  tok.addEventListener('click', function () { if (!chk.checked) return; accepted = true; var f = pending; tm.hidden = true; document.body.style.overflow = ''; pending = null; if (f) f(); });
  $('#tcancel').addEventListener('click', closeT); $('#tclose').addEventListener('click', closeT);
  tm.addEventListener('click', function (e) { if (e.target === tm) closeT() });
  addEventListener('keydown', function (e) {
    if (tm.hidden) return;
    if (e.key === 'Escape') closeT();
    if (e.key === 'Tab') {   // fokus ostane v oknu
      var f = [].slice.call(tm.querySelectorAll('button:not([disabled]),input,[tabindex="0"]')), i = f.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus() } else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus() }
    }
  });
  $('#openterms').addEventListener('click', function () { openT(null) });
  $('#zip').addEventListener('click', function (e) {
    e.preventDefault();
    gate(function () { var a = document.createElement('a'); a.href = $('#zip').dataset.file; a.download = ''; document.body.appendChild(a); a.click(); a.remove() });
  });

  /* ---------- najmanjša velikost (pravi mm, ravnilo) ---------- */
  var PXMM = 96 / 25.4, MIN = { h: 40, v: 23 }, mode = 'h';
  var rng = $('#msz'), mpx = $('#mpx'), stage = $('#mstage'), mbox = $('#mbox'), chip = $('#mchip'), mark = $('#mmark'), dimEl = $('#mdim'), dimTx = $('#mdim span'), lastVal = {};
  function vbRatio() { var vb = $('.m' + mode + ' svg', mbox).getAttribute('viewBox').split(' ').map(Number); return vb[3] / vb[2] }
  function setRange(keep) {
    var maxMm = Math.floor((stage.clientWidth - 48) / PXMM), cap = mode === 'h' ? 100 : 60;
    rng.min = 10; rng.max = Math.max(MIN[mode] + 5, Math.min(cap, maxMm));
    if (!keep) rng.value = MIN[mode];
    if (+rng.value > +rng.max) rng.value = rng.max;
    var pos = (MIN[mode] - rng.min) / (rng.max - rng.min) * 100;
    rng.style.setProperty('--mp', pos + '%');
    var thumb = 13, tw = rng.clientWidth || 1;
    mark.style.left = (thumb + (tw - 2 * thumb) * pos / 100) + 'px';
  }
  function size() {
    var v = +rng.value, ok = v >= MIN[mode], w = v * PXMM;
    stage.dataset.m = mode; stage.dataset.ok = ok ? '1' : '0';
    mbox.style.width = w + 'px';
    dimEl.style.width = w + 'px'; dimTx.textContent = v + ' mm';
    mpx.textContent = v + ' mm';
    chip.textContent = ok ? '✓ ' + v + ' mm · ' + D.ok : '✕ ' + v + ' mm · ' + D.small + ' (' + D.minabbr + ' ' + MIN[mode] + ' mm)';
    rng.setAttribute('aria-valuetext', mpx.textContent + (ok ? ', ' + D.ok : ', ' + D.small));
  }
  $$('#mseg button').forEach(function (b) {
    b.addEventListener('click', function () {
      lastVal[mode] = +rng.value; mode = b.dataset.m;
      $$('#mseg button').forEach(function (x) { x.classList.toggle('on', x === b) });
      setRange(false); if (lastVal[mode]) rng.value = Math.min(lastVal[mode], rng.max); size();
    });
  });
  function toMin() { rng.value = MIN[mode]; size() }
  $('#mreset').addEventListener('click', toMin); mark.addEventListener('click', toMin);
  rng.addEventListener('input', function () {
    var v = +rng.value; if (Math.abs(v - MIN[mode]) <= 1) rng.value = MIN[mode];   // magnetno ob minimumu
    size();
  });
  addEventListener('resize', function () { setRange(true); size() });
  setRange(false); size();

  /* ---------- kopiranje barv ---------- */
  $$('.swc').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.dataset.hex, i = $('i', b);
      function done() { i.textContent = D.copied; setTimeout(function () { i.textContent = D.copy }, 1400) }
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, done); else done();
    });
  });
})();
