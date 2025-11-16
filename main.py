import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from jinja2 import ChoiceLoader, FileSystemLoader
from angelica_ai import ask_angelica  # la tua funzione AI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cartella template = "views"
template_dirs = [os.path.join(BASE_DIR, "views")]

# Cercare cartella static (static o statico)
static_dir = None
for folder in ("static", "statico"):
    path = os.path.join(BASE_DIR, folder)
    if os.path.isdir(path):
        static_dir = path
        break

if static_dir is None:
    static_dir = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=static_dir)

# Loader multiplo (solo views)
app.jinja_loader = ChoiceLoader(
    [FileSystemLoader(d) for d in template_dirs]
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    user_message = (data.get("message") or "").strip()
    reply = ask_angelica(user_message)
    return jsonify({"reply": reply})

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(BASE_DIR, "service-worker.js", mimetype="application/javascript")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
