import os
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from openai import OpenAI

from angelica_ai import genera_risposta

app = Flask(__name__, template_folder="tpl", static_folder="static")

client = OpenAI()

# Cartella dove salviamo gli mp3 della voce
AUDIO_DIR = Path(app.static_folder) / "tts"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def genera_audio(text: str, voice: str = "nova") -> str:
    """
    Genera un file audio mp3 con la voce di Angelica usando OpenAI TTS.
    Ritorna l'URL relativo da usare nel frontend.
    """
    filename = f"angelica_{voice}.mp3"
    output_path = AUDIO_DIR / filename

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
    ) as response:
        response.stream_to_file(output_path)

    return f"/static/tts/{filename}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message", "")
    voce_scelta = data.get("voice", "solstice")

    # mapping simbolico → voci OpenAI reali
    if voce_scelta == "aria":
        voice_id = "alloy"
    else:
        voice_id = "nova"

    risposta = genera_risposta(msg)
    audio_url = genera_audio(risposta, voice=voice_id)

    return jsonify({
        "response": risposta,
        "audio_url": audio_url
    })


if __name__ == "__main__":
    print("✨ Angelica con voce realistica è in ascolto…")
    app.run(host="0.0.0.0", port=10000)
