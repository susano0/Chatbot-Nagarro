from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse,Body,Media,Message
from utils import fetch_reply
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('from')
    # Create reply
    resp = MessagingResponse()
    reply = fetch_reply(msg,sender)
    if isinstance(reply, str):
        resp.message(reply)
    elif isinstance(reply, tuple):
        resp.message(reply[0]).media(reply[1])
    else:
        for msg in list(map(lambda x:Message(x),reply)):
            resp.append(msg)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)