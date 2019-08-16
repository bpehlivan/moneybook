from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(View):
    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user=user)
            return redirect('users:home')
        else:
            return render(request, 'login/login.html',
                          {'is_authentication_failed': True})


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home/home.html')
