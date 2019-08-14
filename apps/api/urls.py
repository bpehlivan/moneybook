from django.urls import path
from rest_framework import routers

from apps.api.views import ApiKeyGeneratorView


router = routers.SimpleRouter()


urlpatterns = [
    path('api-key/', ApiKeyGeneratorView.as_view(), name='api-key'),
]
