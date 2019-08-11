from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.deptors.models import Deptor


class DeptorView(LoginRequiredMixin, View):
    def get(self, request):
        deptors__qs = Deptor.objects.filter(responsible_admin=request.user)
        return render(request, 'deptors/deptors_list.html',
                      {'deptors': deptors__qs})

    def post(self, request):
        import ipdb; ipdb.set_trace()
        return redirect('debtors:deptors-list')
