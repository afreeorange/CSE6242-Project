from flask import render_template, jsonify
from . import wsi_api_blueprint
import sqlite3
from sqlite3 import Error


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

def serialize_wsi_data(row):
    return {
        'name': row[0],
        'wsivalue' : row[1]
    }

@wsi_api_blueprint.route('/wsi/<int:year>')
def wsi_endpoint(year):
    print(year)
    conn = create_connection()
    cur = conn.cursor()

    rows = None
    if(year==1980):
        cur.execute("select country.Name, wsi.Y1980 from wsi join country on country.AreaId = wsi.AreaId")
    elif(year==1985):
        cur.execute("select country.Name, wsi.Y1985 from wsi join country on country.AreaId = wsi.AreaId")
    elif(year==1990):
        cur.execute("select country.Name, wsi.Y1990 from wsi join country on country.AreaId = wsi.AreaId")
    elif(year==1995):
        cur.execute("select country.Name, wsi.Y1995 from wsi join country on country.AreaId = wsi.AreaId")
    elif(year==2000):
        cur.execute("select country.Name, wsi.Y2000 from wsi join country on country.AreaId = wsi.AreaId")
    elif(year==2005):
        cur.execute("select country.Name, wsi.Y2005 from wsi join country on country.AreaId = wsi.AreaId")
    elif(year==2010):
        cur.execute("select country.Name, wsi.Y2010 from wsi join country on country.AreaId = wsi.AreaId")
    elif(year==2015):
        cur.execute("select country.Name, wsi.Y2015 from wsi join country on country.AreaId = wsi.AreaId")
    
    rows = cur.fetchall()

    return (jsonify(json_list = [serialize_wsi_data(i) for i in rows]))

@wsi_api_blueprint.route('/calculate/<int:indicator>')
def calculate_wsi_endpoint(indicator):
    return jsonify({
        "message": "Work in progress",
        "errors": [],
    })