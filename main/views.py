from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Здесь будет главная страница приложения!")

def favorites(request):
    return HttpResponse("Здесь будет список избранных городов!")

def about(request):
    return HttpResponse("Здесь будет информация о приложении!")
