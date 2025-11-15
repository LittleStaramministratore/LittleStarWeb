const CACHE_NAME = "littlestar-cache-v1";

const urlsToCache = [
  "/",
  "/static/manifest.json",
  "/static/angelica_avatar.png",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png"
];

// ✅ Installazione: crea la cache
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
      .catch((err) => console.error("Errore nel caching iniziale:", err))
  );
  self.skipWaiting();
});

// ✅ Attivazione: pulisce le cache vecchie
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log("🧹 Eliminata cache obsoleta:", key);
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

// ✅ Fetch: serve prima dalla cache, poi dalla rete
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return; // ignora POST o altri metodi

  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        if (cachedResponse) return cachedResponse;

        return fetch(event.request)
          .then((networkResponse) => {
            // salva in cache la nuova risposta
            return caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, networkResponse.clone());
              return networkResponse;
            });
          })
          .catch(() => caches.match("/")); // fallback offline
      })
      .catch((err) => console.error("Errore nel fetch:", err))
  );
});
