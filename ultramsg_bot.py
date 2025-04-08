import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ultramsg credentials
INSTANCE_ID = "instance113480"
TOKEN = "788d1vutl9mxas1c"
ULTRAMSG_URL = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

# Your OrderGenie backend (Render)
ORDERGENIE_BOT_URL = "https://ordergenie-bot.onrender.com/webhook"

@app.route("/", methods=["GET"])
def home():
    return "Ultramsg Bot is Running!"

@app.route("/ultramsg-webhook", methods=["POST"])
def ultramsg_webhook():
    data = request.form
    sender = data.get("from")
    message = data.get("body", "")

    # Forward message to OrderGenie bot
    try:
        response = requests.post(ORDERGENIE_BOT_URL, json={"message": message})
        bot_reply = response.json().get("reply", "Sorry, koi response nahi mila.")
    except:
        bot_reply = "Error: OrderGenie Bot se reply nahi mila."

    # Send reply back to WhatsApp via Ultramsg
    payload = {
        "token": TOKEN,
        "to": sender,
        "body": bot_reply
    }
    requests.post(ULTRAMSG_URL, data=payload)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
