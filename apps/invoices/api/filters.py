from django_filters.rest_framework import FilterSet, NumberFilter, CharFilter

from apps.invoices.models import Invoice


class InvoiceFilterSet(FilterSet):
    class Meta:
        model = Invoice

        fields = {
            'status': ['exact'],
            'amount': ['exact'],
            'due_date': ['exact']
        }

    def filter_debtor_mail(self, queryset, name, value):
        return queryset.filter(debtor__email=value)
