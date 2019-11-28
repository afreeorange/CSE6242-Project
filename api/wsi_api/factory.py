from flask import Flask
from flask_cors import CORS


def create_app(db_connection, debug=False):
    """
    API Application Factory
    """
    app = Flask(__name__)
    app.debug = debug

    # Allow API access from anywhere <3
    CORS(app)

    # Make app aware of global connection object
    app.config["db_connection"] = db_connection

    from .app import wsi_api_blueprint
    app.register_blueprint(wsi_api_blueprint)

    return app
