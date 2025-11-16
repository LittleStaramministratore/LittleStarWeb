let deferredPrompt;
const installBtn = document.createElement('button');

installBtn.textContent = '📲 Installa Little Star';
installBtn.style.position = 'fixed';
installBtn.style.bottom = '20px';
installBtn.style.right = '20px';
installBtn.style.background = '#ff5f6d';
installBtn.style.color = 'white';
installBtn.style.border = 'none';
installBtn.style.padding = '12px 20px';
installBtn.style.borderRadius = '10px';
installBtn.style.fontSize = '16px';
installBtn.style.boxShadow = '0 4px 8px rgba(0,0,0,0.3)';
installBtn.style.cursor = 'pointer';
installBtn.style.display = 'none';
document.body.appendChild(installBtn);

// Intercetta l’evento che segnala che l’app è installabile
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  installBtn.style.display = 'block';
});

// Quando l’utente clicca “Installa”
installBtn.addEventListener('click', async () => {
  installBtn.style.display = 'none';
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  if (outcome === 'accepted') {
    console.log('✅ App installata con successo');
  } else {
    console.log('❌ Installazione annullata');
  }
  deferredPrompt = null;
});
