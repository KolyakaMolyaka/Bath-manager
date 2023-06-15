from flask import Blueprint, render_template, request, redirect, url_for
from app.database import get_db
from app.auth import login_required, has_role
from app.auth.roles import *
from .forms import CreateBathForm, EditBathForm

edit_bath_bp = Blueprint('edit_bath', __name__)


@edit_bath_bp.route('/add_bath', methods=['GET', 'POST'])
@has_role(ADMIN_ROLE)
@login_required
def add_bath():
	form = CreateBathForm(request.form)
	if request.method == 'POST' and form.validate():
		db = get_db()
		address = form.address.data
		per_hour_rent = form.per_hour_rent.data
		min_order_time_hours = form.min_order_time_hours.data
		accessories = form.accessories.data
		working_hours_from = form.working_hours_from.data
		working_hours_to = form.working_hours_to.data
		human_capacity = form.human_capacity.data
		db.add_bath(address, per_hour_rent, min_order_time_hours, accessories,
					working_hours_from, working_hours_to, human_capacity)
		return redirect(url_for('admin.edit_bath.edit_bathes'))
	return render_template('edit_bathes/add_bath.html', form=form)


@edit_bath_bp.route('/edit_bathes', methods=['GET', 'POST'])
@has_role(ADMIN_ROLE)
@login_required
def edit_bathes():
	db = get_db()
	bathes = db.get_bathes()
	return render_template('edit_bathes/edit_bathes.html', bathes=bathes)


@edit_bath_bp.route('/edit_bath/<int:bath_id>', methods=['GET', 'POST'])
@has_role(ADMIN_ROLE)
@login_required
def edit_bath(bath_id: str):
	db = get_db()
	form = EditBathForm(request.form)
	if request.method == 'POST' and form.validate():
		address = form.address.data
		per_hour_rent = form.per_hour_rent.data
		min_order_time_hours = form.min_order_time_hours.data
		accessories = form.accessories.data
		working_hours_from = form.working_hours_from.data
		working_hours_to = form.working_hours_to.data
		human_capacity = form.human_capacity.data
		status = form.status.data
		db.update_bath_info(bath_id, address, per_hour_rent, min_order_time_hours, accessories, working_hours_from,
							working_hours_to, human_capacity, status)

		return redirect(url_for('admin.edit_bath.edit_bathes'))

	bath = db.execute_query_fetchone(f"SELECT * from bath WHERE bath_id = '{bath_id}'")
	data = {k.replace('bath_', ''): v for k, v in bath.items()}
	form.process(data=data)
	form.per_hour_rent.render_kw = {'placeholder': data['per_hour_rent']}
	return render_template('edit_bathes/edit_bath.html', form=form, bath=bath)
