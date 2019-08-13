from django.urls import path

from apps.debtors.views import DebtorView, CreateDebtorView,\
    DebtorDetailView, DeleteDebtorView

app_name = 'debtors'

urlpatterns = [
    path('', DebtorView.as_view(), name='debtors-list'),
    path('create/', CreateDebtorView.as_view(), name='debtors-create'),
    path('<int:debtor_id>/', DebtorDetailView.as_view(), name='debtors-detail'),
    path('<int:debtor_id>/delete/', DeleteDebtorView.as_view(),
         name='debtors-delete')
]
