from model_mommy import mommy
from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.debtors.models import Debtor
from apps.debtors.services import DebtorService
from apps.invoices.models import Invoice, InvoiceStatusChoices


class DebtorServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.debtor_service = DebtorService()
        self.admin_1 = mommy.make(get_user_model())

        # debtors
        self.debtor_1 = mommy.make(Debtor)
        self.debtor_2 = mommy.make(Debtor)

        # Invoices
        self.invoice_1 = mommy.make(Invoice, debtor=self.debtor_1,
                                    status=InvoiceStatusChoices.OPEN)
        self.invoice_2 = mommy.make(Invoice, debtor=self.debtor_1,
                                    status=InvoiceStatusChoices.PAID)

        self.invoice_3 = mommy.make(Invoice, debtor=self.debtor_2,
                                    status=InvoiceStatusChoices.OVERDUE)

    def test_create_debtor(self):
        first_name = 'foo'
        last_name = 'bar'
        e_mail = 'foo@bar.com'
        iban = '123456789'

        debtor = self.debtor_service.create_debtor(
            first_name=first_name, last_name=last_name,
            e_mail=e_mail, iban=iban, respobsible_admin=self.admin_1)

        self.assertEqual(debtor.first_name, first_name)
        self.assertEqual(debtor.last_name, last_name)
        self.assertEqual(debtor.email, e_mail)
        self.assertEqual(debtor.iban, iban)
        self.assertEqual(debtor.responsible_admin, self.admin_1)

    def test_update_debtor(self):
        updated_debtor = self.debtor_service.update_debtor(
            instance=self.debtor_1, first_name='foo', random_attr='bar')

        self.assertEqual(updated_debtor.first_name, 'foo')
        self.assertFalse(hasattr(updated_debtor, 'random_attr'))

    def test_delete_debtor(self):
        self.debtor_service.delete_debtor(instance=self.debtor_1)

        self.assertFalse(Debtor.objects.exclude(pk=self.debtor_2.pk).exists())
        self.assertFalse(Invoice.objects.exclude(pk=self.invoice_3.pk).exists())

