import datetime

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .database_config import PostgreSQLConfig
from flask import g
from psycopg2.extras import RealDictCursor


class PostgreSQL:
	def __init__(self):
		self.conn = psycopg2.connect(
			dbname=PostgreSQLConfig.DB_NAME,
			user=PostgreSQLConfig.DB_USERNAME,
			password=PostgreSQLConfig.DB_PASSWORD,
			host=PostgreSQLConfig.DB_HOST,
			port=PostgreSQLConfig.DB_PORT
		)
		self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

	def add_order(self, client_id, bath_id, order_rent_hours, booking_date):
		SQL = f"""
		call add_order('{client_id}', '{bath_id}', '{order_rent_hours}', '{booking_date}'::timestamp)
		"""
		self.execute_query(SQL)

	def get_manager_id_by_phone(self, phone):
		return self.execute_query_fetchone(f"SELECT get_manager_id_by_phone('{phone}')")

	def get_client_id_by_phone(self, phone):
		return self.execute_query_fetchone(f"SELECT get_client_id_by_phone('{phone}')")

	def update_bath_info(self, bath_id, address, per_hour_rent, min_order_time_hours, accessories, working_hours_from,
						 working_hours_to, human_capacity, status):
		SQL = f"""
		call update_bath_info('{bath_id}', '{address}', '{per_hour_rent}'::money, '{min_order_time_hours}',
		 '{accessories}', '{working_hours_from}'::time, '{working_hours_to}'::time, '{human_capacity}', '{status}')
		"""
		self.execute_query(SQL)

	def get_bathes(self):
		SQL = f"""
		SELECT * 
		FROM bath
		ORDER by bath_status DESC
		"""
		return self.execute_query_fetchall(SQL)

	def add_bath(self, address, per_hour_rent, min_order_time_hours, accessories, working_hours_from, working_hours_to,
				 human_capacity):
		SQL = f"""
		call add_bath('{address}', '{per_hour_rent}'::money, '{min_order_time_hours}',
		'{accessories}', '{working_hours_from}'::time, '{working_hours_to}'::time, '{human_capacity}')
		"""

		self.execute_query(SQL)

	def add_manager(self, name, surname, lastname, password, salary, phone):
		self.execute_query(
			f"call add_manager('{name}', '{surname}', '{lastname}', '{password}', '{salary}'::money, '{phone}')")

	def create_payment(self, phone, preorder_id, payment_type, payment_req):
		self.execute_query(f"call add_payment('{phone}', '{preorder_id}', '{payment_type}', '{payment_req}')")

	def get_unpaid_orders(self):
		SQL = f"""
		SELECT *
		FROM orders
		JOIN client USING(client_id)
		WHERE order_status = false
		AND manager_id IS NULL
		"""
		return self.execute_query_fetchall(SQL)


	def get_top_bath_report(self):
		SQL = f"""
		SELECT bath_address, SUM(order_rent_in_hours) as total_hours, SUM(order_cost) as total_revenue FROM report
		JOIN bath USING (bath_id)
		WHERE bath_status = true
		GROUP BY bath_address	
		ORDER BY total_revenue DESC, total_hours DESC
		"""
		return self.execute_query_fetchall(SQL)

	def get_revenue_report(self, report_from_date=None, report_to_date=None):
		SQL = f"""
		SELECT payment_date, order_cost, payment_type,
		payment_requisites, client_phone 
		FROM report 
		JOIN client USING (client_id)
		ORDER BY payment_date DESC	
		"""

		if report_from_date is not None and report_to_date is not None:
			res = self.execute_query_fetchall(SQL)
			res = [dict(r) for r in res]
			res = filter(lambda d: datetime.datetime.date(d['payment_date']) >= datetime.datetime.strptime(report_from_date, '%Y-%m-%d').date()
								   and datetime.datetime.date(d['payment_date']) <= datetime.datetime.strptime(report_to_date, '%Y-%m-%d').date(), res)


			return list(res)
		res = self.execute_query_fetchall(SQL)
		res = [dict(r) for r in res]

		return res

	def add_extraoption(self, name, amount, buy_price, sell_price):
		self.execute_query(f"call add_extraoption("
						   f"'{name}', '{amount}',"
						   f"'{sell_price}', '{buy_price}')")

	def add_car(self, vin, sell_price, buy_price, body_type, conf_name, engine_type, engine_size, engine_power,
				fuel_cons, acceleration, tr_type, gears_count, color, brand, model):
		self.execute_query(f"call add_car("
						   f"'{vin}', '{sell_price}', '{buy_price}',"
						   f"'{body_type}', '{conf_name}', '{engine_type}',"
						   f"'{engine_size}', '{engine_power}', '{fuel_cons}',"
						   f"'{acceleration}', '{tr_type}', '{gears_count}',"
						   f"'{brand}', '{model}', '{color}')")

	def update_manager_info(self, phone, new_phone, name, surname, lastname, password, salary):

		self.execute_query(f"call update_manager_info("
						   f"'{phone}', '{new_phone}',"
						   f"'{name}', '{surname}',"
						   f"'{lastname}', '{password}',"
						   f"'{salary}')")

	def close_conn(self):
		self.conn.close()

	def get_admin_password(self, phone):
		SQL = f"SELECT get_admin_password('{phone}')"
		return self.execute_query_fetchone(SQL)

	# return self.execute_query_fetchone(f"select get_admin_password('{phone}')")

	def get_manager_password(self, phone):
		return self.execute_query_fetchone(f"select get_manager_password('{phone}')")

	def get_client_password(self, phone):
		return self.execute_query_fetchone(f"select get_client_password('{phone}')")

	def add_client(self, phone, password, name, surname, lastname=None):
		if lastname is None:
			self.execute_query(f"call add_client('{phone}', '{password}', '{name}', '{surname}')")
		else:
			self.execute_query(f"call add_client('{phone}', '{password}', '{name}', '{surname}', '{lastname}')")

	def set_monetary_policy(self, cur):
		cur.execute("SET lc_monetary='ru_RU.UTF8'")

	def execute_query(self, sql: str, params=None):
		with self.conn.cursor() as cur:
			cur.execute(sql)

	def execute_query_fetchone(self, sql: str):
		with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
			self.set_monetary_policy(cur)
			cur.execute(sql)
			return cur.fetchone()

	def execute_query_fetchall(self, sql: str):
		with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
			self.set_monetary_policy(cur)
			cur.execute(sql)
			return cur.fetchall()


def get_db():
	db = g.get('db', None)
	if db is None:
		g.db = PostgreSQL()

	return g.db


def close_db(e=None):
	db = g.get('db', None)
	if db is not None:
		db = g.pop('db', None)
		db.close_conn()


def init_db(app):
	app.teardown_appcontext(close_db)
