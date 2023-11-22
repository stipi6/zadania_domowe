import sys
import csv

try:
	input_csv = sys.argv[1]
	output_csv = sys.argv[2]
	data_csv = []
	change_csv = []

	with open(input_csv, "r") as csvfile:
		reader = csv.reader(csvfile)
		for line in reader:
			data_csv.append(line)

	for x in sys.argv[3:]:
		change_csv.append(x.split(','))

	for y in change_csv:
		data_csv[int(y[1])][int(y[0])] = y[2]

	with open(output_csv, "w", newline='') as csvfile:
		writer = csv.writer(csvfile)
		for data in data_csv:
			writer.writerow(data)

	print("plik po zmianach:")
	for line in data_csv:
		print(', '.join(line))

except IndexError:
	print("uruchomienie programu: \n python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> <zmiana_2>"
		  " ... <zmiana_n> \n")
except FileNotFoundError:
	print("podany plik nie istnieje")
except ValueError:
	print("liczby musza byc calkowite")
