from flask import render_template
from . import wsi_api_blueprint


@wsi_api_blueprint.route('/')
def index():
    return render_template('index.html')
