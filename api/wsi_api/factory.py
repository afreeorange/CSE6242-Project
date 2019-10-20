from flask import Flask


def create_app(debug=False):
    """wsi_api application factory
    """

    app = Flask(__name__)
    app.debug = debug

    from .app import wsi_api_blueprint
    app.register_blueprint(wsi_api_blueprint)

    return app
