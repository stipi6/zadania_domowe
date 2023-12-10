class Manager:
	def __init__(self):
		self.actions = {}
		self.warehouse = {}
		self.history = []
		self.balance = 0

	def assign(self, name):
		def decorate(cb):
			self.actions[name] = cb
		return decorate

	def execute(self, name, *args, **kwargs):
		if name in self.actions:
			return self.actions[name](self, *args, **kwargs)
		else:
			print("Action not defined")

	def history_read(self):
		try:
			if len(self.history) == 0:
				with open("historia.txt", "r") as file:
					for line in file:
						item = line.strip()
						self.history.append(item)
		except:
			pass

	def warehouse_save(self):
		try:
			with open("magazyn.txt", "w") as file:
				for k,v in self.warehouse.items():
					for item in v:
						file.write(f"{k}: ilosc: {item['ilosc']}, cena: {item['cena']}\n")
		except:
			pass

	def warehouse_read(self):
		try:
			if len(self.warehouse) < 1:
				with open("magazyn.txt", "r") as file:
					for line in file:
						line = line.rstrip()
						k, v = line.split(": ilosc: ")
						ilosc, cena = v.split(", cena: ")
						self.warehouse[k] = [{'ilosc': int(ilosc), 'cena': float(cena)}]
		except:
			pass


	def balance_read(self):
		try:
			with open("saldo.txt", "r") as file:
				self.balance = float(file.read())
		except:
			self.balance = 0
		return self.balance



manager = Manager()

@manager.assign("balance")
def balance(manager,operation):
	if operation == "dodaj":
		try:
			add = float(input("podaj kwote do dodania [zl]: \n"))
			if add < 0:
				print("kwota nie moze byc ujemna \n")
			else:
				manager.balance += add
				print(f"dodano {add} zl, saldo konta wynosi {manager.balance} zl \n")
				manager.history.append(f"dodano {add} zl. saldo konta wynosi {manager.balance} zl.")
		except:
			print("wymagania: wartosc w formacie [0.00] \n")


	elif operation == "odejmij":
		try:
			subtract = float(input("podaj kwote do odjecia [zl]: \n"))
			if subtract < 0:
				print("kwota nie moze byc ujemna \n")
			elif manager.balance - subtract > 0:
				manager.balance -= subtract
				print(f"odjeto {subtract} zl, saldo konta wynosi {manager.balance} zl \n")
				manager.history.append(f"odjeto {subtract} zl. saldo konta wynosi {manager.balance} zl.")

			else:
				print("saldo nie moze byc nizsze niz 0 \n")
		except:
			print("wymagania: wartosc w formacie [0.00] \n")
	else:
		print("nie ma takiej komendy \n")


@manager.assign("sell")
def sell(manager):
	try:
		item = input("wprowadz nazwe sprzedanego produktu: \n")
		qty = int(input("ilosc sprzedanych sztuk tego produktu: \n"))
		price = float(input(f"cena jednej sztuki produktu [zl]: \n"))

		if item not in manager.warehouse.keys():
			print("produkt nie znajduje sie w magazynie \n")
		else:
			price_is = False
			qty_is = False
			for record in manager.warehouse[item]:
				if record["cena"] == price:
					price_is = True
					if record["ilosc"] >= qty:
						qty_is = True
						record["ilosc"] -= qty
						manager.balance+=(price*qty)
						print(f"sprzedano {item} w ilosci {qty} szt o cenie {price} zl")
						manager.history.append(f"sprzedano {item} w ilosci {qty} o cenie {price} zl. "
									f"dodano do salda {price*qty} zl")
						manager.warehouse_save()
						if record["ilosc"] == 0:
							manager.warehouse[item].remove(record)
							manager.balance += (price * qty)
							print(f"sprzedano {item} w ilosci {qty} szt o cenie {price} zl")
							manager.history.append(f"sprzedano {item} w ilosci {qty} o cenie {price} zl. "
												   f"dodano do salda {price * qty} zl")
							manager.warehouse_save()
			if not price_is:
				print("produkt o takiej cenie nie znajduje sie w magazynie \n")
			elif not qty_is:
				print("nie ma takiej ilosci produktu w magazynie \n")
	except:
		print("wprowadzono niepoprawne dane \n")


@manager.assign("buy")
def buy(manager):
	try:
		item = input("wprowadz nazwe zakupionego produktu: \n").lower()
		qty = int(input("ilosc zakupionych sztuk tego produktu: \n"))
		price = float(input(f"cena jednej sztuki produktu [zl]: \n"))

		if qty * price > manager.balance:
			print("brak srodkow, saldo nie moze byc mniejsze od 0 \n")

		else:
			if item in manager.warehouse.keys():
				no_price = True
				for record in manager.warehouse[item]:
					if record["cena"] == price:
						record["ilosc"] += qty
						no_price = False
						manager.balance-=(qty * price)
						print(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl")
						manager.history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
									f"odjeto od salda {price*qty}")
						manager.warehouse_save()

				if no_price:
					manager.warehouse[item].append({"ilosc":qty, "cena":price})
					manager.balance-=(qty*price)
					print(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl")
					manager.history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
								f"odjeto od salda {price*qty} zl")
					manager.warehouse_save()


			else:
				manager.warehouse[item] = [{"ilosc":qty, "cena":price}]
				manager.balance-=(qty*price)
				print(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl")
				manager.history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
					f"odjeto od salda {price*qty} zl")
				manager.warehouse_save()

	except:
		print("wprowadzono niepoprawne dane \n ")



@manager.assign("saldo")
def saldo(manager):
	try:
		with open("saldo.txt", "r") as file:
			manager.balance = file.read()
			print(f"stan twojego konta to: {file.read()} zl")
	except:
		manager.balance = 0
	return manager.balance


@manager.assign("warehouse")
def warehouse(manager):
	print("stan magazynu: \n")
	for product,status in manager.warehouse.items():
		print(product + ":")
		for values in status:
			for p,s in values.items():
				print(f"{p}: {s}")
	print()


@manager.assign("item")
def item(manager):
	item_warehouse = input("wprowadz nazwe produktu, ktorego stan magazynu chcesz sprawdzic: \n")
	if item_warehouse in manager.warehouse.keys():
		for irecord in manager.warehouse[item_warehouse]:
			qty = irecord["ilosc"]
			price = irecord["cena"]
			print("ilosc:", qty)
			print("cena:", price)
			print()
	else:
		print("nie ma takiego produktu na magazynie")


@manager.assign("history")
def history(manager):
	print(f"wykonano lacznie {len(manager.history)} akcje")
	number_start = input(f"wprowadz numer akcji poczatkowej: \n")
	if number_start:
		number_start = int(number_start) - 1
	else:
		number_start = 0

	number_finish = input(f"wprowadz numer akcji koncowej: \n")
	if number_finish:
		number_finish = int(number_finish) - 1
	else:
		number_finish = len(manager.history) - 1

	if number_start < 0 or number_start >= len(manager.history):
		print(f"numer akcji poczatkowej jest poza zakresem, wybierz numer akcji od 1 do {len(manager.history)}")
	if number_finish < 0 or number_finish >= len(manager.history):
		print(f"numer akcji koncowej jest poza zakresem, wybierz numer akcji od 1 do {len(manager.history)}")
	else:
		for index in range(number_start, number_finish+1):
			print(f"akcja - {index+1}: {manager.history[index]}")

	if len(manager.history) > 0:
		with open("historia.txt", "w") as file:
			for line in manager.history:
				file.write(str(line) + "\n")
