from django.urls import path

from apps.invoices.views import InvoiceView, CreateInvoiceView,\
    InvoiceDetailView

app_name = 'invoices'

urlpatterns = [
    path('invoices/', InvoiceView.as_view(), name='invoices-list'),
    path('invoices/<int:invoice_id>', InvoiceDetailView.as_view(),
         name='invoices-detail'),
    path('<int:debtor_id>/invoices/', InvoiceView.as_view(),
         name='invoice-debtor-list'),
    path('<int:debtor_id>/invoices/create/', CreateInvoiceView.as_view(),
         name='invoice-create')
]
