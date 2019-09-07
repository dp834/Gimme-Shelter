from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

account_sid = "ACc317949de3e2a848d910bd57d08253e0"
auth_token  = "fc0c7571bb1fd023ff296aa34925c3cd"

client = Client(account_sid, auth_token)

def send_sms (number, message): #sends the "message" to the "number" through twilio
    message = client.messages.create(to = str(number), from_="+12672732667", body = str(message))
    print(message.sid)


if __name__=="__main__":
    app.run(debug=True)
