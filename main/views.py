import datetime

from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from main.forms import CreateLocationForm
from main.models import Location

from main.utils import get_weather_by_city


def index(request):
    context = {"title": "Weather Viewer - Главная"}
    if request.method == "POST":
        city = request.POST.get("city", None)

        if city and not city.isspace():
            weather_raw_data = get_weather_by_city(city)

            if weather_raw_data is None:
                context["error"] = "Город не найден. Попробуйте еще раз."
                return render(request, "main/index.html", context)

            weather_data = {
                "today": datetime.datetime.utcfromtimestamp(weather_raw_data["dt"]).strftime("%d-%m-%Y"),
                "city": city,
                "temperature": weather_raw_data["main"]["temp"],
                "description": weather_raw_data["weather"][0]["description"],
                "icon": weather_raw_data["weather"][0]["icon"],
            }
            context["weather_data"] = weather_data

            return render(request, "main/index.html", context)

        else:
            context["error"] = "Необходимо ввести корректное название города!"
            return render(request, "main/index.html", context)

    return render(request, "main/index.html", context)


@require_http_methods(["GET"])
def favorites(request):
    context = {}
    cities = Location.objects.filter(user=request.user)[:6]
    form = CreateLocationForm(initial={'user': request.user}, auto_id=False)
    weather_data_list = []
    for city in cities:
        weather_raw_data = get_weather_by_city(
            city=city.name, coordinates=(city.latitude, city.longitude)
        )
        if weather_raw_data is not None:
            weather_data = {
                "today": datetime.datetime.utcfromtimestamp(weather_raw_data["dt"]).strftime("%d-%m-%Y"),
                "city": city.name,
                "temperature": weather_raw_data["main"]["temp"],
                "description": weather_raw_data["weather"][0]["description"],
                "icon": weather_raw_data["weather"][0]["icon"],
            }
            weather_data_list.append(weather_data)
    context["title"] = "Weather Viewer - Избранные"
    context["weather_data_list"] = weather_data_list
    context["form"] = form
    return render(request, "main/favorites.html", context)

@require_http_methods(["POST"])
def create_location(request):
    form = CreateLocationForm(request.POST)
    if form.is_valid():
        form.save()
    return render(request, "main/include/city_weather.html", {"form": form})

def about(request):
    return HttpResponse("Здесь будет информация о приложении!")
