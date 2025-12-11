from flask import Flask, request
from openai import OpenAI
import telegram
import os

app = Flask(__name__)

OPENAI_KEY = os.getenv("OPENAI_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

client = OpenAI(api_key=OPENAI_KEY)
bot = telegram.Bot(token=TELEGRAM_TOKEN)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" not in data:
        return {"ok": True}

    chat_id = data["message"]["chat"]["id"]
    user_msg = data["message"]["text"]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": user_msg}]
    )

    bot.sendMessage(chat_id, response.choices[0].message.content)
    return {"ok": True}

@app.route("/")
def home():
    return "Bot actif sur Render !"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
