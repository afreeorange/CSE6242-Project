from flask import Blueprint

wsi_api_blueprint = Blueprint(
    'wsi_api_blueprint',
    __name__,
    template_folder='./templates',
    static_folder='./static',
    static_url_path='/app/static',
)

from . import endpoints
