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


class _Venda(Transaction):
    ...


class Imposto(Transaction):
    ...


class Contrato:
    def __init__(self, *transacoes):
        ...


class Venda(Contrato):
    def __init__(self, *transacoes):
        super().__init__(self, [_Venda] + transacoes)

    def __call__(self, amount):
        ...


class Percentual:
    def __init__(self, percentual):
        ...


Venda = Venda(
    Imposto(Percentual(10))
)


venda = Venda(100)
