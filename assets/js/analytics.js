/** Deferred Google Tag Manager + GA (from legacy ilming.io setup) */
window.addEventListener('load', function () {
  (function (w, d, s, l, i) {
    w[l] = w[l] || [];
    w[l].push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var f = d.getElementsByTagName(s)[0];
    var j = d.createElement(s);
    var dl = l !== 'dataLayer' ? '&l=' + l : '';
    j.async = true;
    j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
    f.parentNode.insertBefore(j, f);
  })(window, document, 'script', 'dataLayer', 'GTM-W6FCQMT3');

  var ga = document.createElement('script');
  ga.async = true;
  ga.src = 'https://www.googletagmanager.com/gtag/js?id=G-L9XCLHBPMR';
  document.head.appendChild(ga);
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', 'G-L9XCLHBPMR');
});
