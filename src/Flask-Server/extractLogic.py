from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
import mysql.connector

mydb = mysql.connector.connect(
        host="34.67.115.190",
        user="root",
        passwd="password123",
        database="GIMME_SHELTER"
        )
mycursor = mydb.cursor()



'''
Fuzzy Logic Dictionaries
'''

databases = {
        'Food Bank': 'Food',
        'Hungry': 'Food',
        'Homeless Shelter': 'Shelter',
        'Blanket': 'Shelter',
        'Bed': 'Shelter',
        'Sleep': 'Shelter',
        'Medical': 'Medical',
        'STD': 'Medical',
        'Sex': 'Medical',
        'Blood': 'Medical',
        'Help': 'Medical',
        'Bathroom': 'Medical'
        }

foodFilters = {
        'Food Stamps': 'SNAP',
        'Farmers Market Nutrition Program': 'FMNP',
        'FMNP': 'FMNP',
        'Supplemental Nutrition Assistance Program': 'SNAP',
        'SNAP': 'SNAP',
        'Philly Food Bucks': 'Philly Food Bucks'
        }

medicalFilters = {
        'Hospital': 'Hospital',
        'Emergency Room': 'Hospital',
        'AIDS': 'HIV',
        'HIV': 'HIV',
        'Flu shot': 'Clinic',
        'Blood': 'Clinic',
        'Check Up': 'Health Center',
        'Safe Sex': 'Condom',
        'STD': 'Condom'
        }

genderFilters = {
        'Man': 'Men',
        'Guy': 'Men',
        'Woman': 'Women',
        'Lady': 'Women',
        'Girl': 'Women',
        'Children': 'Family',
        'Family': 'Family',
        'Lesbian': 'LGBTQ',
        'Gay': 'LGBTQ',
        'Bisexual': 'LGBTQ',
        'Transexual': 'LGBTQ',
        'Queer': 'LGBTQ',
        'LGBTQ': 'LGBTQ',
        'Unknown': 'LGBTQ'
        }




# 'Medical'
# ----------
# 'Hospital'
# 'Clinic'
# 'HIV'
# 'Health Center'
# 'Condom'


# 'Food'
# -------
# 'SNAP'
# 'FMNP'
# 'Philly Food Bucks'


# 'Sheltler'
# ----------
# 'Men'
# 'Women'
# 'Family'
# 'LGBTQ'





def fuzzyLogic(text, dictionary):
    print("[DEBUG] Text received: '" + text + "'")
    closestMatch = process.extractOne(text, dictionary.keys())
    accuracy = str(closestMatch[1])
    databaseName = dictionary[closestMatch[0]]
    print("[DEBUG] Using '" + databaseName + "' with " + accuracy + "% accuracy")
    return databaseName



def generateQuery(sentence):
    dbName = fuzzyLogic(sentence, databases)
    query = 'SELECT * FROM ' + dbName + ' WHERE '

    if dbName == 'Medical':
        filters = fuzzyLogic(sentence, medicalFilters)
        query += "Type='"+filters+"';"
    if dbName == 'Food':
        filters = fuzzyLogic(sentence, foodFilters)
        query += "`" + filters + "`='Yes';"
    if dbName == 'Shelter':
       filters = fuzzyLogic(sentence, genderFilters)
       query += "gender IN ('" + filters + "');"
    return query


def parseDatabaseLocations(query):
    mycursor.execute(query)

    results = []

    for t in mycursor:
        result = ""
        if "Shelter" not in query:
            result += t[0] + "|||" + t[1] + "|||" + t[2] + " " + t[3] + "|||"
            try:
                time = [s for s in t[8:14] if s][0]
            except IndexError:
                time = "15:00-19:00"
                result += time + "\n\n"
        else:
            result += t[1] + "|||" + t[2] + "|||" + t[3] + " " + t[4] + "|||"
            try:
                time = [s for s in t[7:14] if s][0]
            except IndexError:
                time = "15:00-19:00"
                result += time + "|||"
        results.append(result)
    return results



if __name__ == "__main__":
    query = generateQuery('please gimme shelter')
    response = parseDatabaseLocations(query)
