(function () {
  const cfg = window.ILMING_SITE || { appUrl: 'https://app.ilming.io' };

  function appPath(path) {
    const base = cfg.appUrl.replace(/\/$/, '');
    const p = path.startsWith('/') ? path : '/' + path;
    return base + p;
  }

  document.querySelectorAll('[data-app-link]').forEach(function (el) {
    const path = el.getAttribute('data-app-link');
    if (path) el.setAttribute('href', appPath(path));
  });

  document.querySelectorAll('[data-mailto]').forEach(function (el) {
    const key = el.getAttribute('data-mailto');
    const email =
      key === 'support'
        ? cfg.supportEmail
        : key === 'info'
          ? cfg.infoEmail
          : cfg.contactEmail;
    const subject = el.getAttribute('data-mailto-subject') || '';
    el.href =
      'mailto:' +
      email +
      (subject ? '?subject=' + encodeURIComponent(subject) : '');
  });

  const navbar = document.getElementById('navbar');
  const menuToggle = document.getElementById('menuToggle');
  const mobileNav = document.getElementById('mobileNav');
  const navBackdrop = document.getElementById('navBackdrop');
  let scrollLockY = 0;

  function syncNavHeight() {
    if (!navbar) return;
    const announce = document.getElementById('siteAnnouncement');
    const announceH =
      announce && !document.body.classList.contains('announcement-dismissed')
        ? announce.getBoundingClientRect().height
        : 0;
    document.documentElement.style.setProperty(
      '--announce-h',
      Math.ceil(announceH) + 'px'
    );
    const navH = navbar.getBoundingClientRect().height;
    document.documentElement.style.setProperty(
      '--nav-h',
      Math.ceil(announceH + navH) + 'px'
    );
  }

  if (navbar) {
    syncNavHeight();
    window.addEventListener('resize', syncNavHeight);
    window.addEventListener('load', syncNavHeight);
    const logoImg = navbar.querySelector('.brand img');
    if (logoImg) {
      if (logoImg.complete) syncNavHeight();
      else logoImg.addEventListener('load', syncNavHeight);
    }
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 80);
    });
  }

  function setMenuOpen(open) {
    if (!mobileNav || !menuToggle || !navbar) return;

    if (open) {
      scrollLockY = window.scrollY;
      document.body.style.top = '-' + scrollLockY + 'px';
      document.body.classList.add('nav-open');
      navbar.classList.add('menu-open');
      mobileNav.classList.add('open');
      if (navBackdrop) navBackdrop.classList.add('is-visible');
      menuToggle.setAttribute('aria-expanded', 'true');
      menuToggle.setAttribute('aria-label', 'Close menu');
    } else {
      document.body.classList.remove('nav-open');
      document.body.style.top = '';
      navbar.classList.remove('menu-open');
      mobileNav.classList.remove('open');
      if (navBackdrop) navBackdrop.classList.remove('is-visible');
      menuToggle.setAttribute('aria-expanded', 'false');
      menuToggle.setAttribute('aria-label', 'Open menu');
      window.scrollTo(0, scrollLockY);
    }
  }

  function closeMobileNav() {
    setMenuOpen(false);
  }

  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', function () {
      const willOpen = !mobileNav.classList.contains('open');
      setMenuOpen(willOpen);
    });

    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMobileNav);
    });

    if (navBackdrop) {
      navBackdrop.addEventListener('click', closeMobileNav);
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mobileNav.classList.contains('open')) {
        closeMobileNav();
      }
    });
  }

  window.addEventListener('resize', function () {
    syncNavHeight();
    if (window.matchMedia('(min-width: 1025px)').matches) {
      closeMobileNav();
    }
  });

  const scrollIndicator = document.getElementById('scrollIndicator');
  if (scrollIndicator) {
    window.addEventListener('scroll', function () {
      if (document.body.classList.contains('nav-open')) return;
      const winScroll =
        document.body.scrollTop || document.documentElement.scrollTop;
      const height =
        document.documentElement.scrollHeight -
        document.documentElement.clientHeight;
      scrollIndicator.style.width =
        (height > 0 ? (winScroll / height) * 100 : 0) + '%';
    });
  }

  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const id = this.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        closeMobileNav();
      }
    });
  });

  document.querySelectorAll('[data-faq-accordion]').forEach(function (accordion) {
    const items = accordion.querySelectorAll('.faq-item');

    function setItemOpen(item, open) {
      const trigger = item.querySelector('.faq-trigger');
      const panel = item.querySelector('.faq-panel');
      if (!trigger || !panel) return;
      item.classList.toggle('is-open', open);
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
      panel.hidden = !open;
    }

    items.forEach(function (item) {
      const trigger = item.querySelector('.faq-trigger');
      if (!trigger) return;

      setItemOpen(item, false);

      trigger.addEventListener('click', function () {
        const wasOpen = item.classList.contains('is-open');
        items.forEach(function (other) {
          setItemOpen(other, false);
        });
        if (!wasOpen) setItemOpen(item, true);
      });
    });
  });

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
        }
      });
    },
    { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
  );
  document.querySelectorAll('.reveal').forEach(function (el) {
    observer.observe(el);
  });

  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const fd = new FormData(contactForm);
      const name = fd.get('name') || '';
      const institute = fd.get('institute') || '';
      const instituteType = fd.get('instituteType') || '';
      const region = fd.get('region') || '';
      const phone = fd.get('phone') || '';
      const email = fd.get('email') || '';
      const message = fd.get('message') || '';
      const body = [
        'Name: ' + name,
        'Institute: ' + institute,
        'Institute type: ' + instituteType,
        'Region: ' + region,
        'Phone: ' + phone,
        'Email: ' + email,
        '',
        message,
      ].join('\n');
      window.location.href =
        'mailto:' +
        cfg.contactEmail +
        '?subject=' +
        encodeURIComponent('ilming — Demo / enquiry from ' + name) +
        '&body=' +
        encodeURIComponent(body);
    });
  }

  const yearEl = document.getElementById('footerYear');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  // Announcement dismiss
  const announceDismiss = document.getElementById('announceDismiss');
  const siteAnnouncement = document.getElementById('siteAnnouncement');
  if (siteAnnouncement) {
    if (localStorage.getItem('ilming_announce_dismissed') === '1') {
      document.body.classList.add('announcement-dismissed');
    }
    syncNavHeight();
  }
  if (announceDismiss && siteAnnouncement) {
    announceDismiss.addEventListener('click', function () {
      document.body.classList.add('announcement-dismissed');
      localStorage.setItem('ilming_announce_dismissed', '1');
      syncNavHeight();
    });
  }

  // Active nav from current path
  (function setActiveNav() {
    var current = window.location.pathname.replace(/\/$/, '') || '/';
    document
      .querySelectorAll('.nav-links a, .mobile-nav a:not(.nav-btn)')
      .forEach(function (a) {
        var href = (a.getAttribute('href') || '').replace(/\/$/, '') || '/';
        var active = href === current;
        if (!active && href === '/blog' && current.indexOf('/blog') === 0) {
          active = true;
        }
        if (active) a.classList.add('active');
      });
  })();

  (function initBlogFilters() {
    var filters = document.querySelector('.blog-filters');
    if (!filters) return;

    var featured = document.getElementById('blogFeatured');
    var cards = document.querySelectorAll('#blogGrid .blog-card[data-topics]');
    var empty = document.getElementById('blogEmpty');
    var buttons = filters.querySelectorAll('.blog-filter');

    function applyFilter(topic) {
      var visible = 0;

      if (featured) {
        var showFeatured =
          topic === 'all' ||
          (featured.getAttribute('data-topics') || '').split(/\s+/).indexOf(topic) !== -1;
        featured.classList.toggle('is-hidden', !showFeatured);
        if (showFeatured) visible += 1;
      }

      cards.forEach(function (card) {
        var topics = (card.getAttribute('data-topics') || '').split(/\s+/);
        var show = topic === 'all' || topics.indexOf(topic) !== -1;
        card.classList.toggle('is-hidden', !show);
        if (show) visible += 1;
      });

      if (empty) {
        empty.hidden = visible > 0;
      }
    }

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var topic = btn.getAttribute('data-filter') || 'all';
        buttons.forEach(function (other) {
          var isActive = other === btn;
          other.classList.toggle('blog-filter--active', isActive);
          other.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });
        applyFilter(topic);
      });
    });
  })();

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      var host = window.location.hostname;
      if (host !== 'localhost' && host !== '127.0.0.1' && window.location.protocol !== 'https:') {
        return;
      }
      navigator.serviceWorker
        .register('/sw.js?v=20260608')
        .catch(function () {});
    });
  }
})();
