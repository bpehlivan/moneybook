from rest_framework import serializers

from apps.invoices.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    debtor_mail = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('amount', 'status', 'due_date', 'debtor', 'debtor_email', )

    def get_debtor_mail(self, obj: Invoice):
        return obj.debtor.email
