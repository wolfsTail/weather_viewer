import asyncio
import aiohttp


async def get_coordinates(city: str, API_KEY: str) -> tuple | None:
    location_url: str = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(location_url) as response:
            if response.status == 200:
                result = await response.json()
                return result[0]["lat"], result[0]["lon"]
            else:
                return None

async def get_weather_value(coordinates: tuple, API_KEY: str) -> dict | None:
    if coordinates is None:
        raise ValueError("API coordinates call failed")
    lat, lon = coordinates
    weather_url: str = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&units=metric&appid={API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(weather_url) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                return None

async def get_weather_by_city(city: str, coordinates: tuple | None = None) -> dict | None:
    from decouple import config

    API_KEY: str = config('OPEN_WEATHER_API_KEY', cast=str, default="api_key")

    if coordinates:
        return await get_weather_value(coordinates, API_KEY)
    else:
        coordinates = await get_coordinates(city, API_KEY)
        return await get_weather_value(coordinates, API_KEY)

async def main():
    city = "Tula"
    weather = await get_weather_by_city(city)
    print(weather, type(weather))

if __name__ == "__main__":
    asyncio.run(main())
