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


@app.route('/<string:page_name>/')
def render_static(page_name):
    if os.path.exists('/home/gimmeshelter/Gimme-Shelter/src/Flask-Server/templates/%s.html' % page_name):
        return render_template('%s.html' % page_name)
    else:
        return render_template('404.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0")
