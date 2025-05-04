from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAO9sv01cTUBO0TYJM7ZBWOESZCkZC82H16Dkp5LvVcWw2SFbM3cmXS6YpzfhRKpcttZC147Agvu4v61z3GDKJkwW8csaJg1IJw2rFq0VuiMSbR3JNewjec8vZBoRsFZCDQeWhoP0VNbOCZBrBrKxZC9ZAZCw4hQwnwLZAJB29xXDzSpe8bezy7MOvpQJBobf0iN6FL'
VERIFY_TOKEN = 'ghorishopaiagent'

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Invalid verification token", 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data['entry']:
        for msg in entry['messaging']:
            if msg.get('message'):
                sender_id = msg['sender']['id']
                text = msg['message'].get('text')
                if text:
                    send_message(sender_id, f"You said: {text}")
    return "ok", 200

def send_message(recipient_id, message_text):
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post("https://graph.facebook.com/v17.0/me/messages", params=params, headers=headers, json=data)

if __name__ == "__main__":
    app.run(debug=True)
