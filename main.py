from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import constants

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Locquet!'

@app.route("/hello")
def test():
    return 'testing'

@app.route("/sms", methods =['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with simple text message."""

    body = str(request.values.get('Body', None)).lower()

    # Start our TwiML response
    resp = MessagingResponse()

    if body == 'helpme':
        resp.message(constants.helpMessage)
    elif body == 'bye':
        resp.message("Goodbye")
    else:
        resp.message(constants.fallthroughMessage)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
