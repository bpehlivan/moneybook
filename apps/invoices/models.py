from django.db import models


class StatusChoices:
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
                              choices=StatusChoices.choices_list(),
                              default=StatusChoices.OPEN)
    due_date = models.DateField()
    deptor = models.ForeignKey('deptors.Deptor', on_delete=models.CASCADE,
                               db_index=True)
