from django.db import transaction
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView

from users.forms import LoginForm, RegistrationForm, UserProfileForm


class RegistrationView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        context = {}
        form = RegistrationForm()
        context['form'] = form
        context['title'] = "Weather Viewer - Регистрация"
        return render(request, 'users/registration.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = {}
        context['title'] = "Weather Viewer - Регистрация"
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            user = authenticate(
                email=new_user.email, password = form.cleaned_data['password']
            )

            login(request, user)
            return HttpResponseRedirect(reverse('users:profile'))

        context['form'] = form            
        return render(request, 'users/registration.html', context)


class LoginView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        context = {}
        form = LoginForm()
        context['form'] = form
        context['title'] = "Weather Viewer - Регистрация"
        return render(request, 'users/login.html', context)
    
    @staticmethod
    def post(request, *args, **kwargs):
        context = {}
        context['title'] = "Weather Viewer - Регистрация"
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(
                email = email, password = password,
            )
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            context['form'] = form
            return render(request, 'users/login.html', context)
    
    
class ProfileView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        context = {}
        form = UserProfileForm(instance=request.user)
        context['title'] = "Weather Viewer - Регистрация"
        context['form'] = form
        return render(request, 'users/profile.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        context = {}
        context['title'] = "Weather Viewer - Регистрация"
        form = UserProfileForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            context['form'] = form
        else:
            context['form'] = form

        return render(request, 'users/profile.html', context)


class UserLogoutView(LogoutView):
    next_page = '/'
    http_method_names = ["post", "options", "get"]
    
    def get(self, request, *args, **kwargs):
        logout(request)
        redirect_to = self.get_success_url()         
        return HttpResponseRedirect(redirect_to)




