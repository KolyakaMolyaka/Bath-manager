from flask import Blueprint
from .managers import edit_managers_bp
from .bathes import edit_bath_bp
from .reports import reports_bp

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')
admin_bp.register_blueprint(edit_managers_bp)
admin_bp.register_blueprint(edit_bath_bp)
admin_bp.register_blueprint(reports_bp)

