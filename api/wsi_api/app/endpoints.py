import sqlite3
from sqlite3 import Error

from flask import jsonify, render_template

from . import wsi_api_blueprint


@wsi_api_blueprint.route('/')
def index():
    return render_template('index.html')


@wsi_api_blueprint.route('/data')
def sample_endpoint():
    return jsonify({
        "message": "Hello from the API!",
        "errors": [],
    })


def create_connection():
    sqlite3.enable_callback_tracebacks(True)
    conn = None
    try:
        conn = sqlite3.connect("./project.db")
    except Error as e:
        print(e)

    return conn


def serialize_wsi_data(rows):
    returnDict = {}
    wsi1980Dict = {}
    wsi1985Dict = {}
    wsi1990Dict = {}
    wsi1995Dict = {}
    wsi2000Dict = {}
    wsi2005Dict = {}
    wsi2010Dict = {}
    wsi2015Dict = {}
    for x in rows:
        wsi1980Dict[x[0]] = x[1]
        wsi1985Dict[x[0]] = x[2]
        wsi1990Dict[x[0]] = x[3]
        wsi1995Dict[x[0]] = x[4]
        wsi2000Dict[x[0]] = x[5]
        wsi2005Dict[x[0]] = x[6]
        wsi2010Dict[x[0]] = x[7]
        wsi2015Dict[x[0]] = x[8]

    returnDict['1980'] = wsi1980Dict
    returnDict['1985'] = wsi1985Dict
    returnDict['1990'] = wsi1990Dict
    returnDict['1995'] = wsi1995Dict
    returnDict['2000'] = wsi2000Dict
    returnDict['2005'] = wsi2005Dict
    returnDict['2010'] = wsi2010Dict
    returnDict['2015'] = wsi2015Dict

    return returnDict


@wsi_api_blueprint.route('/wsi')
def wsi_endpoint():
    #print(year)
    conn = create_connection()
    cur = conn.cursor()

    rows = None
    cur.execute("select country.Name, wsi.Y1980, wsi.Y1985, wsi.Y1990, wsi.Y1995, wsi.Y2000, wsi.Y2005, wsi.Y2010, wsi.Y2015 from wsi join country on country.AreaId = wsi.AreaId")

    rows = cur.fetchall()

    return (jsonify(serialize_wsi_data(rows)))


@wsi_api_blueprint.route('/predict')
def predict_endpoint():
    return jsonify({
        "data":{
            "2020": {
                "Armenia": 0.01,
                "Afganistan": 0.01,
                "Albania": 0.01,
                "Algeria": 100,
                "Angola": 0.01,
                "Antigua and Barb.": 0.01,
            },
            "2025": {
                "Armenia": 1,
                "Afganistan": 1,
                "Albania": 1,
                "Algeria": 5,
                "Angola": 1,
                "Antigua and Barb.": 1,
            },
        },
        "errors": [],
    })
