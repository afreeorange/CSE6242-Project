import os

from flask import g
import sqlite3
from sqlite3 import Error as ConnectionError

sqlite3.enable_callback_tracebacks(True)


def get_db():
    """
    If DEBUG is set, take the SQLite database path from <project root>/data.
    If not, look for the bundled version in this package.
    """
    db_connection = None

    path_to_db = os.path.dirname(__file__) + "/db/wsi_data.db"
    if os.getenv('DEBUG'):
        path_to_db = os.path.dirname(__file__) + "/../../../data/wsi_data.db"

    try:
        db_connection = sqlite3.connect(path_to_db)
    except ConnectionError as e:
        raise ConnectionError("Could not connect to database:", str(e))
    else:
        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = db_connection
        return g.sqlite_db


def prepare_response(rows):
    returnDict = {}

    wsi1980Dict = {}
    wsi1985Dict = {}
    wsi1990Dict = {}
    wsi1995Dict = {}
    wsi2000Dict = {}
    wsi2005Dict = {}
    wsi2010Dict = {}
    wsi2015Dict = {}
    wsi2020Dict = {}
    wsi2025Dict = {}
    wsi2030Dict = {}

    for x in rows:
        wsi1980Dict[x[0]] = x[1]
        wsi1985Dict[x[0]] = x[2]
        wsi1990Dict[x[0]] = x[3]
        wsi1995Dict[x[0]] = x[4]
        wsi2000Dict[x[0]] = x[5]
        wsi2005Dict[x[0]] = x[6]
        wsi2010Dict[x[0]] = x[7]
        wsi2015Dict[x[0]] = x[8]
        wsi2020Dict[x[0]] = x[9]
        wsi2025Dict[x[0]] = x[10]
        wsi2030Dict[x[0]] = x[11]

    returnDict['1980'] = wsi1980Dict
    returnDict['1985'] = wsi1985Dict
    returnDict['1990'] = wsi1990Dict
    returnDict['1995'] = wsi1995Dict
    returnDict['2000'] = wsi2000Dict
    returnDict['2005'] = wsi2005Dict
    returnDict['2010'] = wsi2010Dict
    returnDict['2015'] = wsi2015Dict
    returnDict['2020'] = wsi2020Dict
    returnDict['2025'] = wsi2025Dict
    returnDict['2030'] = wsi2030Dict

    return returnDict
