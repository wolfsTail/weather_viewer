from django.urls import path
from users.views import RegistrationView, LoginView, ProfileView, UserLogoutView


app_name = 'users'


urlpatterns = [
    # registration, autorization
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    ]
