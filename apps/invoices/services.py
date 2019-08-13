from datetime import date

from apps.debtors.models import Debtor
from apps.invoices.models import Invoice


class InvoiceService:
    def create_invoice(self, amount: float, status: str,
                       due_date: date, debtor: Debtor) -> Invoice:
        raise NotImplementedError()

    def update_invoice(self, instance: Invoice, **kwargs) -> Invoice:
        raise NotImplementedError()

    def delete_invoice(self, instance: Invoice) -> None:
        raise NotImplementedError()
