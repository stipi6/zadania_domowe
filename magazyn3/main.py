from func import manager

while True:
	manager.history_read()
	manager.warehouse_read()
	manager.balance = manager.balance_read()
	print("1 - saldo")
	print("2 - sprzedaz")
	print("3 - zakup")
	print("4 - konto")
	print("5 - lista")
	print("6 - magazyn")
	print("7 - przeglad")
	print("8 - koniec")

	print()
	command = input("wybierz komende: \n")

	if command == "1":
		operation = input("wpisz 'dodaj' w celu dodania srodkow do salda lub 'odejmij' w celu odjecia srodkow od "
						"salda \n").lower()
		manager.execute("balance",operation)


	elif command == "2":
		manager.execute("sell")

	elif command == "3":
		manager.execute("buy")

	elif command == "4":
		print(f"stan twojego konta to: {manager.balance} zl")

	elif command == "5":
		manager.execute("warehouse")

	elif command == "6":
		manager.execute("item")

	elif command == "7":
		manager.execute("history")

	elif command == "8":
		break

	with open("saldo.txt", "w") as file:
		file.write(str(manager.balance))

	if len(manager.history) > 0:
		with open("historia.txt", "w") as file:
			for line in manager.history:
				file.write(str(line) + "\n")
