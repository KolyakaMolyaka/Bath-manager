from flask import Blueprint
from .catalog import catalog_bp
from .orders import orders_bp

client_bp = Blueprint('client', __name__, template_folder='templates')
client_bp.register_blueprint(catalog_bp)
client_bp.register_blueprint(orders_bp)
