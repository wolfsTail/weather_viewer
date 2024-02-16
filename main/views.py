from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from main.forms import CreateLocationForm
from main.models import Location

from main.utils import get_weather_by_city, get_weather_data


def index(request):
    context = {}
    context["title"] = "Weather Viewer - Главная"

    if request.method == "POST":
        city = request.POST.get("city", None)

        if city and not city.isspace():
            try:
                weather_raw_data = get_weather_by_city(city)
            except ValueError:
                messages.error(request, "Ошибка. Введите корректное название города\
                                или попробуйте позже!")           
                return render(request, "main/index.html", context)

            weather_data = get_weather_data(weather_raw_data)
            context["weather_data"] = weather_data           

        else:
            messages.error(request, "Ошибка. Введите корректное название города.")                        

    return render(request, "main/index.html", context)


@login_required(login_url="/users/login")
@require_http_methods(["GET"])
def favorites(request):
    context = {}
    context["title"] = "Weather Viewer - Избранные"
    form = CreateLocationForm(initial={'user': request.user}, auto_id=False)
    cities = Location.objects.filter(user=request.user)
    weather_data_list = []

    for city in cities:
        weather_raw_data = get_weather_by_city(
            city=city.name, coordinates=(city.latitude, city.longitude)
        )
        if weather_raw_data is not None:
            weather_data = get_weather_data(weather_raw_data)
            weather_data["city_pk"] = city.pk
            weather_data_list.append(weather_data)
    
    context["weather_data_list"] = weather_data_list
    context["form"] = form

    return render(request, "main/favorites.html", context)

@require_http_methods(["POST"])
def create_location(request):
    context = {}
    form = CreateLocationForm(request.POST)

    if form.is_valid():
        obj = form.save(commit=False)
        city = form.cleaned_data["name"]

        try:
            weather_raw_data = get_weather_by_city(city)
        except ValueError:            
            return render(request, "main/include/city_not_found.html", context)
        
        if weather_raw_data is not None:
            weather_data = get_weather_data(weather_raw_data)
            obj.user = request.user
            obj.latitude = weather_raw_data["coord"]["lat"]
            obj.longitude = weather_raw_data["coord"]["lon"]
            obj.save()
            weather_data["city_pk"] = obj.pk
        context["weather_data"] = weather_data
        return render(request, "main/include/city_weather_favorites.html", context)
        
    return render(request, "main/include/city_not_found.html", context)


@require_http_methods(["DELETE"])
def delete_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    location.delete()
    return HttpResponse(status=200)

@require_http_methods(["POST"])
def hide_error(request):
    return HttpResponse(status=200)

def about(request):
    context = {}
    context = {"title": "Weather Viewer - О нас"}
    return render(request, "main/about.html", context)
