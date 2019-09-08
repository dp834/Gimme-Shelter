import os, math
from flask import Flask, request,render_template
from twilio.twiml.messaging_response import MessagingResponse
import mysql.connector
from twilio.rest import Client
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
    
    response = parseDatabaseLocations(generateQuery(body))
    max = 12
    i = 0
    while i < len(response):
        msg = "(" + str(math.ceil((i+1)/max)) + "/" + str(math.ceil(len(response)/max)) + ")\n"
        if i+max<len(response):
            for j in range(i, i+max):
                msg+=response[j].replace("|||", "\n") + "\n"
            i+=max
        else:
            for j in range(i, i+(len(response)-i)):
                msg+=response[j].replace("|||", "\n") + "\n"
            i+=len(response)-i
        send_sms(number, msg)
    
    if not user_exists(number):
        send_sms(number, "If you would like to receive daily information about things in your area, please send the following info in a space separated format.\n\nAGE\nGENDER\n# OF DEPENDENTS\n(SNAP,FMNP,PFB)\nZIP CODE")

    return ""


def user_exists(number):
    mycursor.execute("SELECT * FROME GIMME_SHELTER.users WHERE phone_number = {number};".format(number=number))
    return len(list(mycursor)) == 1


def add_user(number, age, gender, dependents, food_type, region):
    if(None in [number, age, gender, dependents, food_type, region]):
        resp = MessagingResponse()
        resp.message("Invalid data")
        return str(resp)

    mycursor.execute("INSERT INTO GIMME_SHELTER.users (phone_number, age, gender, dependents, food_type, region)  VALUES ({phone_number}, {age}, {gender}, {dependents}, {food_type}, {region}".format(phone_number, age, gender, dependents, food_type, region))
    return ""


def send_sms(num, msg):
    client.messages.create(body=str(msg),from_="+12673100388",to=str(num))


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