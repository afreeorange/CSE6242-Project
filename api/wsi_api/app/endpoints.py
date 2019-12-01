from flask import jsonify, send_file, send_from_directory
from webargs import fields
from webargs.flaskparser import use_args

from . import wsi_api_blueprint
from .helpers import prepare_response, get_db, prepare_predict_response


# Serve the UI. Something like nginx is best
# suited for this but this is simpler.
# TODO: This needs to be a blueprint...

@wsi_api_blueprint.route('/')
def index():
    return send_file("app/ui/index.html")


@wsi_api_blueprint.route('/static/js/<path:url>')
def static_js_assets(url):
    return send_from_directory("app/ui/static/js", url)


@wsi_api_blueprint.route('/static/css/<path:url>')
def static_css_assets(url):
    return send_from_directory("app/ui/static/css", url)


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
    gdp = args["gdp_delta"]
    pop = args["population_delta"]
    isMultipleYears = False
    p_year = 0

    conn = get_db()
    cur = conn.cursor()
    rows = None

    # select country.Name, deltaforecast.* from deltaforecast JOIN country ON country.AreaId = deltaforecast.AreaId
    # gdp = -2 & population_delta = -2
    if gdp == -2 and pop== -2:
        if "year" in args.keys() and args["year"] != "":
            p_year = int(args["year"])
            if p_year == 2020:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2020""")
            elif p_year == 2025:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2025""")
            elif p_year == 2030:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2030""")
        else:
            isMultipleYears = True
            cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId""")
    elif gdp == -2 and pop== 0:
        if "year" in args.keys() and args["year"] != "":
            p_year = int(args["year"])
            if p_year == 2020:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2020""")
            elif p_year == 2025:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2025""")
            elif p_year == 2030:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2030""")
        else:
            isMultipleYears = True
            cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId""")
    elif gdp == -2 and pop== 2:
        if "year" in args.keys() and args["year"] != "":
            p_year = int(args["year"])
            if p_year == 2020:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2020""")
            elif p_year == 2025:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2025""")
            elif p_year == 2030:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2030""")
        else:
            isMultipleYears = True
            cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp_2_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId""")
    elif gdp == 0 and pop== -2:
        if "year" in args.keys() and args["year"] != "":
            p_year = int(args["year"])
            if p_year == 2020:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2020""")
            elif p_year == 2025:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2025""")
            elif p_year == 2030:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2030""")
        else:
            isMultipleYears = True
            cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId""")
    elif gdp == 0 and pop== 0:
        if "year" in args.keys() and args["year"] != "":
            p_year = int(args["year"])
            if p_year == 2020:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2020""")
            elif p_year == 2025:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2025""")
            elif p_year == 2030:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2030""")
        else:
            isMultipleYears = True
            cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId""")
    elif gdp == 0 and pop== 2:
        if "year" in args.keys() and args["year"] != "":
            p_year = int(args["year"])
            if p_year == 2020:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2020""")
            elif p_year == 2025:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2025""")
            elif p_year == 2030:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2030""")
        else:
            isMultipleYears = True
            cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp0_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId""")
    elif gdp == 2 and pop== -2:
        if "year" in args.keys() and args["year"] != "":
            p_year = int(args["year"])
            if p_year == 2020:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2020""")
            elif p_year == 2025:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2025""")
            elif p_year == 2030:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2030""")
        else:
            isMultipleYears = True
            cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop_2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId""")
    elif gdp == 2 and pop== 0:
        if "year" in args.keys() and args["year"] != "":
            p_year = int(args["year"])
            if p_year == 2020:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2020""")
            elif p_year == 2025:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2025""")
            elif p_year == 2030:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2030""")
        else:
            isMultipleYears = True
            cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop0 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId""")
    elif gdp == 2 and pop== 2:
        if "year" in args.keys() and args["year"] != "":
            p_year = int(args["year"])
            if p_year == 2020:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2020""")
            elif p_year == 2025:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2025""")
            elif p_year == 2030:
                cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId
                                WHERE deltaforecast.year = 2030""")
        else:
            isMultipleYears = True
            cur.execute("""SELECT deltaforecast.year, country.Name, deltaforecast.Gdp2_Pop2 from deltaforecast
                                JOIN country ON country.AreaId = deltaforecast.AreaId""")
    # gdp = 2 & population_delta = 2
    rows = cur.fetchall()

    data = prepare_predict_response(rows, isMultipleYears, p_year)

    # print(rows)
    return jsonify(data)
