import pandas as pd
from sys import argv


class Processing:
	def __init__(self, file_path, change):
		self.file_path = file_path
		self.dataframe = self.read_file()
		self.change = [x.split(",") for x in change]

	def read_file(self):
		file_extension = self.file_path.split(".")[-1]
		if file_extension == "csv":
			return pd.read_csv(self.file_path, header=None)
		elif file_extension == "json":
			return pd.read_json(self.file_path)
		elif file_extension == "pickle":
			return pd.read_pickle(self.file_path)
		elif file_extension == "txt":
			return pd.read_csv(self.file_path, header=None)

	def modify(self):
		for x in self.change:
			self.dataframe.iloc[int(x[1]), int(x[0])] = x[2]
		return self.dataframe


class CSVProcessing(Processing):
	def process(self, out_path):
		dataframe = self.modify()
		dataframe.to_csv(out_path, header=False, index=False)


class JSONProcessing(Processing):
	def process(self, out_path):
		dataframe = self.modify()
		dataframe.to_json(out_path)


class TXTProcessing(Processing):
	def process(self, out_path):
		dataframe = self.modify()
		dataframe.to_csv(out_path, header=False, index=False)


class PICKLEProcessing(Processing):
	def process(self, out_path):
		dataframe = self.modify()
		dataframe.to_pickle(out_path)


try:
	in_path = argv[1]
	out_path = argv[2]
	changes = argv[3:]
	file_format = out_path.split(".")[-1]

	processors = {
		"csv": CSVProcessing,
		"json": JSONProcessing,
		"txt": TXTProcessing,
		"pickle": PICKLEProcessing
	}

	processor_class = processors.get(file_format)
	processor = processor_class(in_path, changes)
	processor.process(out_path)
	print("plik po zmianach: \n")
	print(processor.dataframe)

except IndexError:
	print("uruchomienie programu: \n python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> <zmiana_2>"
" ... <zmiana_n> \n")
except FileNotFoundError:
	print("podany plik nie istnieje")
except ValueError:
	print("liczby musza byc calkowite")
