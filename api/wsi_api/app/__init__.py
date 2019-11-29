from flask import Blueprint

wsi_api_blueprint = Blueprint(
    'wsi_api_blueprint',
    __name__,
    static_folder='./ui',
    static_url_path='',
)

from . import endpoints
