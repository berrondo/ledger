from django.db import models

from polymorphic.models import PolymorphicModel


class Account(models.Model):
    ...


class Transaction(PolymorphicModel):
    created_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    debit_from = models.OneToOneField(Account, on_delete=models.PROTECT)
    credit_to = models.OneToOneField(Account, on_delete=models.PROTECT)
    # uuid =


class Venda(Transaction):
    ...


class Imposto(Transaction):
    ...
