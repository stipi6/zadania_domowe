from flask import Flask, request, render_template, redirect
from func import manager

app = Flask(__name__)

@app.route("/")
def index():
	balance = manager.balance
	message = manager.message
	warehouse = manager.warehouse
	return render_template('index.html', balance=balance, message=message, warehouse=warehouse)

@app.route("/balance", methods=["POST"])
def balance():
	add = request.form.get("add")
	manager.saldo(add)
	return redirect("/")

@app.route("/sell", methods=["POST"])
def sell():
	item = request.form.get("item")
	qty = request.form.get("qty")
	price = request.form.get("price")
	manager.sell(item, qty, price)
	return redirect("/")

@app.route("/buy", methods=["POST"])
def buy():
	item = request.form.get("item")
	qty = request.form.get("qty")
	price = request.form.get("price")
	manager.buy(item, qty, price)
	return redirect("/")

@app.route("/history.html", methods=["GET"])
def history_page():
	return render_template("history.html")

@app.route('/history', methods=['GET', 'POST'])
def history():
    actions = []
    message = ""
    if request.method == 'POST':
        number_start = request.form.get('line_from', type=int)
        number_finish = request.form.get('line_to', type=int)
        actions, message = manager.history_data(number_start, number_finish)
    return render_template("history.html", message=message, actions=actions)


if __name__ == "__main__":
	app.run(debug=True)
