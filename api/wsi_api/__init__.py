import os
from .factory import create_app

app = create_app(debug=os.getenv('DEBUG', False))
