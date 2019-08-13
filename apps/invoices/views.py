import logging
from datetime import date

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.debtors.models import Debtor
from apps.invoices.models import Invoice
from apps.invoices.services import InvoiceService

logger = logging.getLogger(__name__)


class InvoiceView(LoginRequiredMixin, View):
    @staticmethod
    def render_invoice_page(request):

        qs__invoices = Invoice.objects.all()
        template_data = {
            'invoices': qs__invoices,
        }

        return render(request, 'invoices/invoices_list.html', template_data)

    def get(self, request):
        return self.render_invoice_page(request=request)


class CreateInvoiceView(LoginRequiredMixin, View):
    def get(self, request, debtor_id):
        try:
            debtor = Debtor.objects.get(pk=debtor_id)
        except Debtor.DoesNotExist:
            # TODO: add url names
            return redirect('')

        if debtor.responsible_admin == request.user:
            # TODO: return functional invoice detail page
            return render(request, '', {'debtor': debtor})

        # TODO: add disabled template path when ready
        return render(request, '', {'debtor': debtor})

    def post(self, request, debtor_id):
        try:
            debtor = Debtor.objects.get(pk=debtor_id,
                                        responsible_admin=request.user)
        except Debtor.DoesNotExist:
            # TODO: add url names
            return redirect('')

        amount = request.POST.get('amount')
        status = request.POST.get('status')
        due_date_str = request.POST.get('due_date')
        # TODO: convert due_date_str to date object
        due_date = date(1, 1, 1970)

        invoice_service = InvoiceService()
        invoice_service.create_invoice(amount=amount, status=status,
                                       due_date=due_date, debtor=debtor)

        # TODO: notification parameters
        return InvoiceView.render_invoice_page(request)


class InvoiceDetailView(LoginRequiredMixin, View):
    def get(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            # TODO: add url names
            return redirect('')

        if invoice.debtor.responsible_admin == request.user:
            # TODO: detail template
            return render(request, '', {'invoice': invoice})

        # TODO: detail template disabled
        return render(request, '', {'invoice': invoice})

    def post(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(
                pk=invoice_id, debtor__responsible_admin=request.user)
        except Invoice.DoesNotExist:
            # TODO: add url names
            return redirect('')

        amount = request.POST.get('amount')
        status = request.POST.get('status')
        due_date_str = request.POST.get('due_date')

        try:
            due_date = date(1, 1, 1970)
            invoice_service = InvoiceService()
            invoice_service.update_invoice(instance=invoice,
                                           amount=amount, status=status,
                                           due_date=due_date)

        except Exception as exc:
            logging.exception(exc)
            # TODO: add notification parameters
            return InvoiceView.render_invoice_page(request)

        # TODO: add notification parameters
        return InvoiceView.render_invoice_page(request)


class DeleteInvoiceView(LoginRequiredMixin, View):
    def post(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(
                pk=invoice_id, debtor__responsible_admin=request.user)
        except Invoice.DoesNotExist:
            # TODO: add url names
            return redirect('')

        try:
            invoice_service = InvoiceService()
            invoice_service.delete_invoice(instance=invoice)
        except Exception as exc:
            logging.exception(exc)
            # TODO: add notification parameters
            return InvoiceView.render_invoice_page(request)

        # TODO: add notification parameters
        return InvoiceView.render_invoice_page(request)
