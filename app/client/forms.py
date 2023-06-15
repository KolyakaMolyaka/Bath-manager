from wtforms import Form, IntegerField, DateTimeLocalField, DateTimeField, DateField, TimeField
from wtforms.validators import InputRequired,Optional

class OrderBathForm(Form):
	order_rent_hours = IntegerField('Количество часов аренды', [InputRequired()])
	# booking_date = DateTimeLocalField('Дата и время бронирования', [])
	booking_date = DateField('Дата бронирования', [InputRequired()])
	booking_date_time = TimeField('Время бронирования', [InputRequired()])
