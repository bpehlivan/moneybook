"""moneybook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djandebtorsct.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls', 'users')),
    path('debtors/', include(('apps.debtors.urls', 'apps.debtors'),
                             namespace='debtors')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api/', include(('apps.api.urls', 'apps.api'), namespace='api')),
]
