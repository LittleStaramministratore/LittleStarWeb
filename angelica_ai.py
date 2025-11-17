<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>Angelica</title>

<style>
body {
    margin: 0;
    background: #f7f7f7;
    font-family: Arial, sans-serif;
}

/* contenitore principale */
#chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding-bottom: 140px; /* evita che l’input copra i messaggi */
}

/* messaggi */
#chat {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}

/* stile messaggi */
.msg {
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 12px;
    max-width: 80%;
    font-size: 1rem;
}

.user {
    background: #cfe3ff;
    align-self: flex-end;
}

.bot {
    background: #ffe9c7;
    align-self: flex-start;
}

/* barra input */
#input-area {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: white;
    padding: 12px;
    display: flex;
    gap: 10px;
    border-top: 1px solid #cccccc;
}
</style>

</head>
<body>

<div id="chat-container">

    <div id="chat"></div>

    <div id="input-area">
        <input id="msg" type="text" placeholder="Scrivi qui..." style="flex:1; padding:10px; font-size:1rem;">
        <button onclick="send()" style="padding:10px 14px; font-size:1rem;">➤</button>
    </div>

</div>

<script>
// ---------------------
// ANGELICA PARLA
// ---------------------
function speak(text){
    if("speechSynthesis" in window){
        let voice = new SpeechSynthesisUtterance(text);
        voice.lang = "it-IT";
        voice.rate = 1;
        speechSynthesis.speak(voice);
    }
}

// ---------------------
// GESTIONE MESSAGGI
// ---------------------
function appendMessage(text, cls){
    let div = document.createElement("div");
    div.className = "msg " + cls;
    div.innerText = text;
    document.getElementById("chat").appendChild(div);

    // autoscroll
    let chat = document.getElementById("chat");
    chat.scrollTop = chat.scrollHeight;
}

// ---------------------
// INVIO MESSAGGIO
// ---------------------
async function send(){
    const campo = document.getElementById("msg");
    const text = campo.value.trim();
    if(!text) return;

    appendMessage(text, "user");
    campo.value = "";

    const response = await fetch("/chat", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({message: text})
    });

    const data = await response.json();
    const bot = data.response;

    appendMessage(bot, "bot");
    speak(bot);
}
</script>

</body>
</html>
