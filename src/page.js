(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s) }, $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)) };
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x }
  var ease = Stage.ease;
  var reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;

  /* slike makete (en vir, več uporab) */
  $$('img[data-m]').forEach(function (im) { im.src = MOCK[+im.dataset.m] });

  /* ---------- lebdeča navigacija ---------- */
  var nav = $('#nav'), links = $$('#nav a'), pill = $('#nav .pill');
  setTimeout(function () { nav.classList.add('on') }, reduce ? 0 : 1300);
  var secs = links.map(function (a) { return $(a.getAttribute('href')) }), curIdx = -1;
  function movePill() {
    var a = links[curIdx];
    if (!a) { pill.classList.remove('on'); return }
    pill.style.left = a.offsetLeft + 'px'; pill.style.width = a.offsetWidth + 'px'; pill.classList.add('on');
  }
  function spy() {
    var line = innerHeight * .5, idx = -1;
    secs.forEach(function (s, i) { var r = s.getBoundingClientRect(); if (r.top <= line && r.bottom > line) idx = i });
    if (idx !== curIdx) { curIdx = idx; links.forEach(function (a, i) { a.classList.toggle('cur', i === idx) }); movePill() }
  }
  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault(); stopPlay();
      var t = $(a.getAttribute('href'));
      window.scrollTo({ top: t.getBoundingClientRect().top + scrollY, behavior: reduce ? 'auto' : 'smooth' });
    });
  });
  addEventListener('resize', movePill);

  /* ---------- skupni scroll ---------- */
  function prog(el) { var t = el.offsetHeight - innerHeight; return t <= 0 ? 0 : cl(-el.getBoundingClientRect().top / t) }
  var playing = null;
  function stopPlay() { if (playing) { playing.stop(); playing = null } }
  ['wheel', 'touchstart', 'keydown'].forEach(function (ev) { addEventListener(ev, stopPlay, { passive: true }) });

  /* ---------- razvoj logotipa (osnutka 1 in 2) ---------- */
  var binders = [];
  function bindStage(idea) {
    var sec = $('#o' + idea), scrub = $('.scrub', sec), cfg = CFG[idea], sc = SCEN[idea], N = cfg.boards.length;
    var film = $('.film', sec), cnt = $('.cnt', sec), bar = $('.bar i', sec), btn = $('.play', sec), ths = [];
    function topY() { return scrub.getBoundingClientRect().top + scrollY }
    function total() { return scrub.offsetHeight - innerHeight }
    function go(b) { stopPlay(); window.scrollTo({ top: topY() + b / (N - 1) * total(), behavior: reduce ? 'auto' : 'smooth' }) }
    var st = Stage.create({
      svg: $('.stage', sec), idea: idea, boards: cfg.boards, actors: sc.actors, pattern: sc.pattern, camera: sc.camera, hold: .4,
      onPos: function (p, act) {
        ths.forEach(function (t, i) { t.classList.toggle('on', i === act) });
        cnt.textContent = (act < 9 ? '0' : '') + (act + 1) + ' / ' + N;
        bar.style.width = (p / (N - 1) * 100) + '%';
      }
    });
    ths = Stage.thumbs(idea, cfg.boards, film, go);
    function update() { st.setPos(prog(scrub) * (N - 1)); var a = ths[Math.round(st.getPos())]; if (a && film.scrollWidth > film.clientWidth) film.scrollLeft = a.offsetLeft - film.clientWidth / 2 + a.clientWidth / 2 }
    btn.addEventListener('click', function () {
      if (playing && playing.btn === btn) { stopPlay(); return }
      stopPlay();
      var t0 = topY(), tot = total(), from = scrollY;
      if (from >= t0 + tot - 6 || from < t0 - 4) from = t0;
      var dur = (N - 1) * 1900 * (1 - (from - t0) / tot), tt0 = performance.now(), alive = true, raf = 0;
      if (from !== scrollY) window.scrollTo(0, from);
      btn.textContent = 'Pavza';
      playing = { btn: btn, stop: function () { alive = false; cancelAnimationFrame(raf); btn.textContent = 'Predvajaj' } };
      (function f(now) {
        if (!alive) return;
        var p = Math.min(1, (now - tt0) / dur);
        window.scrollTo(0, from + (t0 + tot - from) * p);
        if (p < 1) raf = requestAnimationFrame(f); else stopPlay();
      })(tt0);
    });
    binders.push({ el: scrub, update: update });
    update();
  }
  bindStage(1); bindStage(2);

  /* ---------- končni osnutek: razkritje in preklop ---------- */
  $$('.final').forEach(function (f) {
    var plate = $('.plate', f);
    new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) f.classList.add('in') }) }, { threshold: .35 }).observe(f);
    $$('.seg button', f).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.seg button', f).forEach(function (x) { x.classList.remove('on') }); b.classList.add('on');
        plate.classList.toggle('dk', b.dataset.m === 'dark');
      });
    });
  });

  /* ---------- mockup: približek na napis ---------- */
  $$('.mock').forEach(function (m) {
    var img = $('img', m), view = $('.view', m), fxi = +m.dataset.fx, fyi = +m.dataset.fy, IA = 1800 / 839;
    function update() {
      var p = prog(m), z = ease(cl((p - .08) / .8));
      // točka znaka v koordinatah okvirja (object-fit: cover prireže stranice)
      var va = view.clientWidth / view.clientHeight, vf = Math.min(1, va / IA), hf = Math.min(1, IA / va);
      var px = vf < 1 ? cl((fxi - vf / 2) / (1 - vf)) : 0, py = hf < 1 ? cl((fyi - hf / 2) / (1 - hf)) : 0;
      img.style.objectPosition = (px * 100).toFixed(1) + '% ' + (py * 100).toFixed(1) + '%';
      var fx = (fxi - (1 - vf) * px) / vf, fy = (fyi - (1 - hf) * py) / hf;
      img.style.transformOrigin = (fx * 100).toFixed(2) + '% ' + (fy * 100).toFixed(2) + '%';
      img.style.transform = 'translate(' + ((.5 - fx) * 100 * z).toFixed(2) + '%,' + ((.46 - fy) * 100 * z).toFixed(2) + '%) scale(' + (1 + 1.25 * z).toFixed(4) + ')';
    }
    binders.push({ el: m, update: update }); update();
  });

  /* ---------- osnutek 3: 2D animacija ---------- */
  var o3 = (function () {
    var svg = $('#stage3'), ring = $('#o3r'), parts = {};
    $$('[data-c]', svg).forEach(function (e) { e.style.color = e.getAttribute('data-c') });
    function g(i) { return document.getElementById('a3_0_0_0_' + i) }
    var P = g(0), U = g(1), K = g(2), T = g(3), Nn = g(4), D = g(5), sub = []; for (var i = 0; i < 13; i++) sub.push(document.getElementById('a3_0_0_1_' + i));
    [P, U, K, T, Nn, D].concat(sub).forEach(function (e) { e.style.transformBox = 'fill-box' });
    var anims = [];
    function A(el, kf, opt) { var a = el.animate(kf, Object.assign({ fill: 'both', easing: 'cubic-bezier(.2,.8,.2,1)' }, opt)); anims.push(a); return a }
    function play() {
      anims.forEach(function (a) { a.cancel() }); anims = [];
      var db = D.getBBox(), ub = U.getBBox();
      // črke zdrsnejo na mesto
      [[P, -1, 0], [Nn, 0, 120], [K, 0, 200], [T, 1, 280]].forEach(function (c) {
        var el = c[0], dir = c[1] || (el === Nn ? -1 : 1);
        el.style.transformOrigin = '50% 50%';
        A(el, [{ opacity: 0, transform: 'translateX(' + dir * 90 + 'px)' }, { opacity: 1, transform: 'none' }], { duration: 900, delay: c[2] });
      });
      // U se dvigne od spodaj
      U.style.transformOrigin = '50% 100%';
      A(U, [{ opacity: 0, transform: 'scaleY(.05)' }, { opacity: 1, transform: 'scaleY(1)' }], { duration: 800, delay: 450 });
      // pika pade v U
      var fall = 340;
      D.style.transformOrigin = '50% 100%';
      A(D, [{ opacity: 0, transform: 'translateY(' + -fall + 'px) scale(1,1.15)', offset: 0, easing: 'cubic-bezier(.55,0,1,.45)' },
        { opacity: 1, transform: 'translateY(0) scale(1,1.1)', offset: .5 },
        { transform: 'translateY(0) scale(1.35,.6)', offset: .62, easing: 'ease-out' },
        { transform: 'translateY(-26px) scale(.92,1.1)', offset: .78, easing: 'ease-in' },
        { transform: 'translateY(0) scale(1.12,.86)', offset: .9 },
        { transform: 'translateY(0) scale(1,1)', offset: 1 }], { duration: 1500, delay: 1000, easing: 'linear' });
      A(U, [{ transform: 'scaleY(1)' }, { transform: 'scaleY(.97)' }, { transform: 'scaleY(1)' }], { duration: 380, delay: 1000 + 1500 * .5, easing: 'ease-out', fill: 'forwards' });
      // valovanje
      var cx = db.x + db.width / 2, cy = db.y + db.height / 2;
      ring.setAttribute('cx', cx); ring.setAttribute('cy', cy);
      A(ring, [{ opacity: .7, r: '10px' }, { opacity: 0, r: '85px' }], { duration: 1100, delay: 1000 + 1500 * .5, easing: 'cubic-bezier(.2,.7,.2,1)' });
      // podnapis se razširi v mesto
      sub.forEach(function (el, k) {
        A(el, [{ opacity: 0, transform: 'translateX(' + (k - 6) * 9 + 'px)' }, { opacity: 1, transform: 'none' }], { duration: 900, delay: 2200 + k * 40 });
      });
    }
    function hop() {
      D.animate([{ transform: 'translateY(0)' }, { transform: 'translateY(-44px) scale(.95,1.08)', offset: .45, easing: 'ease-in' }, { transform: 'translateY(0) scale(1.15,.82)', offset: .8 }, { transform: 'none' }], { duration: 650, easing: 'ease-out' });
    }
    U.style.cursor = D.style.cursor = 'pointer';
    [U, D].forEach(function (e) { e.addEventListener('click', function (ev) { ev.stopPropagation(); hop() }) });
    $('#o3play').addEventListener('click', play);
    var started = false;
    new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting && !started) { started = true; play() } }) }, { threshold: .6 }).observe(svg);
    return { play: play };
  })();

  /* ---------- primerjava mockupov ---------- */
  (function () {
    var acc = $('#acc'), ps = $$('.p', acc);
    function on(p) { ps.forEach(function (x) { x.classList.toggle('on', x === p) }); acc.classList.add('has') }
    ps.forEach(function (p) {
      p.addEventListener('mouseenter', function () { if (matchMedia('(hover:hover)').matches) on(p) });
      p.addEventListener('click', function () { on(p) });
    });
    acc.addEventListener('mouseleave', function () { if (matchMedia('(hover:hover)').matches) { acc.classList.remove('has'); ps.forEach(function (x) { x.classList.remove('on') }) } });
  })();

  /* ---------- primerjava logotipov ---------- */
  (function () {
    var sec = $('#pl'), lg = $('#lg'), svgs = $$('.lc svg', lg), mono = false, blur = 0;
    function filt() { svgs.forEach(function (s) { s.style.filter = (mono ? 'grayscale(1) ' : '') + 'blur(' + blur + 'px)' }) }
    $('#psize').addEventListener('input', function (e) { lg.style.setProperty('--w', e.target.value) });
    $('#pblur').addEventListener('input', function (e) { blur = +e.target.value; filt() });
    function seg(id, fn) {
      var bs = $$('#' + id + ' button');
      bs.forEach(function (b) { b.addEventListener('click', function () { bs.forEach(function (x) { x.classList.remove('on') }); b.classList.add('on'); fn(b.dataset.v) }) });
    }
    seg('pbg', function (v) { sec.classList.toggle('dark', v === 'dark'); $$('.lc svg', lg).forEach(function (s) { s.classList.toggle('dk', v === 'dark') }) });
    seg('pcol', function (v) { mono = v === 'mono'; filt() });
  })();

  /* ---------- scroll zanka ---------- */
  var ticking = false;
  function frame() { ticking = false; spy(); binders.forEach(function (b) { var r = b.el.getBoundingClientRect(); if (r.bottom > -200 && r.top < innerHeight + 200) b.update() }) }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame) } }
  addEventListener('scroll', req, { passive: true }); addEventListener('resize', req);
  frame();
  window.__landing = { frame: frame, o3: o3 };
})();
