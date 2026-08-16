(function () {
  const deck = document.getElementById('deck');
  const slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  const tocLinks = Array.prototype.slice.call(document.querySelectorAll('.present-toc a'));
  const countEl = document.getElementById('presentCount');
  const prevBtn = document.getElementById('presentPrev');
  const nextBtn = document.getElementById('presentNext');
  const fullBtn = document.getElementById('presentFull');
  if (!deck || !slides.length) return;

  let index = 0;
  let ticking = false;

  function clamp(n) {
    return Math.max(0, Math.min(slides.length - 1, n));
  }

  function go(n, instant) {
    index = clamp(n);
    slides[index].scrollIntoView({
      behavior: instant ? 'auto' : 'smooth',
      block: 'start',
    });
    sync();
  }

  function sync() {
    if (countEl) {
      countEl.textContent =
        String(index + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
    }
    tocLinks.forEach(function (a, i) {
      a.classList.toggle('is-active', i === index);
    });
    if (prevBtn) prevBtn.disabled = index === 0;
    if (nextBtn) nextBtn.disabled = index === slides.length - 1;
  }

  function nearest() {
    const top = deck.scrollTop;
    let best = 0;
    let dist = Infinity;
    slides.forEach(function (slide, i) {
      const d = Math.abs(slide.offsetTop - top);
      if (d < dist) {
        dist = d;
        best = i;
      }
    });
    return best;
  }

  deck.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      index = nearest();
      sync();
      ticking = false;
    });
  });

  tocLinks.forEach(function (a, i) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      go(i);
    });
  });

  if (prevBtn) prevBtn.addEventListener('click', function () { go(index - 1); });
  if (nextBtn) nextBtn.addEventListener('click', function () { go(index + 1); });

  if (fullBtn) {
    fullBtn.addEventListener('click', function () {
      const root = document.documentElement;
      if (!document.fullscreenElement) {
        if (root.requestFullscreen) root.requestFullscreen();
      } else if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    });
  }

  document.addEventListener('keydown', function (e) {
    const tag = (e.target && e.target.tagName) || '';
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

    if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
      e.preventDefault();
      go(index + 1);
    } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      go(index - 1);
    } else if (e.key === 'Home') {
      e.preventDefault();
      go(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      go(slides.length - 1);
    } else if (e.key === 'f' || e.key === 'F') {
      if (fullBtn) fullBtn.click();
    }
  });

  sync();
})();
