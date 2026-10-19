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
      e.preventDefault();
      window.scrollTo({ top: $(a.getAttribute('href')).getBoundingClientRect().top + scrollY, behavior: reduce ? 'auto' : 'smooth' });
    });
  });
  addEventListener('resize', movePill);

  /* ---------- nastanek: časovna animacija ---------- */
  function stopPlay() { }
  var cine = CinePlayer.create($('#nastanek'), Cine.build($('#nastanek .stage')));
  window.__cine = cine;

  /* ---------- logotip: končno / s poudarkom ---------- */
  var p1 = $('#plate1'), hb = $$('#hseg button');
  hb.forEach(function (b) { b.addEventListener('click', function () { hb.forEach(function (x) { x.classList.remove('on') }); b.classList.add('on'); p1.dataset.h = b.dataset.h }) });

  /* ---------- ikona ---------- */
  var icons = $('#icons'), isz = $('#isize'), ipx = $('#ipx');
  var sz0 = innerWidth < 820 ? 150 : 260; isz.max = sz0; isz.value = sz0; icons.style.setProperty('--sz', sz0 + 'px'); ipx.textContent = sz0 + ' px';
  isz.addEventListener('input', function () { icons.style.setProperty('--sz', isz.value + 'px'); ipx.textContent = isz.value + ' px' });

  /* ---------- različice ---------- */
  var plate = $('#plate2'), vb = $$('#vseg button');
  vb.forEach(function (b) { b.addEventListener('click', function () { vb.forEach(function (x) { x.classList.remove('on') }); b.classList.add('on'); plate.dataset.m = b.dataset.m }) });

  /* ---------- scroll zanka ---------- */
  var ticking = false;
  function frame() { ticking = false; spy() }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame) } }
  addEventListener('scroll', req, { passive: true }); addEventListener('resize', req);
  frame();
})();
