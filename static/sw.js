// Ejitas Service Worker – Offline-first caching
const CACHE_NAME = 'ejitas-v1';
const STATIC_ASSETS = [
  '/',
  '/static/js/app.js',
  '/static/images/ejitas-logo.jpg',
  '/static/manifest.json'
];

// Install – pre-cache essential assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate – clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// Fetch – network-first for API, cache-first for static
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  // API calls: network-first with fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Static assets & pages: cache-first with network fallback
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) {
        // Update cache in background
        fetch(event.request).then((response) => {
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, response));
        }).catch(() => {});
        return cached;
      }
      return fetch(event.request).then((response) => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        return response;
      });
    })
  );
});
