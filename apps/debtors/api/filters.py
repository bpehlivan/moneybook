from django.db.models import Count
from django_filters.rest_framework import FilterSet, NumberFilter, CharFilter

from apps.debtors.models import Debtor


class DebtorFilterSet(FilterSet):
    invoice_count = NumberFilter(field_name='invoice_count',
                                 method='filter_invoice_count')
    invoice_status = CharFilter(field_name='invoice_status',
                                method='filter_invoice_status')

    class Meta:
        model = Debtor

        fields = {
            'first_name': ['exact'],
            'last_name': ['exact'],
            'iban': ['exact'],
            'responsible_admin': ['exact']
        }

    def filter_invoice_count(self, queryset, name, value):
        return queryset.annotate(invoice_count=Count('invoice')).filter(
            invoice_count=value)

    def filter_invoice_status(self, queryset, name, value):
        return queryset.filter(invoice__status=value.upper()).distinct()
