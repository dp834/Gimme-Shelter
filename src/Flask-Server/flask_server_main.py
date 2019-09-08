import os
from flask import Flask, request,render_template
from twilio.twiml.messaging_response import MessagingResponse
import mysql.connector


app = Flask(__name__)

mycursor = None


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

@app.route('/update_count', methods=['GET', 'POST'])
def update_count():
    table = request.values.get("type", None)
    name = request.values.get('name', None)
    new_count = request.values.get('new_count', None)
    if(None in [table, name, new_count]):
        resp = MessagingResponse()
        resp.message("Invalid data")
        return str(resp)

    mycursor.execute("UPDATE {table} SET curr_count={new_count} WHERE GIMIE_SHELTER.{table}.name = {name};".format(table=table, new_count=new_count, name=name))
    return ""

@app.route('/get_names', methods=['GET', 'POST'])
def get_names():
    table = request.values.get("type", None)
    if(None in [table]):
        resp = MessagingResponse()
        resp.message("Invalid data")
        return str(resp)

    mycursor.execute("SELECT name FROM GIMMIE_SHELTER.{table};".format(table=table))
    return ""

@app.route('/get_tables', methods=['GET', 'POST'])
def get_tables():
    mycursor.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \'GIMME_SHELTER\';')
    return list(mycursor)

    
@app.route('/<string:page_name>/')
def render_static(page_name):
    if os.path.exists('/home/gimmeshelter/Gimme-Shelter/src/Flask-Server/templates/%s.html' % page_name):
        return render_template('%s.html' % page_name)
    else:
        return render_template('404.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0")
    mydb = mysql.connector.connect(
        host="34.67.115.190",
        user="root",
        passwd="password123",
        database="GIMMIE_SHELTER"
    )

    mycursor = mydb.cursor()

