import requests
import datetime


def get_coordinates(city: str, API_KEY) -> tuple | None:
    location_url: str = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    result = requests.get(location_url)
    try:        
        result = result.json()
        return result[0]["lat"], result[0]["lon"]
    except IndexError:
        return None


def get_weather_value(coordinates: tuple, API_KEY) -> dict | None:
    if coordinates is None:
        raise ValueError("Ccoordinates incorect or call failed")
    lat, lon = coordinates
    weather_url: str = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&units=metric&appid={API_KEY}"
    result = requests.get(weather_url)
    if result.status_code == 200:
        result = result.json()
        return result
    return None

def get_weather_by_city(city: str, coordinates: tuple | None = None) -> dict | None:
    from decouple import config


    API_KEY: str = config('OPEN_WEATHER_API_KEY', cast=str, default="api_key")

    if coordinates:
        return get_weather_value(coordinates, API_KEY)
    
    coordinates = get_coordinates(city, API_KEY)
    return get_weather_value(coordinates, API_KEY)

def get_weather_data(weather_raw_data: dict|None) -> dict:
    weather_data = {
            "today": datetime.datetime.utcfromtimestamp(weather_raw_data["dt"]).strftime("%d-%m-%Y"),
            "city": weather_raw_data["name"],
            "temperature": weather_raw_data["main"]["temp"],
            "pressure": weather_raw_data["main"]["pressure"],
            "description": weather_raw_data["weather"][0]["description"],
            "icon": weather_raw_data["weather"][0]["icon"],
        }
    return weather_data


if __name__ == "__main__":
    city = "Минск"     
    weather = get_weather_by_city(city)
    print(weather, type(weather))