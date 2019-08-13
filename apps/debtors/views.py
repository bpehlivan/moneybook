import logging

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.debtors.models import Debtor
from apps.debtors.services import DebtorService

logger = logging.getLogger(__name__)


class DebtorView(LoginRequiredMixin, View):
    @staticmethod
    def render_debtor_page(request, is_debtor_created=False,
                           is_debtor_creation_failed=False):
        debtors__qs = Debtor.objects.filter(responsible_admin=request.user)
        template_data = {
            'debtors': debtors__qs,
            'is_debtor_created': is_debtor_created,
            'is_debtor_creation_failed': is_debtor_creation_failed
        }
        return render(request, 'debtors/debtors_list.html', template_data)

    def get(self, request):
        return self.render_debtor_page(request=request)


class CreateDebtorView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'debtors/debtor_create.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        e_mail = request.POST.get('email')
        iban = request.POST.get('iban')

        debtor_service = DebtorService()
        try:
            debtor_service.create_debtor(
                first_name=first_name, last_name=last_name,
                e_mail=e_mail, iban=iban, respobsible_admin=request.user)

            return DebtorView.render_debtor_page(request=request,
                                                 is_debtor_created=True)
        except Exception as exc:
            logger.exception(exc)
            return DebtorView.render_debtor_page(
                request=request, is_debtor_creation_failed=True)


class DebtorDetailView(LoginRequiredMixin, View):
    def get(self, request, debtor_id):
        try:
            debtor_instance = Debtor.objects.get(pk=debtor_id)
            return render(request, 'debtors/debtor_detail.html',
                          {'debtor': debtor_instance})
        except Debtor.DoesNotExist:
            return redirect('debtors:debtors-list')

    def post(self, request, debtor_id):
        try:
            debtor_instance = Debtor.objects.get(pk=debtor_id)
            debtor_service = DebtorService()
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            iban = request.POST.get('iban')

            updated_instance = debtor_service.update_debtor(
                instance=debtor_instance, first_name=first_name,
                last_name=last_name, email=email, iban=iban)

            return render(request, 'debtors/debtor_detail.html',
                          {'debtor': updated_instance})
        except Debtor.DoesNotExist:
            return redirect('debtors-list')
