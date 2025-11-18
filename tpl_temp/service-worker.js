const CACHE_NAME = "angelica-cache-v1";
const OFFLINE_MSG = "Sei offline 💫 Riprova quando la connessione torna disponibile.";

// Installazione del Service Worker
self.addEventListener("install", (event) => {
  self.skipWaiting();
});

// Attivazione
self.addEventListener("activate", (event) => {
  clients.claim();
});

// Intercetta tutte le richieste
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    fetch(event.request)
      .then((response) => response)
      .catch(() => {
        // Risposta offline di fallback
        return new Response(OFFLINE_MSG, {
          headers: { "Content-Type": "text/plain; charset=utf-8" }
        });
      })
  );
});
