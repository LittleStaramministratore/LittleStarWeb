import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from jinja2 import ChoiceLoader, FileSystemLoader
from angelica_ai import ask_angelica  # la tua funzione AI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cerchiamo sia "templates" che "Modelli"
template_dirs = []
for folder in ("templates", "Modelli"):
    path = os.path.join(BASE_DIR, folder)
    if os.path.isdir(path):
        template_dirs.append(path)

# Cerchiamo anche "static" e "statico" (per sicurezza)
static_dir = None
for folder in ("static", "statico"):
    path = os.path.join(BASE_DIR, folder)
    if os.path.isdir(path):
        static_dir = path
        break

# Se non troviamo nulla, usiamo "static" come default
if static_dir is None:
    static_dir = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=static_dir)

# Loader multiplo per i template: templates / Modelli
if template_dirs:
    app.jinja_loader = ChoiceLoader(
        [FileSystemLoader(d) for d in template_dirs]
    )

# 🔹 Rotta principale (home)
@app.route("/")
def home():
    # Flask cercherà index.html in tutte le cartelle trovate sopra
    return render_template("index.html")

# 🔹 Rotta chat / Angelica
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    user_message = (data.get("message") or "").strip()
    reply = ask_angelica(user_message)
    return jsonify({"reply": reply})

# 🔹 Service worker (PWA)
@app.route("/service-worker.js")
def service_worker():
    # lo cerchiamo nella root del progetto
    return send_from_directory(BASE_DIR, "service-worker.js", mimetype="application/javascript")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
