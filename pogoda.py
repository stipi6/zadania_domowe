import os.path
import requests
import json
from datetime import datetime, timedelta

dates = {}
COORDS = [52.40692, 16.92993]


def date_input():
	search_date = input("podaj date w formacie YYYY-MM-DD:\n"
	"(brak podanej daty skutkuje przyjeciem daty jutrzejszej) \n")
	try:
		if search_date:
			datetime.strptime(search_date, '%Y-%m-%d')
			return search_date
		elif search_date == "":
			tommorow_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
			return tommorow_date
	except ValueError:
		print("nieprawidlowy format daty")
		return date_input()


def check_rain(search_date):
	url = (f"https://api.open-meteo.com/v1/forecast?latitude={COORDS[0]}&longitude={COORDS[1]}&hourly=rain&daily="
	f"rain_sum&timezone=Europe%2FLondon&start_date={search_date}&end_date={search_date}")
	response = requests.get(url)
	data = response.json()
	if "daily" in data and "rain_sum" in data["daily"]:
		rain_sum = data["daily"]["rain_sum"][0]
		if rain_sum > 0:
			print(f"dnia {search_date} bedzie padac")
		elif rain_sum == 0:
			print(f"dnia {search_date} nie bedzie padac")
		return rain_sum
	else:
		print("nie wiem")
		return None


def file():
	if os.path.exists("deszcz.json"):
		with open("deszcz.json", "r") as file:
			dates = json.load(file)

	date = date_input()
	rain_sum = check_rain(date)
	if rain_sum is not None:
		dates[date] = rain_sum

	with open("deszcz.json", "w") as file:
		json.dump(dates, file)


file()
