console.log("🌟 Angelica front-end caricato");

const chatEl = document.getElementById("chat");
const inputEl = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

function addMessage(text, sender = "bot", opts = {}) {
    const row = document.createElement("div");
    row.className = `message-row ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = text;

    row.appendChild(bubble);
    chatEl.appendChild(row);
    chatEl.scrollTop = chatEl.scrollHeight;
    return row;
}

function addTyping() {
    const row = document.createElement("div");
    row.className = "message-row bot";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    const wrapper = document.createElement("div");
    wrapper.className = "typing-indicator";

    for (let i = 0; i < 3; i++) {
        const dot = document.createElement("span");
        dot.className = "typing-dot";
        wrapper.appendChild(dot);
    }

    bubble.appendChild(wrapper);
    row.appendChild(bubble);
    chatEl.appendChild(row);
    chatEl.scrollTop = chatEl.scrollHeight;
    return row;
}

function removeElement(el) {
    if (el && el.parentNode) {
        el.parentNode.removeChild(el);
    }
}

async function sendMessage() {
    const text = (inputEl.value || "").trim();
    if (!text) return;

    addMessage(text, "user");
    inputEl.value = "";
    inputEl.focus();

    const typingRow = addTyping();

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await res.json();
        removeElement(typingRow);

        const reply = data.response || "Ho avuto un piccolo problema nel risponderti.";
        addMessage(reply, "bot");

        if (data.audio_url) {
            const audio = new Audio(data.audio_url);
            audio.play().catch(err => console.warn("Audio non riproducibile:", err));
        }

    } catch (err) {
        console.error("Errore chiamata /chat:", err);
        removeElement(typingRow);
        addMessage("Ops, c'è stato un errore di connessione. Riprova tra poco 💫", "bot");
    }
}

// invio da bottone
sendBtn.addEventListener("click", sendMessage);

// invio con Enter
inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
});

// messaggio di benvenuto
addMessage("Ciao, sono Angelica 🌟\nCome posso aiutarti oggi?", "bot");
