from flask import Blueprint

detail_bp = Blueprint('detail', __name__, url_prefix='/details')

from . import views
