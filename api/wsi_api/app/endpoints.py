from flask import jsonify, send_file
from webargs import fields
from webargs.flaskparser import use_args

from . import wsi_api_blueprint
from .helpers import prepare_response, get_db


# Serve the UI. Something like nginx is best
# suited for this but this is simpler.

@wsi_api_blueprint.route('/')
def index():
    return send_file("app/ui/index.html")


@wsi_api_blueprint.route('/<path:url>')
def sample_endpoint(url):
    return send_file(url)


# WSI API Endpoints

@wsi_api_blueprint.route('/wsi')
def wsi_endpoint():
    conn = get_db()
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
            wsi.Y2015,
            wsi.Y2020,
            wsi.Y2025,
            wsi.Y2030
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
        "population_delta": fields.Int(required=True)
    }
)
def predict_endpoint(args):
    """
    TODO: Finish this endpoint
    """
    return jsonify(args)
