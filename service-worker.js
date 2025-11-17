self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  self.clients.claim();
});

// NIENTE CACHE! 
// Tutto passa sempre dalla rete per evitare problemi su iPhone.
self.addEventListener("fetch", (event) => {
  return;
});
