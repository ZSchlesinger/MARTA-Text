from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods =['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with simple text message."""

    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    if body == 'hello':
        resp.message("hi!")
    elif body == 'bye':
        resp.message("Goodbye")
    else:
        resp.message("alternate")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)