from django.urls import path
from django.contrib.auth.views import LogoutView

from apps.users.views import LoginView, HomeView

app_name = 'users'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
