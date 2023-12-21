class Manager:
	def __init__(self):
		self.warehouse = {}
		self.history = []
		self.balance = self.balance_read()
		self.message = ""
		self.history_read()
		self.warehouse_read()

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

	def saldo(self, add):
			try:
				add = float(add)
				if manager.balance + add < 0:
					self.message = "saldo konta nie moze byc ujemne"
				else:
					self.balance += add
					self.message = f"zmieniono saldo o {add} zl, saldo konta wynosi {manager.balance} zl"
					self.history.append(f"zmiana salda o {add} zl. saldo konta wynosi {manager.balance} zl.")
				with open("saldo.txt", "w") as file:
					file.write(str(self.balance))
			except:
				pass

	def sell(self, item, qty, price):
		try:
			item = item.lower()
			qty = int(qty)
			price = float(price)

			if item not in manager.warehouse.keys():
				self.message = "produkt nie znajduje sie w magazynie"
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
							self.message = f"sprzedano {item} w ilosci {qty} szt o cenie {price} zl"
							manager.history.append(f"sprzedano {item} w ilosci {qty} o cenie {price} zl. "
										f"dodano do salda {price*qty} zl")
							manager.warehouse_save()
							if record["ilosc"] == 0:
								manager.warehouse[item].remove(record)
								manager.balance += (price * qty)
								self.message = f"sprzedano {item} w ilosci {qty} szt o cenie {price} zl"
								manager.history.append(f"sprzedano {item} w ilosci {qty} o cenie {price} zl. "
													   f"dodano do salda {price * qty} zl")
								manager.warehouse_save()
				if not price_is:
					self.message = "produkt o takiej cenie nie znajduje sie w magazynie"
				elif not qty_is:
					self.message ="nie ma takiej ilosci produktu w magazynie"
		except:
			self.message = "wprowadzono niepoprawne dane"

	def buy(self, item, qty, price):
		try:
			item = item.lower()
			qty = int(qty)
			price = float(price)

			if qty * price > manager.balance:
				self.message = "brak srodkow, saldo nie moze byc mniejsze od 0"

			else:
				if item in manager.warehouse.keys():
					no_price = True
					for record in manager.warehouse[item]:
						if record["cena"] == price:
							record["ilosc"] += qty
							no_price = False
							manager.balance-=(qty * price)
							self.message= f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl"
							manager.history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
										f"odjeto od salda {price*qty}")
							manager.warehouse_save()

					if no_price:
						manager.warehouse[item].append({"ilosc":qty, "cena":price})
						manager.balance-=(qty*price)
						self.message = f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl"
						manager.history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
									f"odjeto od salda {price*qty} zl")
						manager.warehouse_save()


				else:
					manager.warehouse[item] = [{"ilosc":qty, "cena":price}]
					manager.balance-=(qty*price)
					self.message = f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl"
					manager.history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
						f"odjeto od salda {price*qty} zl")
					manager.warehouse_save()

		except:
			self.message = "wprowadzono niepoprawne dane"

	def add_action(self, action):
		self.history.append(action)

	def history_data(self, number_start=None, number_finish=None):
		self.message = f"wykonano lacznie {len(self.history)} akcje"
		actions = []
		if number_start is not None:
			number_start = int(number_start) - 1
		else:
			number_start = 0

		if number_finish is not None:
			number_finish = int(number_finish) - 1
		else:
			number_finish = len(self.history) - 1

		if number_start < 0 or number_start >= len(self.history):
			self.message = f"numer akcji poczatkowej jest poza zakresem, wybierz numer akcji od 1 do {len(self.history)}"
		elif number_finish < 0 or number_finish >= len(self.history):
			self.message = f"numer akcji koncowej jest poza zakresem, wybierz numer akcji od 1 do {len(self.history)}"
		else:
			for index in range(number_start, number_finish + 1):
				actions.append(f"akcja - {index + 1}: {self.history[index]}")

		if len(self.history) > 0:
			with open("historia.txt", "w") as file:
				for line in self.history:
					file.write(str(line) + "\n")

		return actions, self.message


manager = Manager()