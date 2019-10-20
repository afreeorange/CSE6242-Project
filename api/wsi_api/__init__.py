from datetime import datetime
import os

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

app = create_app(debug=os.getenv('DEBUG', False))
