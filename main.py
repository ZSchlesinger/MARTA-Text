from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import constants
from autocorrect import spell
import random

app = Flask(__name__)

users = {}

@app.route('/')
def hello_world():
    return 'Hello, Locquet!'

@app.route("/sms", methods =['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with simple text message."""
    global users

    commandList = ['help','stations near me','route info','outages','look up breeze card']

    body = str(request.values.get('Body', None)).lower()
    key = request.values.get('From', None)

    if key not in users:
        users[key] = 0

    state = users[key]
    corrected = ' '.join(map(lambda x: spell(x), body.split()))

    # Start our TwiML response
    resp = MessagingResponse()

    if body != corrected:
        resp.message("Did you mean: " + corrected)
        users[key] = -1
        return str(resp)

    if state == 0:
        if body == "breezecard":
            users[key] = 1
            resp.message(constants.breezecardMessage)
    elif state == 1:
        if checkSerialNumber(body):
            resp.message(random.randInt(0,100))
        else:
            resp.message("Invalid serial number. Try again")
    else:
        resp.message(constants.fallthroughMessage)

    # if body == 'helpme':
        # resp.message(constants.helpMessage)
    # elif body == 'bye':
    #     resp.message("Goodbye")
    # elif body != corrected and corrected in commandList:
    # 	resp.message("Did you mean: " + corrected)
    # else:
    #     resp.message(constants.fallthroughMessage)

    return str(resp)

# checks if valid serial number
def checkSerialNumber(serial):
    serialnums = ['01641452714095607049', '22222222222222222222', '11111111111111111111', '99999999999999999999']
    return serial in serialnums

if __name__ == "__main__":
    app.run(debug=True)
