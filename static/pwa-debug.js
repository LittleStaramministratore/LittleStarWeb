// ===============================
// 🌟 Little Star PWA Debug Script
// ===============================

console.log("📱 PWA Debug: script caricato con successo ✅");

let deferredPrompt;

// Quando Chrome intercetta l'evento 'beforeinstallprompt'
window.addEventListener('beforeinstallprompt', (e) => {
    console.log("📱 PWA Debug: beforeinstallprompt catturato correttamente");
    e.preventDefault();
    deferredPrompt = e;

    // Crea il bottone d'installazione
    const installBtn = document.createElement('button');
    installBtn.textContent = '📲 Installa Little Star App';
    installBtn.style.position = 'fixed';
    installBtn.style.bottom = '20px';
    installBtn.style.left = '50%';
    installBtn.style.transform = 'translateX(-50%)';
    installBtn.style.background = '#ff5f6d';
    installBtn.style.color = '#fff';
    installBtn.style.padding = '12px 24px';
    installBtn.style.border = 'none';
    installBtn.style.borderRadius = '10px';
    installBtn.style.fontWeight = 'bold';
    installBtn.style.cursor = 'pointer';
    installBtn.style.zIndex = '9999';
    installBtn.style.boxShadow = '0 4px 10px rgba(0,0,0,0.3)';
    installBtn.style.fontSize = '16px';

    document.body.appendChild(installBtn);

    installBtn.addEventListener('click', async () => {
        installBtn.style.display = 'none';
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`🎯 PWA Debug: l'utente ha scelto: ${outcome}`);
        deferredPrompt = null;
    });
});

// Quando l'app viene installata
window.addEventListener('appinstalled', () => {
    console.log("✅ PWA Debug: App installata con successo!");
});
