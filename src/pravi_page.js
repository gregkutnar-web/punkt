(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s) }, $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)) };
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x }
  var reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;

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
      e.preventDefault(); stopPlay();
      window.scrollTo({ top: $(a.getAttribute('href')).getBoundingClientRect().top + scrollY, behavior: reduce ? 'auto' : 'smooth' });
    });
  });
  addEventListener('resize', movePill);

  /* ---------- scroll-scrub prizori ---------- */
  function prog(el) { var t = el.offsetHeight - innerHeight; return t <= 0 ? 0 : cl(-el.getBoundingClientRect().top / t) }
  var playing = null;
  function stopPlay() { if (playing) { playing.stop(); playing = null } }
  ['wheel', 'touchstart', 'keydown'].forEach(function (ev) { addEventListener(ev, stopPlay, { passive: true }) });
  var binders = [];

  function bindScene(id, make) {
    var sec = $('#' + id), scrub = $('.scrub', sec), svg = $('.stage', sec), sc = make(svg), tl = sc.tl;
    var chips = $('.chips', sec), capEl = $('.cap span', sec), bar = $('.bar i', sec), btn = $('.play', sec), capNow = '';
    function topY() { return scrub.getBoundingClientRect().top + scrollY }
    function total() { return scrub.offsetHeight - innerHeight }
    function go(t) { stopPlay(); window.scrollTo({ top: topY() + t * total(), behavior: reduce ? 'auto' : 'smooth' }) }
    var cbs = sc.steps.map(function (s) { var b = document.createElement('button'); b.textContent = s.label; b.onclick = function () { go(s.t) }; chips.appendChild(b); return b });
    function update() {
      var p = prog(scrub); tl.render(p);
      var act = 0; sc.steps.forEach(function (s, i) { if (p >= s.t - .02) act = i }); cbs.forEach(function (b, i) { b.classList.toggle('on', i === act) });
      var c = sc.caps[0][1]; sc.caps.forEach(function (x) { if (p >= x[0]) c = x[1] });
      if (c !== capNow) { capNow = c; capEl.classList.add('sw'); setTimeout(function () { capEl.textContent = c; capEl.classList.remove('sw') }, reduce ? 0 : 160) }
      bar.style.width = (p * 100) + '%';
    }
    btn.addEventListener('click', function () {
      if (playing && playing.btn === btn) { stopPlay(); return }
      stopPlay();
      var t0 = topY(), tot = total(), from = scrollY;
      if (from >= t0 + tot - 6 || from < t0 - 4) from = t0;
      var dur = 22000 * (1 - (from - t0) / tot), tt0 = performance.now(), alive = true, raf = 0;
      if (from !== scrollY) window.scrollTo(0, from);
      btn.textContent = 'Pavza';
      playing = { btn: btn, stop: function () { alive = false; cancelAnimationFrame(raf); btn.textContent = 'Predvajaj' } };
      (function f(now) {
        if (!alive) return;
        var p = Math.min(1, (now - tt0) / dur); window.scrollTo(0, from + (t0 + tot - from) * p);
        if (p < 1) raf = requestAnimationFrame(f); else stopPlay();
      })(tt0);
    });
    binders.push({ el: scrub, update: update }); update();
  }
  bindScene('ideja', PraviScen.idea);
  bindScene('logotip', PraviScen.logo);

  /* ---------- ikona ---------- */
  var icons = $('#icons'), isz = $('#isize'), ipx = $('#ipx');
  var sz0 = innerWidth < 820 ? 150 : 260; isz.max = sz0; isz.value = sz0; icons.style.setProperty('--sz', sz0 + 'px'); ipx.textContent = sz0 + ' px';
  isz.addEventListener('input', function () { icons.style.setProperty('--sz', isz.value + 'px'); ipx.textContent = isz.value + ' px' });

  /* ---------- različice ---------- */
  var plate = $('#plate2'), vb = $$('#vseg button');
  vb.forEach(function (b) { b.addEventListener('click', function () { vb.forEach(function (x) { x.classList.remove('on') }); b.classList.add('on'); plate.dataset.m = b.dataset.m }) });

  /* ---------- scroll zanka ---------- */
  var ticking = false;
  function frame() { ticking = false; spy(); binders.forEach(function (b) { var r = b.el.getBoundingClientRect(); if (r.bottom > -200 && r.top < innerHeight + 200) b.update() }) }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame) } }
  addEventListener('scroll', req, { passive: true }); addEventListener('resize', req);
  frame();
})();
