import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from jinja2 import ChoiceLoader, FileSystemLoader
from angelica_ai import ask_angelica  # la tua IA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✔️ Cartella template DEFINITIVA che GitHub non traduce
TEMPLATE_DIR = os.path.join(BASE_DIR, "tpl")

# ✔️ Cartelle static che potrebbero esistere (static / statico)
STATIC_DIR = None
for folder in ("static", "statico"):
    path = os.path.join(BASE_DIR, folder)
    if os.path.isdir(path):
        STATIC_DIR = path
        break

# Se nessuna trovata, scegli 'static' come default
if STATIC_DIR is None:
    STATIC_DIR = os.path.join(BASE_DIR, "static")

# ✔️ Crea app Flask
app = Flask(__name__, static_folder=STATIC_DIR)

# ✔️ Loader che punta SOLO a tpl
app.jinja_loader = ChoiceLoader([FileSystemLoader(TEMPLATE_DIR)])


# 🔹 ROUTE HOME (carica index.html da tpl)
@app.route("/")
def home():
    return render_template("index.html")


# 🔹 ROUTE CHAT
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    user_message = (data.get("message") or "").strip()
    reply = ask_angelica(user_message)
    return jsonify({"reply": reply})


# 🔹 ROUTE SERVICE WORKER
@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(BASE_DIR, "service-worker.js",
                               mimetype="application/javascript")


# 🔹 AVVIO SERVER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
