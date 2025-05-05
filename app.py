# === File: app.py ===
from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction

openai.api_key = os.getenv("OPENAI_API_KEY")

chat_logs = {}

def ask_chatgpt(user_id, message):
    if user_id not in chat_logs:
        chat_logs[user_id] = []

    chat_logs[user_id].append({"role": "user", "content": message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_logs[user_id][-10:],
            temperature=0.7
        )
        reply = response.choices[0].message['content'].strip()
        chat_logs[user_id].append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "Missing user_id or message"}), 400

    reply = ask_chatgpt(user_id, message)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
