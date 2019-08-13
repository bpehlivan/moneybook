from django.contrib.auth.models import User
from django.db.transaction import atomic

from apps.debtors.models import Debtor
from apps.invoices.services import InvoiceService


class DebtorService:
    def create_debtor(self, first_name: str, last_name: str,
                      e_mail: str, iban: str, respobsible_admin: User):
        return Debtor.objects.create(
            first_name=first_name, last_name=last_name, email=e_mail,
            iban=iban, responsible_admin=respobsible_admin)

    def update_debtor(self, instance: Debtor, **kwargs):
        update_fields = []

        for k, v in kwargs.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
                update_fields.append(k)

        instance.save(update_fields=update_fields)
        return instance

    def delete_debtor(self, instance: Debtor):
        qs__invoices = instance.invoice_set.only('pk').all()
        invoice_service = InvoiceService()

        with atomic():
            for invoice in qs__invoices:
                invoice_service.delete_invoice(instance=invoice)

            instance.delete()
