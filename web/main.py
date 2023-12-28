from flask import Flask, render_template, request, redirect
from flask_alembic import Alembic
import func
from func import manager, db
from app import app


@app.route("/")
def index():
	func.db_create()
	balance = func.Balance.query.first().balance
	history = func.History.query.all()
	products = func.Product.query.all()
	message = manager.message
	return render_template('index.html', balance=balance, history=history, products=products, message=message)

@app.route("/balance", methods=["POST"])
def balance_r():
	add = int(request.form.get("add"))
	func.update_balance(add)
	manager.message = f"zmieniono saldo o {add} zl"
	history = func.History(action=f"zmieniono saldo o {add} zl")
	db.session.add(history)
	db.session.commit()
	return redirect("/")

@app.route("/sell", methods=["POST"])
def sell_r():
	try:
		name = request.form.get("item")
		qty = int(request.form.get("qty"))
		price = int(request.form.get("price"))
		product = func.Product(name=name, qty=qty, price=price)
		func.sell(product)
	except ValueError:
		manager.message = "uzupelnij wszystkie pola"
	return redirect("/")

@app.route("/buy", methods=["POST"])
def buy_r():
	try:
		name = request.form.get("item")
		qty = int(request.form.get("qty"))
		price = int(request.form.get("price"))
		product = func.Product(name=name, qty=qty, price=price)
		func.buy(product)
	except ValueError:
		manager.message = "uzupelnij wszystkie pola"
	return redirect("/")

@app.route("/history.html", methods=["GET"])
def history_page():
	return render_template("history.html")

@app.route('/history', methods=['GET', 'POST'])
def history_r():
	if request.method == 'POST':
		number_start = request.form.get('line_from', type=int)
		number_finish = request.form.get('line_to', type=int)
		actions = func.History.query.order_by(func.History.id).slice(number_start, number_finish).all()
	else:
		actions = func.History.query.all()
	return render_template("history.html", actions=actions)

alembic = Alembic()
alembic.init_app(app)

if __name__ == "__main__":
	app.run(debug=True)
