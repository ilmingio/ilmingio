/**
 * ilming marketing site — environment-aware URLs.
 * Static site on ilming.io; LMS app on app.ilming.io (or localhost:3000 in dev).
 */
(function (global) {
  const host = global.location?.hostname || '';
  const isLocal =
    host === 'localhost' || host === '127.0.0.1' || host.endsWith('.local');

  global.ILMING_SITE = {
    appUrl: isLocal ? 'http://localhost:3000' : 'https://app.ilming.io',
    siteUrl: isLocal ? 'http://localhost:8000' : 'https://ilming.io',
    contactEmail: 'contact@ilming.io',
    supportEmail: 'support@ilming.io',
    infoEmail: 'info@ilming.io',
    /** Institute pilots are provisioned by the team — not via /register (student signup). */
    instituteCtaUrl: '/contact/',
    studentEnrollPath: '/register',
    loginPath: '/login',
  };
})(typeof window !== 'undefined' ? window : globalThis);
