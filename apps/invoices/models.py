from django.db import models


class InvoiceStatusChoices:
    OPEN = "OPEN"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"

    @classmethod
    def choices_list(cls):
        return [
            (cls.OPEN, 'open'),
            (cls.PAID, 'paid'),
            (cls.OVERDUE, 'overdue'),
            (cls.CANCELLED, 'cancelled')
        ]


class Invoice(models.Model):
    amount = models.DecimalField(max_digits=32, decimal_places=5)
    status = models.CharField(max_length=16, null=False,
                              choices=InvoiceStatusChoices.choices_list(),
                              default=InvoiceStatusChoices.OPEN)
    due_date = models.DateField()
    debtor = models.ForeignKey('debtors.Debtor', on_delete=models.CASCADE,
                               db_index=True)

    @property
    def debtor_name(self):
        return "{} {}".format(self.debtor.first_name, self.debtor.last_name)
