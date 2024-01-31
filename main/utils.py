import requests
from decouple import config



url = f"http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={config('OPEN_WEATHER_API_KEY')}"

res = requests.get(url).json()

print(type(res))