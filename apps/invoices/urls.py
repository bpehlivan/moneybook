from django.urls import path

from apps.invoices.views import InvoiceView

app_name = 'invoices'

urlpatterns = [
    path('invoices/', InvoiceView.as_view(), name='invoices-list'),
    path('<int:debtor_id>/invoices/', InvoiceView.as_view(),
         name='invoice-debtor-list'),
]
