from django.db import models

from polymorphic.models import PolymorphicModel


class Transacao(PolymorphicModel):
    valor = models.DecimalField()
    created_at = models.DateTimeField(auto_now=True)


class Venda(Transacao):
    ...


class Imposto(Transacao):
    ...
