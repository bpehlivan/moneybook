from django.urls import path

from apps.deptors.views import DeptorView

app_name = 'debtors'

urlpatterns = [
    path('', DeptorView.as_view(), name='deptors-list'),
]
