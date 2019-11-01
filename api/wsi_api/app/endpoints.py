from flask import render_template, jsonify
from . import wsi_api_blueprint
from .models import db, Parameter


@wsi_api_blueprint.route('/')
def index():
    return render_template('index.html')


@wsi_api_blueprint.route('/data')
def sample_endpoint():
    return jsonify({
        "message": "Hello from the API!",
        "errors": [],
    })

@wsi_api_blueprint.route('/wsi/<int:year>')
def wsi_endpoint(year):
    print(year)
    data = Parameter.query.filter(Parameter.VariableName == 'SDG 6.4.2. Water Stress', Parameter.Year == year).all()
    
    print(data)
    return jsonify(json_list=[i.serialize for i in data])
