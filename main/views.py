from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {"title": "Главная"}
    return render(request, "main/index.html", context)    

def favorites(request):
    return HttpResponse("Здесь будет список избранных городов!")

def about(request):
    return HttpResponse("Здесь будет информация о приложении!")
