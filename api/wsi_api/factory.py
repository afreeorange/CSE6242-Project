from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(debug=False):
    """wsi_api application factory
    """

    app = Flask(__name__)
    app.debug = debug
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .app import wsi_api_blueprint
    app.register_blueprint(wsi_api_blueprint)

    with app.app_context():
        db.create_all()

    return app
