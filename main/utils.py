import requests
from decouple import config


API_KEY: str = config('OPEN_WEATHER_API_KEY', cast=str, default="api_key")


def get_coordinates(city: str, counry_code: str) -> tuple | None:
    location_url: str = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{counry_code}&limit=1&appid={API_KEY}"
    result = requests.get(location_url)
    if result.status_code == 200:
        result = result.json()
        return result[0]["lat"], result[0]["lon"]
    return None


def get_weather_value(coordinates: tuple) -> dict | None:
    if coordinates is None:
        raise ValueError("Api coordinates call failed")
    lat, lon = coordinates
    weather_url: str = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    result = requests.get(weather_url)
    if result.status_code == 200:
        result = result.json()
        return result
    return None

if __name__ == "__main__":
    city = "Tula"
    counry_code = "ru"
    coordinates = get_coordinates(city, counry_code)
    print(coordinates, type(coordinates))
    weather = get_weather_value(coordinates)
    print(weather, type(weather))