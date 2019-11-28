import os
import sqlite3
import sys
from sqlite3 import Error as ConnectionError

from .factory import create_app

sqlite3.enable_callback_tracebacks(True)
db_connection = None

try:
    db_connection = sqlite3.connect("wsi_data.db")
except ConnectionError as e:
    print("Could not connect to database:", str(e))
    sys.exit(1)

app = create_app(db_connection, debug=os.getenv('DEBUG', False))
