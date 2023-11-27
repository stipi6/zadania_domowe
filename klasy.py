class User:

	def __init__(self, fullname, classname=None, subject=None):
		self.fullname = fullname
		self.classname = classname
		self.subject = subject

	def __str__(self):
		return self.fullname


students = []
teachers = []
tutors = []

while True:
	print("'utworz' - przechodzi do procesu tworzenia uzytkownikow")
	print("'zarzadzaj' - przechodzi do procesu zarzadzania uzytkownikow")
	print("'koniec' - konczy dzialanie aplikacji")
	command = input("wybierz komende: \n").lower()

	if command == "utworz":
		while True:
			print("'uczen' - utworz ucznia")
			print("'nauczyciel' - utworz nauczyciela")
			print("'wychowawca' - utworz wychowawce")
			print("'koniec' - powrot do glownego menu")
			create = input("wybierz komende: \n").lower()

			if create == "uczen":
				fullname = input("podaj imie i nazwisko ucznia \n").lower()
				classname = input("podaj klase ucznia \n").lower()
				students.append(User(fullname, classname))

			elif create == "nauczyciel":
				fullname = input("podaj imie i nazwisko nauczyciela \n").lower()
				subject = input("podaj przedmiot nauczany przez nauczyciela \n").lower()
				classes = []
				while True:
					classname = input("podaj klasy ktore prowadzi nauczyciel (enter aby zakonczyc) \n").lower()
					if not classname:
						print("zakonczono podawanie klas")
						break
					classes.append(classname)
				teachers.append(User(fullname, classes, subject))


			elif create == "wychowawca":
				fullname = input("podaj imie i nazwisko wychowawcy \n").lower()
				classname = input("podaj klase ktorej nauczyciel jest wychowawca \n").lower()
				tutors.append(User(fullname, classname))

			elif create == "koniec":
				print("powrot do glownego menu")
				break

			else:
				print("nie ma takiej komendy")

	elif command == "zarzadzaj":
		print("'klasa' - wyswietlenie klasy")
		print("'uczen' - wyswietlenie konkretnego ucznia")
		print("'nauczyciel' - wyswietlenie konkretnego nauczyciela")
		print("'wychowawca' - wyswietlenie konkretnego wychowawcy")
		print(" 'koniec' - powrot do glownego menu")
		manage = input("wybierz komende: \n").lower()

		if manage == "klasa":
			search_class = input("podaj nazwe klasy: \n").lower()
			class_found = False
			student_found = False
			tutor_found = False

			print(f"uczniowie klasy {search_class}:")
			for student in students:
				if student.classname == search_class:
					student_found = True
					class_found = True
					print(student.fullname)
			if student_found is False:
				print("klasa nie ma przypisanych uczniow")

			print(f"wychowawca klasy {search_class}:")
			for tutor in tutors:
				if tutor.classname == search_class:
					tutor_found = True
					class_found = True
					print(tutor.fullname)
			if tutor_found is False:
				print("klasa nie ma przypisanego wychowawcy")

			if class_found is False:
				print("brak podanej klasy w bazie")


		elif manage == "uczen":
			search_student = input("podaj imie i nazwisko ucznia \n").lower()
			student_found = False

			print(f"lekcje ucznia {search_student} oraz nauczyciele prowadzacy:")
			for student in students:
				if student.fullname == search_student:
					student_found = True
					for teacher in teachers:
						if student.classname in teacher.classname:
							student_found = True
							print(f"{teacher.subject} - {teacher.fullname}")
			if student_found is False:
				print("brak podanego ucznia w bazie")

		elif manage == "nauczyciel":
			search_teacher = input("podaj imie i nazwisko nauczyciela \n").lower()
			teacher_found = False
			class_found = False
			for teacher in teachers:
				if teacher.fullname == search_teacher:
					teacher_found = True
					class_found = True
					print(f"klasy ktore prowadzi nauczyciel {search_teacher}:")
					for classname in teacher.classname:
						print(classname)
			if class_found is False:
					print("nauczyciel nie prowadzi zadnej klasy")
			if teacher_found is False:
				print("brak podanego nauczyciela w bazie")

		elif manage == "wychowawca":
			search_tutor = input("podaj imie i nazwisko wychowawcy \n").lower()
			tutor_found = False
			student_found = False
			for tutor in tutors:
				if tutor.fullname == search_tutor:
					tutor_found = True
					student_found = True
					print(f"uczniowie ktorych prowadzi wychowawca {search_tutor}:")
					for student in students:
						if student.classname == tutor.classname:
							print(student)
			if student_found is False:
				print("wychowawca nie prowadzi zadnych uczniow")
			if tutor_found is False:
				print("brak podanego wychowawcy w klasie")

		elif manage == "koniec":
			pass

		else:
			print("nie ma takiej komendy")


	elif command == "koniec":
		break

	else:
		print("nie ma takiej komendy")
