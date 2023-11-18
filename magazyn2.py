history = []
warehouse = {}


def history_read():
    try:
        if len(history) == 0:
            with open("historia.txt", "r") as file:
                for line in file:
                    item = line.strip()
                    history.append(item)
    except:
        pass


def warehouse_save():
    try:
        with open("magazyn.txt", "w") as file:
            for k,v in warehouse.items():
                for item in v:
                    file.write(f"{k}: ilosc: {item['ilosc']}, cena: {item['cena']}\n")
    except:
        pass


def warehouse_read():
    try:
        if len(warehouse) < 1:
            with open("magazyn.txt", "r") as file:
                for line in file:
                    line = line.rstrip()
                    k, v = line.split(": ilosc: ")
                    ilosc, cena = v.split(", cena: ")
                    warehouse[k] = [{'ilosc': int(ilosc), 'cena': float(cena)}]
    except:
        pass


def balance_read():
    try:
        with open("saldo.txt", "r") as file:
            saldo = float(file.read())
    except:
        saldo = 0
    return saldo



while True:
    history_read()
    warehouse_read()
    balance = balance_read()
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



    if command == "2":
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
                                warehouse_save()

                if not price_is:
                    print("produkt o takiej cenie nie znajduje sie w magazynie \n")
                elif not qty_is:
                    print("nie ma takiej ilosci produktu w magazynie \n")
        except:
            print("wprowadzono niepoprawne dane \n")




    if command == "3":
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
                            balance-=(qty * price)
                            print(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl")
                            history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
                                           f"odjeto od salda {price*qty}")
                            warehouse_save()


                    if no_price:
                        warehouse[item].append({"ilosc":qty, "cena":price})
                        balance-=(qty*price)
                        print(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl")
                        history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
                                       f"odjeto od salda {price*qty} zl")
                        warehouse_save()

                else:
                    warehouse[item] = [{"ilosc":qty, "cena":price}]
                    balance-=(qty*price)
                    print(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl")
                    history.append(f"zakupiono produkt o nazwie {item} w ilosci {qty} o cenie {price} zl. "
                                   f"odjeto od salda {price*qty} zl")
                    warehouse_save()

        except:
            print("wprowadzono niepoprawne dane \n ")




    if command == "4":
        try:
            with open("saldo.txt", "r") as file:
                print(f"stan twojego konta to: {file.read()} zl")
        except:
            print(f"stan twojego konta to: {balance} zl")


    if command == "5":
        print("stan magazynu: \n")
        for product,status in warehouse.items():
            print(product + ":")
            for values in status:
                for p,s in values.items():
                    print(f"{p}: {s}")
        print()


    if command == "6":
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


    if command == "7":
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

    with open("saldo.txt", "w") as file:
        file.write(str(balance))

    if len(history) > 0:
        with open("historia.txt", "w") as file:
            for line in history:
                file.write(str(line) + "\n")

    if command == "8":
        break
