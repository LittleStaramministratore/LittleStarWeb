self.addEventListener('install', event => {
    console.log('Service Worker installato');
});

self.addEventListener('fetch', event => {
    // Qui puoi aggiungere caching dei file statici se vuoi
});
