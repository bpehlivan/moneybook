from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from model_mommy import mommy

from apps.debtors.models import Debtor
from apps.invoices.models import Invoice, InvoiceStatusChoices


class InvoiceViewSetTestCase(TestCase):
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

        self.debtor_1 = mommy.make(Debtor, email='foo@bar.com')
        self.debtor_2 = mommy.make(Debtor)

        # Invoices
        mommy.make(Invoice, debtor=self.debtor_1, _quantity=2,
                   status=InvoiceStatusChoices.OPEN)
        mommy.make(Invoice, debtor=self.debtor_1, _quantity=3,
                   status=InvoiceStatusChoices.PAID)

        self.invoice = mommy.make(Invoice, debtor=self.debtor_2, _quantity=1,
                                  status=InvoiceStatusChoices.OVERDUE)
        mommy.make(Invoice, debtor=self.debtor_2, _quantity=3,
                   status=InvoiceStatusChoices.CANCELLED)

    def test_list(self):
        url = reverse('api:viewsets:invoices-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_dict = response.json()

        self.assertEqual(len(response_dict['results']), 9)

    def test_list_filter(self):
        # test status filter
        url = '{url}?{filter}={value}'.format(
            url=reverse('api:viewsets:invoices-list'),
            filter='status', value=InvoiceStatusChoices.PAID)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_dict = response.json()

        self.assertEqual(len(response_dict['results']), 3)

        # test debtor mail filter
        url = '{url}?{filter}={value}'.format(
            url=reverse('api:viewsets:invoices-list'),
            filter='debtor_mail', value='foo@bar.com')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_dict = response.json()

        self.assertEqual(len(response_dict['results']), 5)
