from wtforms import Form, StringField, validators
from wtforms import ValidationError


class AuthForm(Form):
	phone = StringField('Номер телефона', [validators.Length(min=11, max=11)], render_kw={'placeholder': '79205392642'})
	password = StringField('Пароль', [validators.Length(min=6, max=32)])


class LoginForm(AuthForm):
	pass


class RegistrationForm(AuthForm):
	name = StringField('Имя', render_kw={'placeholder': 'Иван'})
	surname = StringField('Фамилия', render_kw={'placeholder': 'Иванов'})
	lastname = StringField('Отчество', render_kw={'placeholder': 'Иванович'})
	confirm_password = StringField('Повторите пароль')

	def validate_confirm_password(form, field):
		if form.password.data != field.data:
			raise ValidationError('Пароли не совпадают')
