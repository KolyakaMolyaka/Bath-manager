import datetime
from random import choice, randint
from app.database import get_db


def generate_n_users(n: int):
	alphabet = 'abcdefghijklmnopqrstuvwxyz12345678'
	db = get_db()
	for _ in range(n):
		name = choice(['Николай', 'Василий', 'Георгий', 'Алексей', 'Наталья', 'Валентина', 'Ольга', 'Екатерина'])
		surname = choice(['Ткаченко', 'Иванченко', 'Обушко', 'Ильенко', 'Туменко', 'Игнатьенко'])
		lastname = choice(['В.', 'Н.', 'Г.', 'Т.', 'П.'])
		password = ''.join([choice(alphabet) for _ in range(16)])
		phone = str(randint(89000000000, 89999999999))
		db.add_client(phone, password, name, surname, lastname)


def generate_n_managers(n: int):
	alphabet = 'abcdefghijklmnopqrstuvwxyz12345678'
	db = get_db()
	for _ in range(n):
		name = choice(['Николай', 'Василий', 'Георгий', 'Алексей', 'Наталья', 'Валентина', 'Ольга', 'Екатерина'])
		surname = choice(['Ткаченко', 'Иванченко', 'Обушко', 'Ильенко', 'Туменко', 'Игнатьенко'])
		lastname = choice(['В.', 'Н.', 'Г.', 'Т.', 'П.'])
		password = ''.join([choice(alphabet) for _ in range(16)])
		phone = str(randint(89000000000, 89999999999))
		salary = str(randint(30_000, 45_000))
		db.add_manager(name, surname, lastname, password, salary, phone)

def generate_n_bathes(n: int):
	db = get_db()
	for i in range(1, n+1):
		address = f'address #{i}'
		per_hour_rent = str(randint(1000, 2100))
		min_order_time_hours = str(randint(2, 4))
		accessories = False
		working_hours_from = datetime.datetime(hour=randint(11, 13), year=2024, month=2, day=23).time()
		working_hours_to = datetime.datetime(hour=randint(19, 23), year=2024, month=2, day=23).time()
		human_capacity = str(randint(2, 8))
		db.add_bath(address, per_hour_rent, min_order_time_hours, accessories, working_hours_from, working_hours_to, human_capacity)
