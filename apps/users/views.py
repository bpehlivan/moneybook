from django.shortcuts import render, redirect
from django.views import View


class LoginView(View):
    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        return redirect('home')


class HomeView(View):
    def get(self, request):
        return render(request, 'home/home.html')
