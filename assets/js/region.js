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
    aed: { place: 'the UAE', here: 'UAE', circle: 'AED 4', kicker: 'For Tahfiz institutes in the UAE' },
    sar: { place: 'Saudi Arabia', here: 'Saudi Arabia', circle: 'SAR 4', kicker: 'For Tahfiz institutes in Saudi Arabia' },
    qar: { place: 'Qatar', here: 'Qatar', circle: 'QAR 4', kicker: 'For Tahfiz institutes in Qatar' },
    kwd: { place: 'Kuwait', here: 'Kuwait', circle: 'KWD 0.300', kicker: 'For Tahfiz institutes in Kuwait' },
    bhd: { place: 'Bahrain', here: 'Bahrain', circle: 'BHD 0.400', kicker: 'For Tahfiz institutes in Bahrain' },
    omr: { place: 'Oman', here: 'Oman', circle: 'OMR 0.400', kicker: 'For Tahfiz institutes in Oman' },
    gbp: { place: 'the United Kingdom', here: 'United Kingdom', circle: '£1', kicker: 'For Tahfiz institutes in the United Kingdom' },
    inr: { place: 'India', here: 'India', circle: '₹50', kicker: 'For Tahfiz institutes in India' },
    usd: { place: 'your country', here: 'international', circle: '$1', kicker: 'For Tahfiz institutes' },
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
        'Halaqa is a 30-day trial for 10 students. Circle is ' +
        info.circle +
        ' per active student each month for institutes in ' +
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

  function suggest(region) {
    var here = currentRegion();
    if (!here || !region || region === here || !PATH[region]) return;
    var info = COPY[region];
    var current = COPY[here];
    var nav = document.querySelector('.currency-switch');
    if (!nav || !info || !current) return;
    var note = document.getElementById('regionSuggest');
    if (!note) {
      note = document.createElement('p');
      note.id = 'regionSuggest';
      note.className = 'region-suggest';
      nav.insertAdjacentElement('afterend', note);
    }
    note.textContent = '';
    note.appendChild(document.createTextNode('This page shows ' + current.here + ' prices. '));
    var link = document.createElement('a');
    link.href = PATH[region];
    link.textContent = region === 'usd' ? 'View international pricing' : 'View pricing for ' + info.place;
    note.appendChild(link);
    note.appendChild(document.createTextNode('.'));
  }

  if (!document.getElementById('regionSuggestStyle')) {
    var style = document.createElement('style');
    style.id = 'regionSuggestStyle';
    style.textContent =
      '.region-suggest{margin:0.85rem auto 0;max-width:40rem;font-size:0.95rem;line-height:1.45;color:#3d4f49}' +
      '.region-suggest a{color:#0a6b5c;font-weight:600}';
    document.head.appendChild(style);
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
  var tz = tzRegion();
  var guess = choice || tz || (here || 'usd');
  apply(guess);
  document.documentElement.classList.remove('region-pending');

  if (choice) {
    suggest(choice);
    return;
  }

  if (tz) suggest(tz);

  fetch('https://get.geojs.io/v1/ip/country.json')
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      var region = COUNTRY[(data.country || '').toUpperCase()] || '';
      document.documentElement.classList.remove('region-pending');
      if (!region) {
        if (!tz && !here) apply('usd');
        return;
      }
      if (!choice) apply(region);
      suggest(region);
    })
    .catch(function () {
      document.documentElement.classList.remove('region-pending');
      if (!tz && !here) apply('usd');
    });
})();
