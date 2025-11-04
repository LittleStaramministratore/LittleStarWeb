window.addEventListener('load', async () => {
    if ('serviceWorker' in navigator) {
        const reg = await navigator.serviceWorker.getRegistration();
        console.log('🔍 Service Worker trovato:', !!reg);
    }

    const linkManifest = document.querySelector('link[rel="manifest"]');
    if (linkManifest) {
        console.log('✅ Manifest trovato:', linkManifest.href);
    } else {
        console.warn('⚠️ Manifest mancante nel <head>');
    }

    window.matchMedia('(display-mode: standalone)').addEventListener('change', e => {
        console.log('🪄 Modalità display cambiata:', e.matches ? 'Standalone' : 'Browser');
    });

    if (window.matchMedia('(display-mode: standalone)').matches) {
        console.log('📱 App già installata!');
    } else {
        console.log('🌐 Non installata ancora.');
    }

    window.addEventListener('beforeinstallprompt', (e) => {
        console.log('📲 Evento beforeinstallprompt catturato!');
    });
});
