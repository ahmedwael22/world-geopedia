from typing import Counter
import MySQLdb
from flask import Flask, json, jsonify, request
from flask_cors import cross_origin
from datetime import datetime
import phonenumbers

#TODO zabat python interpreter

app = Flask(__name__)
db = MySQLdb.connect("www.db4free.net", "your-username-here", "your-password-here", "your-database-name-here")



# #General

# @app.route('/')
# @cross_origin()
# def index():
#     return ("<h1>Hello World! </h1> <h2>Get It? Cause World Geopedia.</h2>")



#SELECT


@app.route('/api/viewCountryVisits', methods=["POST"])
@cross_origin()
def viewCountryVisits():
    cn = request.json["countryname"]
    
    cursor = db.cursor()
    query ="SELECT *\
            FROM visit\
            WHERE COUNTRYNAME = '" + cn +"'"
    cursor.execute(query)
    qres = cursor.fetchall()

    visits = []
    for row in qres:
        visit={}
        visit["countryname"] = row[0]
        visit["user"] = row[1]
        visit["arrival"] = row[2].strftime("%Y-%m-%d")
        visit["departure"] = row[3].strftime("%Y-%m-%d")
        visit["rating"] = row[4]
        visit["review"] = row[5]
        visits.append(visit)

    return jsonify (data=visits), 200


@app.route('/api/viewCountryReviews', methods=["POST"])
@cross_origin()
def viewCountryReviews():
    cn = request.json["countryname"]
    
    cursor = db.cursor()
    query ="SELECT TEXTREVIEW\
            FROM visit\
            WHERE COUNTRYNAME = '" + cn +"'"
    cursor.execute(query)
    qres = cursor.fetchall()

    reviews = []
    for row in qres:
        reviews.append(row[0])

    return jsonify (data=reviews), 200


@app.route('/api/getCountriesByLegislation', methods=["POST"])
@cross_origin()
def getCountriesByLegislation():
    leg = request.json["legislation"]
    
    cursor = db.cursor()
    query ="SELECT NAME\
            FROM country\
            WHERE LEGISLATURE LIKE '%" + leg + "%'"
    cursor.execute(query)
    qres = cursor.fetchall()

    countries = []
    for row in qres:
        countries.append(row[0])

    return jsonify (data = countries), 200


@app.route('/api/getCountriesByDrivingSide', methods=["POST"])
@cross_origin()
def getCountriesByDrivingSide():
    side = request.json["side"]
    
    cursor = db.cursor()
    query ="SELECT NAME\
            FROM country\
            WHERE DRIVINGSIDE ='" + side + "'"
    cursor.execute(query)
    qres = cursor.fetchall()

    countries = []
    for row in qres:
        countries.append(row[0])

    return jsonify (data = countries), 200


@app.route('/api/getCountry', methods=["POST"])
@cross_origin()
def getCountry():
    cn = request.json["countryname"]
    
    cursor = db.cursor()
    query ="SELECT C.*, GROUP_CONCAT(DISTINCT L.language SEPARATOR ','), GROUP_CONCAT(DISTINCT T.Timezone SEPARATOR ',')\
            FROM country C\
            LEFT OUTER JOIN officiallanguages L\
            ON C.name = L.name\
            LEFT OUTER JOIN timezones T\
            ON C.name = T.name\
            WHERE C.NAME ='" + cn + "'\
            GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17"
    cursor.execute(query)
    qres = cursor.fetchone()

    if qres is None:
        return jsonify(), 404

    languages = []
    languagesstring = qres[17]
    if languagesstring is not None:
        for lang in languagesstring.split(','):
            languages.append(lang.strip())

    timezones = []
    tzstring = qres[18]
    if tzstring is not None:
        for tz in tzstring.split(','):
            timezones.append(float(tz))

    info = {}
    
    info["countryname"] = qres[0]
    info["continent"] = qres[1]
    info["population"] = qres[2]
    info["area"] = qres[3]
    info["waterpercentage"] = qres[4]
    info["gdpnominal"] = qres[5]
    info["gdppp"] = qres[6]
    info["legislature"] = qres[7]
    info["headofstate"] = qres[8]
    info["drivingside"] = qres[9]
    info["callingcode"] = qres[10]
    info["currency"] = qres[11]
    info["hdi"] = qres[12]
    info["gini"] = qres[13]
    info["dateassumedoffice"] = qres[14].strftime("%Y-%m-%d")
    info["covidcases"] = qres[15]
    info["covidvaccinations"] = qres[16]
    info["languages"] = languages
    info["timezones"] = timezones

    return jsonify (data = info), 200


@app.route('/api/getCity', methods=["POST"])
@cross_origin()
def getCity():
    cityname = request.json["cityname"]

    cursor = db.cursor()
    query ="SELECT *\
            FROM capitalcity\
            WHERE NAME ='" + cityname + "'"
    cursor.execute(query)
    qres = cursor.fetchone()

    if qres is None:
        return jsonify(), 404

    info = {}
    
    info["longitude"] = qres[0]
    info["latitude"] = qres[1]
    info["cityname"] = qres[2]
    info["countryname"] = qres[3]
    info["population"] = qres[4]
    info["area"] = qres[5]
    info["governor"] = qres[6]

    return jsonify (data = info), 200


@app.route('/api/getCityFromCountry', methods=["POST"])
@cross_origin()
def getCityFromCountry():
    cn = request.json["countryname"]

    cursor = db.cursor()
    query ="SELECT *\
            FROM capitalcity\
            WHERE COUNTRYNAME ='" + cn + "'"
    cursor.execute(query)
    qres = cursor.fetchone()

    if qres is None:
        return jsonify(), 404

    info = {}
    
    info["longitude"] = qres[0]
    info["latitude"] = qres[1]
    info["cityname"] = qres[2]
    info["countryname"] = qres[3]
    info["population"] = qres[4]
    info["area"] = qres[5]
    info["governor"] = qres[6]

    return jsonify (data = info), 200


@app.route('/api/getCountryNameFromCity', methods=["POST"])
@cross_origin()
def getCountryNameFromCity():
    cityname = request.json["cityname"]

    cursor = db.cursor()
    query ="SELECT COUNTRYNAME\
            FROM capitalcity\
            WHERE NAME ='" + cityname + "'"
    cursor.execute(query)
    qres = cursor.fetchone()

    if qres is None:
        return jsonify(), 404
    
    contryname = qres[0]

    return jsonify (data = contryname), 200


@app.route('/api/getTopTen', methods=["POST"])
@cross_origin()
def getTopTen():
    category = request.json["category"]

    cursor = db.cursor()
    
    if category == "gdp_n_percapita":
        query ="SELECT NAME, GDPNOMINAL/POPULATION AS GDP_NOMINAL_PER_CAPITA\
                FROM country\
                ORDER BY 2 DESC\
                LIMIT 10"
    elif category == "gdp_pp_percapita":
        query ="SELECT NAME, GDPPP/POPULATION AS GDP_PP_PER_CAPITA\
                FROM country\
                ORDER BY 2 DESC\
                LIMIT 10"
    elif category == "density":
        query ="SELECT NAME, POPULATION/AREA AS DENSITY\
                FROM country\
                ORDER BY 2 DESC\
                LIMIT 10"
    else:
        query ="SELECT NAME, " + category \
            + " FROM country\
                ORDER BY " + category + " DESC\
                LIMIT 10"

    cursor.execute(query)
    qres = cursor.fetchall()
    countries = []
    for row in qres:
        temp = {}
        temp["countryname"] = row[0]
        if "percapita" in category:
            temp[category] = row[1] * 1000000
        else:
            temp[category] = row[1]
        countries.append(temp)


    return jsonify (data = countries), 200


@app.route('/api/getTopTenInContinent', methods=["POST"])
@cross_origin()
def getTopTenInContinent():
    category = request.json["category"]
    continent = request.json["continent"]
    
    cursor = db.cursor()
    
    if category == "gdp_n_percapita":
        query ="SELECT NAME, GDPNOMINAL/POPULATION AS GDP_NOMINAL_PER_CAPITA\
                FROM country\
                WHERE continent = '" + continent + "'\
                ORDER BY 2 DESC\
                LIMIT 10"
    elif category == "gdp_pp_percapita":
        query ="SELECT NAME, GDPPP/POPULATION AS GDP_PP_PER_CAPITA\
                FROM country\
                WHERE continent = '" + continent + "'\
                ORDER BY 2 DESC\
                LIMIT 10"
    elif category == "density":
        query ="SELECT NAME, POPULATION/AREA AS GDP_PP_PER_CAPITA\
                FROM country\
                WHERE continent = '" + continent + "'\
                ORDER BY 2 DESC\
                LIMIT 10"
    else:
        query ="SELECT NAME, " + category \
            + " FROM country\
                WHERE continent = '" + continent + "'\
                ORDER BY " + category + " DESC\
                LIMIT 10"

    cursor.execute(query)
    qres = cursor.fetchall()
    countries = []
    for row in qres:
        temp = {}
        temp["countryname"] = row[0]
        if "gdp" in category:
            temp[category] = row[1] * 1000000
        else:
            temp[category] = row[1]
        countries.append(temp)


    return jsonify (data = countries), 200


@app.route('/api/getHeadOfState', methods=["POST"])
@cross_origin()
def getHeadOfState():
    headofstate = request.json["headofstate"]

    cursor = db.cursor()
    query ="SELECT H.name, H.politicalparty, H.dob, C.name, C.dateassumedoffice\
            FROM headofstate H\
            INNER JOIN country C\
            ON C.HEADOFSTATENAME = H.name\
            WHERE H.NAME ='" + headofstate + "'"
    cursor.execute(query)
    qres = cursor.fetchall()

    info = {}
    info["name"] = qres[0][0]
    info["politicalparty"] = qres[0][1]
    info["dob"] = qres[0][2].strftime("%Y-%m-%d")
    info["countries"]=[]
    for row in qres:
        temp = {}
        temp ["countryname"] = row[3]
        temp["dateassumedoffice"] = row[4].strftime("%Y-%m-%d")
        info["countries"].append(temp)

    return jsonify (data = info), 200


@app.route('/api/getHeadOfStateFromCountry', methods=["POST"])
@cross_origin()
def getHeadOfStateFromCountry():
    cn = request.json["countryname"]

    cursor = db.cursor()
    query ="SELECT H.name, H.politicalparty, H.dob\
            FROM headofstate H\
            INNER JOIN country C\
            ON C.HEADOFSTATENAME = H.name\
            WHERE C.NAME ='" + cn + "'"
    cursor.execute(query)
    qres = cursor.fetchone()

    if qres is None:
        return jsonify(), 404

    info = {}
    
    info["name"] = qres[0]
    info["politicalparty"] = qres[1]
    info["dob"] = qres[2].strftime("%Y-%m-%d")

    return jsonify (data = info), 200


@app.route('/api/covidGlobal', methods=["POST"])
@cross_origin()
def covidGlobal():
    category = request.json["category"]

    cursor = db.cursor()
    query = "SELECT NAME, " + category + "\
            FROM country\
            WHERE " + category + " IS NOT NULL\
            ORDER BY " + category + " DESC\
            LIMIT 5"
    cursor.execute(query)
    qres = cursor.fetchall()

    top = []
    for row in qres:
        temp = {}
        temp["countryname"] = row[0]
        temp[category] = row[1]
        top.append(temp)

    cursor = db.cursor()
    query= "SELECT NAME, " + category + "\
            FROM country\
            WHERE " + category + " IS NOT NULL\
            ORDER BY " + category + " ASC\
            LIMIT 5"
    cursor.execute(query)
    qres = cursor.fetchall()
    
    bottom = []
    for row in qres:
        temp = {}
        temp["countryname"] = row[0]
        temp[category] = row[1]
        bottom.append(temp)


    return jsonify (top=top, bottom=bottom), 200


@app.route('/api/covidContinent', methods=["POST"])
@cross_origin()
def covidContinent():
    category = request.json["category"]
    continent = request.json["continent"]

    cursor = db.cursor()
    query = "SELECT NAME, " + category + "\
            FROM country\
            WHERE " + category + " IS NOT NULL\
            AND continent = '" + continent + "'\
            ORDER BY " + category + " DESC\
            LIMIT 5"
    cursor.execute(query)
    qres = cursor.fetchall()

    top = []
    for row in qres:
        temp = {}
        temp["countryname"] = row[0]
        temp[category] = row[1]
        top.append(temp)

    cursor = db.cursor()
    query= "SELECT NAME, " + category + "\
            FROM country\
            WHERE " + category + " IS NOT NULL\
            AND continent = '" + continent + "'\
            ORDER BY " + category + " ASC\
            LIMIT 5"
    cursor.execute(query)
    qres = cursor.fetchall()
    
    bottom = []
    for row in qres:
        temp = {}
        temp["countryname"] = row[0]
        temp[category] = row[1]
        bottom.append(temp)


    return jsonify (top=top, bottom=bottom), 200



#INSERT

@app.route('/api/addUser', methods=["POST"])
@cross_origin()
def addUser():
    username = request.json["username"]
    email = request.json["email"]
    gender = request.json["gender"]
    dob = request.json["dob"]
    print("I am here")
    try:
        cursor = db.cursor()
        query ="INSERT INTO user (username, email, dob, gender)\
            VALUES ('" + username + "', '" + email + "', '" + dob + "', '" + gender + "')"
        cursor.execute(query)
        db.commit()
    except Exception as e:
        return jsonify(error=repr(e)), 409

    return jsonify(), 200


@app.route('/api/addVisit', methods=["POST"])
@cross_origin()
def addVisit():
    cn = request.json["countryname"]
    username = request.json["username"]
    arrivaldate = request.json["arrivaldate"]
    departuredate = request.json["departuredate"]
    rating = request.json["rating"]
    review = request.json["review"]
    
    try:
        cursor = db.cursor()
        query ="INSERT INTO visit (countryname, username, arrivaldate, departuredate, rating, textreview)\
                VALUES ('" + cn +"', '" + username + "', '" + arrivaldate + "', '" + departuredate + "', " + str(rating) +", '" + review + "')"
        cursor.execute(query)
        db.commit()
    except Exception as e:
        errorstring = repr(e)
        if "IntegrityError(1062" in errorstring: #duplicate entry
            return jsonify(error=repr(e)), 409
        else:
            return jsonify(error=repr(e)), 404

    return jsonify (), 200




#Others
@app.route('/api/reconnect')
@cross_origin()
def reconnect():
    try:
        db = MySQLdb.connect("www.db4free.net", "your-username-here", "your-password-here", "your-database-name-here")
        return jsonify(), 200
    except:
        return 500



@app.route('/api/test', methods=["POST"])
@cross_origin()
def test():

    cursor = db.cursor()
    query ="SELECT * FROM visit"
    cursor.execute(query)
    qres = cursor.fetchall()

    return jsonify (qres=qres)


@app.route('/api/phonenumber', methods=["POST"])
@cross_origin()
def phonenumber():
    ph = phonenumbers.parse(request.json["ph"], None)

    cc = "+" + str(ph.country_code)

    cursor = db.cursor()
    query ="SELECT name FROM country\
            WHERE callingcode = '" + cc + "'"
    cursor.execute(query)
    qres = cursor.fetchone()

    return jsonify(data=qres[0])