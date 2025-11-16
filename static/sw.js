const CACHE_NAME = 'little-star-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/icon-192.png',
  '/static/icon-512.png',
];

// Installazione: cache dei file principali
self.addEventListener('install', event => {
  console.log('Service Worker installato ✅');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching file iniziali...');
        return cache.addAll(urlsToCache);
      })
  );
});

// Attivazione: pulizia cache vecchie
self.addEventListener('activate', event => {
  console.log('Service Worker attivato 🚀');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(name => {
          if (name !== CACHE_NAME) {
            console.log('Cache vecchia rimossa:', name);
            return caches.delete(name);
          }
        })
      );
    })
  );
});

// Gestione richieste (offline support)
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Se il file è in cache, lo usa
        if (response) {
          return response;
        }
        // Altrimenti prova a prenderlo dalla rete
        return fetch(event.request).catch(() => {
          // Se anche la rete fallisce, mostra un fallback base (facoltativo)
          return new Response('Offline, riprova più tardi.');
        });
      })
  );
});
