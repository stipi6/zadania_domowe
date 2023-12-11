def collatz_length(x):
	length = 1
	while x != 1:
		if x % 2 == 0:
			x = x / 2
		else:
			x = 3 * x + 1
		length += 1
	return length

x = int(input("wprowadz liczbe z zakresu od 1 do 100: \n"))

if x < 1 or x > 100:
	print("liczba musi miescic sie w przedziale od 1 do 100")
else:
	print(f"dlugosc ciaglu collatza dla liczby {x} wynosi {collatz_length(x)}")
