from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from apps.invoices.api.serializers import InvoiceSerializer
from apps.invoices.models import Invoice


class InvoiceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    http_method_names = ['get']
