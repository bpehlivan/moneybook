import logging
from datetime import date, datetime

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.debtors.models import Debtor
from apps.invoices.models import Invoice
from apps.invoices.services import InvoiceService

logger = logging.getLogger(__name__)


class InvoiceView(LoginRequiredMixin, View):
    @staticmethod
    def render_invoice_page(request, send_notification: bool = False,
                            is_operation_succeeded: bool = False):

        qs__invoices = Invoice.objects.all()
        template_data = {
            'invoices': qs__invoices,
            'send_notification': send_notification,
            'is_operation_succeeded': is_operation_succeeded,
        }

        return render(request, 'invoices/invoices_list.html', template_data)

    @staticmethod
    def render_invoice_page_for_debtor(request, debtor: Debtor,
                                       send_notification: bool = False,
                                       is_operation_succeeded: bool = False):
        qs__invoices = Invoice.objects.filter(debtor=debtor)
        template_data = {
            'debtor': debtor,
            'invoices': qs__invoices,
            'send_notification': send_notification,
            'is_operation_succeeded': is_operation_succeeded,
        }

        return render(request, 'invoices/invoices_list.html', template_data)

    def get(self, request, debtor_id=None):
        if debtor_id:
            try:
                debtor = Debtor.objects.get(pk=debtor_id)
            except Debtor.DoesNotExist:
                return redirect('users:home')
            return self.render_invoice_page_for_debtor(request=request,
                                                       debtor=debtor)
        return self.render_invoice_page(request=request)


class CreateInvoiceView(LoginRequiredMixin, View):
    def get(self, request, debtor_id):
        try:
            debtor = Debtor.objects.get(
                pk=debtor_id, responsible_admin=request.user)
        except Debtor.DoesNotExist:
            return redirect('users:home')

        return render(request, 'invoices/invoice_create.html',
                      {'debtor': debtor})

    def post(self, request, debtor_id):
        try:
            debtor = Debtor.objects.get(pk=debtor_id,
                                        responsible_admin=request.user)
        except Debtor.DoesNotExist:
            return redirect('debtors:invoices:invoices-list')

        amount = request.POST.get('amount')
        status = request.POST.get('status')
        due_date_str = request.POST.get('due_date')

        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

            invoice_service = InvoiceService()
            invoice_service.create_invoice(amount=amount, status=status,
                                           due_date=due_date, debtor=debtor)
        except Exception as exc:
            logging.exception(exc)
            return InvoiceView.render_invoice_page_for_debtor(
                request=request, debtor=debtor, send_notification=True,
                is_operation_succeeded=False)

        return InvoiceView.render_invoice_page_for_debtor(
            request, debtor=debtor, send_notification=True,
            is_operation_succeeded=True)


class InvoiceDetailView(LoginRequiredMixin, View):
    def get(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
        except Invoice.DoesNotExist:
            return redirect('debtors:invoices:invoices-list')

        if invoice.debtor.responsible_admin == request.user:
            return render(request, 'invoices/invoice_detail.html',
                          {'invoice': invoice})

        return render(request, 'invoices/invoice_detail_disabled.html',
                      {'invoice': invoice})

    def post(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(
                pk=invoice_id, debtor__responsible_admin=request.user)
        except Invoice.DoesNotExist:
            return redirect('debtors:invoices:invoices-list')

        amount = request.POST.get('amount')
        status = request.POST.get('status')
        due_date_str = request.POST.get('due_date')

        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            invoice_service = InvoiceService()
            invoice_service.update_invoice(instance=invoice,
                                           amount=amount, status=status,
                                           due_date=due_date)

        except Exception as exc:
            logging.exception(exc)
            return InvoiceView.render_invoice_page_for_debtor(
                request, debtor=invoice.debtor, send_notification=True,
                is_operation_succeeded=False)

        return InvoiceView.render_invoice_page_for_debtor(
            request=request, debtor=invoice.debtor, send_notification=True,
            is_operation_succeeded=True)


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
