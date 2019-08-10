from django.db import models
from django.contrib.auth import get_user_model


user_model = get_user_model()


class Deptor(models.Model):
    """
    According to online information(google), maximum length
    of an IBAN is 34 characters
    """
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    iban = models.CharField(max_length=34)
    responsible_admin = models.ForeignKey(user_model,
                                          on_delete=models.DO_NOTHING)
