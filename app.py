from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Your page access token and verify token
PAGE_ACCESS_TOKEN = 'EAAO9sv01cTUBO0TYJM7ZBWOESZCkZC82H16Dkp5LvVcWw2SFbM3cmXS6YpzfhRKpcttZC147Agvu4v61z3GDKJkwW8csaJg1IJw2rFq0VuiMSbR3JNewjec8vZBoRsFZCDQeWhoP0VNbOCZBrBrKxZC9ZAZCw4hQwnwLZAJB29xXDzSpe8bezy7MOvpQJBobf0iN6FL'
VERIFY_TOKEN = 'ghorishopaiagent'

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return "Verification token mismatch", 403
        return "Missing parameters", 400

    elif request.method == 'POST':
        data = request.get_json()

        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                if messaging_event.get("message"):
                    if "text" in messaging_event["message"]:
                        user_message = messaging_event["message"]["text"]
                        send_message(sender_id, f"Hi! You said: {user_message}")

        return "Message received", 200

def send_message(recipient_id, message_text):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(
        f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}",
        headers=headers,
        json=payload
    )
    print("Sent:", message_text)

if __name__ == '__main__':
    app.run(debug=True)
