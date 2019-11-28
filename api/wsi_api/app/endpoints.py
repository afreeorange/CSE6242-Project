from flask import current_app as app
from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_args

from . import wsi_api_blueprint
from .helpers import prepare_response


@wsi_api_blueprint.route('/')
def sample_endpoint():
    return jsonify({
        "message": "Hello from the WSI API <3",
    })


@wsi_api_blueprint.route('/wsi')
def wsi_endpoint():
    conn = app.config["db_connection"]
    cur = conn.cursor()
    rows = None

    cur.execute("""
        SELECT
            country.Name,
            wsi.Y1980,
            wsi.Y1985,
            wsi.Y1990,
            wsi.Y1995,
            wsi.Y2000,
            wsi.Y2005,
            wsi.Y2010,
            wsi.Y2015
        FROM wsi
        JOIN country ON country.AreaId = wsi.AreaId
    """)

    rows = cur.fetchall()

    return (jsonify(prepare_response(rows)))


@wsi_api_blueprint.route('/predict')
@use_args(
    {
        "year": fields.Str(required=False),
        "gdp_delta": fields.Int(required=True),
        "population_delta": fields.Int(required=True),
    }
)
def predict_endpoint(args):
    """
    TODO: Finish this endpoint
    """
    return jsonify(args)
