from ledger.core.models import (
    Transaction as T,
    Schema,
)
from ..calculations import Percentual
from ..register import SchemaRegister as R


def test():
    # creating a Transaction by naming it automatically
    # registers its Schema to be reused:
    T('VendaComplicada',
        amount=100)

    T('ImpostoInjusto',
        amount=Percentual(10))

    assert Schema.objects.all().count() == 2

    assert R.VendaComplicada
    assert type(R.VendaComplicada) == T
    assert R.VendaComplicada.amount == 100

    assert R.ImpostoInjusto
    assert type(R.ImpostoInjusto) == T
    assert R.ImpostoInjusto.amount == Percentual(10)

    #using:
    VendaComplicada = \
    R.VendaComplicada(
        R.ImpostoInjusto
    )
