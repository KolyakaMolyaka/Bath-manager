import datetime
import os
import xlsxwriter
from flask import Blueprint, render_template, request, redirect, url_for, make_response, send_from_directory, send_file
from app.database import get_db
from app.auth.login import login_required, has_role
from app.auth.roles import *
import json

reports_bp = Blueprint('reports', __name__, url_prefix='reports')


@reports_bp.route('/revenue')
@has_role(ADMIN_ROLE)
@login_required
def revenue():
	db = get_db()
	report_from_date = request.args.get('report_from_date', None)
	report_to_date = request.args.get('report_to_date', None)

	report = db.get_revenue_report(report_from_date, report_to_date)
	month_ago = datetime.datetime.today() - datetime.timedelta(days=30)
	month_ago = month_ago.date()
	resp = make_response(render_template('reports/revenue.html', report=report,
										 today=datetime.datetime.today().date(),
										 month_ago=month_ago))

	resp.set_cookie('from_date', value=json.dumps(report_from_date))
	resp.set_cookie('to_date', value=json.dumps(report_to_date))

	return resp

@reports_bp.route('/save_revenue', methods=['POST'])
def save_revenue():
	from_date = json.loads(request.cookies.get('from_date'))
	to_date = json.loads(request.cookies.get('to_date'))
	db = get_db()

	report = list(db.get_revenue_report(from_date, to_date))
	headers = [list(report[0].keys())]
	report_rows = [[v for v in d.values()] for d in list(report)]
	for i in range(len(report_rows)):
		report_rows[i][0] = report_rows[i][0].date()
	headers_map_to_russian = {'payment_date': 'Дата оплаты',
							  'order_cost': 'Стоимость заказа',
							  'payment_type': 'Тип оплаты',
							  'payment_requisites': 'Реквизиты оплаты',
							  'client_phone': 'Номер телефона клиента'}

	REVENUE_REPORT_FILENAME = 'revenue_report.xlsx'
	with xlsxwriter.Workbook(os.path.join('app', REVENUE_REPORT_FILENAME), {'default_date_format': 'dd/mm/yy'}) as workbook:
		worksheet = workbook.add_worksheet()

		for row_num, h in enumerate(headers):
			for i in range(len(h)):
				h[i] = headers_map_to_russian[h[i]]
			worksheet.write_row(row_num, 0, h)

		header_offset = 1
		for row_num, data in enumerate(report_rows):
			worksheet.write_row(row_num+header_offset, 0, data)

	return send_file(REVENUE_REPORT_FILENAME)

@reports_bp.route('/bath_top')
@has_role(ADMIN_ROLE)
@login_required
def top_bath():
	db = get_db()
	report = db.get_top_bath_report()
	return render_template('reports/top_bath.html', report=report)

@reports_bp.route('/save_bath_top', methods=['POST'])
def save_bath_top():
	db = get_db()
	report = list(db.get_top_bath_report())
	headers = [list(report[0].keys())]
	report_rows = [[v for v in d.values()] for d in list(report)]
	# for i in range(len(report_rows)):
	# 	report_rows[i][0] = report_rows[i][0].date()

	headers_map_to_russian = {'bath_address': 'Адрес бани',
							  'total_hours': 'Общее количество арендованных часов',
							  'total_revenue': 'Общеая выручка'}

	BATH_TOP_REPORT_FILENAME = 'top_bath_report.xlsx'
	with xlsxwriter.Workbook(os.path.join('app', BATH_TOP_REPORT_FILENAME)) as workbook:
		worksheet = workbook.add_worksheet()

		for row_num, h in enumerate(headers):
			for i in range(len(h)):
				h[i] = headers_map_to_russian[h[i]]
			worksheet.write_row(row_num, 0, h)

		header_offset = 1
		for row_num, data in enumerate(report_rows):
			worksheet.write_row(row_num + header_offset, 0, data)

	return send_file(BATH_TOP_REPORT_FILENAME)
