import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS 
from openai import OpenAI

app = Flask(__name__, static_folder=None)
CORS(app) 

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Defina OPENAI_API_KEY nas Environment Variables do Vercel")

client = OpenAI(api_key=OPENAI_KEY)


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "SUSI (Flask on Vercel)"})


@app.route("/chat", methods=["POST"])
def chat():
    try:
        payload = request.get_json(force=True)
        user_message = payload.get("message", "")
        if not user_message:
            return jsonify({"reply": "Envie uma 'message' no body."}), 400

        system_prompt = (
            "Você é a SUSI, assistente virtual de saúde. "
            "Seja empática, prática e NÃO forneça diagnóstico definitivo. "
            "Oriente procurar atendimento quando necessário."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=600
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Erro interno: {str(e)}"}), 500
