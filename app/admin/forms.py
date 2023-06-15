from wtforms import Form, StringField, IntegerField, BooleanField, TimeField
from wtforms.validators import InputRequired, Optional
from wtforms import ValidationError


class CreateManagerForm(Form):
	phone = StringField('Телефон', [InputRequired()], render_kw={'placeholder': '79205392642'})
	name = StringField('Имя', [InputRequired()], render_kw={'placeholder': 'Николай'})
	surname = StringField('Фамилия', [InputRequired()], render_kw={'placeholder': 'Маркеев'})
	lastname = StringField('Отчество', [Optional()], render_kw={'placeholder': 'Васильевич'})
	password = StringField('Пароль', [InputRequired()])
	password_confirm = StringField('Введите пароль ещё раз', [InputRequired()])
	salary = IntegerField('Зарплата', [InputRequired()], render_kw={'placeholder': '15000'})

	def validate_password_confirm(form, field):
		if form.password.data != field.data:
			raise ValidationError('Повторный пароль введен неверно!')


class EditManagerForm(Form):
	phone = StringField('Телефон', [InputRequired()])
	name = StringField('Имя', [InputRequired()])
	surname = StringField('Фамилия', [InputRequired()])
	lastname = StringField('Отчество', [Optional()])
	password = StringField('Пароль', [InputRequired()])
	salary = IntegerField('Зарплата', [InputRequired()])


class CreateBathForm(Form):
	address = StringField('Адрес', [InputRequired()], render_kw={'placeholder': 'г. Гусев, ул. Зеленая, д. 12'})
	per_hour_rent = IntegerField('Стоимость за час аренды', [InputRequired()], render_kw={'placeholder': '1000'})
	min_order_time_hours = IntegerField('Минимальное кол-во часов аренды', [InputRequired()],
										render_kw={'placeholder': '2'})
	accessories = BooleanField('Банные принадлежности', [Optional()])
	working_hours_from = TimeField('Время работы с', [InputRequired()])
	working_hours_to = TimeField('Время работы по', [InputRequired()])
	human_capacity = IntegerField('Вместимость людей', [InputRequired()], render_kw={'placeholder': '10'})


class EditBathForm(Form):
	address = StringField('Адрес', [InputRequired()])
	per_hour_rent = IntegerField('Стоимость за час аренды', [InputRequired()])
	min_order_time_hours = IntegerField('Минимальное кол-во часов аренды', [InputRequired()])
	accessories = BooleanField('Банные принадлежности', [Optional()])
	working_hours_from = TimeField('Время работы с', [InputRequired()])
	working_hours_to = TimeField('Время работы по', [InputRequired()])
	human_capacity = IntegerField('Вместимость людей', [InputRequired()])
	status = BooleanField('Статус', [Optional()])
