import os.path
import requests
import json
from datetime import datetime, timedelta

COORDS = [52.40692, 16.92993]

class WeatherForecast:

    def __init__(self):
        self.dates = {}
        if os.path.exists("deszcz.json"):
            with open("deszcz.json", "r") as file:
                try:
                    self.dates = json.load(file)
                except json.JSONDecodeError:
                    print("plik jest pusty lub zawiera niepoprawne dane")



    def __setitem__(self, date, rain_sum):
        self.dates[date] = rain_sum
        with open("deszcz.json", "w") as file:
            json.dump(self.dates, file)

    def __getitem__(self, date):
        return self.dates.get(date)

    def __iter__(self):
        return iter(self.dates)

    def items(self):
        for date, weather in self.dates.items():
            yield (date, weather)

    def check_rain(self, search_date):
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

    def date_input(self):
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
            return self.date_input()


weather_forecast = WeatherForecast()
date = weather_forecast.date_input()
rain_sum = weather_forecast.check_rain(date)
if rain_sum is not None:
    weather_forecast[date] = rain_sum

print("wszystkie zapisane dane:")
for item in weather_forecast.items():
    print(item)

print("wszystkie daty dla których znana jest pogoda:")
for date in weather_forecast:
    print(date)