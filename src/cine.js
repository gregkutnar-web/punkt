/* Predvajalnik za časovno animacijo »Nastanek«: samodejni začetek, pavza, seek, hitrost, poglavja. */
(function (W) {
  'use strict';
  function $(s, r) { return (r || document).querySelector(s) }
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x }
  function create(sec, sc) {
    var tl = sc.tl, dur = sc.duration, t = 0, playing = false, speed = 1, last = 0, raf = 0, wantPlay = false, visible = false;
    var btn = $('.play', sec), seek = $('.seek', sec), fill = $('i', seek), knob = $('b', seek), tm = $('.tm', sec), spd = $('.spd', sec), chips = $('.chips', sec), cap = $('.cap span', sec);
    var reduce = matchMedia('(prefers-reduced-motion:reduce)').matches, capNow = '', capCol = '';
    sc.chapters.forEach(function (c) { var m = document.createElement('span'); m.className = 'tkm'; m.style.left = (c.t / dur * 100) + '%'; seek.appendChild(m) });
    var cbs = sc.chapters.map(function (c) { var b = document.createElement('button'); b.textContent = c.label; b.onclick = function () { go(c.t, true) }; chips.appendChild(b); return b });

    function fmt(x) { var s = Math.floor(x); return Math.floor(s / 60) + ':' + (s % 60 < 10 ? '0' : '') + (s % 60) }
    function ui() {
      var p = t / dur; fill.style.width = (p * 100) + '%'; knob.style.left = (p * 100) + '%'; tm.textContent = fmt(t);
      var act = 0; sc.chapters.forEach(function (c, i) { if (t >= c.t - .01) act = i }); cbs.forEach(function (b, i) { b.classList.toggle('on', i === act) });
      var c = sc.caps[0], col = ''; sc.caps.forEach(function (x) { if (t >= x[0]) c = x });
      if (c[1] !== capNow) { capNow = c[1]; cap.textContent = capNow; cap.classList.remove('pop'); void cap.offsetWidth; cap.classList.add('pop') }
      var nc = c[2] || ''; if (nc !== capCol) { capCol = nc; cap.style.color = nc }
      btn.textContent = playing ? 'Pavza' : (t >= dur - .01 ? 'Ponovi' : 'Predvajaj');
    }
    function render() { tl.render(t); ui() }
    function tick(now) {
      if (!playing) return;
      t = Math.min(dur, t + Math.max(0, (now - last) / 1000) * speed); last = now; render();
      if (t >= dur) { playing = false; ui(); return }
      raf = requestAnimationFrame(tick);
    }
    function play() { if (t >= dur - .01) t = 0; playing = true; wantPlay = true; last = performance.now(); cancelAnimationFrame(raf); raf = requestAnimationFrame(tick); ui() }
    function pause() { playing = false; wantPlay = false; cancelAnimationFrame(raf); ui() }
    function go(x, keep) { t = Math.max(0, Math.min(dur, x)); render(); if (keep && !playing) play() }
    btn.onclick = function () { playing ? pause() : play() };
    spd.onclick = function () { speed = speed === 1 ? 2 : 1; spd.textContent = speed + '×' };
    function pos(e) { var r = seek.getBoundingClientRect(); return cl((e.clientX - r.left) / r.width) * dur }
    var drag = false, was = false;
    seek.addEventListener('pointerdown', function (e) { drag = true; was = playing; playing = false; cancelAnimationFrame(raf); seek.setPointerCapture(e.pointerId); go(pos(e)) });
    seek.addEventListener('pointermove', function (e) { if (drag) go(pos(e)) });
    function up() { if (!drag) return; drag = false; if (was) play(); else ui() }
    seek.addEventListener('pointerup', up); seek.addEventListener('pointercancel', up);
    addEventListener('keydown', function (e) {
      if (e.code !== 'Space' || !visible || /INPUT|BUTTON|TEXTAREA/.test((e.target || {}).tagName || '')) return;
      e.preventDefault(); playing ? pause() : play();
    });
    // samodejni začetek ob vstopu, pavza ob izstopu
    var started = false;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        visible = e.isIntersecting;
        if (e.isIntersecting && e.intersectionRatio >= .55 && !started && !reduce) { started = true; play() }
        else if (!e.isIntersecting && playing) { playing = false; cancelAnimationFrame(raf); wantPlay = true; ui() }
        else if (e.isIntersecting && wantPlay && !playing && e.intersectionRatio >= .4) { play() }
      });
    }, { threshold: [0, .4, .55, .8] }).observe(sec);
    if (reduce) { t = dur; }
    render();
    return { go: go, play: play, pause: pause, dur: dur, time: function () { return t } };
  }
  W.CinePlayer = { create: create };
})(window);
