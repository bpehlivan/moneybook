from django.urls import path

from apps.users.views import LoginView, HomeView


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home')
]
