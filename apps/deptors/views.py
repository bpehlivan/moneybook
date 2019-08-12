import logging

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.deptors.models import Deptor
from apps.deptors.services import DeptorService

logger = logging.getLogger(__name__)


class DeptorView(LoginRequiredMixin, View):
    @staticmethod
    def render_deptor_page(request, is_deptor_created=False,
                           is_debtor_creation_failed=False):
        deptors__qs = Deptor.objects.filter(responsible_admin=request.user)
        template_data = {
            'deptors': deptors__qs,
            'is_deptor_created': is_deptor_created,
            'is_debtor_creation_failed': is_debtor_creation_failed
        }
        return render(request, 'deptors/deptors_list.html', template_data)

    def get(self, request):
        return self.render_deptor_page(request=request)


class CreateDebtorView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'deptors/deptor_create.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        e_mail = request.POST.get('e-mail')
        iban = request.POST.get('iban')

        deptor_service = DeptorService()
        try:
            deptor_service.create_deptor(
                first_name=first_name, last_name=last_name,
                e_mail=e_mail, iban=iban, respobsible_admin=request.user)

            return DeptorView.render_deptor_page(request=request,
                                                 is_deptor_created=True)
        except Exception as exc:
            logger.exception(exc)
            return DeptorView.render_deptor_page(
                request=request, is_debtor_creation_failed=True)


class DebtorDetailView(LoginRequiredMixin, View):
    def get(self, request, deptor_id):
        try:
            debtor_instance = Deptor.objects.get(pk=deptor_id)
            # TODO: refactor after template created
            return render(request, '')
        except Deptor.DoesNotExist:
            return redirect('debtors-list')
