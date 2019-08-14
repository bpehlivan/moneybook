from django.urls import path

from apps.api.views import ApiKeyGeneratorView


urlpatterns = [
    path('api-key/', ApiKeyGeneratorView.as_view(), name='api-key'),
]
