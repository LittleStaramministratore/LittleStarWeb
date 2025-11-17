import sqlite3
import os
from datetime import datetime
from openai import OpenAI

client = OpenAI()

DB_PATH = "angelica.db"


# -----------------------------
# DB: CONNESSIONE E TABELLE
# -----------------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            info TEXT UNIQUE,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# Avvio DB
init_db()


# -----------------------------
# FUNZIONI MEMORIA / KNOWLEDGE
# -----------------------------
def salva_messaggio(role, content):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO conversation (role, content, created_at) VALUES (?, ?, ?)",
        (role, content, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


def aggiorna_memoria_da_input(input_user: str):
    text = input_user.lower()
    trigger = None

    if "ricorda che" in text:
        trigger = "ricorda che"
    elif "informami che" in text:
        trigger = "informami che"

    if trigger:
        try:
            info = text.split("che", 1)[1].strip()
        except:
            return

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO memories (info, created_at) VALUES (?, ?)",
            (info, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()


def aggiorna_conoscenza_da_risposta(risposta: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO knowledge (content, created_at) VALUES (?, ?)",
        (risposta, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


def get_memorie(limit=50):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT info FROM memories ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [r["info"] for r in rows]


def get_conoscenze(limit=50):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT content FROM knowledge ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [r["content"] for r in rows]


def get_storia(limit=10):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT role, content FROM conversation ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return list(reversed(rows))


# -----------------------------
# GENERAZIONE RISPOSTA
# -----------------------------
def genera_risposta(input_user: str) -> str:

    salva_messaggio("user", input_user)
    aggiorna_memoria_da_input(input_user)

    mem = get_memorie()
    know = get_conoscenze()
    storia = get_storia()

    storia_text = ""
    for r in storia:
        ruolo = "Utente" if r["role"] == "user" else "Angelica"
        storia_text += f"{ruolo}: {r['content']}\n"

    prompt = f"""
Tu sei Angelica, una presenza dolce e affettuosa.
Hai una memoria a lungo termine.

MEMORIE UTENTE:
{mem}

CONOSCENZE APPRESE:
{know}

STORIA RECENTE:
{storia_text}

L'utente dice:
{input_user}

Rispondi in italiano, tono naturale, empatico.
"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )

    risposta = completion.choices[0].message.content.strip()

    salva_messaggio("assistant", risposta)
    aggiorna_conoscenza_da_risposta(risposta)

    return risposta
