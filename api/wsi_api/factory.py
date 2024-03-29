from flask import Flask
from flask_cors import CORS


def create_app(debug=False):
    """
    API Application Factory
    """
    app = Flask(__name__)
    app.debug = debug

    # Allow API access from anywhere <3
    CORS(app)

    from .app import wsi_api_blueprint
    app.register_blueprint(wsi_api_blueprint)

    return app
