ilosc_elem = int(input("ile elementow chcesz wyslac? \n"))

waga_ogolem = 0
liczba_paczek_ogolem = 0
pusta_waga_ogolem = 0
max_pusta_waga = -1
numer_paczki_max_puste = 0
aktualna_waga_paczki = 0

for i in range(ilosc_elem):
    waga_elem = float(input(f"ile kg wazy element nr {i+1}? \n"))

    if waga_elem < 1 or waga_elem > 10:
        print("waga elementu nie miesci sie w przedziale od 1 do 10 kg")
        break

    waga_ogolem += waga_elem

    if i == 0:
        liczba_paczek_ogolem += 1

    if aktualna_waga_paczki + waga_elem > 20:
        if 20 - aktualna_waga_paczki > max_pusta_waga:
            max_pusta_waga = 20 - aktualna_waga_paczki
            numer_paczki_max_puste = liczba_paczek_ogolem

        liczba_paczek_ogolem += 1
        aktualna_waga_paczki = waga_elem
    else:
        aktualna_waga_paczki += waga_elem

if 20 - aktualna_waga_paczki > max_pusta_waga:
    max_pusta_waga = 20 - aktualna_waga_paczki
    numer_paczki_max_puste = liczba_paczek_ogolem

if liczba_paczek_ogolem > 0:
    print(f"ilosc wyslanych paczek wynosi: {liczba_paczek_ogolem}")
    print(f"suma wyslanych kilogramow wynosi: {waga_ogolem} kg")
    print(f"suma pustych kilogramow wynosi: {liczba_paczek_ogolem * 20 - waga_ogolem} kg")
    print(f"paczka nr {numer_paczki_max_puste} ma najwiecej pustych kilogramow i jest to: {max_pusta_waga} kg")
else:
    print("nie wyslano zadnej paczki")