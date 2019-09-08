import mysql.connector

mydb = mysql.connector.connect(
    host="34.67.115.190",
    user="root",
    passwd="password123",
    database="GIMME_SHELTER"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for t in mycursor:
    print(t)
