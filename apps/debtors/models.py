from django.db import models
from django.contrib.auth import get_user_model

from apps.invoices.models import InvoiceStatusChoices

user_model = get_user_model()


class Debtor(models.Model):
    """
    According to online information(google), maximum length
    of an IBAN is 34 characters
    """
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    iban = models.CharField(max_length=34)
    responsible_admin = models.ForeignKey(user_model, db_index=True,
                                          on_delete=models.DO_NOTHING)

    @property
    def open_invoice_count(self):
        return self.invoice_set.filter(status=InvoiceStatusChoices.OPEN).count()

    @property
    def paid_invoice_count(self):
        return self.invoice_set.filter(status=InvoiceStatusChoices.PAID).count()

    @property
    def overdue_invoice_count(self):
        return self.invoice_set.filter(
            status=InvoiceStatusChoices.OVERDUE).count()

    @property
    def cancelled_invoice_count(self):
        return self.invoice_set.filter(
            status=InvoiceStatusChoices.CANCELLED).count()

    @property
    def full_name(self):
        return "{first_name} {last_name}".format(first_name=self.first_name,
                                                 last_name=self.last_name)
