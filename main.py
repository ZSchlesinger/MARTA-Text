from flask import Flask, request, redirect, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import constants
from autocorrect import spell
import random
import requests
import json
import nearme

app = Flask(__name__)

users = {}

@app.route('/dashboard')
def create():
    return render_template(
        'create.html',
        title='Create Page',
        name='Zach',
        year=6969,
        message="uh-huh hyuk"
        )

@app.route('/')
def hello_world():
    return redirect('/dashboard')

@app.route('/test')
def test_connect():
    try:
        import urllib2
        url="http://google.com"
        page =urllib2.urlopen(url)
        data=page.read()
        return str(data)
    except e:
        return str(e)

@app.route('/sendsms', methods=['POST'])
def send_sms():
    account_sid = "ACdbeb4628fda468dbff0e2b41ab4af47a"
    auth_token = "ca4bc7698e959f7e34948138a996c5fa"

    client = Client(account_sid, auth_token)
    print(request.form.get('data'))
    for number in users:
        message = client.messages.create(
            to=str(number),
            from_="+14703001965",
            body=request.form.get('Message from MARTA:' + 'data')
            )
    return str(len(users))

@app.route("/sms", methods =['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with simple text message."""
    global users

    commandList = ['help','stations', 'route info','outages','look up breeze card']
    states = {'default':0, 'breezecard':1, 'station':2, 'busstationaddress':3, 'trainstation':4, 'trainstationaddress':5, 'routeinfo':6}

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
        elif body == "stations":
            users[key] = states['station']
            resp.message("Please enter your location:")
        elif body == "outages":
            # TODO: add outage info
            resp.message("These are the current outages:\n")
        elif body == "route info":
            resp.message("Please enter the station:")
        else:
            resp.message(constants.fallthroughMessage)
    elif state == states['breezecard']:
        if checkSerialNumber(body):
            resp.message("Your breezecard balance is: " + str(random.randint(0,101)))
            users[key] = states['default']
        else:
            resp.message("Invalid serial number. Try again")
    elif state == states['station']:
        response = nearme.closest_stop(body)
        if response is None:
            resp.message("Invalid address or address not found. Please try again")
        else:
            resp.message(response)
            users[key] = states['default']
    elif state == states['routeinfo']:
        response = getArrivalsForStation(corrected).upper()
        if response == "":
            resp.message("Station not found")
            users[key] = states['default']
        resp.message(response)
    else:
        resp.message(constants.fallthroughMessage + "State: " + str(state))

    return str(resp)

# checks if valid serial number
def checkSerialNumber(serial):
    serialnums = ['01641452714095607049', '22222222222222222222', '11111111111111111111', '99999999999999999999']
    return serial in serialnums

def getArrivalsForStation(station):
    resp = requests.get('http://developer.itsmarta.com/RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals?apikey=7e5d3ddb-a9fd-4165-8624-b8f3f27abfc2')
    if resp.status_code != 200:
        return
    stations = resp.json()
    matches = [d for d in stations if d['STATION'] == station]
    output = ''
    for match in matches:
        output += match['LINE'] + ' to ' + match['DESTINATION'] + ' in ' + match['WAITING_TIME'] + '\n'
    return output

if __name__ == "__main__":
    app.run(debug=True)

