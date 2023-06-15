from flask import Blueprint, render_template, request, redirect, url_for, g
from app.database import get_db
import datetime

unpaid_orders_bp = Blueprint('unpaid_orders', __name__)


@unpaid_orders_bp.route('/unpaid_orders', methods=['GET', 'POST'])
def unpaid_orders():
	db = get_db()
	if request.method == 'POST':
		payment_type = 'Налич.' if request.form.get('payment_type') == 'cash' else 'Безнал.'
		payment_req = request.form.get('payment_req')
		preorder_id = request.form.get('order_id')

		db.create_payment(g.phone, preorder_id, payment_type, payment_req)
		return redirect(url_for('manager.unpaid_orders.unpaid_orders'))
	unpaid_orders = db.get_unpaid_orders()
	return render_template('unpaid_orders/unpaid_orders.html', unpaid_orders=unpaid_orders)


@unpaid_orders_bp.route('/make_order/<int:order_id>', methods=['GET', 'POST'])
def make_order(order_id):
	"""Оформление заказа менеджером"""
	db = get_db()
	manager_id = str(db.get_manager_id_by_phone(g.phone)['get_manager_id_by_phone'])
	SQL = f"""UPDATE orders SET manager_id = '{manager_id}' WHERE order_id = '{order_id}'"""
	db.execute_query(SQL)
	return redirect(url_for('manager.unpaid_orders.unpaid_orders'))

@unpaid_orders_bp.route('/cancel_order/<int:order_id>', methods=['GET', 'POST'])
def cancel_order(order_id):
	"""Отмена оформления заказа менеджером"""
	db = get_db()
	SQL = f"""DELETE from orders WHERE order_id = '{order_id}'"""
	db.execute_query(SQL)
	return redirect(url_for('manager.unpaid_orders.unpaid_orders'))



@unpaid_orders_bp.route('/payments', methods=['GET'])
def payments():
	db = get_db()
	SQL = f"""SELECT * FROM orders LEFT JOIN client USING (client_id) WHERE order_status = false AND manager_id IS NOT NULL"""
	possible_payments = db.execute_query_fetchall(SQL)
	# print(possible_payments)
	payments = []

	for p in possible_payments:
		end = p['order_booking_date'] + datetime.timedelta(hours=p['order_rent_in_hours'])
		print('=')
		print(end.date(), datetime.datetime.now().date())
		print(end.time(), datetime.datetime.now().time())
		print('=')
		if end.date() == datetime.datetime.now().date():
			if end.time() <= datetime.datetime.now().time():
				payments.append(p)
		elif end.date() < datetime.datetime.now().date():
			payments.append(p)

	print('!'*30)
	print(payments)

	return render_template('unpaid_orders/payments.html', possible_payments=payments)

@unpaid_orders_bp.route('/create_payment/<int:order_id>', methods=['POST'])
def create_payment(order_id):
	"""Создание оплаты на заказ"""
	db = get_db()
	if request.method == 'POST':

		payment_type = request.form.get('payment_type')
		payment_req = request.form.get('payment_req')
		if payment_type == 'cash':
			payment_type = 'Наличные'
		else:
			payment_type = 'Безналичные'

		SQL = f"""INSERT INTO payment(order_id, payment_type, payment_requisites, payment_date) VALUES
		('{order_id}', '{payment_type}', '{payment_req}', current_timestamp)"""
		db.execute_query(SQL)

	return redirect(url_for('manager.unpaid_orders.payments'))
