import datetime
from django.contrib import messages

from django.shortcuts import get_object_or_404, render
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
                messages.error(request, "Ошибка. Сервис API временно не доступен.")                
                return render(request, "main/index.html", context)

            weather_data = {
                "today": datetime.datetime.utcfromtimestamp(weather_raw_data["dt"]).strftime("%d-%m-%Y"),
                "city": city,
                "temperature": weather_raw_data["main"]["temp"],
                "description": weather_raw_data["weather"][0]["description"],
                "icon": weather_raw_data["weather"][0]["icon"],
            }
            context["weather_data"] = weather_data           

        else:
            messages.error(request, "Ошибка. Введите корректиное название города")                        

    return render(request, "main/index.html", context)


@require_http_methods(["GET"])
def favorites(request):
    context = {}
    context["title"] = "Weather Viewer - Избранные"
    cities = Location.objects.filter(user=request.user)
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
                "city_pk": city.pk,
            }
            weather_data_list.append(weather_data)
    
    context["weather_data_list"] = weather_data_list
    context["form"] = form
    return render(request, "main/favorites.html", context)

@require_http_methods(["POST"])
def create_location(request):
    context = {}
    form = CreateLocationForm(request.POST)
    if form.is_valid():
        if request.user.locations.count() >= 6:
            messages.error(request, "Вы не можете добавлять больше 5 городов в избранное")
            return render(request, "main/include/city_weather_favorites.html", {"form": CreateLocationForm(), "messages": messages})
        else:
            obj = form.save(commit=False)
            city = form.cleaned_data["name"]
            weather_raw_data = get_weather_by_city(city)
            if weather_raw_data is not None:
                weather_data = {
                    "today": datetime.datetime.utcfromtimestamp(weather_raw_data["dt"]).strftime("%d-%m-%Y"),
                    "city": city,
                    "temperature": weather_raw_data["main"]["temp"],
                    "description": weather_raw_data["weather"][0]["description"],
                    "icon": weather_raw_data["weather"][0]["icon"],
                    "city_pk": None,
                }
                obj.user = request.user
                obj.latitude = weather_raw_data["coord"]["lat"]
                obj.longitude = weather_raw_data["coord"]["lon"]
                obj.save()
                weather_data["city_pk"] = obj.pk
            context["weather_data"] = weather_data
    else:
        messages.error(request, "Пожалуйста, введите корректное название города.")
        return render(request, "main/include/city_weather_favorites.html", {"form": CreateLocationForm(), "messages": messages})

    return render(request, "main/include/city_weather_favorites.html", context)

@require_http_methods(["DELETE"])
def delete_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    location.delete()
    return HttpResponse(status=200)

def about(request):
    return HttpResponse("Здесь будет информация о приложении!")
