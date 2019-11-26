from flask import render_template, jsonify
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

@wsi_api_blueprint.route('/wsi')
def wsi_endpoint():
    return jsonify({
        "data":{
            "1980": {
                "Armenia": 0.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 1.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },

            "1985": {
                "Armenia": 0.1,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 17.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
            "1990": {
                "Armenia": 58.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 12.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
            "1995": {
                "Armenia": 15.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 7.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
            "2000": {
                "Armenia": 98.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 4.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
            "2005": {
                "Armenia": 1.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 0.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
            "2010": {
                "Armenia": 28.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 0.06,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
            "2015": {
                "Armenia": 158.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 4.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
            "2020": {
                "Armenia": 5.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 0.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
            "2025": {
                "Armenia": 8.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 227.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
            "2030": {
                "Armenia": 8.38,
                "Afganistan": 54.7,
                "Albania": 7.879,
                "Algeria": 327.6,
                "Angola": 1.872,
                "Antigua and Barb.": 8.462,
            },
        },
        "errors": [],
    })

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
