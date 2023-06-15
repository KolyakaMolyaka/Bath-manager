from .login import login_bp
from .register import register_bp
from flask import Blueprint


auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')
auth_bp.register_blueprint(login_bp)
auth_bp.register_blueprint(register_bp)