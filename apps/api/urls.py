from django.urls import path, include
from rest_framework import routers

from apps.api.views import ApiKeyGeneratorView
from apps.debtors.api.views import DebtorViewSet
from apps.invoices.api.views import InvoiceViewSet


router = routers.SimpleRouter()

router.register('debtors', DebtorViewSet, 'debtors')
router.register('invoices', InvoiceViewSet, 'invoices')


urlpatterns = [
    path('api-key/', ApiKeyGeneratorView.as_view(), name='api-key'),
    path('v1/', include((router.urls, 'apps.api'), namespace='viewsets'))
]
