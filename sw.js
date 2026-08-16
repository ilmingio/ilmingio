/* ilming marketing site — lightweight PWA shell cache */
const CACHE = 'ilming-site-v20260815';

const PRECACHE = [
  '/',
  '/assets/css/site.css',
  '/assets/js/site.js',
  '/assets/js/config.js',
  '/assets/images/favicon/favicon.svg',
  '/assets/images/favicon/icon-192.png',
  '/assets/images/favicon/icon-512.png',
  '/assets/images/logo/ilming_icon-mark.svg',
  '/assets/images/favicon/site.webmanifest',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  const isNavigation =
    event.request.mode === 'navigate' ||
    (event.request.headers.get('accept') || '').includes('text/html');

  if (isNavigation) {
    event.respondWith(
      fetch(event.request).catch(() => caches.match('/') || caches.match(event.request))
    );
    return;
  }

  if (url.pathname.startsWith('/assets/')) {
    event.respondWith(
      caches.match(event.request).then(
        (cached) =>
          cached ||
          fetch(event.request).then((response) => {
            if (response.ok) {
              const copy = response.clone();
              caches.open(CACHE).then((cache) => cache.put(event.request, copy));
            }
            return response;
          })
      )
    );
  }
});
