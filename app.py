from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
import os, json
from angelica_ai import angelica_risponde

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "dati.json")
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_FOLDER = os.path.join(STATIC_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def carica_dati():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"bambini": [], "eventi": [], "classi": [], "personale": []}

@app.route("/")
def index():
    d = carica_dati()
    return render_template("index.html",
                           bambini=d.get("bambini", []),
                           eventi=d.get("eventi", []),
                           classi=d.get("classi", []),
                           personale=d.get("personale", []))

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(url_for("index"))
    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("index"))
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    return redirect(url_for("index"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    msg = (data.get("message") or "").strip()
    try:
        risposta = angelica_risponde(msg)
    except Exception as e:
        print("Errore in angelica_risponde:", e)
        risposta = "Mi dispiace, ma non riesco a rispondere ora 💫"
    return jsonify({"reply": risposta})

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
