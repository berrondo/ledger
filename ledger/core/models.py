from django.db import models

from polymorphic.models import PolymorphicModel


class Transacao(PolymorphicModel):
    valor = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now=True)


class Venda(Transacao):
    ...


class Imposto(Transacao):
    ...
