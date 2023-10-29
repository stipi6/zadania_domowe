balance = 0
history = []
warehouse = {}

while True:
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
        operation = input("wpisz 'dodaj' w celu dodania srodkow do salda lub 'odejmij' w celu odjecia srodkow "
                          "od salda \n").lower()

        if operation == "dodaj":
            try:
                add = float(input("podaj kwote do dodania [zl]: \n"))
                if add < 0:
                    print("kwota nie moze byc ujemna \n")
                else:
                    balance += add
                    print(f"dodano {add} zl, saldo konta wynosi {balance} zl \n")
                    history.append(f"dodano {add} zl. saldo konta wynosi {balance} zl.")
            except:
                print("wymagania: wartosc w formacie [0.00] \n")

        elif operation == "odejmij":
            try:
                subtract = float(input("podaj kwote do odjecia [zl]: \n"))
                if subtract < 0:
                    print("kwota nie moze byc ujemna \n")
                elif balance - subtract > 0:
                    balance -= subtract
                    print(f"odjeto {subtract} zl, saldo konta wynosi {balance} zl \n")
                    history.append(f"odjeto {subtract} zl. saldo konta wynosi {balance} zl.")
                else:
                    print("saldo nie moze byc nizsze niz 0 \n")
            except:
                print("wymagania: wartosc w formacie [0.00] \n")

        else:
            print("nie ma takiej komendy \n")


    elif command == "2":
        try:
            item = input("wprowadz nazwe sprzedanego produktu: \n")
            qty = int(input("ilosc sprzedanych sztuk tego produktu: \n"))
            price = float(input(f"cena jednej sztuki produktu [zl]: \n"))

            if item not in warehouse.keys():
                print("produkt nie znajduje sie w magazynie \n")
            else:
                price_is = False
                qty_is = False
                for record in warehouse[item]:
                    if record["cena"] == price:
                        price_is = True
                        if record["ilosc"] >= qty:
                            qty_is = True
                            record["ilosc"] -= qty
                            balance+=(price*qty)
                            print(f"sprzedano {item} w ilosci {qty} szt o cenie {price} zl")
                            history.append(f"sprzedano {item} w ilosci {qty} o cenie {price} zl. "
                                           f"dodano do salda {price*qty} zl")
                            if record["ilosc"] == 0:
                                warehouse[item].remove(record)

                if not price_is:
                    print("produkt o takiej cenie nie znajduje sie w magazynie \n")
                elif not qty_is:
                    print("nie ma takiej ilosci produktu w magazynie \n")
        except:
            print("wprowadzono niepoprawne dane \n")


    elif command == "3":
        try:
            item = input("wprowadz nazwe zakupionego produktu: \n").lower()
            qty = int(input("ilosc zakupionych sztuk tego produktu: \n"))
            price = float(input(f"cena jednej sztuki produktu [zl]: \n"))

            if qty * price > balance:
                print("brak srodkow, saldo nie moze byc mniejsze od 0 \n")

            else:
                if item in warehouse.keys():
                    no_price = True
                    for record in warehouse[item]:
                        if record["cena"] == price:
                            record["ilosc"] += qty
                            no_price = False
                            print(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl")
                            history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
                                           f"odjeto od salda {price*qty}")

                    if no_price:
                        warehouse[item].append({"ilosc":qty, "cena":price})
                        print(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl")
                        history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
                                       f"odjeto od salda {price*qty} zl")
                else:
                    warehouse[item] = [{"ilosc":qty, "cena":price}]
                    print(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl")
                    history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
                                   f"odjeto od salda {price*qty} zl")
        except:
            print("wprowadzono niepoprawne dane \n ")


    elif command == "4":
        print(f"twoj stan konta to: {balance} zl \n")


    elif command == "5":
        print("stan magazynu: \n")
        for product,status in warehouse.items():
            print(product + ":")
            for values in status:
                for p,s in values.items():
                    print(f"{p}: {s}")
        print()


    elif command == "6":
        item_warehouse = input("wprowadz nazwe produktu, ktorego stan magazynu chcesz sprawdzic: \n")
        if item_warehouse in warehouse.keys():
            for irecord in warehouse[item_warehouse]:
                qty = irecord["ilosc"]
                price = irecord["cena"]
                print("ilosc:", qty)
                print("cena:", price)
                print()
        else:
            print("nie ma takiego produktu na magazynie")


    elif command == "7":
        print(f"wykonano lacznie {len(history)} akcje")
        number_start = input(f"wprowadz numer akcji poczatkowej: \n")
        if number_start:
            number_start = int(number_start) - 1
        else:
            number_start = 0

        number_finish = input(f"wprowadz numer akcji koncowej: \n")
        if number_finish:
            number_finish = int(number_finish) - 1
        else:
            number_finish = len(history) - 1

        if number_start < 0 or number_start >= len(history):
            print(f"numer akcji poczatkowej jest poza zakresem, wybierz numer akcji od 1 do {len(history)}")
        if number_finish < 0 or number_finish >= len(history):
            print(f"numer akcji koncowej jest poza zakresem, wybierz numer akcji od 1 do {len(history)}")
        else:
            for index in range(number_start, number_finish+1):
                print(f"akcja - {index+1}: {history[index]}")

    elif command == "8":
        break

    else:
        print("nie ma takiej komendy")