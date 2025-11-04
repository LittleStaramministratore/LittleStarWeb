from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "dati.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

# Assicuriamoci che la cartella uploads esista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Controlla se il file dati.json è scrivibile
if not os.access(DATA_FILE, os.W_OK):
    print("Il file non è scrivibile. Provo a sistemare i permessi...")
    try:
        os.chmod(DATA_FILE, 0o666)
    except Exception as e:
        print("Errore nel cambiare i permessi:", e)

# Funzione per caricare i dati
def carica_dati():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Funzione per salvare i dati
def salva_dati(dati):
    with open(DATA_FILE, "w") as f:
        json.dump(dati, f, indent=4)

@app.route("/")
def index():
    dati = carica_dati()
    return render_template("index.html", bambini=dati.get("bambini", []), eventi=dati.get("eventi", []))

@app.route("/api/dati")
def api_dati():
    dati = carica_dati()
    return jsonify(dati)

# Rotta per upload immagini
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Ascolta tutte le interfacce per permettere accesso da altri dispositivi sulla rete
    app.run(host="0.0.0.0", port=5000, debug=True)
