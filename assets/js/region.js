(function () {
  var KEY = 'ilming-region';
  var COUNTRY = {
    AE: 'aed',
    SA: 'sar',
    QA: 'qar',
    KW: 'kwd',
    BH: 'bhd',
    OM: 'omr',
    GB: 'gbp',
    IN: 'inr',
  };
  var TZ = {
    'Asia/Dubai': 'aed',
    'Asia/Riyadh': 'sar',
    'Asia/Qatar': 'qar',
    'Asia/Kuwait': 'kwd',
    'Asia/Bahrain': 'bhd',
    'Asia/Muscat': 'omr',
    'Europe/London': 'gbp',
    'Asia/Kolkata': 'inr',
    'Asia/Calcutta': 'inr',
  };
  var PATH = {
    inr: '/pricing/',
    aed: '/pricing/aed/',
    sar: '/pricing/sar/',
    qar: '/pricing/qar/',
    kwd: '/pricing/kwd/',
    bhd: '/pricing/bhd/',
    omr: '/pricing/omr/',
    gbp: '/pricing/gbp/',
    usd: '/pricing/usd/',
  };
  var COPY = {
    aed: { place: 'the UAE', circle: 'AED 69', kicker: 'For Tahfiz institutes in the UAE' },
    sar: { place: 'Saudi Arabia', circle: 'SAR 75', kicker: 'For Tahfiz institutes in Saudi Arabia' },
    qar: { place: 'Qatar', circle: 'QAR 69', kicker: 'For Tahfiz institutes in Qatar' },
    kwd: { place: 'Kuwait', circle: 'KWD 6', kicker: 'For Tahfiz institutes in Kuwait' },
    bhd: { place: 'Bahrain', circle: 'BHD 7', kicker: 'For Tahfiz institutes in Bahrain' },
    omr: { place: 'Oman', circle: 'OMR 7', kicker: 'For Tahfiz institutes in Oman' },
    gbp: { place: 'the United Kingdom', circle: '£15', kicker: 'For Tahfiz institutes in the United Kingdom' },
    inr: { place: 'India', circle: '₹499', kicker: 'For Tahfiz institutes in India' },
    usd: { place: 'your country', circle: '$19', kicker: 'For Tahfiz institutes' },
  };

  function saved() {
    try {
      return localStorage.getItem(KEY) || '';
    } catch (e) {
      return '';
    }
  }

  function tzRegion() {
    try {
      return TZ[Intl.DateTimeFormat().resolvedOptions().timeZone] || '';
    } catch (e) {
      return '';
    }
  }

  function currentRegion() {
    var path = location.pathname.replace(/\/index\.html$/, '').replace(/\/+$/, '');
    var keys = Object.keys(PATH);
    for (var i = 0; i < keys.length; i++) {
      var region = keys[i];
      var url = PATH[region].replace(/\/+$/, '');
      if (region !== 'inr' && path.endsWith(url)) return region;
    }
    if (path.endsWith('/pricing')) return 'inr';
    return '';
  }

  function apply(region) {
    var info = COPY[region] || COPY.usd;
    var lead = document.getElementById('homePricingLead');
    if (lead) {
      lead.textContent =
        'Halaqa is free for 30 students. Circle is ' +
        info.circle +
        ' a month for institutes in ' +
        info.place +
        '.';
    }
    var cta = document.getElementById('homePricingCta');
    if (cta) {
      cta.textContent = region === 'usd' ? 'See international pricing' : 'See pricing';
      cta.href = PATH[region] || PATH.usd;
    }
    var kicker = document.getElementById('heroKicker');
    if (kicker) kicker.textContent = info.kicker;
  }

  document.querySelectorAll('[data-region]').forEach(function (el) {
    el.addEventListener('click', function () {
      try {
        localStorage.setItem(KEY, el.getAttribute('data-region') || '');
      } catch (e) {}
    });
  });

  var choice = saved();
  var here = currentRegion();
  var guess = choice || tzRegion() || (here || 'usd');
  apply(guess);

  if (choice) {
    document.documentElement.classList.remove('region-pending');
    return;
  }

  fetch('https://get.geojs.io/v1/ip/country.json')
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      var region = COUNTRY[(data.country || '').toUpperCase()] || '';
      if (!region) {
        if (!tzRegion() && here === 'inr') location.replace(PATH.usd);
        document.documentElement.classList.remove('region-pending');
        if (!tzRegion()) apply('usd');
        return;
      }
      apply(region);
      if (here === 'inr' && region !== 'inr') location.replace(PATH[region]);
      else document.documentElement.classList.remove('region-pending');
    })
    .catch(function () {
      document.documentElement.classList.remove('region-pending');
      if (!tzRegion() && !here) apply('usd');
    });
})();
