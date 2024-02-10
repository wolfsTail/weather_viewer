from django.urls import path

from main import views


app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('favorites/', views.favorites, name="favorites"),
    path('create_location/', views.create_location, name="create_location"),
    path('delete_location/<int:pk>/', views.delete_location, name="delete_location"),
    path('hide_error/', views.hide_error, name="hide_error"),
]