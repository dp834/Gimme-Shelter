import os
from flask import Flask, request,render_template
from twilio.twiml.messaging_response import MessagingResponse
import mysql.connector
from twilio.rest import Client
from textwrap import wrap
from extractLogic import *

client = Client("AC8adb168951a9e1c7845994be9e1ceabd", "57166fb17768f7561e426bae9a446666")


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

    response = parseDatabaseLocations(generateQuery(body))
    print(len(response))
    for i in range(0, len(response), 5):
        sendMsg = "(" + str(int(i/5)+1) + "/" + str(int(len(response)/5)) + ")"
        if i < len(response):
            sendMsg += response[i].replace("|||", "\n") + "\n"
        if i < len(response)-1:
            sendMsg += response[i+1].replace("|||", "\n") + "\n"
        if i < len(response)-2:
            sendMsg += response[i+2].replace("|||", "\n") + "\n"
        if i < len(response)-3:
            sendMsg += response[i+3].replace("|||", "\n") + "\n"
        if i < len(response)-4:
            sendMsg += response[i+4].replace("|||", "\n") + "\n"
        send_sms(number, sendMsg)
    resp = MessagingResponse()
    resp.message(body)

    return str(resp)


def send_sms(num, msg):
    client.messages.create(body=str(msg),from_="+12673100388",to=str(num))

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    number = request.values.get("number", None)
    age = int(request.values.get("age", None))
    gender = request.values.get("gender", None)
    dependents = requests.values.get("dependents", None)
    food_type = requests.values.get("food_type", None)
    region = requests.values.get("region", None)

    if(None in [number, age, gender, dependents, food_type, region]):
        resp = MessagingResponse()
        resp.message("Invalid data")
        return str(resp)


    mycursor.execute("INSERT INTO GIMME_SHELTER.users (phone_number, age, gender, dependents, food_type, region)  VALUES ({phone_number}, {age}, {gender}, {dependents}, {food_type}, {region}".format(phone_number, age, gender, dependents, food_type, region))

    return ""

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
    for c in mycursor:
        print(c)
    return ""

    
if __name__ == "__main__":
    mydb = mysql.connector.connect(
        host="34.67.115.190",
        user="root",
        passwd="password123",
        database="GIMME_SHELTER"
    )
    mycursor = mydb.cursor()
    app.run(host="0.0.0.0")
