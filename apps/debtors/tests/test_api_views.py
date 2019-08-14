from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from model_mommy import mommy

from apps.debtors.models import Debtor
from apps.invoices.models import Invoice, InvoiceStatusChoices


class DebtorViewSetTestCase(TestCase):
    def setUp(self) -> None:
        credentials = {
            'username': 'moneybook',
            'password': 'password123',
            'email': 'foo@bar.com',
            'first_name': 'foo',
            'last_name': 'bar',
            'is_superuser': True,
            'is_staff': True
        }
        user, _ = User.objects.get_or_create(
            username=credentials.pop('username'),
            defaults={**credentials})

        self.client.force_login(user=user)

        # debtors
        self.debtor_1 = mommy.make(Debtor, first_name='foo')
        self.debtor_2 = mommy.make(Debtor)
        self.debtor_3 = mommy.make(Debtor)

        # Invoices
        mommy.make(Invoice, debtor=self.debtor_1, _quantity=2,
                   status=InvoiceStatusChoices.OPEN)
        mommy.make(Invoice, debtor=self.debtor_1, _quantity=3,
                   status=InvoiceStatusChoices.PAID)

        mommy.make(Invoice, debtor=self.debtor_2, _quantity=1,
                   status=InvoiceStatusChoices.OVERDUE)
        mommy.make(Invoice, debtor=self.debtor_2, _quantity=3,
                   status=InvoiceStatusChoices.CANCELLED)

        mommy.make(Invoice, debtor=self.debtor_3, _quantity=2,
                   status=InvoiceStatusChoices.PAID)

    def test_list(self):
        url = reverse('api:viewsets:debtors-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_dict = response.json()

        self.assertEqual(len(response_dict['results']), 3)

        debtor_1_dict = next(filter(lambda x: x['pk'] == self.debtor_1.pk,
                                    response_dict['results']))

        self.assertEqual(debtor_1_dict['open_invoices'], 2)
        self.assertEqual(debtor_1_dict['paid_invoices'], 3)
        self.assertEqual(debtor_1_dict['overdue_invoices'], 0)
        self.assertEqual(debtor_1_dict['cancelled_invoices'], 0)

        debtor_2_dict = next(filter(lambda x: x['pk'] == self.debtor_2.pk,
                                    response_dict['results']))

        self.assertEqual(debtor_2_dict['open_invoices'], 0)
        self.assertEqual(debtor_2_dict['paid_invoices'], 0)
        self.assertEqual(debtor_2_dict['overdue_invoices'], 1)
        self.assertEqual(debtor_2_dict['cancelled_invoices'], 3)

        debtor_3_dict = next(filter(lambda x: x['pk'] == self.debtor_3.pk,
                                    response_dict['results']))

        self.assertEqual(debtor_3_dict['open_invoices'], 0)
        self.assertEqual(debtor_3_dict['paid_invoices'], 2)
        self.assertEqual(debtor_3_dict['overdue_invoices'], 0)
        self.assertEqual(debtor_3_dict['cancelled_invoices'], 0)

    def test_list__filter(self):
        # test first name
        url = '{url}?{filter}={value}'.format(
            url=reverse('api:viewsets:debtors-list'),
            filter='first_name', value='foo')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()

        self.assertEqual(len(response_dict['results']), 1)

        self.assertEqual(response_dict['results'][0]['pk'], self.debtor_1.pk)

        # test invoice count
        url = '{url}?{filter}={value}'.format(
            url=reverse('api:viewsets:debtors-list'),
            filter='invoice_count', value='2')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()

        self.assertEqual(len(response_dict['results']), 1)

        self.assertEqual(response_dict['results'][0]['pk'], self.debtor_3.pk)

        # test invoice status
        url = '{url}?{filter}={value}'.format(
            url=reverse('api:viewsets:debtors-list'),
            filter='invoice_status', value='paid')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()

        self.assertEqual(len(response_dict['results']), 2)
