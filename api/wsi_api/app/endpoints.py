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
