from django.urls import path

from apps.debtors.views import DebtorView, CreateDebtorView, DebtorDetailView

app_name = 'debtors'

urlpatterns = [
    path('<int:debtor_id>/', DebtorDetailView.as_view(), name='debtors-detail'),
    path('', DebtorView.as_view(), name='debtors-list'),
    path('create/', CreateDebtorView.as_view(), name='debtors-create'),
]
