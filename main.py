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

    states = {'default':0, 'breezecard':1, 'busstation':2, 'busstationaddress':3, 'trainstation':4, 'trainstationaddress':5}
    commandList = ['help','bus stations','train stations', 'route info','outages','look up breeze card']

    body = str(request.values.get('Body', None)).lower()

    key = request.values.get('From', None)

    if key not in users:
        users[key] = 0

    state = users[key]
    corrected = ' '.join(map(lambda x: spell(x), body.split()))

    # Start our TwiML response
    resp = MessagingResponse()

    if body != corrected and corrected in commandList:
        resp.message("Did you mean: " + corrected)
        users[key] = -1
        return str(resp)

    if body == "helpme":
        resp.message(constants.helpMessage)
        return str(resp)

    if body == "exit":
        users[key] = states['default']
        return str(resp)

    if state == states['default']:
        if body == "breezecard":
            users[key] = states['breezecard']
            resp.message(constants.breezecardMessage)
        elif body == "bus stations":
            users[key] = states['busstation']
            resp.message("Enter your current address in the following format so we can get the nearest bus station. " + constants.sampleAddress)
        elif body == "train stations":
            users[key] = states['trainstation']
            resp.message("Enter your current address in the following format so we can get the nearest train station. " + constants.sampleAddress)
        elif body == "outages":
            # TODO: add outage info
            resp.message("These are the current outages:\n")
        else:
            resp.message(constats.fallthroughMessage)
    elif state == states['breezecard']:
        if checkSerialNumber(body):
            resp.message("Your breezecard balance is: " + str(random.randint(0,101)))
            users[key] = states['default']
        else:
            resp.message("Invalid serial number. Try again")
    elif state == states['busstation']:
        if checkAddress(body):
            resp.message(getClosestStation(busstations))
        else:
            resp.message("Invalid address. Try again")
    elif state == states['trainstation']:
        if checkAddress(body):
            resp.message(getClosestStation(trainstations))
        else:
            resp.message("Invalid address. Try again")
    else:
        resp.message(constants.fallthroughMessage + "State: " + str(state))

    return str(resp)

# checks if valid serial number
def checkSerialNumber(serial):
    serialnums = ['01641452714095607049', '22222222222222222222', '11111111111111111111', '99999999999999999999']
    return serial in serialnums

if __name__ == "__main__":
    app.run(debug=True)
