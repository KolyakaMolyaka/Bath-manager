from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.auth.login import login_required, has_role
from app.auth.roles import *
from app.database import get_db
from .forms import CreateManagerForm, EditManagerForm

edit_managers_bp = Blueprint('edit_managers', __name__)

@edit_managers_bp.route('/edit_managers')
@has_role(ADMIN_ROLE)
@login_required
def edit_managers():
	db = get_db()
	hide_archived = request.args.get('hide_archived')
	if hide_archived in (None, ''):
		hide_archived = False
	SQL = 'SELECT * from manager'
	if hide_archived:
		SQL += f" WHERE archived = False"
	managers = db.execute_query_fetchall(SQL)

	return render_template('edit_managers/edit_managers.html', managers=managers, checked=hide_archived)


@edit_managers_bp.route('/edit_manager/<phone>', methods=['GET', 'POST'])
@has_role(ADMIN_ROLE)
@login_required
def edit_manager(phone: str):
	db = get_db()
	form = EditManagerForm(request.form)
	if request.method == 'POST' and form.validate():

		name = form.name.data
		surname = form.surname.data
		lastname = form.lastname.data
		password = form.password.data
		new_phone = form.phone.data
		salary = form.salary.data
		db.update_manager_info(phone, new_phone, name, surname, lastname, password, salary)
		g.phone = new_phone

		return redirect(url_for('admin.edit_managers.edit_managers'))

	manager = db.execute_query_fetchone(f"SELECT * from manager WHERE manager_phone = '{phone}'")
	data = {k.replace('manager_', '') :v for k,v in manager.items()}
	form.process(data=data)
	form.salary.render_kw = {'placeholder': data['salary']}
	return render_template('edit_managers/edit_manager.html', manager=manager, form=form)


@edit_managers_bp.route('add_manager', methods=['GET', 'POST'])
@has_role(ADMIN_ROLE)
@login_required
def add_manager():
	form = CreateManagerForm(request.form)
	if request.method == 'POST' and form.validate():
		phone = form.phone.data
		name = form.name.data
		surname = form.surname.data
		lastname = form.lastname.data
		password = form.password.data
		salary = form.salary.data

		db = get_db()
		db.add_manager(name, surname, lastname, password, salary, phone)
		return redirect(url_for('admin.edit_managers.edit_managers'))

	return render_template('edit_managers/add_manager.html', form=form)