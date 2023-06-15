import psycopg2.errors
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db
from .login import logout_required

register_bp = Blueprint('register', __name__)
from app.forms import RegistrationForm


@register_bp.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		surname = form.surname.data
		lastname = form.lastname.data
		password = form.password.data
		phone = form.phone.data
		try:
			int(phone)
		except:
			flash('Некорректный номер телефона')
			return redirect(url_for('auth.register.register'))

		db = get_db()

		try:
			db.add_client(phone, password, name, surname, lastname)
		except:
			if len(phone) != 11:
				flash('В номере телефона должно присутствовать 11 цифр, пример: "79205392642"')
			else:
				flash('Неизвестная ошибка')

			return redirect(url_for('auth.register.register'))


		flash('Теперь пройдите авторизацию')
		return redirect(url_for('auth.login.login'))
	return render_template('user/user_register.html', form=form)
