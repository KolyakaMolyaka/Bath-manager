import datetime

from flask import Blueprint, render_template, g
from app.database import get_db

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/orders')
def orders():
	db = get_db()
	client_id = str(db.get_client_id_by_phone(g.phone)['get_client_id_by_phone'])
	shops = db.execute_query_fetchall(f"SELECT * FROM payment RIGHT JOIN orders USING (order_id) JOIN bath USING (bath_id) WHERE client_id = '{client_id}' ORDER BY payment_id DESC")
	shops = [dict(d) for d in shops]
	for i in range(len(shops)):
		rent_hours = shops[i]['order_rent_in_hours']
		booking_end_date = shops[i]['order_booking_date'] + datetime.timedelta(hours=rent_hours)
		shops[i]['booking_end_date'] = booking_end_date
		print(booking_end_date)
	return render_template('orders/orders.html', shops=shops)