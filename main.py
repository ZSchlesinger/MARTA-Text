from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import constants
from autocorrect import spell

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

    commandList = ['help','stations near me','route info','outages','look up breeze card']

    body = str(request.values.get('Body', None)).lower()
    corrected = ' '.join(map(lambda x: spell(x), body.split()))

    # Start our TwiML response
    resp = MessagingResponse()

    if body == 'helpme':
        resp.message(constants.helpMessage)
    elif body == 'bye':
        resp.message("Goodbye")
    elif body != corrected and corrected in commandList:
    	resp.message("Did you mean: " + corrected)
    else:
        resp.message(constants.fallthroughMessage)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
