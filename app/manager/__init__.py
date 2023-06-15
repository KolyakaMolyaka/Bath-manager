from flask import Blueprint
from .unpaid_orders import unpaid_orders_bp

manager_bp = Blueprint('manager', __name__, url_prefix='/manager', template_folder='templates')
manager_bp.register_blueprint(unpaid_orders_bp)
