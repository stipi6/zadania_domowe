from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # test db to nazwa pliku w którym utworzymy bazę danych
db = SQLAlchemy(app)

class Balance(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	balance = db.Column(db.Integer, nullable=False)

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(180), nullable=False)
	qty = db.Column(db.Integer, nullable=False)
	price = db.Column(db.Integer, nullable=False)

class History(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	action = db.Column(db.String(180), nullable=False)

def db_create():
	db.create_all()
	balance = Balance.query.first()
	if not balance:
		initial_balance = Balance(balance=0)
		db.session.add(initial_balance)
		db.session.commit()

class Manager:
	def __init__(self):
		self.message = ""

manager = Manager()

def update_balance(add):
	balance = Balance.query.first().balance
	if balance + add < 0:
		manager.message = "saldo konta nie moze byc ujemne"
	else:
		Balance.query.first().balance += add
		db.session.commit()
		return True

def sell(product: Product):
	the_product = Product.query.filter_by(name=product.name).first()
	if the_product:
		if the_product.qty >= product.qty:
			update_balance(product.price * product.qty)
			the_product.qty -= product.qty
			manager.message = f"sprzedano produkt o nazwie {product.name} w ilosci {product.qty} o cenie {product.price} zl"
			history = History(action=f"sprzedano produkt o nazwie {product.name} w ilosci {product.qty} o cenie {product.price} zl. "
					 f"dodano do salda {product.price * product.qty} zl")
			db.session.add(history)
			db.session.commit()
			if the_product.qty == 0:
				db.session.delete(the_product)
				db.session.commit()
		else:
			manager.message = "nie ma takiej ilosci produktu w magazynie"
	else:
		manager.message = "nie ma takiego produktu w magazynie"

def buy(product: Product):
	balance = Balance.query.first().balance
	if balance >= product.price * product.qty:
		the_product = Product.query.filter_by(name=product.name).first()
		if the_product is not None and product.price == the_product.price:
			update_balance(-product.price * product.qty)
			the_product.qty += product.qty
			manager.message = f"zakupiono produkt o nazwie {product.name} w ilosci {product.qty} o cenie {product.price} zl"
			history = History(action=f"zakupiono produkt o nazwie {product.name} w ilosci {product.qty} o cenie {product.price} zl. "
					 f"odjeto od salda {product.price * product.qty} zl")
			db.session.add(history)
			db.session.commit()
		elif the_product is not None and product.price != the_product.price:
			manager.message = "ten sam produkt ma inna cene"
		else:
			manager.message = f"zakupiono produkt o nazwie {product.name} w ilosci {product.qty} o cenie {product.price} zl"
			history = History(action=f"sprzedano produkt o nazwie {product.name} w ilosci {product.qty} o cenie {product.price} zl. "
					 f"odjeto od salda {product.price * product.qty} zl")
			db.session.add(history)
			db.session.add(product)
			db.session.commit()
			update_balance(-product.price * product.qty)
		return True
	else:
		manager.message = "brak wystarczajacych srodkow na zakup"
		return False

