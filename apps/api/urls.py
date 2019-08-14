from django.urls import path, include
from rest_framework import routers

from apps.api.views import ApiKeyGeneratorView
from apps.debtors.api.views import DebtorViewSet

router = routers.SimpleRouter()

router.register('debtors', DebtorViewSet, 'debtors')


urlpatterns = [
    path('api-key/', ApiKeyGeneratorView.as_view(), name='api-key'),
    path('api/v1', include((router.urls, 'apps.api'), namespace='viewsets'))
]
