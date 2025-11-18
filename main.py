import json
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI

from angelica_ai import genera_risposta

# IMPORTANTE: specifico template_folder="tpl"
app = Flask(__name__, template_folder="tpl", static_folder="static")

client = OpenAI()

# Cartella dove salviamo gli mp3 della voce
AUDIO_DIR = Path(app.static_folder) / "tts"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# File di conoscenza della scuola
DATA_PATH = Path("little_star_knowledge.json")


def load_knowledge() -> dict:
    if DATA_PATH.exists():
        with DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_knowledge(data: dict):
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def genera_audio(text: str, voice: str = "alloy") -> str:
    """
    Genera un file mp3 con voce calda e dolce (Angelica).
    Usato solo su PC, non su smartphone.
    """
    filename = f"angelica_{voice}.mp3"
    output_path = AUDIO_DIR / filename

    # Genera audio con streaming
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text
    ) as response:
        response.stream_to_file(output_path)

    return f"/static/tts/{filename}"


@app.route("/")
def home():
    # Viene preso da tpl/index.html
    return render_template("index.html")


@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(app.static_folder, "service-worker.js", mimetype="application/javascript")


def handle_admin_command(msg: str) -> dict:
    """
    Gestione comandi del tipo:
    /aggiungi personale Maestro Luca
    """
    parts = msg.strip().split()
    if len(parts) < 3:
        return {
            "response": "Comando non valido. Usa: /aggiungi categoria valore",
            "audio_url": None
        }

    _, categoria, *rest = parts
    valore = " ".join(rest)

    data = load_knowledge()

    if categoria not in data:
        data[categoria] = []

    if not isinstance(data[categoria], list):
        data[categoria] = [data[categoria]]

    data[categoria].append(valore)
    save_knowledge(data)

    return {
        "response": f'Ho aggiunto "{valore}" alla categoria "{categoria}".',
        "audio_url": None
    }


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message", "").strip()

    if not msg:
        return jsonify({"response": "Dimmi pure, ti ascolto 💫", "audio_url": None})

    # Comandi admin
    if msg.startswith("/aggiungi"):
        return jsonify(handle_admin_command(msg))

    # Carica dati scuola
    knowledge = load_knowledge()

    # Risposta AI
    risposta = genera_risposta(msg, knowledge=knowledge)

    # Genera audio (solo PC lo riprodurrà)
    audio_url = genera_audio(risposta, voice="alloy")

    return jsonify({
        "response": risposta,
        "audio_url": audio_url
    })


if __name__ == "__main__":
    print("✨ Angelica (voce calda e dolce) è pronta.")
    app.run(host="0.0.0.0", port=10000, debug=True)
