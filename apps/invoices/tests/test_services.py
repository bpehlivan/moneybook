from datetime import date
from django.test import TestCase
from model_mommy import mommy

from apps.debtors.models import Debtor
from apps.invoices.models import Invoice, InvoiceStatusChoices
from apps.invoices.services import InvoiceService


class InvoiceServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.invoice_service = InvoiceService()

        self.debtor_1 = mommy.make(Debtor)
        self.invoice_1 = mommy.make(Invoice, debtor=self.debtor_1)

    def test_create_invoice(self):
        invoice = self.invoice_service.create_invoice(
            amount=12.1, status=InvoiceStatusChoices.OVERDUE,
            due_date=date(2019, 4, 1), debtor=self.debtor_1)

        self.assertEqual(invoice.amount, 12.1)
        self.assertEqual(invoice.status, InvoiceStatusChoices.OVERDUE)
        self.assertEqual(invoice.due_date, date(2019, 4, 1))
        self.assertEqual(invoice.debtor, self.debtor_1)

    def test_update_invoice(self):
        updated_invoice = self.invoice_service.update_invoice(
            instance=self.invoice_1, status=InvoiceStatusChoices.PAID,
            random_attr='foo')

        self.assertEqual(updated_invoice.status, InvoiceStatusChoices.PAID)
        self.assertFalse(hasattr(updated_invoice, 'random_attr'))

    def test_delete_invoice(self):
        self.invoice_service.delete_invoice(instance=self.invoice_1)

        self.assertFalse(Invoice.objects.all().exists())
