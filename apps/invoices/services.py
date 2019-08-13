from datetime import date

from apps.debtors.models import Debtor
from apps.invoices.models import Invoice


class InvoiceService:
    def create_invoice(self, amount: float, status: str,
                       due_date: date, debtor: Debtor) -> Invoice:
        return Invoice.objects.create(amount=amount, status=status,
                                      due_date=due_date, debtor=debtor)

    def update_invoice(self, instance: Invoice, **kwargs) -> Invoice:
        update_fields = []

        for k, v in kwargs.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
                update_fields.append(k)

        instance.save(update_fields=update_fields)
        return instance

    def delete_invoice(self, instance: Invoice) -> None:
        instance.delete()
