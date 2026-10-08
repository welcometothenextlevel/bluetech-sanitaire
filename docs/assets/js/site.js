/* Bluetech Sanitaire — interactions. Content is fully visible without JS; JS only sets start states. */
(function () {
  'use strict';
  var d = document, de = d.documentElement, W = window;
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var RM = W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FINE = W.matchMedia('(pointer: fine)').matches;
  var isMob = function () { return W.innerWidth <= 900; };
  var LATE = Date.now() - (W.__t0 || 0) > 2300;
  var G = W.gsap, ST = W.ScrollTrigger;
  var WA = d.body.getAttribute('data-wa') || '';
  var MAIL = d.body.getAttribute('data-mail') || '';

  $$('[data-year]').forEach(function (e) { e.textContent = new Date().getFullYear(); });
  $$('[data-today]').forEach(function (e) { e.textContent = new Date().toLocaleDateString('fr-CH', { day: '2-digit', month: '2-digit', year: 'numeric' }); });

  if (!G || !ST) { de.classList.remove('pre-intro'); }
  else { G.registerPlugin(ST); }

  /* ---------------- smooth scroll (desktop only) ---------------- */
  var lenis = null;
  if (G && W.Lenis && FINE && !RM) {
    lenis = new W.Lenis({ duration: 1.15, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, smoothWheel: true });
    lenis.on('scroll', ST.update);
    G.ticker.add(function (t) { lenis.raf(t * 1000); });
    G.ticker.lagSmoothing(0);
  }
  W.__lenis = lenis;
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href'); if (id.length < 2) return;
      var t = $(id); if (!t) return;
      e.preventDefault();
      if (lenis) lenis.scrollTo(t, { offset: -80 }); else t.scrollIntoView({ behavior: RM ? 'auto' : 'smooth' });
    });
  });

  /* ---------------- header, progress, mega menu, mobile menu ---------------- */
  var hd = $('[data-hd]'), prog = $('[data-progress]'), side = $('[data-sidepipe]'), lastY = W.scrollY, ticking = false;
  function onScroll() {
    var y = W.scrollY, max = Math.max(1, de.scrollHeight - W.innerHeight), p = Math.min(1, Math.max(0, y / max));
    hd.classList.toggle('is-scrolled', y > 24);
    var menuOpen = de.classList.contains('menu-open') || hd.classList.contains('dd-open');
    // on phones the header (and its menu button) always stays visible
    var hide = !menuOpen && !isMob() && y > lastY + 2 && y > 420;
    var show = isMob() || y < lastY - 2 || y < 420;
    if (hide) { hd.classList.add('is-hidden'); de.classList.add('hd-hide'); }
    else if (show) { hd.classList.remove('is-hidden'); de.classList.remove('hd-hide'); }
    lastY = y;
    if (prog) prog.style.transform = 'scaleX(' + p + ')';
    if (side) side.style.transform = 'scaleY(' + p + ')';
    ticking = false;
  }
  W.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  var dd = $('[data-dd]');
  if (dd) {
    var ddBtn = $('[data-dd-btn]', dd), ddT;
    var setDD = function (on) { dd.classList.toggle('is-open', on); hd.classList.toggle('dd-open', on); ddBtn.setAttribute('aria-expanded', on); };
    ddBtn.addEventListener('click', function () { setDD(!dd.classList.contains('is-open')); });
    if (FINE) {
      dd.addEventListener('mouseenter', function () { clearTimeout(ddT); setDD(true); });
      dd.addEventListener('mouseleave', function () { ddT = setTimeout(function () { setDD(false); }, 180); });
    }
    d.addEventListener('click', function (e) { if (!dd.contains(e.target)) setDD(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && dd.classList.contains('is-open')) { setDD(false); ddBtn.focus(); } });
  }

  var burger = $('[data-burger]'), menu = $('[data-menu]'), lockY = 0, bs = d.body.style, kbd = false;
  // iOS ignores overflow:hidden on body, so the page is pinned with position:fixed while the menu is open
  function lockPage(on) {
    if (lenis) { on ? lenis.stop() : lenis.start(); return; }
    if (on) { lockY = W.scrollY; bs.position = 'fixed'; bs.top = -lockY + 'px'; bs.left = '0'; bs.right = '0'; bs.width = '100%'; }
    else { bs.position = ''; bs.top = ''; bs.left = ''; bs.right = ''; bs.width = ''; W.scrollTo(0, lockY); }
  }
  function setMenu(on) {
    if (on === de.classList.contains('menu-open')) return;
    de.classList.toggle('menu-open', on);
    burger.setAttribute('aria-expanded', on);
    burger.setAttribute('aria-label', on ? 'Fermer le menu' : 'Ouvrir le menu');
    menu.setAttribute('aria-hidden', !on);
    lockPage(on);
    if (on) { hd.classList.remove('is-hidden'); de.classList.remove('hd-hide'); menu.scrollTop = 0; if (kbd) setTimeout(function () { var f = $('a', menu); if (f) f.focus({ preventScroll: true }); }, 350); }
  }
  var msvc = $('[data-msvc]');
  if (msvc) msvc.addEventListener('click', function () {
    var on = msvc.getAttribute('aria-expanded') !== 'true';
    msvc.setAttribute('aria-expanded', on); $('#msvc').classList.toggle('is-open', on);
  });
  if (burger && menu) {
    burger.addEventListener('click', function (e) { kbd = e.detail === 0; setMenu(!de.classList.contains('menu-open')); });
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    d.addEventListener('keydown', function (e) {
      if (!de.classList.contains('menu-open')) return;
      if (e.key === 'Escape') { setMenu(false); burger.focus(); }
      if (e.key === 'Tab') {
        var f = [burger].concat($$('a, button', menu).filter(function (x) { return x.offsetParent !== null; })), i = f.indexOf(d.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    W.addEventListener('resize', function () { if (W.innerWidth > 1180 && de.classList.contains('menu-open')) setMenu(false); });
  }

  var fab = $('[data-fab]'), ft = $('.ft');
  if (fab && ft && 'IntersectionObserver' in W) {
    new IntersectionObserver(function (en) { fab.classList.toggle('is-off', en[0].isIntersecting); }, { rootMargin: '0px 0px -30% 0px' }).observe(ft);
  }

  /* ---------------- text splitting ---------------- */
  function split(el) {
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var parts = n.textContent.split(/(\s+)/), frag = d.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(d.createTextNode(' ')); return; }
            var w = d.createElement('span'); w.className = 'w';
            var i = d.createElement('span'); i.className = 'wi'; i.textContent = p;
            w.appendChild(i); frag.appendChild(w);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    };
    el.setAttribute('aria-label', el.textContent.trim());
    walk(el);
    $$('.w', el).forEach(function (w) { w.setAttribute('aria-hidden', 'true'); });
    return $$('.wi', el);
  }

  /* ---------------- reveals ---------------- */
  function inFirstView(el) { var r = el.getBoundingClientRect(); return r.top < W.innerHeight && r.bottom > 0; }
  var introEls = $$('[data-intro]');
  if (G) {
    // 1. start states
    var splits = $$('[data-split]').map(function (el) { return { el: el, words: split(el) }; });
    var skip = function (el) { return LATE && inFirstView(el); };
    if (!RM) {
      splits.forEach(function (s) { if (!skip(s.el)) G.set(s.words, { yPercent: 115 }); });
      $$('[data-r]').forEach(function (el) { if (!skip(el)) G.set(el, { autoAlpha: 0, y: 34 }); });
      introEls.forEach(function (el) { if (!skip(el) && !el.hasAttribute('data-split')) G.set(el, { autoAlpha: 0, y: 26 }); });
      // service illustration: prepare stroke drawing
      $$('[data-art] .d').forEach(function (el) {
        var shapes = el.tagName === 'g' ? $$('path,rect,circle,ellipse', el) : [el];
        shapes.forEach(function (s) {
          if (!s.getTotalLength || s.closest('.ghost')) return;
          var L = 0; try { L = s.getTotalLength(); } catch (e) { return; }
          if (!L) return;
          s.style.strokeDasharray = L; s.style.strokeDashoffset = L; s.classList.add('draw');
        });
      });
    }
    // 2. reveal the page
    de.classList.remove('pre-intro');
    // 3. intro timeline (first viewport)
    if (!RM && !LATE) {
      var tl = G.timeline({ delay: 0.1, defaults: { ease: 'expo.out' } });
      introEls.forEach(function (el, k) {
        if (el.hasAttribute('data-split')) {
          var s = splits.filter(function (x) { return x.el === el; })[0];
          G.set(el, { autoAlpha: 1 });
          tl.to(s.words, { yPercent: 0, duration: 1.3, stagger: 0.06 }, k === 0 ? 0 : '<0.05');
        } else {
          tl.to(el, { autoAlpha: 1, y: 0, duration: 1.2 }, k === 0 ? 0 : '<0.12');
        }
      });
      var draws = $$('[data-art] .draw');
      if (draws.length) tl.to(draws, { strokeDashoffset: 0, duration: 1.8, ease: 'power2.inOut', stagger: 0.05 }, 0.3);
    } else {
      $$('[data-art] .draw').forEach(function (s) { s.style.strokeDashoffset = 0; });
    }
    // 4. scroll reveals
    if (!RM) {
      splits.forEach(function (s) {
        if (s.el.hasAttribute('data-intro') || skip(s.el)) return;
        ST.create({ trigger: s.el, start: 'top 88%', once: true, onEnter: function () { G.to(s.words, { yPercent: 0, duration: 1.2, ease: 'expo.out', stagger: 0.035 }); } });
      });
      ST.batch($$('[data-r]').filter(function (el) { return !skip(el); }), {
        start: 'top 90%', once: true,
        onEnter: function (els) { G.to(els, { autoAlpha: 1, y: 0, duration: 1.1, ease: 'expo.out', stagger: 0.08, overwrite: true }); }
      });
      // image veils
      $$('.wc__ph, .gi__b, .band__f picture, .story__ph').forEach(function (box) {
        if (skip(box)) return;
        var v = d.createElement('span'); v.className = 'veil'; v.setAttribute('aria-hidden', 'true');
        box.style.position = box.style.position || 'relative'; box.appendChild(v);
        var img = $('img', box);
        ST.create({ trigger: box, start: 'top 92%', once: true, onEnter: function () {
          G.to(v, { scaleY: 0, duration: 1.3, ease: 'expo.inOut', onComplete: function () { v.remove(); } });
          if (img) G.fromTo(img, { scale: 1.25 }, { scale: box.classList.contains('wc__ph') ? 1.06 : 1, duration: 1.8, ease: 'expo.out', clearProps: box.classList.contains('wc__ph') ? '' : 'transform' });
        } });
      });
    }
  }
  // failsafe: anything still hidden after 4 s gets shown
  setTimeout(function () {
    $$('[data-r],[data-intro]').forEach(function (el) { if (getComputedStyle(el).opacity < 0.05) { el.style.opacity = 1; el.style.visibility = 'visible'; el.style.transform = 'none'; } });
    $$('.wi').forEach(function (w) { var r = w.getBoundingClientRect(); if (r.top < W.innerHeight && r.bottom > 0 && getComputedStyle(w).transform !== 'none' && !G) w.style.transform = 'none'; });
  }, 4000);

  /* ---------------- services manifold ---------------- */
  var mani = $('[data-mani]');
  if (mani && G && !RM) {
    mani.classList.add('is-js');
    var water = $('[data-mani-water]'), rows = $$('[data-mani-row]', mani), pipe = water.parentNode;
    var thresholds = [];
    var measure = function () { var ph = pipe.offsetHeight; thresholds = rows.map(function (r) { return (r.offsetTop + r.offsetHeight / 2) / ph; }); };
    measure(); W.addEventListener('resize', measure);
    var fill = { v: 0 };
    var apply = function () {
      water.style.setProperty('--fill', fill.v);
      rows.forEach(function (r, i) { r.classList.toggle('is-on', fill.v >= thresholds[i] - 0.01); });
    };
    apply();
    G.to(fill, { v: 1, ease: 'none', onUpdate: apply, scrollTrigger: { trigger: mani, start: 'top 72%', end: 'bottom 62%', scrub: 0.6 } });
  }

  /* ---------------- X-ray lens ---------------- */
  var xr = $('[data-xray]');
  if (xr) (function () {
    var stage = $('[data-xray-stage]', xr), ring = $('[data-ring]', xr), tog = $('[data-xray-toggle]', xr);
    var tx = 0.5, ty = 0.7, cx = 0.5, cy = 0.7, user = 0, run = false, raf = 0, t0 = performance.now();
    var size = { w: 1, h: 1 };
    var resize = function () { size.w = stage.offsetWidth; size.h = stage.offsetHeight; };
    resize(); W.addEventListener('resize', resize);
    var setPos = function (e) { var r = stage.getBoundingClientRect(); tx = (e.clientX - r.left) / r.width; ty = (e.clientY - r.top) / r.height; user = performance.now(); };
    stage.addEventListener('pointermove', setPos);
    stage.addEventListener('pointerdown', setPos);
    var loop = function (now) {
      if (now - user > 2600 && !RM) {
        var k = (now - t0) / 1000;
        tx = 0.5 + 0.3 * Math.sin(k * 0.55); ty = 0.78 + 0.13 * Math.sin(k * 0.83 + 1.2);
      }
      var ease = now - user < 2600 ? 0.22 : 0.06;
      cx += (tx - cx) * ease; cy += (ty - cy) * ease;
      var px = cx * size.w, py = cy * size.h;
      stage.style.setProperty('--x', px + 'px'); stage.style.setProperty('--y', py + 'px');
      ring.style.left = px + 'px'; ring.style.top = py + 'px';
      if (run) raf = requestAnimationFrame(loop);
    };
    var start = function () { if (!run) { run = true; raf = requestAnimationFrame(loop); } };
    var stop = function () { run = false; cancelAnimationFrame(raf); };
    if ('IntersectionObserver' in W) new IntersectionObserver(function (en) { en[0].isIntersecting ? start() : stop(); }).observe(stage);
    else start();
    loop(performance.now());
    if (tog) tog.addEventListener('click', function () {
      var on = !xr.classList.contains('is-all'); xr.classList.toggle('is-all', on);
      tog.setAttribute('aria-pressed', on); $('.btn__t', tog).textContent = on ? 'Mode loupe' : 'Tout révéler';
    });
  })();

  /* ---------------- work gallery: pinned horizontal (desktop) / 3D coverflow (mobile) ---------------- */
  var track = $('[data-work-track]');
  if (track) {
    var cards = $$('.wc', track), bar = $('[data-work-bar]');
    var tilt = function (vw) {
      cards.forEach(function (c) {
        var r = c.getBoundingClientRect(), o = ((r.left + r.width / 2) - vw / 2) / vw;
        o = Math.max(-1, Math.min(1, o));
        if (isMob()) c.style.transform = 'rotateY(' + (o * -38) + 'deg) translateZ(' + (-Math.abs(o) * 120) + 'px) scale(' + (1 - Math.abs(o) * 0.06) + ')';
        else c.style.transform = 'rotateY(' + (o * -10) + 'deg)';
      });
    };
    if (G && !RM) {
      var mm = G.matchMedia();
      mm.add('(min-width: 901px)', function () {
        var pin = $('[data-work-pin]');
        pin.style.perspective = '1600px';
        var dist = function () { return Math.max(0, track.scrollWidth - W.innerWidth); };
        var tw = G.to(track, {
          x: function () { return -dist(); }, ease: 'none',
          scrollTrigger: { trigger: pin, start: 'center 54%', end: function () { return '+=' + dist(); }, pin: true, scrub: 0.8, invalidateOnRefresh: true, anticipatePin: 1,
            onUpdate: function (s) { if (bar) bar.style.transform = 'scaleX(' + s.progress + ')'; tilt(W.innerWidth); } }
        });
        tilt(W.innerWidth);
        return function () { tw.kill(); track.style.transform = ''; pin.style.perspective = ''; cards.forEach(function (c) { c.style.transform = ''; }); };
      });
    }
    var tk = false;
    track.addEventListener('scroll', function () {
      if (!isMob() || tk) return; tk = true;
      requestAnimationFrame(function () { tilt(W.innerWidth); if (bar) bar.style.transform = 'scaleX(' + (track.scrollLeft / Math.max(1, track.scrollWidth - track.clientWidth)) + ')'; tk = false; });
    }, { passive: true });
    if (isMob() && !RM) tilt(W.innerWidth);

    // mobile: auto-playing carousel with dots; a touch pauses it for a few seconds
    var dots = d.createElement('div'); dots.className = 'work__dots'; dots.setAttribute('aria-hidden', 'true');
    cards.forEach(function (c, i) { var b = d.createElement('button'); b.type = 'button'; b.tabIndex = -1; b.addEventListener('click', function () { go(i); hold = performance.now(); }); dots.appendChild(b); });
    track.parentNode.parentNode.insertBefore(dots, track.parentNode.nextSibling);
    var hold = 0, inView = false, timer = null;
    var center = function (c) { var tr = track.getBoundingClientRect(), r = c.getBoundingClientRect(); return track.scrollLeft + (r.left + r.width / 2) - (tr.left + tr.width / 2); };
    var current = function () { var tr = track.getBoundingClientRect(), mid = tr.left + tr.width / 2, best = 0, bd = 1e9; cards.forEach(function (c, i) { var r = c.getBoundingClientRect(), dd = Math.abs(r.left + r.width / 2 - mid); if (dd < bd) { bd = dd; best = i; } }); return best; };
    var go = function (i) { track.scrollTo({ left: Math.max(0, center(cards[i])), behavior: RM ? 'auto' : 'smooth' }); };
    var mark = function () { var k = current(); $$('button', dots).forEach(function (b, i) { b.classList.toggle('is-on', i === k); }); };
    mark();
    track.addEventListener('scroll', function () { if (isMob()) requestAnimationFrame(mark); }, { passive: true });
    ['touchstart', 'pointerdown', 'wheel'].forEach(function (ev) { track.addEventListener(ev, function () { hold = performance.now(); }, { passive: true }); });
    var tick = function () {
      if (!isMob() || !inView || d.hidden || RM || performance.now() - hold < 5000) return;
      var k = current(); go(k + 1 >= cards.length ? 0 : k + 1);
    };
    if ('IntersectionObserver' in W) new IntersectionObserver(function (en) {
      inView = en[0].isIntersecting;
      if (inView && !timer) timer = setInterval(tick, 3000); else if (!inView && timer) { clearInterval(timer); timer = null; }
    }, { threshold: 0.35 }).observe(track);
  }

  /* ---------------- process gauge ---------------- */
  $$('[data-proc]').forEach(function (proc) {
    var needle = $('[data-needle]', proc), gp = $('[data-gauge-prog]', proc), lab = $('[data-gauge-step]', proc), ok = $('[data-ok]', proc);
    var steps = $$('[data-step]', proc), list = $('.proc__steps', proc);
    var set = function (p) {
      var bar = p * 9.2, n = steps.length;
      needle.style.transform = 'rotate(' + (-135 + bar * 27) + 'deg)';
      gp.style.strokeDashoffset = 1 - bar / 10;
      var idx = Math.min(n - 1, Math.floor(p * n * 0.999));
      steps.forEach(function (s, i) { s.classList.toggle('is-on', i <= idx); });
      if (lab) lab.textContent = 'Étape 0' + (idx + 1) + ' / 0' + n;
      if (ok) { var on = p > 0.94; ok.style.setProperty('--ok', on ? 1 : 0.4); ok.style.setProperty('--oko', on ? 1 : 0); }
    };
    if (!G || RM) { set(1); return; }
    proc.classList.add('is-js');
    if (ok) ok.style.transition = 'transform .6s cubic-bezier(.3,1.6,.5,1), opacity .3s';
    var o = { p: 0 }; set(0);
    G.to(o, { p: 1, ease: 'none', onUpdate: function () { set(o.p); }, scrollTrigger: { trigger: list, start: 'top 62%', end: 'bottom 70%', scrub: 0.5 } });
  });

  /* ---------------- reviews rail ---------------- */
  var rail = $('[data-rail]');
  if (rail) (function () {
    var tr = $('[data-track]', rail);
    var orig = tr.innerHTML; tr.innerHTML = orig + orig;
    $$('.rv', tr).slice(tr.children.length / 2).forEach(function (c) { c.setAttribute('aria-hidden', 'true'); });
    var x = 0, v = 0, target = RM ? 0 : -0.5, drag = false, sx = 0, sp = 0, lastX = 0, lastT = 0, vel = 0, half = 1, run = false, raf = 0, prevT = 0, tween = null;
    var measure = function () { half = tr.scrollWidth / 2; };
    measure(); W.addEventListener('resize', measure); W.addEventListener('load', measure);
    var wrap = function () { while (x <= -half) x += half; while (x > 0) x -= half; };
    var frame = function (now) {
      var dt = Math.min(48, now - (prevT || now)) / 16.67; prevT = now;
      if (!drag && !tween) { v += (target - v) * 0.04; x += v * dt; }
      wrap();
      tr.style.transform = 'translate3d(' + x + 'px,0,0)';
      if (run) raf = requestAnimationFrame(frame);
    };
    var start = function () { if (!run) { run = true; prevT = 0; raf = requestAnimationFrame(frame); } };
    var stop = function () { run = false; cancelAnimationFrame(raf); };
    if ('IntersectionObserver' in W) new IntersectionObserver(function (en) { en[0].isIntersecting ? start() : stop(); }).observe(rail); else start();
    if (FINE) { rail.addEventListener('mouseenter', function () { target = 0; }); rail.addEventListener('mouseleave', function () { target = RM ? 0 : -0.5; }); }
    rail.addEventListener('pointerdown', function (e) { drag = true; sx = e.clientX; sp = x; lastX = e.clientX; lastT = performance.now(); vel = 0; rail.classList.add('is-drag'); });
    W.addEventListener('pointermove', function (e) {
      if (!drag) return;
      x = sp + (e.clientX - sx);
      var now = performance.now(); vel = (e.clientX - lastX) / Math.max(1, now - lastT) * 16.67; lastX = e.clientX; lastT = now;
    });
    var end = function () { if (!drag) return; drag = false; v = Math.max(-40, Math.min(40, vel)); rail.classList.remove('is-drag'); };
    W.addEventListener('pointerup', end); W.addEventListener('pointercancel', end);
    rail.addEventListener('dragstart', function (e) { e.preventDefault(); });
    var step = function (dir) {
      var c = $('.rv', tr); if (!c) return; var w = c.offsetWidth + 20;
      var o = { x: x }; v = 0; target = 0;
      if (G) { if (tween) tween.kill(); tween = G.to(o, { x: x - dir * w, duration: 0.9, ease: 'expo.out', onUpdate: function () { x = o.x; }, onComplete: function () { tween = null; setTimeout(function () { target = RM ? 0 : -0.5; }, 2500); } }); }
      else { x -= dir * w; }
    };
    var pv = $('[data-rail-prev]'), nx = $('[data-rail-next]');
    if (pv) pv.addEventListener('click', function () { step(-1); });
    if (nx) nx.addEventListener('click', function () { step(1); });
    rail.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') step(1); if (e.key === 'ArrowLeft') step(-1); });
  })();

  /* ---------------- FAQ (animated details) ---------------- */
  $$('.faq__i').forEach(function (det) {
    var sum = $('summary', det), body = $('.faq__a', det);
    sum.addEventListener('click', function (e) {
      if (!G || RM) return;
      e.preventDefault();
      if (det.open) {
        G.to(body, { height: 0, duration: 0.5, ease: 'expo.out', onComplete: function () { det.open = false; body.style.height = ''; } });
      } else {
        det.open = true; var h = body.scrollHeight;
        G.fromTo(body, { height: 0 }, { height: h, duration: 0.7, ease: 'expo.out', onComplete: function () { body.style.height = ''; if (ST) ST.refresh(); } });
      }
    });
  });

  /* ---------------- 3D tilt cards (fine pointer) ---------------- */
  if (FINE && !RM) $$('.scard, .val').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect(), px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
      c.style.transform = 'perspective(900px) rotateX(' + (-py * 7) + 'deg) rotateY(' + (px * 9) + 'deg) translateZ(0)';
    });
    c.addEventListener('pointerleave', function () { c.style.transition = 'transform .8s cubic-bezier(.2,.75,.15,1)'; c.style.transform = ''; setTimeout(function () { c.style.transition = ''; }, 800); });
  });

  /* ---------------- water ripple (CTA) ---------------- */
  $$('[data-water]').forEach(function (cv) { waterSurface(cv, cv.closest('[data-cta]')); });
  function waterSurface(cv, host) {
    var gl = cv.getContext('webgl', { antialias: false, alpha: false, premultipliedAlpha: false, preserveDrawingBuffer: false });
    if (!gl) return;
    var vs = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
    var fs = [
      'precision highp float;',
      'uniform vec2 res;uniform float t;uniform vec4 drops[10];',
      'float H(vec2 uv){float h=0.;float a=res.x/res.y;',
      ' for(int i=0;i<10;i++){vec4 dr=drops[i];float age=t-dr.z;if(age<0.||age>7.)continue;',
      '  vec2 dp=uv-dr.xy;dp.x*=a;float dist=length(dp);float front=age*.21;',
      '  float env=exp(-abs(dist-front)*16.)*exp(-age*.55)*dr.w*smoothstep(0.,.05,front);',
      '  h+=sin((dist-front)*70.)*env;}',
      ' h+=.035*sin(uv.x*a*7.+t*.6+sin(uv.y*6.+t*.4))+.03*sin(uv.y*11.-t*.7+uv.x*3.);',
      ' return h;}',
      'float caust(vec2 q0,float tt){vec2 p=q0*6.28318-250.;vec2 i=p;float c=1.;float inten=.005;',
      ' for(int n=0;n<4;n++){float q=tt*(1.-(3.5/float(n+1)));i=p+vec2(cos(q-i.x)+sin(q+i.y),sin(q-i.y)+cos(q+i.x));',
      '  c+=1./length(vec2(p.x/(sin(i.x+q)/inten),p.y/(cos(i.y+q)/inten)));}',
      ' c/=4.;c=1.17-pow(c,1.4);return clamp(pow(abs(c),8.),0.,2.);}',
      'void main(){vec2 uv=gl_FragCoord.xy/res;float e=1.5/res.y;',
      ' float hx=H(uv+vec2(e,0.))-H(uv-vec2(e,0.));float hy=H(uv+vec2(0.,e))-H(uv-vec2(0.,e));',
      ' vec3 n=normalize(vec3(-hx*5.,-hy*5.,.08));',
      ' vec3 deep=vec3(.02,.07,.16);vec3 mid=vec3(.06,.2,.42);',
      ' vec3 col=mix(deep,mid,smoothstep(0.,1.,uv.y*.9+.1));',
      ' vec2 cp=uv*vec2(res.x/res.y,1.)*.9+n.xy*.08;',
      ' float c=caust(cp,t*.35);',
      ' col+=vec3(.25,.6,1.)*c*.28;',
      ' vec3 L=normalize(vec3(-.4,.6,.7));float spec=pow(max(dot(reflect(-L,n),vec3(0.,0.,1.)),0.),60.);',
      ' col+=vec3(.75,.9,1.)*spec*.7;',
      ' col+=vec3(.15,.4,.8)*max(0.,dot(n,L)-.97)*4.;',
      ' float vig=smoothstep(1.25,.25,length((uv-vec2(.5,.55))*vec2(1.2,1.)));col*=.55+.45*vig;',
      ' gl_FragColor=vec4(col,1.);}'
    ].join('\n');
    var sh = function (type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
    var pr = gl.createProgram();
    gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
    gl.useProgram(pr);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var lp = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
    var uRes = gl.getUniformLocation(pr, 'res'), uT = gl.getUniformLocation(pr, 't'), uD = gl.getUniformLocation(pr, 'drops');
    var drops = new Float32Array(40), di = 0, T = 0, run = false, raf = 0, prev = 0, lastMove = 0, auto = 0;
    for (var k = 0; k < 10; k++) drops[k * 4 + 2] = -99;
    var scale = isMob() ? 0.5 : 0.6;
    var resize = function () {
      var r = host.getBoundingClientRect(), dpr = Math.min(W.devicePixelRatio || 1, 2);
      cv.width = Math.max(2, Math.round(r.width * dpr * scale)); cv.height = Math.max(2, Math.round(r.height * dpr * scale));
      gl.viewport(0, 0, cv.width, cv.height);
    };
    resize(); W.addEventListener('resize', resize);
    var drop = function (x, y, s) { drops[di * 4] = x; drops[di * 4 + 1] = y; drops[di * 4 + 2] = T; drops[di * 4 + 3] = s; di = (di + 1) % 10; };
    var rel = function (e) { var r = host.getBoundingClientRect(); return [(e.clientX - r.left) / r.width, 1 - (e.clientY - r.top) / r.height]; };
    host.addEventListener('pointerdown', function (e) { var p = rel(e); drop(p[0], p[1], 1.4); });
    if (FINE) host.addEventListener('pointermove', function (e) { var now = performance.now(); if (now - lastMove < 110) return; lastMove = now; var p = rel(e); drop(p[0], p[1], 0.45); });
    var frame = function (now) {
      var dt = prev ? Math.min(0.05, (now - prev) / 1000) : 0.016; prev = now; T += RM ? dt * 0.2 : dt;
      if (T - auto > 1.9) { auto = T; drop(0.15 + Math.random() * 0.7, 0.15 + Math.random() * 0.7, 0.9); }
      gl.uniform2f(uRes, cv.width, cv.height); gl.uniform1f(uT, T); gl.uniform4fv(uD, drops);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      if (run) raf = requestAnimationFrame(frame);
    };
    var start = function () { if (!run) { run = true; prev = 0; raf = requestAnimationFrame(frame); } };
    var stop = function () { run = false; cancelAnimationFrame(raf); };
    drop(0.5, 0.5, 1.2);
    frame(performance.now());
    if ('IntersectionObserver' in W) new IntersectionObserver(function (en) { en[0].isIntersecting ? start() : stop(); }, { rootMargin: '100px' }).observe(host); else start();
    d.addEventListener('visibilitychange', function () { if (d.hidden) stop(); });
  }

  /* ---------------- forms → WhatsApp / e-mail ---------------- */
  function send(via, subject, lines) {
    var text = lines.filter(function (l) { return l !== null; }).join('\n');
    if (via === 'mail' && MAIL) { W.location.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(text); return 'Votre messagerie s’ouvre avec le message prêt à être envoyé.'; }
    W.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
    return 'WhatsApp s’ouvre avec votre message — il ne reste qu’à appuyer sur « Envoyer ».';
  }
  function check(form, names) {
    var ok = true, first = null;
    names.forEach(function (n) {
      var f = form.elements[n]; if (!f) return;
      var fld = f.closest ? f.closest('.fld') : null, bad = !String(f.value || '').trim();
      if (n === 'tel' && !bad) bad = String(f.value).replace(/\D/g, '').length < 9;
      if (fld) fld.classList.toggle('is-err', bad);
      if (bad) { ok = false; if (!first) first = f; }
    });
    if (first) first.focus();
    return ok;
  }
  $$('form[data-form="quick"]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!check(form, ['nom', 'tel', 'message'])) return;
      var via = (e.submitter && e.submitter.getAttribute('data-via')) || 'wa', el = form.elements;
      var msg = send(via, 'Demande — ' + el.service.value, ['Bonjour Bluetech Sanitaire,', '', 'Service : ' + el.service.value, 'Nom : ' + el.nom.value.trim(), 'Téléphone : ' + el.tel.value.trim(), '', el.message.value.trim()]);
      $('.form__ok', form).textContent = msg;
    });
    $$('input,textarea', form).forEach(function (f) { f.addEventListener('input', function () { var x = f.closest('.fld'); if (x) x.classList.remove('is-err'); }); });
  });

  var wiz = $('form[data-form="wizard"]');
  if (wiz) (function () {
    var steps = $$('[data-wstep]', wiz), cur = 1, n = steps.length;
    var prev = $('[data-wiz-prev]', wiz), next = $('[data-wiz-next]', wiz), subs = $$('[data-via]', wiz), water = $('[data-wiz-water]', wiz), nodes = $$('.wiz__node', wiz), sum = $('[data-wiz-sum]', wiz);
    var slugs = {}; try { slugs = JSON.parse(wiz.getAttribute('data-slugs')); } catch (e) {}
    var q = new URLSearchParams(W.location.search).get('service');
    if (q && slugs[q]) { var r = $('input[name="service"][value="' + slugs[q].replace(/"/g, '\\"') + '"]', wiz); if (r) r.checked = true; }
    var val = function (name) { var f = wiz.elements[name]; if (!f) return ''; if (f.length && !f.tagName) { var c = $('input[name="' + name + '"]:checked', wiz); return c ? c.value : ''; } return String(f.value || '').trim(); };
    var show = function (k, focus) {
      cur = k;
      steps.forEach(function (s) { s.classList.toggle('is-on', +s.getAttribute('data-wstep') === k); });
      nodes.forEach(function (nd, i) { nd.classList.toggle('is-on', i < k); });
      water.parentNode.style.setProperty('--w', (k - 1) / (n - 1));
      water.style.transform = 'scaleX(' + ((k - 1) / (n - 1)) + ')';
      prev.hidden = k === 1; next.hidden = k === n; subs.forEach(function (b) { b.hidden = k !== n; });
      if (k === n) {
        var rows = [['Demande', val('service')], ['Bien', val('bien')], ['Délai', val('delai')], ['Message', val('message').slice(0, 140) + (val('message').length > 140 ? '…' : '')]];
        sum.innerHTML = rows.filter(function (r) { return r[1]; }).map(function (r) { return '<span><b>' + r[0] + ' :</b> ' + r[1].replace(/[<>&]/g, function (c) { return { '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]; }) + '</span>'; }).join('');
      }
      if (focus) {
        var top = wiz.getBoundingClientRect().top;
        if (top < 70) { if (lenis) lenis.scrollTo(wiz, { offset: -90 }); else W.scrollTo({ top: W.scrollY + top - 90, behavior: RM ? 'auto' : 'smooth' }); }
        var f = $('.is-on input, .is-on textarea', wiz); if (f && k > 1) setTimeout(function () { f.focus({ preventScroll: true }); }, 320);
      }
      if (ST) ST.refresh();
    };
    var valid = function (k) {
      if (k === 1) { var ok = !!val('service'); $('[data-err="service"]', wiz).classList.toggle('is-on', !ok); return ok; }
      if (k === 2) return check(wiz, ['message']);
      if (k === 3) return check(wiz, ['nom', 'tel']);
      return true;
    };
    next.addEventListener('click', function () { if (valid(cur)) show(cur + 1, true); });
    prev.addEventListener('click', function () { show(cur - 1, true); });
    $$('input[name="service"]', wiz).forEach(function (r) { r.addEventListener('change', function () { $('[data-err="service"]', wiz).classList.remove('is-on'); setTimeout(function () { if (cur === 1) show(2, true); }, 260); }); });
    $$('input,textarea', wiz).forEach(function (f) { f.addEventListener('input', function () { var x = f.closest('.fld'); if (x) x.classList.remove('is-err'); }); });
    wiz.addEventListener('keydown', function (e) { if (e.key === 'Enter' && e.target.tagName === 'INPUT' && cur < n) { e.preventDefault(); next.click(); } });
    wiz.addEventListener('submit', function (e) {
      e.preventDefault();
      if (cur < n) { next.click(); return; }
      if (!valid(3)) return;
      var via = (e.submitter && e.submitter.getAttribute('data-via')) || 'wa';
      var msg = send(via, 'Demande de devis — ' + val('service'), [
        'Bonjour Bluetech Sanitaire,', '', 'Demande de devis : ' + val('service'),
        val('bien') ? 'Type de bien : ' + val('bien') : null, val('delai') ? 'Délai : ' + val('delai') : null, val('lieu') ? 'Lieu : ' + val('lieu') : null,
        '', val('message'), '', 'Nom : ' + val('nom'), 'Téléphone : ' + val('tel'), val('email') ? 'E-mail : ' + val('email') : null]);
      $('.form__ok', wiz).textContent = msg;
    });
    show(1, false);
  })();

  /* ---------------- gallery filters + lightbox ---------------- */
  var gal = $('[data-gal]');
  if (gal) (function () {
    var items = $$('.gi', gal), btns = $$('[data-filter]');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        btns.forEach(function (x) { var on = x === b; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on); });
        items.forEach(function (it) { it.classList.toggle('is-hidden', f !== 'all' && it.getAttribute('data-tag') !== f); });
        if (G && !RM) G.fromTo(items.filter(function (it) { return !it.classList.contains('is-hidden'); }), { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 0.8, ease: 'expo.out', stagger: 0.05 });
        if (ST) ST.refresh();
      });
    });
    var data = []; try { data = JSON.parse($('#work-data').textContent); } catch (e) {}
    var box = $('[data-lb-box]'), img = $('[data-lb-img]', box), cur = 0, opener = null, base = $('link[rel="stylesheet"]').getAttribute('href').split('assets/')[0];
    var visible = function () { return items.filter(function (it) { return !it.classList.contains('is-hidden'); }).map(function (it) { return +$('[data-lb]', it).getAttribute('data-lb'); }); };
    var load = function (k) {
      cur = k; var w = data[k];
      img.src = base + 'assets/img/work/' + w.n + '.webp'; img.alt = w.t + ' — ' + w.c;
      $('[data-lb-n]', box).textContent = 'R—' + (k < 9 ? '0' : '') + (k + 1); $('[data-lb-t]', box).textContent = w.t; $('[data-lb-c]', box).textContent = w.c;
    };
    var open = function (k, from) { opener = from; load(k); box.hidden = false; requestAnimationFrame(function () { box.classList.add('is-open'); }); if (lenis) lenis.stop(); d.body.style.overflow = 'hidden'; $('[data-lb-close]', box).focus(); };
    var close = function () { box.classList.remove('is-open'); setTimeout(function () { box.hidden = true; }, 350); if (lenis) lenis.start(); d.body.style.overflow = ''; if (opener) opener.focus(); };
    var go = function (dir) { var v = visible(), i = v.indexOf(cur); load(v[(i + dir + v.length) % v.length]); };
    $$('[data-lb]').forEach(function (b) { b.addEventListener('click', function () { open(+b.getAttribute('data-lb'), b); }); });
    $('[data-lb-close]', box).addEventListener('click', close);
    $('[data-lb-prev]', box).addEventListener('click', function () { go(-1); });
    $('[data-lb-next]', box).addEventListener('click', function () { go(1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    d.addEventListener('keydown', function (e) {
      if (box.hidden) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') go(1); if (e.key === 'ArrowLeft') go(-1);
      if (e.key === 'Tab') { var f = $$('button', box), i = f.indexOf(d.activeElement); if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); } else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); } }
    });
    var sx = null;
    box.addEventListener('pointerdown', function (e) { sx = e.clientX; });
    box.addEventListener('pointerup', function (e) { if (sx === null) return; var dx = e.clientX - sx; if (Math.abs(dx) > 50) go(dx < 0 ? 1 : -1); sx = null; });
    if (W.location.hash) { var t = $(W.location.hash); if (t && t.classList.contains('gi')) setTimeout(function () { t.scrollIntoView({ block: 'center' }); }, 300); }
  })();

  if (ST) { W.addEventListener('load', function () { ST.refresh(); }); }
})();
