import os
import requests
from flask import Flask, request, abort

TOKEN = os.environ["BOT_TOKEN"]
APP_URL = os.environ["RENDER_EXTERNAL_URL"]
SECRET = os.environ["WEBHOOK_SECRET"]

app = Flask(__name__)

API = f"https://api.telegram.org/bot{TOKEN}/"

requests.post(
    API + "setWebhook",
    json={
        "url": APP_URL + "/webhook",
        "secret_token": SECRET
    },
    timeout=15
).raise_for_status()


def send_message(chat_id, text):
    requests.post(
        API + "sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=15
    )


@app.route("/")
def home():
    return "LEAF VILLAGE Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token"
    ) != SECRET:
        abort(403)

    data = request.get_json(silent=True) or {}
    message = data.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "")

    if not chat_id:
        return "OK"

    if text == "/start":
        send_message(
            chat_id,
            "🔥 Welcome to LEAF VILLAGE!\n"
            "🏆 Guild ID: 3106886619\n"
            "Use /guild to check guild information."
        )

    elif text == "/guild":
        send_message(
            chat_id,
            "🏆 LEAF VILLAGE\n"
            "Guild ID: 3106886619\n"
            "Glory tracking: Coming soon!"
        )

    else:
        send_message(chat_id, "Use /start or /guild")

    return "OK"
