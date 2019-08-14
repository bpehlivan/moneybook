from rest_framework import serializers

from apps.debtors.models import Debtor


class DebtorSerializer(serializers.ModelSerializer):
    open_invoices = serializers.SerializerMethodField()
    paid_invoices = serializers.SerializerMethodField()
    overdue_invoices = serializers.SerializerMethodField()
    cancelled_invoices = serializers.SerializerMethodField()

    class Meta:
        model = Debtor
        fields = ('first_name', 'last_name', 'email', 'iban',
                  'open_invoices', 'paid_invoices', 'overdue_invoices',
                  'cancelled_invoices', 'pk',)

    def get_open_invoices(self, obj: Debtor):
        return obj.open_invoice_count

    def get_paid_invoices(self, obj: Debtor):
        return obj.paid_invoice_count

    def get_overdue_invoices(self, obj: Debtor):
        return obj.overdue_invoice_count

    def get_cancelled_invoices(self, obj: Debtor):
        return obj.cancelled_invoice_count
