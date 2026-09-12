/* Shared by the home page and /video/. Every block guards on its elements, so a page can
   leave any of them out (the video page has no montage; the home page has no carousel). */
(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const phone = window.matchMedia('(max-width:720px)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const smooth = t => t * t * (3 - 2 * t);

  /* ---------- page load: release the hero masks ---------- */
  const arm = () => document.body.classList.add('is-loaded');
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(arm);
    setTimeout(arm, 1200); // never hold the page hostage to a slow font
  } else {
    requestAnimationFrame(arm);
  }

  /* ---------- scroll reveals ---------- */
  const revealIO = new IntersectionObserver(entries => {
    for (const e of entries) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); revealIO.unobserve(e.target); }
    }
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
  document.querySelectorAll('.reveal').forEach(el => revealIO.observe(el));

  /* ---------- proof numbers count up once ---------- */
  const countIO = new IntersectionObserver(entries => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      const el = e.target, target = +el.dataset.count;
      countIO.unobserve(el);
      if (reduced) { el.textContent = target; continue; }
      const t0 = performance.now(), dur = 1100;
      const tick = now => {
        const p = clamp((now - t0) / dur, 0, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }
  }, { threshold: 0.6 });
  document.querySelectorAll('[data-count]').forEach(el => countIO.observe(el));

  /* ---------- hero montage: scroll zooms the frame out to full width ---------- */
  const topbar = document.getElementById('topbar');
  const montage = document.getElementById('montage');
  const montageWrap = document.getElementById('montageWrap');
  const heroCopy = document.getElementById('heroCopy');
  const M0 = 0.66;
  function updateMontage() {
    if (!montage || reduced || window.innerWidth <= 720) return;
    const rect = montageWrap.getBoundingClientRect();
    const vh = window.innerHeight;
    const p = smooth(clamp((vh * 0.88 - rect.top) / (vh * 0.70), 0, 1));
    const y = window.scrollY;
    heroCopy.style.setProperty('--hy', (y * 0.18).toFixed(1));
    heroCopy.style.setProperty('--ho', (1 - clamp(y / (vh * 0.7), 0, 1) * 0.9).toFixed(3));
    montage.style.setProperty('--m', (M0 + (1 - M0) * p).toFixed(4));
    montage.style.setProperty('--p', p.toFixed(3));
    const slack = montage.offsetHeight * (1 - (M0 + (1 - M0) * p));
    montage.style.marginBottom = (-slack).toFixed(1) + 'px';
  }

  /* ---------- one scroll loop ---------- */
  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      topbar.classList.toggle('is-scrolled', window.scrollY > 12);
      updateMontage();
      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- hero loop: iOS Low Power Mode refuses autoplay, so retry on the first touch ---------- */
  const mv = document.getElementById('montageVideo');
  if (mv) {
    const mBox = mv.closest('.montage');
    mv.muted = true;
    const tryPlay = () => mv.play().catch(() => {});
    mv.addEventListener('playing', () => mBox.classList.add('is-playing'));
    if (!mv.paused) mBox.classList.add('is-playing');
    tryPlay();
    ['touchstart', 'touchend', 'click', 'scroll'].forEach(ev => {
      const once = () => { if (mv.paused) tryPlay(); window.removeEventListener(ev, once); };
      window.addEventListener(ev, once, { passive: true });
    });
    document.addEventListener('visibilitychange', () => { if (!document.hidden && mv.paused) tryPlay(); });
  }

  /* ---------- work carousel: a continuously looping film strip (desktop); a plain stack on phones ---------- */
  const carTrack = document.getElementById('carTrack');
  if (carTrack) {
    const originals = [...carTrack.children];
    if (!phone) originals.forEach(c => carTrack.appendChild(c.cloneNode(true)));
    let loopWidth = 0;
    const measureLoop = () => {
      const gap = parseFloat(getComputedStyle(carTrack).columnGap) || 24;
      loopWidth = originals.reduce((w, c) => w + c.getBoundingClientRect().width + gap, 0);
    };
    measureLoop();
    window.addEventListener('resize', measureLoop);

    let marqueePaused = reduced || phone;
    let holdUntil = 0;
    let lastT = performance.now();
    let pos = 0; // float accumulator: Safari rounds fractional scrollLeft writes, so track our own
    const SPEED = 32; // px per second
    function marquee(now) {
      const dt = Math.min(now - lastT, 100) / 1000;
      lastT = now;
      if (!marqueePaused && now > holdUntil && loopWidth > 0) {
        pos += SPEED * dt;
        if (pos >= loopWidth) pos -= loopWidth;
        carTrack.scrollLeft = pos;
      }
      requestAnimationFrame(marquee);
    }
    requestAnimationFrame(marquee);
    carTrack.addEventListener('mouseenter', () => { marqueePaused = true; });
    carTrack.addEventListener('mouseleave', () => { marqueePaused = reduced || phone; });
    carTrack.addEventListener('touchstart', () => { holdUntil = performance.now() + 4000; }, { passive: true });
    carTrack.addEventListener('scroll', () => {
      if (Math.abs(carTrack.scrollLeft - pos) > 4) pos = carTrack.scrollLeft;
      if (loopWidth > 0 && pos >= loopWidth) { pos -= loopWidth; carTrack.scrollLeft = pos; }
    }, { passive: true });
    const nudge = dir => {
      const gap = parseFloat(getComputedStyle(carTrack).columnGap) || 24;
      const step = (originals[0] ? originals[0].getBoundingClientRect().width : 560) + gap;
      holdUntil = performance.now() + 3500;
      carTrack.scrollBy({ left: dir * step, behavior: reduced ? 'auto' : 'smooth' });
    };
    const prev = document.getElementById('carPrev'), next = document.getElementById('carNext');
    if (prev) prev.addEventListener('click', () => nudge(-1));
    if (next) next.addEventListener('click', () => nudge(1));
  }

  /* ---------- hover previews: work cards and the offer cards ---------- */
  document.querySelectorAll('.card, .offer-card').forEach(card => {
    const v = card.querySelector('video');
    if (!v || !canHover) return;
    let timer;
    card.addEventListener('mouseenter', () => {
      timer = setTimeout(() => {
        if (!v.src) v.src = v.dataset.src;
        v.currentTime = 1.5;
        v.play().then(() => card.classList.add('is-previewing')).catch(() => {});
      }, 160);
    });
    card.addEventListener('mouseleave', () => {
      clearTimeout(timer);
      card.classList.remove('is-previewing');
      v.pause();
    });
  });

  /* ---------- phones: four quotes / three videos up front, the rest behind one tap ---------- */
  const fold = (btnId, listSel, always) => {
    const btn = document.getElementById(btnId), list = document.querySelector(listSel);
    if (!btn || !list || (!phone && !always)) return;
    list.classList.add('is-folded');
    btn.hidden = false;
    btn.addEventListener('click', () => { list.classList.remove('is-folded'); btn.hidden = true; });
  };
  fold('quotesMore', '.quotes', true);
  fold('workMore', '#carTrack');

  /* ---------- player ---------- */
  const player = document.getElementById('player');
  const playerVideo = document.getElementById('playerVideo');
  const playerTitle = document.getElementById('playerTitle');
  const playerClose = document.getElementById('playerClose');
  let lastFocus = null;
  let lockY = 0;
  function openPlayer(src, title) {
    lastFocus = document.activeElement;
    lockY = window.scrollY;
    document.body.style.top = -lockY + 'px';
    playerVideo.src = src;
    playerTitle.textContent = title;
    player.classList.add('is-open');
    player.setAttribute('aria-hidden', 'false');
    document.body.classList.add('is-locked');
    playerVideo.play().catch(() => {});
    playerClose.focus({ preventScroll: true });
  }
  function closePlayer() {
    playerVideo.pause();
    playerVideo.removeAttribute('src');
    playerVideo.load();
    player.classList.remove('is-open');
    player.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('is-locked');
    document.body.style.top = '';
    window.scrollTo({ top: lockY, behavior: 'instant' });
    if (lastFocus) lastFocus.focus({ preventScroll: true });
  }
  if (player) {
    document.querySelectorAll('[data-video]').forEach(el => {
      const go = () => openPlayer(el.dataset.video, el.dataset.title);
      el.addEventListener('click', go);
      if (el.tagName !== 'BUTTON') {
        el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
      }
    });
    playerClose.addEventListener('click', closePlayer);
    player.addEventListener('click', e => { if (e.target === player) closePlayer(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && player.classList.contains('is-open')) closePlayer(); });
  }
})();
