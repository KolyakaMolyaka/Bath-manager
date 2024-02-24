import psycopg2
import json
from flask import Blueprint, render_template, request, g, url_for, redirect, flash
from app.database import get_db
from .forms import OrderBathForm
import datetime

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/catalog')
def catalog():
	# from app.utils import generate_n_managers, generate_n_users, generate_n_bathes
	# generate_n_managers(1000)
	# generate_n_users(10000)
	# generate_n_bathes(50000)

	db = get_db()
	start = datetime.datetime.now()
	bathes = db.get_bathes()
	end = datetime.datetime.now() - start
	print(end)
	return render_template('catalog/catalog.html', bathes=bathes)


@catalog_bp.route('/bath_info/<int:bath_id>', methods=['GET', 'POST'])
def bath_info(bath_id):
	db = get_db()
	form = OrderBathForm(request.form)
	if request.method == 'POST' and form.validate():
		order_rent_hours = form.order_rent_hours.data
		booking_date = form.booking_date.data
		booking_date_time = form.booking_date_time.data
		client_id = str(db.get_client_id_by_phone(g.phone)['get_client_id_by_phone'])
		booking_date = datetime.datetime.combine(booking_date, booking_date_time)

		try:
			db.add_order(client_id, bath_id, order_rent_hours, booking_date)
		except psycopg2.InternalError as e:
			flash(e.diag.message_primary)
			return redirect(url_for('client.catalog.bath_info', bath_id=bath_id))
		return redirect(url_for('client.orders.orders'))

	bath = db.execute_query_fetchone(f"SELECT * FROM bath WHERE bath_id = '{bath_id}'")

	shedule = db.execute_query_fetchall(f"SELECT * FROM bathes_shedule WHERE bath_id = '{bath_id}'")
	shedule = [dict(s) for s in shedule]
	for i in range(len(shedule)):
		rend_hours = shedule[i]['order_rent_in_hours']
		shedule[i]['booking_end_date'] = shedule[i]['order_booking_date'] + datetime.timedelta(hours=rend_hours)

	return render_template('bath_info/bath_info.html', bath=bath, bath_id=bath_id, form=form,
						   shedule=shedule)

# @catalog_bp.route('/order_bath/<int:bath_id>', methods=['POST'])
# def order_bath(bath_id):
# 	form = OrderBathForm(request.form)
# 	return 'false'

# return render_template('bath_info/order_bath.html', form=form, bath_id=bath_id)
