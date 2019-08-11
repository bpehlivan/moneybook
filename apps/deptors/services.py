from django.contrib.auth.models import User

from apps.deptors.models import Deptor


class DeptorService:
    def create_deptor(self, first_name: str, last_name: str,
                      e_mail: str, iban: str, respobsible_admin: User):
        return Deptor.objects.create(
            first_name=first_name, last_name=last_name, email=e_mail,
            iban=iban, responsible_admin=respobsible_admin)

    def update_deptor(self, instance: Deptor, **kwargs):
        update_fields = []

        for k, v in kwargs.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
                update_fields.append(k)

        instance.save(update_fields=update_fields)
        return instance

    def delete_deptor(self, instance: Deptor):
        raise NotImplementedError()
