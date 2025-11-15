from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from angelica_ai import ask_angelica  # funzione che risponde

# ✅ Flask ora sa dove cercare i file statici e i templates HTML
app = Flask(__name__, static_folder='static', template_folder='templates')

# 🔹 Rotta principale (index)
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 Rotta per Angelica (chat)
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    reply = ask_angelica(user_message)
    return jsonify({"reply": reply})

# 🔹 Rotta per il service worker (necessario per la PWA)
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js', mimetype='application/javascript')

# 🔹 Avvio server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # 🔥 Render usa la porta 10000
    app.run(host="0.0.0.0", port=port)
