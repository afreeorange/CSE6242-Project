import os
import sqlite3
import sys
from datetime import datetime
from sqlite3 import Error as ConnectionError

from .factory import create_app

__title__ = 'wsi_api'
__version__ = '0.0.1',
__author__ = 'Team 102'
__author_email__ = 'nikhil.anand@gatech.edu'
__license__ = 'MIT'
__copyright__ = '(c) {}'.format(datetime.now().year)
__url__ = 'https://github.gatech.edu/sprice31/cse6242fall2019team102'
__description__ = """
Upstream API for an app that shows Global  Water Stress Index
"""

# Initialize a DB connection
sqlite3.enable_callback_tracebacks(True)
db_connection = None

try:
    db_connection = sqlite3.connect("wsi_data.db")
except ConnectionError as e:
    print("Could not connect to database:", str(e))
    sys.exit(1)

app = create_app(db_connection, debug=os.getenv('DEBUG', False))
