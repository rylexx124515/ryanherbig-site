(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  /* ---------- page load: release the hero masks ---------- */
  const arm = () => document.body.classList.add('is-loaded');
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(arm);
    setTimeout(arm, 1200);
  } else {
    requestAnimationFrame(arm);
  }

  /* ---------- top bar hairline + which piece type you're looking at ---------- */
  const topbar = document.getElementById('topbar');
  const jumps = [...document.querySelectorAll('#packnav a')].map(a => ({
    a, section: document.querySelector(a.getAttribute('href'))
  })).filter(j => j.section);
  const markJump = () => {
    if (!jumps.length) return;
    // a type lights up once its section fills the top third, not the instant it clears the bar
    const line = Math.max(132, window.innerHeight * 0.34);
    let on = null;
    for (const j of jumps) if (j.section.getBoundingClientRect().top <= line) on = j;
    for (const j of jumps) j.a.classList.toggle('is-on', j === on);
  };
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      topbar.classList.toggle('is-scrolled', window.scrollY > 12);
      markJump();
      ticking = false;
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- scroll reveals ---------- */
  const revealIO = new IntersectionObserver(entries => {
    for (const e of entries) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); revealIO.unobserve(e.target); }
    }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  document.querySelectorAll('.reveal').forEach(el => revealIO.observe(el));

  /* ---------- stat numbers count up once ---------- */
  const countIO = new IntersectionObserver(entries => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      const el = e.target, target = +el.dataset.count;
      countIO.unobserve(el);
      if (reduced) { el.textContent = target; continue; }
      const t0 = performance.now(), dur = 1000;
      const tick = now => {
        const p = clamp((now - t0) / dur, 0, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }
  }, { threshold: 0.6 });
  document.querySelectorAll('[data-count]').forEach(el => countIO.observe(el));

  /* ---------- reels: hover plays a muted 540p preview ---------- */
  document.querySelectorAll('.phone').forEach(card => {
    const v = card.querySelector('video');
    if (!v || !canHover) return;
    let timer;
    card.addEventListener('mouseenter', () => {
      timer = setTimeout(() => {
        if (!v.src) v.src = v.dataset.src;
        v.currentTime = 0;
        v.play().then(() => card.classList.add('is-previewing')).catch(() => {});
      }, 140);
    });
    card.addEventListener('mouseleave', () => {
      clearTimeout(timer);
      card.classList.remove('is-previewing');
      v.pause();
    });
  });

  /* ---------- carousels: scroll-snap track, arrows, dots, counter ---------- */
  document.querySelectorAll('.post').forEach(post => {
    const track = post.querySelector('.slides');
    const slides = [...track.children];
    const prev = post.querySelector('.slide-prev');
    const next = post.querySelector('.slide-next');
    const dots = [...post.querySelectorAll('.post-dots button')];
    const count = post.querySelector('.post-count b');
    let idx = 0;
    const width = () => track.getBoundingClientRect().width;
    const paint = () => {
      dots.forEach((d, i) => d.classList.toggle('is-on', i === idx));
      count.textContent = idx + 1;
      prev.disabled = idx === 0;
      next.disabled = idx === slides.length - 1;
    };
    const go = i => {
      idx = clamp(i, 0, slides.length - 1);
      track.scrollTo({ left: idx * width(), behavior: reduced ? 'auto' : 'smooth' });
      paint();
    };
    prev.addEventListener('click', e => { e.stopPropagation(); go(idx - 1); });
    next.addEventListener('click', e => { e.stopPropagation(); go(idx + 1); });
    dots.forEach((d, i) => d.addEventListener('click', () => go(i)));
    let raf;
    track.addEventListener('scroll', () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const i = Math.round(track.scrollLeft / width());
        if (i !== idx) { idx = clamp(i, 0, slides.length - 1); paint(); }
      });
    }, { passive: true });
    post.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1); }
    });
    // a click on the slide itself opens it full size
    slides.forEach(s => s.addEventListener('click', () => openImage(s.dataset.full, s.dataset.title)));
    paint();
  });

  /* ---------- stills rail arrows ---------- */
  const rail = document.getElementById('rail');
  if (rail && document.getElementById('railPrev')) {
  const railStep = dir => {
    const first = rail.querySelector('.still');
    const step = first ? first.getBoundingClientRect().width + 20 : 300;
    rail.scrollBy({ left: dir * step * 2, behavior: reduced ? 'auto' : 'smooth' });
  };
  document.getElementById('railPrev').addEventListener('click', () => railStep(-1));
  document.getElementById('railNext').addEventListener('click', () => railStep(1));
  }

  /* ---------- captions picker ---------- */
  const picks = [...document.querySelectorAll('.cap-picks button')];
  const pairs = [...document.querySelectorAll('.cap-pair')];
  picks.forEach(btn => btn.addEventListener('click', () => {
    const i = +btn.dataset.i;
    picks.forEach(b => { const on = b === btn; b.classList.toggle('is-on', on); b.setAttribute('aria-selected', on ? 'true' : 'false'); });
    pairs.forEach(p => { p.hidden = +p.dataset.i !== i; });
  }));

  /* ---------- viewer: portrait reels with sound, and stills full size ---------- */
  const player = document.getElementById('player');
  const stage = document.getElementById('playerStage');
  const playerVideo = document.getElementById('playerVideo');
  const playerImg = document.getElementById('playerImg');
  const playerTitle = document.getElementById('playerTitle');
  const playerClose = document.getElementById('playerClose');
  let lastFocus = null, lockY = 0;

  function open(title) {
    lastFocus = document.activeElement;
    lockY = window.scrollY;
    document.body.style.top = -lockY + 'px';
    playerTitle.textContent = title || '';
    player.classList.add('is-open');
    player.setAttribute('aria-hidden', 'false');
    document.body.classList.add('is-locked');
    playerClose.focus({ preventScroll: true });
  }
  function openVideo(src, title, portrait) {
    stage.classList.toggle('is-portrait', !!portrait);
    stage.classList.remove('is-image');
    playerImg.hidden = true; playerImg.removeAttribute('src');
    playerVideo.hidden = false;
    playerVideo.src = src;
    open(title);
    playerVideo.play().catch(() => {});
  }
  function openImage(src, title) {
    stage.classList.add('is-image');
    stage.classList.remove('is-portrait');
    playerVideo.hidden = true; playerVideo.pause(); playerVideo.removeAttribute('src'); playerVideo.load();
    playerImg.hidden = false;
    playerImg.src = src;
    open(title);
  }
  function close() {
    playerVideo.pause();
    playerVideo.removeAttribute('src');
    playerVideo.load();
    playerImg.removeAttribute('src');
    player.classList.remove('is-open');
    player.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('is-locked');
    document.body.style.top = '';
    window.scrollTo({ top: lockY, behavior: 'instant' });
    if (lastFocus) lastFocus.focus({ preventScroll: true });
  }
  document.querySelectorAll('[data-video]').forEach(el => {
    const go = () => openVideo(el.dataset.video, el.dataset.title, el.dataset.portrait === '1');
    el.addEventListener('click', go);
    el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
  });
  document.querySelectorAll('[data-full]:not(.slide)').forEach(el => {
    const go = () => openImage(el.dataset.full, el.dataset.title);
    el.addEventListener('click', go);
    el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
  });
  playerClose.addEventListener('click', close);
  player.addEventListener('click', e => { if (e.target === player) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && player.classList.contains('is-open')) close(); });
})();
