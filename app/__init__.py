from flask import Flask, render_template


def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'secret'

	@app.route('/index')
	def index():
		return render_template('index.html')

	app.add_url_rule('/', view_func=index)

	from app.auth import is_logged_in
	app.before_request(is_logged_in)

	from app.auth import auth_bp
	app.register_blueprint(auth_bp)

	from app.database import init_db
	init_db(app)

	from app.admin import admin_bp
	app.register_blueprint(admin_bp)

	from app.client import client_bp
	app.register_blueprint(client_bp)

	from app.manager import manager_bp
	app.register_blueprint(manager_bp)

	return app
