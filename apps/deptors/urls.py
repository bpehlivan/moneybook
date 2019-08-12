from django.urls import path

from apps.deptors.views import DeptorView, CreateDebtorView

app_name = 'debtors'

urlpatterns = [
    path('', DeptorView.as_view(), name='deptors-list'),
    path('create/', CreateDebtorView.as_view(), name='deptors-create')
]
