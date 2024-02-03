import datetime

from django.shortcuts import render
from django.http import HttpResponse

from main.utils import get_weather_by_city


def index(request):
    context = {"title": "Weather Viewer - Главная"}
    if request.method == "POST":
        city = request.POST.get('city', None)

        if city and not city.isspace():
            weather_raw_data = get_weather_by_city(city)

            if weather_raw_data is None:
                context['error'] = "Город не найден. Попробуйте еще раз."
                return render(request, "main/index.html", context)
            
            weather_data = {
                "today": datetime.date.today().strftime("%d-%m-%Y"),
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

def favorites(request):
    return HttpResponse("Здесь будет список избранных городов!")

def about(request):
    return HttpResponse("Здесь будет информация о приложении!")
