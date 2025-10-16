import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["https://vita-blush-psi.vercel.app"]}})

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Defina a variável OPENAI_API_KEY no painel da Vercel!")

client = OpenAI(api_key=OPENAI_KEY)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "assistant": "SUSI"}), 200


@app.route("/chat", methods=["POST"])
def chat():
    try:
        payload = request.get_json(force=True)
        user_message = payload.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Envie uma mensagem no campo 'message'."}), 400

        system_prompt = (
            "Você é a SUSI, uma assistente virtual de saúde simpática, empática e informativa. "
            "Você deve orientar o usuário sobre bem-estar, prevenção e autocuidado, mas SEM dar diagnósticos. "
            "Se a questão for séria, recomende procurar atendimento médico profissional."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.6,
            max_tokens=500
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply}), 200

    except Exception as e:
        print("❌ ERRO:", e)
        return jsonify({"reply": f"Erro interno: {str(e)}"}), 500

@app.route("/favicon.ico")
def favicon():
    return "", 204

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
