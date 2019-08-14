from rest_framework.serializers import ModelSerializer

from apps.debtors.models import Debtor


class DebtorSerializer(ModelSerializer):
    class Meta:
        model = Debtor
        fields = ('first_name', 'last_name', 'email', 'iban',)
