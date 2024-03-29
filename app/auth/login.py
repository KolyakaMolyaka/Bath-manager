import datetime
import functools

from flask import Blueprint, render_template, request, redirect, url_for, session, g, flash
from app.database import get_db
from .roles import *
from app.forms import LoginForm

login_bp = Blueprint('login', __name__)


def has_role(role: str):
	"""
	Декоратор проверки роли у пользователя
	:param role:str роль, наличие которой проверяется
	:return:
	"""
	def wrapped_func(view):
		@functools.wraps(view)
		def wrapped_view(**kwargs):
			"""
			Вызов функции, соответствующего view для пользователя в случае,
			если он имеет заданную роль.
			:param kwargs: параметры соответствующей view функции
			:return:
			"""
			if role == g.role:
				return view(**kwargs)
			return redirect(url_for('index'))
		return wrapped_view
	return wrapped_func


def login_required(view):
	"""
	Декоратор проверки авторизации пользователя
	:param view: функция обработки view
	:return:
	"""
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		"""
		Проверка наличия идентификатора пользователя в сессии.
		Если он отсутствует, то пользователь перенаправляется на страницу авторизации.
		:param kwargs: параметры соответствующей view функции
		:return:
		"""
		if g.phone is None:
			return redirect(url_for('auth.login.login'))
		return view(**kwargs)

	return wrapped_view


def logout_required(view):
	"""
	Декоратор проверки, что пользователь НЕ авторизован
	:param view: функция обработки view
	:return:
	"""
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		"""
		Проверка наличия идентификатора пользователя в сессии.
		Если он присутствует, то пользователь перенаправляется на главную страницу.
		:param kwargs:
		:return:
		"""
		if g.phone is not None:
			return redirect(url_for('index'))
		return view(**kwargs)

	return wrapped_view


def is_logged_in():
	phone = session.get('phone')
	role = session.get('role')
	if phone is None:
		g.phone = None
		g.role = None
	else:
		g.phone = phone
		g.role = role


@login_bp.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
	"""
	Авторизация пользователя
	:return: html страница для авторизации
	"""
	# создание формы для авторизации с требуемыми реквизитами
	form = LoginForm(request.form)

	# если пользователь отравил данные и они валидны (соотв. типов и ограничений)
	if request.method == 'POST' and form.validate():
		# получение реквизитов авторизации
		phone = form.phone.data
		password = form.password.data

		# получение доступа к БД
		db = get_db()

		# проверка пароля
		right_password = str(db.get_client_password(phone)['get_client_password'])
		if password != right_password:
			# если парль неправильный, то возвращаем html страницу с авторизацией
			# и информационным сообщением
			flash('Неправильный пароль')
			return redirect(url_for('auth.login.login'))
		else:
			# сохраняем в сессии авторизованного пользователя
			# и перенаправляем его на страницу с каталогом
			session['phone'] = phone
			session['role'] = CLIENT_ROLE
			return redirect(url_for('client.catalog.catalog'))

	# возвращаем пользователю html страницу для авторизации
	return render_template('user/user_login.html', form=form)


@login_bp.route('/manager/login', methods=['GET', 'POST'])
@logout_required
def login_manager():
	if request.method == 'POST':
		phone = request.form['phone']
		password = request.form['password']

		db = get_db()
		right_password = str(db.get_manager_password(phone)['get_manager_password'])

		if password != right_password:
			return redirect(url_for('auth.login.login_manager'))
		else:
			session['phone'] = phone
			session['role'] = MANAGER_ROLE
			return redirect(url_for('index'))

	return render_template('manager/manager_login.html')


@login_bp.route('/admin/login', methods=['GET', 'POST'])
@logout_required
def login_admin():
	if request.method == 'POST':

		phone = request.form['phone']
		print(phone)
		password = request.form['password']

		db = get_db()
		right_password = str(db.get_admin_password(phone)['get_admin_password'])
		print(password, right_password, type(password), type(right_password))

		if password != right_password:
			return redirect(url_for('auth.login.login_admin'))
		else:
			session['phone'] = phone
			session['role'] = ADMIN_ROLE
			return redirect(url_for('admin.reports.revenue'))

	return render_template('admin/admin_login.html')


@login_bp.route('/logout')
@login_required
def logout():
	session.pop('phone', None)
	role = session.pop('role', None)
	if role is None or role == CLIENT_ROLE:
		return redirect(url_for('auth.login.login'))
	elif role == MANAGER_ROLE:
		return redirect(url_for('auth.login.login_manager'))

	return redirect(url_for('auth.login.login_admin'))
