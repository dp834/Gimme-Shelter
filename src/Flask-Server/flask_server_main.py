import os
from flask import Flask, request,render_template
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


@app.route('/')
def render_home():
    return render_template('index.html')


@app.route('/receivesms',methods=['GET', 'POST'])
def receivesms():
    body = request.values.get('Body', None)
    number = request.values.get('From', None)

    print(body)

    resp = MessagingResponse()
    resp.message(body)

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
