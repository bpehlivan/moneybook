from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from apps.debtors.api.filters import DebtorFilterSet
from apps.debtors.api.serializers import DebtorSerializer
from apps.debtors.models import Debtor


class DebtorViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Debtor.objects.all()
    serializer_class = DebtorSerializer
    http_method_names = ['get']
    filterset_class = DebtorFilterSet

