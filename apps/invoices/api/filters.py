from django_filters.rest_framework import FilterSet, CharFilter

from apps.invoices.models import Invoice


class InvoiceFilterSet(FilterSet):
    debtor_mail = CharFilter(field_name='debtor_mail',
                             method='filter_debtor_mail')

    class Meta:
        model = Invoice

        fields = {
            'status': ['exact'],
            'amount': ['exact'],
            'due_date': ['exact']
        }

    def filter_debtor_mail(self, queryset, name, value):
        return queryset.filter(debtor__email=value)
